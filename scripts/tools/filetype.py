def ifile(m):
  if m.lower().endswith('.bam'):
    return True
  elif m.lower().endswith('.fastq.gz'):
    return False
  else:
    sys.exit("Input file must either have .bam or .fastq.gz extension")
