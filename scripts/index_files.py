# Script to rename multiple files in a directory to numerically indexed filenames
  
import os 
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--directory', '-d', help='Directory in which to rename files')
parser.add_argument('--leading_zeros', '-n', help='Number of leading zeros in filename')
parser.add_argument('--extension', '-e', help='Extension of file')
args = parser.parse_args()
target_dir = args.directory
n_leading_zeros = int(args.leading_zeros)
file_format = args.extension

# Rename files
i = 0 
n_files = len(os.listdir(target_dir))
for filename in os.listdir(target_dir): 
    dst = str(i).zfill(n_leading_zeros) + '.' +  file_format
    src = os.path.join(target_dir, filename) 
    dst = os.path.join(target_dir, dst)
    os.rename(src, dst) 
    i += 1
    sys.stdout.write("\rProcessed {}/{} files.".format(i, n_files))
