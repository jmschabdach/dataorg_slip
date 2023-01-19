#!/usr/bin/bash

SCRIPTPATH=$(dirname "$0")
echo $SCRIPTPATH
BASE=$1

# BASE=/Users/schabdachj/Data/sandbox/
SRC=$BASE/sourcedata
OUT=$BASE/rawdata

for subj in $SRC/*/ ; do   
    echo $subj
    subjbase=$(basename -- $subj)

    # Occasionally, the next immediate subdirectory is Radiology.
    INDIR="$SRC/{subject}/*/{session}/*/*/*.dcm"

    # For each session the subject has
    for deidses in $subj/*/ ; do
        for sess in $deidses/*/ ; do 
            sessbase=$(basename $sess)                

            # Convert the .dcm files to avoid a JPG Compression error
#            if [ -L $sess/*.dcm ] ; then
#                datalad unlock $sess
#            fi
            find $sess -name '*.dcm' -exec gdcmconv -w {} {} \; 
            
            echo $sess
            ls $sess
            # Run heudiconv
            heudiconv -d $INDIR -o $OUT -f $SCRIPTPATH/heuristic.py -s $subjbase -ss $sessbase -c dcm2niix -b --overwrite

        done
    done
done

