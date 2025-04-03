import argparse

from scam.core.commit import CommitManager
from scam.core.push import PushManager


def main():
    parser = argparse.ArgumentParser(prog="scam", description="Simple Commit & Archival Manager (SCAM)")
    subparsers = parser.add_subparsers(dest="command")

    commit_parser = subparsers.add_parser("commit", help="Commit a file with a message")
    commit_parser.add_argument("filename", help="Path to the file to commit")
    commit_parser.add_argument("-m", "--message", required=True, help="Commit message")

    _ = subparsers.add_parser("push", help="Push committed files to cloud")

    args = parser.parse_args()

    if args.command == "commit":
        cm = CommitManager()
        path = cm.commit(args.filename, args.message)
        print(f"Committed to: {path}")
    elif args.command == "push":
        pm = PushManager()
        pm.push()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
