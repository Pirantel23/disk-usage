from scanner import DiskUsage
import argparse
import coloring as cl
from exceptions import EmptyDirectoryException, InvalidDirectoryException

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Disk Usage Analyzer")
    parser.add_argument("directory", help="Directory to analyze")
    parser.add_argument("-e", "--extension", help="Filter by extension (.txt)")
    parser.add_argument("-d", "--date", help="Filter by creation date (dd-mm-yyyy).")
    args = parser.parse_args()

    try:
        diskusage = DiskUsage()
        print(f'{cl.YELLOW}Looking for files in {args.directory}{cl.RESET}')
        if args.extension:
            print(f'{cl.YELLOW}Extension filter set to {args.extension}{cl.RESET}')
        if args.date:
            print(f'{cl.YELLOW}Date filter set to {args.date}{cl.RESET}')
        files = diskusage.get_disk_usage(args.directory, args.extension, args.date)
        if not files:
            print(f"{cl.RED}No files found.{cl.RESET}")
        else:
            print(f"{cl.GREEN}Found {len(files)} files. Would you like to see them? (y/n){cl.RESET}")
            ans = input()
            if ans.lower() == 'y':
                print('\n'.join((file.path for file in files)))
    except EmptyDirectoryException:
        print(f"{cl.RED}No files were found in this directory.{cl.RESET}")
    except InvalidDirectoryException:
        print(f"{cl.RED}Directory does not exits.{cl.RESET}")
    except KeyboardInterrupt:
        print(f"\n{cl.RED}Operation interrupted by the user.{cl.RESET}")