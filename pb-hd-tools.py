#!/usr/bin/env python3

import sys
import argparse
import os

import json
import gzip
import pysam

import hd-functions

parser = argparse.ArgumentParser(
    prog="pb-hd-tools",
    description="A set of tools to count, filter and mask heteroduplex molecules and bases in PacBio HiFi data",
    epilog="Thanks for using %(prog)s! :)",
)

parser.add_argument("infile")
parser.add_argument("outfile")

parser.add_argument("-f","--filter",action="store_true")
parser.add_argument("-m","--mask",action="store_true")
