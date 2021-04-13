#!/bin/bash
echo "Streaming from Twitter firehose for Russian " $1
# arg $1 = kind (filter, random) arg $2 = variation
#CL arg must be one of 
#   filter  - filter the firehose for a default (given) set of keywords
#       1 - keyword list a
#       2 - keyword list b
#       3 - keyword list c
#   random  - stream random Russian tweets from the firehose
#
# EXAMPLE USAGE:
# ./ukraineCollector.sh filter 1

# python3 $twitterator ukraine $1 $outdir $kwfile $appname $prefix $langs 

# root directory - where everything happens
rootdir=/home/ubuntu/Twitterator
# Twitterator application path
twitterator="${rootdir}/twitterator/Twitterator.py"

# Keyword files
kwfile0="${rootdir}/keywordfiles/ukraineKeywords_1113a.txt"
kwfile1="${rootdir}/keywordfiles/ukraineKeywords_1113b.txt"
kwfile2="${rootdir}/keywordfiles/ukraineKeywords_1113c.txt"
kwfile3="${rootdir}/keywordfiles/ukraineKeywords_1113d.txt"
# Languages to filter for
langs="ru,uk"

case $1 in 
	"random" )
		echo "RANDOM UK, RU FIREHOSE STREAM"
		kwfile="None"
		prefix="ru-uk-random"
		appname=goat_team_0
		;;
	"filter" )
		echo "FIREHOSE FILTER"
		;;
esac

case $2 in
    0)
        echo "FILTER -11/13 A-" 
        kwfile=$kwfile0
        prefix="ukraine-keywords-a"
        appname=goat_team_1
        ;;
    1)
        echo "FILTER -11/13 B-" 
        kwfile=$kwfile1
        prefix="ukraine-keywords-b"
        appname=goat_team_2
        ;;
    2)
        echo "FILTER -11/13 C-" 
        kwfile=$kwfile2
		prefix="ukraine-keywords-c"
		appname=goat_team_3
        ;;
    3)
        echo "FILTER -11/13 D-" 
        kwfile=$kwfile3
        prefix="ukraine-keywords-d"
        appname=goat_team_4
        ;;
esac

outdir="${rootdir}/stream_data/"

command=( "python3" $twitterator "ukraine" $1 $outdir $kwfile $appname $prefix $langs )
# execute it:
"${command[@]}"


