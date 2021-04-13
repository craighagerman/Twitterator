#!/bin/bash
echo "Streaming from Twitter firehose for arabic ($1)"
#CL arg must be one of 
#   filter  - filter the firehose for a default (given) set of keywords
#		1 - new keywords obtained 10/06
#		2 - new keywords obtained 10/20
#   random  - stream random Arabic tweets from the firehose
#
# EXAMPLES:
# ./arabicCollector.sh filter 0
# sh arabicCollector.sh random


# root directory - where everything happens
# rootdir=/Users/chagerman/Dropbox/Code/Twitterator
rootdir=/home/ubuntu/Twitterator
# Twitterator application path
twitterator="${rootdir}/twitterator/Twitterator.py"

# Keyword files
kwfile0="${rootdir}/keywordfiles/arabic_isil_1113a.txt"
kwfile1="${rootdir}/keywordfiles/arabic_isil_1113b.txt"
kwfile2="${rootdir}/keywordfiles/arabic_isil_1113c.txt"
kwfile3="${rootdir}/keywordfiles/opisis-keywords.txt"

# Languages to filter for
langs="ar"

case $1 in 
	"random" )
		echo "RANDOM AR FIREHOSE STREAM"
		kwfile="None"
		prefix="ar-random"
		appname=mProbe
		;;
	"filter" )
		echo "FIREHOSE FILTER"
		;;
esac

case $2 in
    0)
        echo "FILTER -11/13 A-" 
        kwfile=${kwfile0}
        prefix="isil-keywords-a"
        appname=Sekr_0
        ;;
    1)
        echo "FILTER -11/13 B-" 
        kwfile=${kwfile1}
        prefix="isil-keywords-b"
        appname=Sekr_1
        ;;
    2)
        echo "FILTER -11/13 C-" 
        kwfile=${kwfile2}
		prefix="isil-keywords-c"
		appname=Sekr_2
        ;;

    3)
        echo "FILTER -OP_ISIS-" 
        kwfile=${kwfile3}
		prefix="op-isis"
		appname=mProbe_0
        ;;


esac


# Output directory for streaming files
outdir="${rootdir}/stream_data"

command=( "python3" ${twitterator} "arabic" $1 ${outdir} ${kwfile} ${appname} ${prefix} ${langs} )
# execute it:
"${command[@]}"


