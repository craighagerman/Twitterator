#coding: utf-8
#!/usr/bin/python

# builtin imports

import gzip
import json
import os
import re




nlpattern = re.compile(r"[\n\t\r]+")

####### standalone functions #####
# GZIP compress existing file
def gzip_it(inpath):
    outpath = inpath + ".gz"
    with open(inpath, 'rb') as f_in:
        with gzip.open(outpath, 'wb') as f_out:
            f_out.writelines(f_in)
    os.remove(inpath)


#
# ......................  OUTPUT METHODS  .........................................................................
#
##################################################################
#   Write list of users to a file in JL format
##################################################################
def writeJson(jlists_list, outfile):
    with open(outfile, "w") as fo:
        for jlists in jlists_list:
            fo.write(json.dumps(jlists) + "\n")

def writeTuple(tup_list, outfile):
    with open(outfile, "w") as fo:
        fo.write("\n".join(["\t".join(x) for x in tup_list]))

def checkOrMakeOutputDir(basedir, dirname):
    outpath = os.path.join(basedir, dirname)
    os.makedirs(outpath, exist_ok=True)
    return outpath

