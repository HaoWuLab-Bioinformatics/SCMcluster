import numpy as np
import pandas as pd
import scipy.io
import argparse
import os
import sys

def equalsIgnoreCase(a, b):
    if isinstance(a, str):
        if isinstance(b, str):
            return len(a) == len(b) and a.upper() == b.upper()
    return False

def feature_selection(data_path, out_path, markers):
    """
    Parameters
    ----------
    data_path: Path to the input matrix
    out_path: Path to the output matrix
    markers: Path to markers file

    Returns
    -------
    """
    df = pd.read_csv(data_path, index_col=0, sep='\t')
    # df=pd.read_csv('./data/camp1_data.txt',index_col=0,sep='\t')
    # d=pd.read_csv('data/pancreas_marker316.txt', sep='\t', header=None)
    d = pd.read_csv(markers, header=None, sep='\t')
    #print(d)

    n = 0
    new = pd.DataFrame()
    for i in range(0, len(d.index)):  # 筛选出表达集里有的marker
        for j in range(0, len(df.index)):
            if not equalsIgnoreCase(df.index[j], d.iloc[i, 0]):
                continue
            n = n + 1
            #print(n, df.index[j])
            #print(df.loc[df.index[j], :])
            new = new.append(df.loc[df.index[j], :])

    # print(new)
    new.to_csv(out_path, sep='\t')

def parse(args=None):
    '''arguments.
    '''
    parser = argparse.ArgumentParser(prog='SCMclsuter feature selection',
                                     description='Feature selection using SCMclsuter. doi: 10.1093/bfgp/elad004',
                                     epilog='(c) authors')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + '1',
                        help="Show program's version number and exit.")
    parser.add_argument('-i', '--mat_file', type=str, help='Path to the input matrix')
    parser.add_argument('-o', '--out_file', type=str, help='Path to the output matrix')
    parser.add_argument('-m', '--marker', type=str, help='Path to the markers')

    args_parsed = parser.parse_args(args)
    return args_parsed

def main():
    args = parse(sys.argv[1:])
    if args.mat_file and args.out_file and args.marker:
        print('Matrix have been submitted...')
        feature_selection(args.mat_file, args.out_file, args.marker)
        print('Matrix have been returned... Run SCMcluster.py now!')
if __name__ == '__main__':
    main()