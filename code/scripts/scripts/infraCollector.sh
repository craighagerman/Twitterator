#!/bin/bash
echo "Streaming from Twitter firehose for ($1)"
#
# NOTE: AWS sh *really* is sh. Have to run this script with:
#  $ bash infraCollector.sh

echo "- Syrian Infrastructure -" 

# root directory - where everything happens
# rootdir=/Users/chagerman/Dropbox/Code/Twitterator
rootdir=/home/ubuntu/Twitterator
# Twitterator application path
twitterator="${rootdir}/twitterator/Twitterator.py"

# Keyword files
kwfile="${rootdir}/resources/infrastructure_keywords.txt"
prefix="infra-keywords"
appname=Sekr_0

# Output directory for streaming files
outdir="${rootdir}/stream_data"

# Print parameters
myshell=$(ps -p $$)
echo "------------------------------------------------------
echo "rootdir:     ${rootdir}"
echo "twitterator: ${twitterator}"
echo "kwfile:      ${kwfile}"
echo "prefix:      ${prefix}"
echo "appname:     ${appname}"
echo "outdir:      ${outdir}"
echo "shell:     ${myshell}"
echo "------------------------------------------------------
echo 

# USAGE:
# Twitterator.py collection_kind stream_kind out_dir keyword_path appname prefix {langs}
# command=( "python3" $twitterator "infra" "filter" $outdir $kwfile $appname $prefix )
command=( "python3" $twitterator "infra" "filter" $outdir $kwfile $appname $prefix )

# execute it:
"${command[@]}"
