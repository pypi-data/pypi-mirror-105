#!/bin/bash
# requesting the number of nodes needed
#SBATCH --partition=hourly
#SBATCH --time=1:00:00
#SBATCH --ntasks=40
# do not touch these unless you know what you are doing!
#SBATCH --clusters=merlin6
#SBATCH --output=meg/slurm-%j.out
#SBATCH --input=meg/menu.txt

echo "Started as $0 $@"

this=./submit.sh

if [ -f "/usr/bin/srun" ]; then
    export PATH=/data/project/general/lepton-nnlo/.usr/bin:$PATH
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/data/project/general/lepton-nnlo/.usr/lib
    export PYTHONPATH=$PYTHONPATH:/data/project/general/lepton-nnlo/.usr//lib/python2.7/site-packages/
    export UDOCKER_DIR=/data/project/general/lepton-nnlo/.usr/udocker
    export UDOCKER_DEFAULT_EXECUTION_MODE=P2
fi


if [ $# -gt 0 ]; then
if [[ $1 == *.conf  || $1 == *.tconf ]]; then
    # We are a runner
    
    echo "[`date`] Runner start as $0 $@"
    hostname
    
    seed=$2
    xi=$3
    part=$4
    flavour=$5
    cuts=$6
    del=${7:-$xi}
    binary="mcmule"
    
    source $1

    olddir=`pwd`
    
    runstring="${STAT[$part]}"
    runstring="${runstring}\n$seed\n$xi\n$del\n$part\n$flavour\n$cuts"
   
    if [ -z $containerid ]; then
        binary="`pwd`/$binary"
        sha1=$(cat $binary | sha1sum)
        sha2=$(make hash)
        cd $folder
    else
        sha1=$(udocker run $containerid sh -c "cat /monte-carlo/$binary | sha1sum")
        sha2=$(udocker run $containerid sh -c "cd /monte-carlo/ && make hash")
        binary="stdbuf -oL -eL udocker run --volume=`pwd`/$folder/out/:/root/out $containerid /monte-carlo/$binary"
    fi
    echo "[`date`] Runner start as $0 $@"
    echo "[`date`] Hash of mcmule: $sha1"
    echo "[`date`] SHA of source: $sha2"
    echo -e "$runstring"
    echo -e "$runstring" | $binary


    echo "[`date`] Runner $0 $@ finishes"
    
    cd $olddir
    exit 0
else
    echo "Not a valid config file. skipping."
fi
fi

function nonmerlintrap() {
    trap  SIGCHLD
    exec 1>&6 6>&-
    cat <<'EOF'
+----------------------------------------------------------+
|  __          __              _                           |
|  \ \        / /             (_)                          |
|   \ \  /\  / /_ _ _ __ _ __  _ _ __   __ _               |
|    \ \/  \/ / _` |  __|  _ \| | '_ \ / _` |              |
|     \  /\  / (_| | |  | | | | | | | | (_| |              |
|      \/  \/ \__,_|_|  |_| |_|_|_| |_|\__, |              |
|                                       __/ |              |
|                                      |___/               |
+----------------------------------------------------------+

 You just send SIGINT (most likely through ^C). For you
 own good, this is blocked. I'm unblocking it now for five
 seconds. If you are sure, hit it again in three seconds.

------------------------------------------------------------
EOF
    for i in {3..1} ; do
        echo -ne "\rUnblocking in in ${i}s\r"
        sleep 1
    done
    echo "Trap removed!               "
    trap - SIGINT
    set +m
    for i in {5..1} ; do
        echo -ne "\rBlocking in in ${i}s\r"
        sleep 1 || exit 1
    done
    set -m
    echo "Trap added!                 "
    echo `list_descendants $$`
    trap 'nonmerlintrap' SIGINT
    exec 6>&1
    trap 'wakeup' SIGCHLD
    wakeup
}
function list_descendants () {
    local children=$(ps -o pid= --ppid "$1")
    for pid in $children
    do
        list_descendants "$pid"
    done
    echo "$children"
}
function diegracefully () {
    echo "Killing $$ (self) and all children"
    if [ ! -f "/usr/bin/srun" ]; then
        kill `list_descendants $$`
    fi
    if [ -n "$containerid" ]; then
        echo "Removing docker container $containerid"
        udocker unprotect $containerid
        udocker rm $containerid
    fi
    exit
}
spid=1
function wakeup () {
    psout=`ps -o pid= -o cmd= -p $spid`
    if [[ $psout == *"sleep infinity"* ]]; then
        echo "Killing $spid"
        kill $spid
        spid=1
    fi
}

if [ -f "/usr/bin/srun" ]; then
    echo "This is a merlin system"
    maxjobs=100000
    trap 'diegracefully' TERM
else
    set -m
    export SLURM_JOB_ID=`date +%s`
    maxjobs=$( cat $0 | grep "^#SBATCH --ntasks" | cut -d'=' -f2 )
    menufile=$( cat $0 | grep "^#SBATCH --input" | cut -d'=' -f2 )
    outputfile=`dirname $0`/nm-$SLURM_JOB_ID.out
    echo "This is *not* a merlin system"
    echo "Redirecting all output to $outputfile and reading from $menufile"
    # save stdout
    exec 6>&2
    # redirect everything
    exec < $menufile
    exec >> $outputfile
    exec 2>&1
    echo "This is *not* a merlin system"
    echo "Redirecting all output to $outputfile and reading from $menufile"
    echo "Running with $maxjobs jobs"
    trap 'nonmerlintrap' SIGINT
    trap 'diegracefully' EXIT
    set -o monitor
    trap 'wakeup' SIGCHLD
fi

function joinname {
    local IFS="_" ; echo "$*"
}

# https://lunarc-documentation.readthedocs.io/en/latest/batch_system/#running-multiple-serial-jobs-within-a-single-job-submission
function run (){
 # Arguemnts are:
 #  1. config file
 #  2. seed
 #  3. xi cut
 #  4. which_piece
 #  5. flavour
 #  6. cuts flag (opt)
 #  7. delcut (opt) if not present xi cut is used
  conf=$1 ; shift
  source $conf
  echo "[`date`] Executing job $this $conf $@"
    
  # --exclusive guarantees that each job gets its own CPU core
  # -n 1: one task
  # -N 1: one node
  outfile=$folder/worker_`joinname $@`_${SLURM_JOB_ID}
  echo "srun --exclusive -n 1 -c 1 $this $conf $@ &> $outfile &"
  if [ -f "/usr/bin/srun" ]; then
      srun --exclusive -n 1 -c 1 $this $conf $@ &> $outfile &
  else
      stdbuf -oL -eL $this $conf $@ &> $outfile &
  fi
  sleep 1
}


if ! git ls-files 2>&1 > /dev/null ; then
  echo "Warning! not a git repository, no self-tracking"
else
  echo "Git rev is `git rev-parse --short HEAD` (branch `git rev-parse --abbrev-ref HEAD`)"
  if [ -z "$(git status --porcelain)" ]; then
    echo "Working directory clean"
  else
    patchpath=`dirname $this`/diff-`git rev-parse --short HEAD`-${SLURM_JOB_ID}.patch.gz
    git diff | gzip > $patchpath
    patchsize=`git diff | wc -c`
    csize=`wc -c $patchpath`
    echo "There are uncommitted changes. I have created"
    echo "   $patchpath ($patchsize byte > $csize)"
    echo "with the differences to `git rev-parse --short HEAD`."
  fi
  if test -f "user.f95"; then
    userpath=`dirname $this`/user-`git rev-parse --short HEAD`-${SLURM_JOB_ID}.f95.gz
    cat user.f95 | gzip > $userpath
    echo "I have create a copy of the user file at $userpath"
  else
    echo "Warning! I cannot find the user file, no self-tracking"
  fi

fi

time {
if [ -f "/usr/bin/srun" ]; then
    :
else
    set -o monitor
    trap 'wakeup' SIGCHLD
fi
  #$1: config file
  #$2: seed
  #$3: xicut
  #$4: part
  #$5: flavour
  #$4: cuts
config=""
while IFS=" " read -r command args
do
    [ -z $command ] && continue
    set -- $args
    runningjobs=`jobs | wc -l`
    if [ "$runningjobs" -ge "$maxjobs" ]; then
        echo "[`date`] $runningjobs running. Standing by"
        jobs
        while [ "$runningjobs" -ge "$maxjobs" ] ; do
            sleep infinity & spid=$!
            echo "Falling asleep with spid=$spid"
            wait $spid
            echo "Awake!"
            runningjobs=`jobs | wc -l`
        done
        echo "[`date`] A job returned. Continue reading"
        jobs
    fi
    case "$command" in
        image)
            if [ -n "$containerid" ]; then
                echo "Only one image specification is allowed"
                diegracefully
                exit 1
            fi
            img=$1
            echo "Using Docker image $img"
            export containerid=$(udocker create $img)
            echo "Created container $containerid"
            udocker protect $containerid
            if [ -n "$2" ]; then
                userpath=$2
                echo "Copy user file $userpath"
                cat $userpath | udocker run $containerid sh -c "cat > /monte-carlo/src/user.f95"
                udocker run $containerid sh -c "cd /monte-carlo && touch src/mat_el.f95 && make" || exit
            else
                userpath=`dirname $this`/user-$img-${SLURM_JOB_ID}.f95.gz
                echo udocker run $containerid cat /monte-carlo/src/user.f95
                udocker run $containerid cat /monte-carlo/src/user.f95 | gzip > $userpath
            fi

            patchpath=`dirname $this`/diff-$img-${SLURM_JOB_ID}.patch.gz
            echo udocker run $containerid sh -c "cd /monte-carlo && git diff"
            udocker run $containerid sh -c "cd /monte-carlo && git diff" | gzip > $patchpath
            ;;
        run)
            echo "running with $args"
            run $config $@
            ;;
        conf)
            echo "loading config file $1"
            config=$1
            if [ ! -z "$containerid" ]; then
                cat $config > ${config%.conf}.$SLURM_JOB_ID.tconf
                echo "" >> ${config%.conf}.$SLURM_JOB_ID.tconf
                echo "containerid=\"$containerid\"" >> ${config%.conf}.$SLURM_JOB_ID.tconf
                config=${config%.conf}.$SLURM_JOB_ID.tconf
            fi
            ;;
        [#]* )
            echo "Comment $command $args"
            ;;
        *)
            echo "Unknown command $command"
            ;;
    esac
done

echo "[`date`] All jobs scheduled. Standing by for result"

until wait ; do : ; done

}

echo "[`date`] All jobs returned"
trap - EXIT
trap - SIGCHLD
if [ -n "$containerid" ]; then
    udocker ps
    udocker unprotect $containerid
    udocker rm $containerid
fi
