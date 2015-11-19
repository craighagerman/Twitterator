#coding: utf-8
#!/usr/bin/python

# builtin imports
import json
import gzip
import os




####### standalone functions #####
# GZIP compress existing file

def gzip_it(inpath):
    outpath = inpath + ".gz"
    with open(inpath, 'rb') as f_in:
        with gzip.open(outpath, 'wb') as f_out:
            f_out.writelines(f_in)
    os.remove(inpath)







