#!/bin/sh

# This tool is a quick & dirty tool to launch transcoding processes
# I will make it re-usable and generic soon. For now, 
# consider it highly experimental and use-at-your-own-risk.

# TODO:
# - license headers
# - getopts & help
# - check path first for post-process.sh

set -m

STARTDIR=`pwd`
export STARTDIR

find . -type d -mindepth 1 |\
while read directory
do
   DIR=`basename ${directory}`
   echo "Launching processing engine for: ${DIR}"
   LOGFILE="${STARTDIR}/${DIR}.log"
   echo "Logs will be in ${LOGFILE}"
   ~/freeseer/bin/post-process.sh ${directory} &> ${LOGFILE} &
   echo "Engine launched for ${DIR}"
done
