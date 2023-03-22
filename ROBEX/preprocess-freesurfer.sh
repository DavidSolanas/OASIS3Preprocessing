#!/bin/bash

BASE_DIR='/Disco2021-I/david/tfm/dataset/OASIS3/*'
#export SUBJECTS_DIR='./OASIS3_subjects/'


if ! [ -d "$SUBJECTS_DIR" ];
then
    echo "AAAA"
    mkdir $SUBJECTS_DIR
fi

for session_dir in $BASE_DIR    # list directories in the form "/tmp/dirname/"
do
    session_dir=${session_dir%*/}      # remove the trailing "/"
    echo "${session_dir}"    # print everything after the final "/"

    for scan_dir in $session_dir/*    # list directories in the form "/tmp/dirname/"
    do
        scan_dir=${scan_dir%*/}      # remove the trailing "/"
        echo "${scan_dir}"    # print everything after the final "/"
        for files in $scan_dir/*    # list directories in the form "/tmp/dirname/"
        do
            file=${files%*/}      # remove the trailing "/"
            echo "${file}"    # print everything after the final "/"
            outfolder=$(echo $file | tr "/." "_")
            outfolder=${outfolder#*_} # remove prefix ending in "_"
            outfolder=${outfolder#*_} # remove prefix ending in "_"
            echo "$outfolder"
            #freeview
            # Execute recon-all if file does not exists
            if ! [ -f "$SUBJECTS_DIR/$outfolder/orig_nu.mgz" ];
            then
                recon-all -subject $outfolder -i $file -autorecon1
                robex_input_path="$SUBJECTS_DIR/$outfolder/mri/orig_nu.mgz"
                mv $robex_input_path $SUBJECTS_DIR
                rm -rf "$SUBJECTS_DIR/$outfolder"/*
                mv "$SUBJECTS_DIR/orig_nu.mgz" "$SUBJECTS_DIR/$outfolder/"
            fi
            # Convert to nii.gz file format
            input_folder="$SUBJECTS_DIR/$outfolder"
            robex_input_path="$input_folder/orig_nu.mgz"
            if ! [ -f "$input_folder/orig_nu.nii.gz" ];
            then
                mri_convert $robex_input_path "$input_folder/orig_nu.nii.gz"
            fi

            robex_input_path="$input_folder/orig_nu.nii.gz"
            robex_output_path="$input_folder/orig_nu_noskull.nii.gz"
            if ! [ -f $robex_output_path ];
            then
                ./ROBEX "$robex_input_path" "$robex_output_path"
            fi
            break
        done
    done
done