## Introduction


Python scripts to count the number of heteroduplex molecules and sequencing reads. Heteroduplex DNA molecules can occur during the annealing step of PCR, when non-complementary (but highly similar) DNA strands come together. [PacBio's _ccs_ tool (starting with v6.3.0)](https://ccs.how/faq/mode-heteroduplex-filtering.html) has an algorithm to detect heteroduplexes during HiFi read generation. The scripts here provide a simplified report.

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

__IMPORTANT!!!__ The scripts assume that reads are order by ZMW id. This means that two single stranded HiFi reads coming from a heteroduplex molecule in a single ZMW will be *neighbors*  (i.e., two consecutive records in either BAM or FASTQ.GZ input file). 

This is true for output files of PacBio computational tools, including:

* On-instrument CCS [(Sequel IIe system)](https://www.pacb.com/sequencing-systems/)
* Circular Consensus Sequencing (CCS) and Export Reads applications in [SMRT Link](https://www.pacb.com/support/software-downloads/)
* [_ccs_](https://ccs.how/) and [_extracthifi_](https://github.com/PacificBiosciences/extracthifi/) tools from PacBio's [Bioconda repository](https://github.com/PacificBiosciences/pbbioconda)

## Usage


There are two python scripts available:

* `hd_counter_from_bam.py` - using unaligned BAM files as [input](#Input)
* `hd_counter_from_fastq.py` - using compressed FASTQ files as [input](#Input)

### Unaligned BAM files

```
usage: python hd_counter_from_bam.py bam_filename output_filename

positional arguments:
  bam_filename      Unaligned BAM file
  output_filename   JSON or CSV output file

```

### Compressed FASTQ files

```
usage: python hd_counter_from_fastq.py fqgz_filename output_filename

positional arguments:
  fqgz_filename     Compressed FASTQ input file
  output_filename   JSON or CSV output file
```

## Input


The python scripts can process files that were generated using the computational tools listed under [Assumption](#Assumption). Of course, in order to count heteroduplex molecules and sequencing reads the algorithm for heteroduplex detection had to be activated when generating HiFi reads.

Inputs files can be:

* `hd_counter_from_bam.py`
    a.  hifi_reads.bam
    b.  reads.bam
* `hd_counter_from_fastq.py`
    a.  hifi_reads.fastq.gz

## Output

***

The scripts support two output formats either JSON or CSV. Both formats have the similar content. There are three variables, which form the properties in a JSON object and the header of the CSV file:

1. `data` variable is a `str` that indicates data type and can be one of:
    a. `HiFi` with QV≥20 (≥99% predicted accuracy)
    b. `Other CCS` with QV<20 (<99% predicted accuracy)
2. `description` variable is a `str` that can be one of:
    a. `All ZMWs (DNA molecules)` - total number of ZMWs/DNA molecules 
    b. `Heteroduplex ZMWs (DNA molecules)` - number of ZMWs/DNA molecules that tested positive for a heteroduplex 
    c. `Proportion of heteroduplex ZMWs (%)` - `100 x ( 2b / 2a )` 
    d. `Double stranded reads` - number of reads coming from a ZMW that tested negative for a heteroduplex and _ccs_ generates one consensus sequence for both DNA strand (i.e., double-stranded)
    e. `Single stranded reads` - number of reads coming from a ZMW that tested positive for a heteroduplex _ccs_ splits the data on the fly to produce single-stranded CCS reads 
    f. `Proportion single stranded reads (%)` - `100 x ( 2e / ( 2e + 2d ) )`
3. `value` is either a `int` or a `float`:
    a. `int` is a count
    b. `float` is a percentage


## Examples


### All reads bam with JSON output

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

### HiFi reads fastq.gz with CSV output

The `hd_counter_from_fastq` script needs manual adjustment to switch the output format. Change the `json_out = True`  to `json_out = False` on `line 214` of the script using a text editor.

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

...

***

