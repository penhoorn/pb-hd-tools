#!/usr/bin/env python3

import sys
import argparse
import os

import json
import gzip
import pysam

from tools import filetype as ft
from count import fastq as fq
from count import bam as bm

parser = argparse.ArgumentParser(
    prog="pb-hd-tools.py",
    description="A set of tools to count, filter and mask heteroduplex molecules and bases in PacBio CCS data",
    epilog="Thanks for using %(prog)s! :)",
)

parser.add_argument("infile", type=str, help="Input file (either BAM or FASTQ.GZ)")
parser.add_argument("outfile", type=str, help="Output file (either JSON or CSV)")

parser.add_argument("-f","--filter",action="store_true",help="Filter out heteroduplex data (i.e., single-strand ccs reads)")
parser.add_argument("-m","--mask",action="store_true", help="Mask heteroduplex bases")

args = parser.parse_args()

# print arguments to stdout
print("Input file:", args.infile)
print("Output file:", args.outfile)

# check i/o file extensions and print result to stdout
is_bam = ft.ifile(args.infile)
is_json = ft.ofile(args.outfile)
if is_bam:
  print("Input file is BAM format")
else: 
  print("Input file is FASTQ.GZ format")
if is_json:
  print("Output file is JSON format")
else:
  print("Output file is CSV format")

# print options to stdout
if args.filter:
  print("Option -f/--filter: heteroduplex read filter is active")
if args.mask:
  print("Option -m/--mask: heteroduplex base masking is active")

# data dictionary
my_dict = {
  'hifi': {'zm': 0, 'hd': 0, 'ds': 0, 'ss': 0},
  'occs': {'zm': 0, 'hd': 0, 'ds': 0, 'ss': 0}
}

# count heteroduplexes (default)
if is_bam:
  bm.count_heteroduplexes(args.infile, args.outfile, my_dict, json_out = is_json)
else:
  fq.count_heteroduplexes(args.infile, args.outfile, my_dict, json_out = is_json)

# filter out heteroduplex reads (-f/--filter option)
if args.filter:
  if is_bam:
    sys.exit("ERROR: filter heteroduplex reads from BAM input not (yet) supported")
  else:
    from filter import fastq as ff
    print("Filtered output file:", ft.ext_change(args.outfile,'.fastq'))
    ff.filter_heteroduplexes(args.infile, ft.ext_change(args.outfile,'.fastq'))
