## Introduction

Python scripts to count and filter the number of heteroduplex molecules and sequencing reads. Heteroduplex DNA molecules can occur during the annealing step of PCR, when non-complementary (but highly similar) DNA strands come together. [PacBio's _ccs_ tool (starting with v6.3.0)](https://ccs.how/faq/mode-heteroduplex-filtering.html) has an `--hd-finder` algorithm to detect heteroduplexes during HiFi read generation. The scripts here provide a simplified report.

### Disclaimer

These scripts are not official PacBio products and come with no warranty. 

## Pre-requisites

### Programming language

* Python 3

Python libraries:

* [pysam](https://anaconda.org/bioconda/pysam) - for BAM input files
* [gzip](https://docs.python.org/3/library/gzip.html) - for FASTQ.GZ input files
* [sys](https://docs.python.org/3/library/sys.html)
* [os](https://docs.python.org/3/library/os.html)
* [json](https://docs.python.org/3/library/json.html)

### Assumption

__IMPORTANT!!!__ The heteroduplex count scripts assume that reads are order by ZMW id. This means that two single stranded HiFi reads coming from a heteroduplex molecule in a single ZMW will be *neighbors*  (i.e., two consecutive records in either BAM or FASTQ.GZ input file). 

This is true for output files of PacBio computational tools, including:

* On-instrument CCS [(Sequel IIe system)](https://www.pacb.com/sequencing-systems/)
* Circular Consensus Sequencing (CCS) and Export Reads applications in [SMRT Link](https://www.pacb.com/support/software-downloads/)
* [_ccs_](https://ccs.how/) and [_extracthifi_](https://github.com/PacificBiosciences/extracthifi/) tools from PacBio's [Bioconda repository](https://github.com/PacificBiosciences/pbbioconda)

## Usage

There are three python scripts available:

* `hd_counter_from_bam.py` - count heteroduplex molecules and by-strand HiFi reads using unaligned BAM files as [input](#Input)
* `hd_counter_from_fastq.py` - count heteroduplex molecules and by-strand HiFi reads using compressed FASTQ files as [input](#Input)
* `hd_filter_from_fastq.py` - filter out by-strand HiFi reads using compressed FASTQ files as [input](#Input)

### Count from unaligned BAM files

```
usage: python hd_counter_from_bam.py bam_filename output_filename

positional arguments:
  bam_filename              Unaligned BAM file
  output_filename           JSON or CSV output file

```

### Count from compressed FASTQ files

```
usage: python hd_counter_from_fastq.py fqgz_filename output_filename

positional arguments:
  fqgz_filename             Compressed FASTQ input file
  output_filename           JSON or CSV output file
```

###  Filter from compressed FASTQ files

```
usage: python hd_filter_from_fastq.py fqgz_input_filename fq_output_filename

positional arguments:
  fqgz_input_filename       Compressed FASTQ input file
  fq_output_filename        Filtered FASTQ output file
```

## Input

The python scripts can process files that were generated using the computational tools listed under [Assumption](#Assumption). Of course, in order to count heteroduplex molecules and sequencing reads the `--hd-finder` algorithm for heteroduplex detection had to be activated when generating HiFi reads.

Inputs files can be:

* `hd_counter_from_bam.py`
    1.  hifi_reads.bam
    2.  reads.bam
* `hd_counter_from_fastq.py`
    1.  hifi_reads.fastq.gz
* `hd_filter_from_fastq.py`
    1. hifi_reads.fastq.gz

## Output

The two heteroduplex count scripts support two output formats either JSON or CSV. Both formats have the similar content. There are three variables, which form the properties in a JSON object and the header of the CSV file:

* `data` variable is a `str` that indicates data type and can be one of:
    1. `HiFi` with QV≥20 (≥99% predicted accuracy)
    2. `Other CCS` with QV<20 (<99% predicted accuracy)
* `description` variable is a `str` that can be one of:
    1. `All ZMWs (DNA molecules)` - total number of ZMWs/DNA molecules 
    2. `Heteroduplex ZMWs (DNA molecules)` - number of ZMWs/DNA molecules that tested positive for a heteroduplex 
    3. `Proportion of heteroduplex ZMWs (%)` - `100 x ( 2b / 2a )` 
    4. `Double stranded reads` - number of reads coming from a ZMW that tested negative for a heteroduplex and _ccs_ generates one consensus sequence for both DNA strand (i.e., double-stranded)
    5. `Single stranded reads` - number of reads coming from a ZMW that tested positive for a heteroduplex _ccs_ splits the data on the fly to produce single-stranded CCS reads 
    6. `Proportion single stranded reads (%)` - `100 x ( 2e / ( 2e + 2d ) )`
* `value` is either a `int` or a `float`:
    1. `int` is a count
    2. `float` is a percentage

## Examples

### Count heteroduplexes in reads.bam with JSON output

```
# count
python hd_counter_from_bam.py \
        reads.bam \
        reads.json
        
# view output json
cat reads.json
[
    {
        "data": "HiFi",
        "description": "All ZMWs (DNA molecules)",
        "value": 2291275
    },
    {
        "data": "HiFi",
        "description": "Heteroduplex ZMWs (DNA molecules)",
        "value": 374024
    },
    {
        "data": "HiFi",
        "description": "Proportion heteroduplex ZMWs (%)",
        "value": 16.323837164897274
    },
    {
        "data": "HiFi",
        "description": "Double stranded reads",
        "value": 1917251
    },
    {
        "data": "HiFi",
        "description": "Single stranded reads",
        "value": 747273
    },
    {
        "data": "HiFi",
        "description": "Proportion single stranded reads (%)",
        "value": 28.045271875952327
    },
    {
        "data": "Other CCS",
        "description": "All ZMWs (DNA molecules)",
        "value": 477908
    },
    {
        "data": "Other CCS",
        "description": "Heteroduplex ZMWs (DNA molecules)",
        "value": 117232
    },
    {
        "data": "Other CCS",
        "description": "Proportion heteroduplex ZMWs (%)",
        "value": 24.530244314805362
    },
    {
        "data": "Other CCS",
        "description": "Double stranded reads",
        "value": 360676
    },
    {
        "data": "Other CCS",
        "description": "Single stranded reads",
        "value": 224707
    },
    {
        "data": "Other CCS",
        "description": "Proportion single stranded reads (%)",
        "value": 38.38632143400133
    }
]
```

### Count heteroduplexes in hifi_reads.fastq.gz with CSV output

The `hd_counter_from_fastq.py` script needs manual adjustment to switch the output format. Change the `json_out = True`  to `json_out = False` on `line 214` of the script using a text editor.

```
count_heteroduplexes(infile, outfile, my_dict, json_out = False)
```

Upon saving the edited script you can run it.

```
# count
python hd_counter_from_fastq \
        hifi_reads.fastq.gz \
        hifi_reads.csv
        
# view csv output
cat hifi_reads.csv
data,description,value
HiFi,All ZMWs (DNA molecules),23942
HiFi,Heteroduplex ZMWs (DNA molecules),2960
HiFi,Proportion heteroduplex ZMWs (%),12.363211093475899
HiFi,Double stranded reads,20982
HiFi,Single stranded reads,5676
HiFi,Proportion single stranded reads (%),21.291919873959035
Other CCS,All ZMWs (DNA molecules),0
Other CCS,Heteroduplex ZMWs (DNA molecules),0
Other CCS,Proportion heteroduplex ZMWs (%),0
Other CCS,Double stranded reads,0
Other CCS,Single stranded reads,0
Other CCS,Proportion single stranded reads (%),0
```

### Filter out single stranded reads from hifi_reads.fastq.gz

```
# filter
python hd_filter_from_fastq.py hifi_reads.fastq.gz filtered.hifi_reads.fastq

# compress
bgzip filtered.hifi_reads.fastq
```

## FAQ

### Was the heteroduplex finder algorithm deployed during HiFi read generation?

When counts and percentages of Heteroduplex ZMWs and single strand reads are all 0, then either the input contained no heteroduplexes (unlikely for amplicon data) or the HiFi reads were generated without the  heteroduplex finder algorithm. You can inspect the bam header file to see if `--hd-finder` was deployed when running the _ccs_ tool.

```
samtools view -H reads.bam
@HD	VN:1.6	SO:unknown	pb:5.0.0
@RG	ID:9a56c5da	PL:PACBIO	DS:READTYPE=CCS;BINDINGKIT=101-789-500;SEQUENCINGKIT=101-826-100;BASECALLERVERSION=5.0.0;FRAMERATEHZ=100.000000;STRAND=REVERSE	LB:P0014-01_L3C2C1	PU:m64012_200601_182415	PM:SEQUELII	CM:S/P4-C2/5.0-8M
@RG	ID:9ee1de03	PL:PACBIO	DS:READTYPE=CCS;BINDINGKIT=101-789-500;SEQUENCINGKIT=101-826-100;BASECALLERVERSION=5.0.0;FRAMERATEHZ=100.000000;STRAND=FORWARD	LB:P0014-01_L3C2C1	PU:m64012_200601_182415	PM:SEQUELII	CM:S/P4-C2/5.0-8M
@RG	ID:c2fbb488	PL:PACBIO	DS:READTYPE=CCS;BINDINGKIT=101-789-500;SEQUENCINGKIT=101-826-100;BASECALLERVERSION=5.0.0;FRAMERATEHZ=100.000000	LB:P0014-01_L3C2C1	PU:m64012_200601_182415	PM:SEQUELII	CM:S/P4-C2/5.0-8M
@PG	ID:ccs	PN:ccs	VN:6.3.0	DS:Generate circular consensus sequences (ccs) from subreads.	CL:/pbi/analysis/smrtlink/release/smrtlink/install/smrtlink-release_11.0.0.146107/bundles/smrttools/install/smrttools-release_11.0.0.146107/private/pacbio/unanimity/binwrap/../../../../private/pacbio/unanimity/bin/ccs /pbi/analysis/smrtlink/release/smrtlink/userdata/jobs_root.default/0000/0000059/0000059702/entry-points/1368fb61/m64012_200601_182415.subreadset.xml out.consensusreadset.xml --log-level INFO --chunk 1/300 --all --minLength 10 --maxLength 50000 --minPasses 3 --minSnr 2.5 --minPredictedAccuracy 0.99 --hd-finder --alarms alarms.json --task-report task-report.json --report-json ccs_processing.report.json --zmw-metrics-json ccs_zmws.json.gz -j 4
@PG	ID:pbmerge-2.0.0	PN:pbmerge	VN:2.0.0
@PG	ID:samtools	PN:samtools	PP:pbmerge-2.0.0	VN:1.15.1	CL:samtools view -H temp/reads.bam

```

For data analyzed with the `--hd-finder` the header should contain:

- Three separate read groups (`@RG`) representing double stranded and single stranded (forward and reverse) reads. 
- The _ccs_ `@PG` line should include the `--hd-finder` flag in the `CL` field. In addition, the `VN` field should have version number `6.3.0` or higher.

### Why is the number of single stranded reads not double of the number heteroduplex ZMWs?

Whenever the `--hd-finder` algorithm detects a heteroduplex, it will run _ccs_ in by-strand mode and attempts to generate a HiFi read per DNA strand. Each strand has roughly half the number of passes over the molecule and less coverage to generate HiFi data. There will be individual strands with too little passes/coverage to generate HiFi data. So, not every heteroduplex ZMW will generate two single stranded HiFi reads.


