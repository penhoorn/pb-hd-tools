#!/usr/bin/env python3

import sys
import os
import json
import gzip

# process 4 standard fastq lines, see: https://www.biostars.org/p/317524/
def process(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

# determine read type (ccs = ds_ccs, fwd/rev = ss_ccs)
def get_ccs_read_type(record):
  # get read id
  qname = record['name'].decode('UTF-8')
  
  # last three characters contain read type information (ccs, fwd, or rev)
  tp = qname[-3:]

  if tp == 'ccs':
    # return ds_ccs (double stranded ccs) as read type
    return('ds_ccs')
  else:
    # return ss_ccs (single stranded ccs) as read type
    return('ss_ccs')

# write read to file
def write_ccs_read(record, outfile):
  # get 4 elements of FASTQ record
  qnm = record['name'].decode('UTF-8')
  seq = record['sequence'].decode('UTF-8')
  opt = record['optional'].decode('UTF-8')
  qty = record['quality'].decode('UTF-8')
  
  # write to output fastq file
  with open(outfile, 'a') as of:
    of.write(qnm + '\n')
    of.write(seq + '\n')
    of.write(opt + '\n')
    of.write(qty + '\n')
  
# filter out hd reads and write non-hd reads
def filter_heteroduplexes(infile, outfile):
  n = 4
  # work with compressed fastq input file
  with gzip.open(infile, 'r') as fh:
    # make empty list to collect all lines per record
    lines = []
    
    # loop over lines
    for line in fh:
      # append line to list
      lines.append(line.rstrip())
      
      # process if 4 lines are collected
      if (len(lines)) == n:
        record = process(lines)
        
        # determine read type 
        my_read = get_ccs_read_type(record)
        
        # write if ds_ccs, else skip
        if my_read == 'ds_ccs':
          write_ccs_read(record, outfile)
          lines = []
        else:
          lines = []
          continue



