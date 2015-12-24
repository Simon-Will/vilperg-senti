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
  
dir_name = sys.argv[1]
output_file = sys.argv[2]
header_names = sys.argv[3:]

   
data = get_files(dir_name, 'features', symlinks=True)
arff_data = []

for feature_file in data:
  for line in open(feature_file):
    line = line.strip()
    list_line = line.split('\t')
    if list_line[0] in header_names:
      arff_data.append(list_line)


with open(output_file, 'w') as f:
  #write relation to arff file
  f.write("@relation {0}\n".format('Review_sentiment'))
  #write attributes to arff file
  for a in arff_data:
    f.write("@attribute {0} {1}\n".format(a[0],a[2]))
  #write data to arff file
  for d in arff_data:
    f.write("@data {0}\n".format(d[1]))
