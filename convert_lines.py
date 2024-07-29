import sys

source_line = True
for line in sys.stdin:
    if line.strip() == "":
        continue
    if source_line:
        source_line = False
        print(line.strip(), end="\t")
    else:
        source_line = True
        print(line.strip())
