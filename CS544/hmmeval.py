# script for finding tag accuracy between two docs

import re
import argparse
import json



# python hmmdecode.py ./it_isdt_dev_raw.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('truepath', help='/path/to/input')
    parser.add_argument('mypath', help='/path/to/input')

    args = parser.parse_args()
    
    
    my_file = open(args.mypath, "r")
    raw_mydata = my_file.read()
    my_split = re.split('\s',raw_mydata)
    
    
    true_file = open(args.truepath, "r")
    raw_true = true_file.read()
    true_split = re.split('\s',raw_true)

