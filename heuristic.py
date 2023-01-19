import os
import numpy as np


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

#     data = create_key('run{item:03d}')
#     info = {data: []}
#     last_run = len(seqinfo)

    # Create the template output filename for each modality
    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:03d}_T1w')
    spgr = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-SPGR_run-{item:03d}_T1w')
    mpr = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-MPR_run-{item:03d}_T1w')
    tse = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-TSE_run-{item:03d}_T1w')

    t2w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:03d}_T2w')
    flair = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:03d}_FLAIR')
    angio = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:03d}_angio')

    asl = create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_run-{item:03d}_asl')
    dti = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:03d}_dwi')
    ep2d = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:03d}_EP2D')
    
    bold = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_run-{item:03d}_BOLD')
   
   # Set up the dictionary of modality types
    info = {
                t1w: [],
                mpr: [],
                tse: [],
                t2w: [],
                flair: [],
                dti: [],
                ep2d: [],
                spgr: [],
                bold: [],
                asl: []
            }

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
        protocol = s.protocol_name.lower()
        description = s.series_description.lower()

        if str(s.is_derived) == "False" and s.dim1 > 0 and s.dim2 > 0 and s.dim3 > 0:
            if "mpr" in protocol or "mpr" in description:
                print("MPR found")
                info[mpr].append(s.series_id)
            elif "asl" in protocol or "asl" in description:
                print("ASL found")
                info[asl].append(s.series_id)
            elif ("dti" in protocol or "dti" in description) and s.dim4 > 0:
                print("DTI found")
                info[dti].append(s.series_id)
            elif "tse" in protocol or "tse" in description:
                print("TSE found")
                info[tse].append(s.series_id)
            elif ("bold" in protocol or "bold" in description) and s.dim4 > 0:
                print("BOLD found")
                info[bold].append(s.series_id)
            elif "flair" in protocol or "flair" in description:
                print("FLAIR found")
                info[flair].append(s.series_id)
            elif "spgr" in protocol or "spgr" in description:
                print("SPGR found")
                info[spgr].append(s.series_id)
            elif "t1" in protocol or "t1" in description:
                print("Generic T1 found")
                info[t1w].append(s.series_id)
            elif "t2" in protocol or "t2" in description:
                print("Generic T2 found")
                info[t2w].append(s.series_id)
            else:
                print("OTHER:", protocol, description)

    return info
