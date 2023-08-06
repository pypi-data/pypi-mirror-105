import argparse
import subprocess


def create_parser(subparsers):
    parser = subparsers.add_parser(
        'image-builder',
        description='builds a docker image from McMule with perfect caching'
    )
    parser.add_argument(
        'groups', nargs='+'
    )
    parser.add_argument(
        '--tag',
        default=None
    )
    parser.set_defaults(func=main)


def pull(tag):
    proc = subprocess.Popen(["docker", "pull", tag])
    proc.wait()


def push(tag):
    proc = subprocess.Popen(["docker", "push", tag])
    proc.wait()


def build(path, tag="", dockerfile="Dockerfile", cache_from=[], target=""):
    args = ['docker', 'build']

    for i in cache_from:
        args += ["--cache-from", i]

    if tag:
        args += ['-t', tag]

    if target:
        args += ['--target', target]

    if dockerfile != "Dockerfile":
        args += ['-f', dockerfile]

    args += [path]
    proc = subprocess.Popen(args)
    proc.wait()


def main(parsed):
    if parsed.tag:
        tag = parsed.tag
    else:
        tag = "mcmule:mcmule"
    repo, btag = tag.rsplit(":", 1)
    tags = [btag + "-" + i for i in parsed.groups + ["pre"]]
    tags.insert(0, btag)

    for i in tags:
        pull("%s:%s" % (repo, i))

    cachelist = []
    for stage in ['pre'] + parsed.groups:
        fulltag = "%s:%s-%s" % (repo, btag, stage)
        cachelist.append(fulltag)
        build(
            ".",
            tag=fulltag,
            cache_from=cachelist,
            target="build"+stage
        )

    fulltag = "%s:%s" % (repo, btag)
    cachelist.append(fulltag)
    build(
        ".",
        tag=fulltag,
        cache_from=cachelist
    )

    for i in tags:
        push("%s:%s" % (repo, i))
