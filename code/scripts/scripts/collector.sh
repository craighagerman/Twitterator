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
rootdir=/Users/chagerman/Dropbox/Code/Twitterator
# rootdir=/home/ubuntu/Twitterator
# Twitterator application path
twitterator="${rootdir}/twitterator/Twitterator.py"

# Keyword files
kwfile0="${rootdir}/keywordfiles/keywords_a.txt"



case $1 in 
	"random" )
		echo "RANDOM FIREHOSE STREAM"
		kwfile="None"
		prefix="random"
		appname=mProbe
		;;
	"filter" )
		echo "FIREHOSE FILTER"
		;;
esac

case $2 in
    0)
        echo "FILTER A-" 
        kwfile=${kwfile0}
        prefix="keywords-a"
        appname=Sekr_0
        ;;

esac


# Output directory for streaming files
outdir="${rootdir}/stream_data"

echo
echo "calling:    " ${twitterator}
echo "collection:  ukraine"
echo "kind:       " $1
echo "outdir:     " ${outdir}
echo "kwfile:     " ${kwfile}
echo "appname:    " ${appname}
echo "prefix:     " ${prefix}
echo "langs:      " ${langs}
echo



command=( "python3" ${twitterator} "arabic" $1 ${outdir} ${kwfile} ${appname} ${prefix})
# execute it:
"${command[@]}"


