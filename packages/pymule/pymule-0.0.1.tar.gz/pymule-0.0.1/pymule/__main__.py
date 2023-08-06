import argparse
import pymule.createrun  as createrun
import pymule.manageruns as manageruns
import pymule.switcheroo as switcheroo
import pymule.ffilter    as ffilter


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    createrun.create_parser(subparsers)
    manageruns.create_dup_parser(subparsers)
    manageruns.create_rm_parser(subparsers)
    manageruns.create_backup_parser(subparsers)
    switcheroo.create_parser(subparsers)
    ffilter.create_parser(subparsers)

    parsed = parser.parse_args()
    parsed.func(parsed)


if __name__ == '__main__':
    main()
