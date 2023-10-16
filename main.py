from scanner import DiskUsage
import argparse
import coloring as cl
from exceptions import EmptyDirectoryException, InvalidDirectoryException
from utils import Utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Disk Usage Analyzer")
    parser.add_argument("directory", help="Directory to analyze")
    parser.add_argument("-e", "--extension", help="Filter by extension (.*)")
    parser.add_argument("-d", "--date", help="Filter by creation date (dd-mm-yyyy).")
    parser.add_argument("-n", "--nested", help="Filter by nested level (<lowest_nested_level>-<highest_nested_level>).")
    parser.add_argument("-s", "--size", help = "Filter by size (9kb-10gb)")
    parser.add_argument("-a", "--author", help = "Filter by author (User)")

    args = parser.parse_args()

    try:
        diskusage = DiskUsage(args.directory, args.extension, args.date, args.size, args.author, args.nested)
        if args.extension:
            print(f'{cl.YELLOW}Extension filter set to {args.extension}{cl.RESET}')
        if args.date:
            print(f'{cl.YELLOW}Date filter set to {args.date}{cl.RESET}')
        files = diskusage.get_disk_usage()
        if not files:
            print(f"{cl.RED}No files found.{cl.RESET}")
        else:
            ans = input(f"{cl.GREEN}Found {len(files)} files occupying {Utils.get_total_size(files)}. Would you like to see them? (y/n)\n:{cl.RESET}")
            sorted_files = sorted(files, key=lambda file: file.size, reverse=True)
            if ans.lower() == 'y':
                print('\n\n'.join((repr(file) for file in sorted_files)))
    except EmptyDirectoryException:
        print(f"{cl.RED}No files were found in this directory.{cl.RESET}")
    except InvalidDirectoryException:
        print(f"{cl.RED}Directory does not exits.{cl.RESET}")
    except KeyboardInterrupt:
        print(f"\n{cl.RED}Operation interrupted by the user.{cl.RESET}")