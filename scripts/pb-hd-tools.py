#!/usr/bin/env python3

import sys
import argparse
import os

import json
import gzip
import pysam

# import hd-functions

parser = argparse.ArgumentParser(
    prog="pb-hd-tools",
    description="A set of tools to count, filter and mask heteroduplex molecules and bases in PacBio CCS data",
    epilog="Thanks for using %(prog)s! :)",
)

parser.add_argument("infile", type=str, help="Input file (either BAM or FASTQ.GZ)")
parser.add_argument("outfile", type=str, help="Output file (either JSON or CSV)")

parser.add_argument("-f","--filter",action="store_true",help="Filter out heteroduplex data (i.e., single-strand ccs reads")
parser.add_argument("-m","--mask",action="store_true", help="Mask heteroduplex bases")

args = parser.parse_args()
