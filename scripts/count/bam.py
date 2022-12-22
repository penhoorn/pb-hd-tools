import sys
import os
import pysam
import json

def get_tag(tags, label):
  for tag, val in tags:
    if tag == label:
      return val

def get_ccs_read_type(read):
  # get read id
  qname = read.query_name
  
  # last three characters contain read type information (ccs, fwd, or rev)
  tp = qname[-3:]

  if tp == 'ccs':
    # return ds_ccs (double stranded ccs) as read type
    return('ds_ccs')
  else:
    # return ss_ccs (single stranded ccs) as read type
    return('ss_ccs')

def update_counts(my_dict, read, zmws, key = 'hifi'):
  # get read type
  tp = get_ccs_read_type(read)
  # print("CCS read type:", tp)

  # get zmw id
  zm = get_tag(read.tags,'zm')
    
  # append if current zmw not in list
  if zm not in zmws:
    # append new zmw to list (keeping track)
    zmws.append(zm)
    
    # increment total zmw count in dictionary
    my_dict[key]['zm'] += 1
    
    # if type ss_ccs increment ss and hd counts,
    #   else increment ds count
    if tp == 'ss_ccs':
      my_dict[key]['hd'] += 1
      my_dict[key]['ss'] += 1
    else:
      my_dict[key]['ds'] += 1
      
  else:
    # if type ss_ccs increment ss counts
    if tp == 'ss_ccs':
      my_dict[key]['ss'] += 1
    
  # return updated dictionary
  return(my_dict)

def write_json(my_dict, outfile):
  # hifi data
  if my_dict['hifi']['hd'] == 0:
    hifi_zm_per = 0
  else:
    hifi_zm_per = 100 * (my_dict['hifi']['hd'] / my_dict['hifi']['zm'])
  hifi_rd_sum = my_dict['hifi']['ds'] + my_dict['hifi']['ss']
  if hifi_rd_sum == 0:
    hifi_rd_per = None
  else:
    hifi_rd_per = 100 * (my_dict['hifi']['ss'] / hifi_rd_sum)
    
  # other ccs data
  if my_dict['occs']['hd'] == 0:
    occs_zm_per = 0
  else:
    occs_zm_per = 100 * (my_dict['occs']['hd'] / my_dict['occs']['zm'])
  occs_rd_sum = my_dict['occs']['ds'] + my_dict['occs']['ss']
  if occs_rd_sum == 0:
    occs_rd_per = 0
  else:
    occs_rd_per = 100 * (my_dict['occs']['ss'] / occs_rd_sum)

  # create output dictionary
  out_dict = [
    {'data':'HiFi','description':'All ZMWs (DNA molecules)','value':my_dict['hifi']['zm']},
    {'data':'HiFi','description':'Heteroduplex ZMWs (DNA molecules)','value':my_dict['hifi']['hd']},
    {'data':'HiFi','description':'Proportion heteroduplex ZMWs (%)','value':hifi_zm_per},
    {'data':'HiFi','description':'Double stranded reads','value':my_dict['hifi']['ds']},
    {'data':'HiFi','description':'Single stranded reads','value':my_dict['hifi']['ss']},
    {'data':'HiFi','description':'Proportion single stranded reads (%)','value':hifi_rd_per},
    {'data':'Other CCS','description':'All ZMWs (DNA molecules)','value':my_dict['occs']['zm']},
    {'data':'Other CCS','description':'Heteroduplex ZMWs (DNA molecules)','value':my_dict['occs']['hd']},
    {'data':'Other CCS','description':'Proportion heteroduplex ZMWs (%)','value':occs_zm_per},
    {'data':'Other CCS','description':'Double stranded reads','value':my_dict['occs']['ds']},
    {'data':'Other CCS','description':'Single stranded reads','value':my_dict['occs']['ss']},
    {'data':'Other CCS','description':'Proportion single stranded reads (%)','value':occs_rd_per}
  ]
  
  # make json object
  json_string = json.dumps(out_dict,indent=4)
  # print(json_string)
  
  # write to output json file
  with open(outfile, "w") as of:
      of.write(json_string)
  
def write_csv(my_dict, outfile):
  # hifi data
  if my_dict['hifi']['hd'] == 0:
    hifi_zm_per = 0
  else:
    hifi_zm_per = 100 * (my_dict['hifi']['hd'] / my_dict['hifi']['zm'])
  hifi_rd_sum = my_dict['hifi']['ds'] + my_dict['hifi']['ss']
  if hifi_rd_sum == 0:
    hifi_rd_per = None
  else:
    hifi_rd_per = 100 * (my_dict['hifi']['ss'] / hifi_rd_sum)
    
  # other ccs data
  if my_dict['occs']['hd'] == 0:
    occs_zm_per = 0
  else:
    occs_zm_per = 100 * (my_dict['occs']['hd'] / my_dict['occs']['zm'])
  occs_rd_sum = my_dict['occs']['ds'] + my_dict['occs']['ss']
  if occs_rd_sum == 0:
    occs_rd_per = 0
  else:
    occs_rd_per = 100 * (my_dict['occs']['ss'] / occs_rd_sum)

  # write to output csv file
  with open(outfile, "w") as of:
    of.write('data,description,value' + '\n')
    of.write('HiFi,All ZMWs (DNA molecules),' + str(my_dict['hifi']['zm']) + '\n')
    of.write('HiFi,Heteroduplex ZMWs (DNA molecules),' + str(my_dict['hifi']['hd']) + '\n')
    of.write('HiFi,Proportion heteroduplex ZMWs (%),' + str(hifi_zm_per) + '\n')
    of.write('HiFi,Double stranded reads,' + str(my_dict['hifi']['ds']) + '\n')
    of.write('HiFi,Single stranded reads,' + str(my_dict['hifi']['ss']) + '\n')
    of.write('HiFi,Proportion single stranded reads (%),' + str(hifi_rd_per) + '\n')
    of.write('Other CCS,All ZMWs (DNA molecules),' + str(my_dict['occs']['zm']) + '\n')
    of.write('Other CCS,Heteroduplex ZMWs (DNA molecules),' + str(my_dict['occs']['hd']) + '\n')
    of.write('Other CCS,Proportion heteroduplex ZMWs (%),' + str(occs_zm_per) + '\n')
    of.write('Other CCS,Double stranded reads,' + str(my_dict['occs']['ds']) + '\n')
    of.write('Other CCS,Single stranded reads,' + str(my_dict['occs']['ss']) + '\n')
    of.write('Other CCS,Proportion single stranded reads (%),' + str(occs_rd_per) + '\n')
  
def count_heteroduplexes(infile, outfile, my_dict, json_out = True):
  # input bam file
  bam_input = pysam.AlignmentFile(infile,'rb',check_sq=False)
  
  # make empty list to collect zmw ids
  zmws = []
  
  # loop over all reads
  for read in bam_input.fetch(until_eof=True):
    # get read quality information
    rq = get_tag(read.tags,'rq')
    
    # skip if rq <0 (low pass reads - not css)
    if rq < 0:
      continue
    
    # mark if read is hifi quality or not
    if rq >= 0.99:
      my_dict = update_counts(my_dict, read, zmws, key = 'hifi')
    else:
      my_dict = update_counts(my_dict, read, zmws, key = 'occs')
      
    # keep zmws list short - reads are ordered by zmw no need to keep long list
    if len(zmws) > 10:
      # remove oldest item
      del zmws[0]
      # print(zmws)
  
  # write output
  if json_out:
    write_json(my_dict, outfile)
  else:
    write_csv(my_dict, outfile)
    
    
try:
    infile = sys.argv[1]
except IndexError as ie:
    raise SystemError("Error: Specify input fastq file name\n")

if not os.path.exists(infile):
    raise SystemError("Error: File does not exist\n")
try:
    outfile = sys.argv[2]
except IndexError as ie:
    raise SystemError("Error: Specify output fasta file name")

print("Input file:", infile)
print("Output file:", outfile)

# data dictionary
my_dict = {
  'hifi': {'zm': 0, 'hd': 0, 'ds': 0, 'ss': 0},
  'occs': {'zm': 0, 'hd': 0, 'ds': 0, 'ss': 0}
}
# print(my_dict)

# run functions
count_heteroduplexes(infile, outfile, my_dict, json_out = True)
print(my_dict)
