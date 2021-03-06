#!/usr/bin/env python3
import sys
import os

def get_files(dir_name, f_name, symlinks=False):
    """Recursively get regular files called f_name in the directory dir_name.
    Args:
        dir_name (str): The name of a directory.
        f_name (str): The name of the files to be found.
    Returns:
        files (list): A list of strings containing the full paths to the files.
    """
    files = [os.path.join(root, name)
            for root, dirs, files in os.walk(dir_name, followlinks=symlinks)
            for name in files
            if name == f_name]
    return files

    """Assigning multiple parameters to the module in the following order:
    dir_name = directory containing the feature files
    output_file = write data to output file in arff format
    header_names = list of features that will be written to output_file
    """
dir_name = sys.argv[1]
output_file = sys.argv[2]
header_names = sys.argv[3:]
data = get_files(dir_name, 'features', symlinks=True)
arff_data = []

for feature_file in data:
  attribute_dict = {}
  for line in open(feature_file):
    line = line.strip()
    list_line = line.split('\t')
    for attribute in header_names:
      if attribute == list_line[0]:
        attribute_dict[attribute] = list_line[1]
  if len(attribute_dict) == len(header_names):
    arff_data.append(attribute_dict)



    #attribute dictionary
d = {'token_number':'numeric', 'normalized_overall_sentiment':'numeric',
        'normalized_adjective_sentiment':'numeric', 'normalized_verb_sentiment':'numeric',
        'normalized_noun_sentiment':'numeric', 'binary_judgement':'{good, bad}', 'stars':'{1,2,3,4,5}'}

with open(output_file, 'w') as f:
  """write arff_data to output_file
  """

  f.write("@relation {0}\n\n\n".format('Review_sentiment'))

  for attribute in header_names:
    f.write ("@attribute {0} {1}\n".format(attribute,d[attribute]))

  f.write("@data\n")
  data = []
  for d in arff_data:
    for attribute in header_names:
      data.append(d[attribute])

    final_data = ','.join(data)
    f.write(final_data)
    f.write('\n')
    data = []
