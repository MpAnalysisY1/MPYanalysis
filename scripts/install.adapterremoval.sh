#!/bin/bash

# AdapterRemoval

# Schubert, Lindgreen, and Orlando (2016). AdapterRemoval v2: rapid adapter trimming, identification, and read merging. BMC Research Notes, 12;9(1):88
# http://bmcresnotes.biomedcentral.com/articles/10.1186/s13104-016-1900-2

# Lindgreen (2012): AdapterRemoval: Easy Cleaning of Next Generation Sequencing Reads, BMC Research Notes, 5:337
# http://www.biomedcentral.com/1756-0500/5/337/

# This program searches for and removes remnant adapter sequences 
# from High-Throughput Sequencing (HTS) data and (optionally) trims 
# low quality bases from the 3' end of reads following adapter removal. 

# AdapterRemoval can analyze both single end and paired end data, 
# and can be used to merge overlapping paired-ended reads into (longer) 
# consensus sequences. Additionally, the AdapterRemoval may be used to 

# recover a consensus adapter sequence for paired-ended data, for which 
# this information is not available.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $SCRIPT_DIR
echo "Installing AdapterRemoval ..."

INSTALL_DIR="${SCRIPT_DIR}/../tools/AdapterRemoval"
rm -rf "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}"

tar -zxvf ../archives/adapterremoval-2.1.7.tar.gz -C $INSTALL_DIR
chmod a+rwx -R *
cd "$INSTALL_DIR/adapterremoval-2.1.7"
make

echo "Finished installing AdapterRemoval."
