#!/bin/bash
echo "Streaming from Twitter firehose for ($1)"
#CL arg must be one of 
#   filter  - filter the firehose for a default (given) set of keywords
#		1 - new keywords obtained 10/06
#		2 - new keywords obtained 10/20
#   random  - stream random Arabic tweets from the firehose
#
# EXAMPLES:
# ./collector.sh filter 0
# sh ./collector.sh random


# root directory - where everything happens
ROOTDIR=/home/ubuntu/CraigsTwitterCollector/Twitterator
OUTDIR="${ROOTDIR}/stream_data"


# Keyword files
CONFIGDIR=/home/ubuntu/TwitterCollector/config
kwfile0="${CONFIGDIR}/isil_keywords.txt"
kwfile1="${CONFIGDIR}/isil_keywords_2.txt"
kwfile2="${CONFIGDIR}/trump_keywords.txt"


echo "Isil-Keywords Filter" 
kwfile=${kwfile0}
prefix="isil_keywords"
appname=Sekr_0

# Output directory for streaming files
outdir0="${OUTDIR}/${prefix}"
outdir=$outdir0

# Twitterator application path
twitterator="${ROOTDIR}/Twitterator.py"

email_file="${ROOTDIR}/email_credentials.json"

echo
echo "calling:    " ${twitterator}
echo "outdir:     " ${outdir}
echo "kwfile:     " ${kwfile}
echo "appname:    " ${appname}
echo "prefix:     " ${prefix}
echo



python3 ${twitterator} ${outdir} ${kwfile} ${appname} ${prefix} ${email_file}

#command=( "python3" ${twitterator} ${outdir} ${kwfile} ${appname} ${prefix} )
#
# execute it:
#"${command[@]}"


