import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Define the root folder path
root_folder = './OASIS3_final/validation'

# Initialize variables to store volume data
total_volume = None
num_volumes = 0

# Function to load and accumulate NIfTI volumes
def load_and_accumulate_nifti(filename):
    global total_volume, num_volumes

    # Load the NIfTI file
    img = nib.load(filename)
    data = img.get_fdata()

    if total_volume is None:
        total_volume = data
    else:
        total_volume += data

    num_volumes += 1


# Recursively iterate through subdirectories
for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file == 'orig_nu_noskull_mni_prealigned_rigid_affine_no_skullWarped.nii':
            file_path = os.path.join(root, file)
            load_and_accumulate_nifti(file_path)
            

# Compute the average volume
average_volume = total_volume / num_volumes

# Define the affine transformation matrix (usually an identity matrix for raw data)
affine = np.eye(4)

# Create a NIfTI image from the NumPy array and affine matrix
nifti_image = nib.Nifti1Image(average_volume, affine)

nib.save(nifti_image, 'avg_val.nii')
