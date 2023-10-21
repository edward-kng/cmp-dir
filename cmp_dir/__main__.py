from .print_diffs import print_diffs
from .reader import Reader
import sys

def main():
    if len(sys.argv) < 3:
        print("Error: Too few arguments")
        exit(1)

    if len(sys.argv) > 3:
        try:
            maxThreads = int(sys.argv[3])
        except:
            print("Error: Number of threads must be an integer")
            exit(1)
    else:
        maxThreads = 1

    dirs = (sys.argv[1], sys.argv[2])
    reader = Reader(dirs[0], dirs[1], maxThreads)
    
    try:
        data = reader.read()
    except KeyboardInterrupt:
        print("\nInterrupted: cancelling...")
        sys.exit(0)
    
    if data[0].keys() == data[1].keys():
        print(f"\n\nNo differences found. {dirs[0]} and {dirs[1]} contain all the same files.")
    else:
        print_diffs(dirs[0], dirs[1], data[0], data[1])
        print_diffs(dirs[1], dirs[0], data[1], data[0])

if __name__ == "__main__":
    main()
