import sys
import os

def ifile(m):
  if m.lower().endswith('.bam'):
    return True
  elif m.lower().endswith('.fastq.gz'):
    return False
  else:
    sys.exit("ERROR: input file must either have .bam or .fastq.gz extension")

def ofile(m):
  if m.lower().endswith('.json'):
    return True
  elif m.lower().endswith('.csv'):
    return False
  else:
    sys.exit("ERROR: output file must either have .json or .csv extension")

def ext_change(filename, new_ext):
  name, old_ext = os.path.splitext(filename)
  return name + new_ext
