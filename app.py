from tools.csv import gff_to_csv
import sys
from tools import parser

if __name__ == "__main__":
    args = sys.argv
    print(args)

    parser.main("files/dmel-all-r5.6.gff")
    sys.exit(0)

    if len(args) > 1:
        command = args[1]
        if command == "tocsv":
            if not len(args) < 2:
                filename = args[2]
                gff_to_csv(filename)
            else:
                sys.exit(0)
        else:
            sys.exit(0)
    else:
        sys.exit(0)