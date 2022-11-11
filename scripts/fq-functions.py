# hd-count: global data dictionary
my_dict = {
  'hifi': {'zm': 0, 'hd': 0, 'ds': 0, 'ss': 0},
  'occs': {'zm': 0, 'hd': 0, 'ds': 0, 'ss': 0}
}

# generic: process 4 standard fastq lines, see: https://www.biostars.org/p/317524/
def process(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

# generic: determine read type (ds_ccs or ss_ccs)
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

# generic: retrieve zmw id 
def get_zmw_id(record):
  # get read id
  qname = record['name'].decode('UTF-8')
  
  # split on / character
  elements = qname.split("/")
  
  # return zmw id (2nd element in list)
  return(elements[1])

# hd-count: update counts in global dictionary
def update_counts(my_dict, record, zmws, key = 'hifi'):
  # get read type
  tp = get_ccs_read_type(record)
  # print("CCS read type:", tp)

  # get zmw id
  zm = get_zmw_id(record)
    
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

# hd-count: write global dictionary as json formatted output file
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
  
# hd-count: write global dictionary as csv output file
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

# hd-count: main function to count heteroduplex ZMWs and by-strand reads
def count_heteroduplexes(infile, outfile, my_dict, json_out = True):
  n = 4
  # work with compressed fastq input file
  with gzip.open(infile, 'r') as fh:
    # make empty list to collect zmw ids
    zmws = []
    
    # make empty list to collect all lines per record
    lines = []
    
    # loop over lines
    for line in fh:
      # append line to list
      lines.append(line.rstrip())
      
      # process if 4 lines are collected
      if (len(lines)) == n:
        record = process(lines)
        
        # update counts in dictionary
        my_dict = update_counts(my_dict, record, zmws, key = 'hifi')
        
        # empty list
        lines = []
      
        # keep zmws list short - reads are ordered by zmw no need to keep long list
        if len(zmws) > 10:
          # remove oldest item
          del zmws[0]

  # write output
  if json_out:
    write_json(my_dict, outfile)
  else:
    write_csv(my_dict, outfile)

# hd-filter: write read to file
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
  
# hd-filter: main function to filter out hd reads and write non-hd reads
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