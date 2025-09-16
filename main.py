import argparse
from flow import FileOrganizerFlow

def main():
    parser = argparse.ArgumentParser(description='Organize files from source to destination directory.')
    parser.add_argument('source', help='Source directory to organize')
    parser.add_argument('destination', help='Destination directory for organized files')
    args = parser.parse_args()
    flow = FileOrganizerFlow(args.source, args.destination)
    flow.run()

if __name__ == '__main__':
    main()
import argparse
from flow import FileOrganizerFlow
