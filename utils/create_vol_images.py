import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Define the root folder path
root_folder = './OASIS3_final/validation'
dest_folder = './OASIS3_final_images/validation'

# Precomputed crop
#(xmin: 14 xmax:179, ymin: 16 ymax:221, zmin: 60 zmax:242)
min_x = 14
max_x = 179
min_y = 16
max_y = 221
min_z = 60
max_z = 242


def save_central_slices_as_png(volume_path, output_path):
    """
    Save central slices (sagittal, coronal, axial) from a NIfTI volume as a PNG image.

    Args:
        volume_path (str): Path to the NIfTI volume file.
        output_path (str): Path to save the PNG image.
    """
    # Load the NIfTI volume
    nifti_image = nib.load(volume_path)

    # Get the NIfTI data as a NumPy array
    volume_data = nifti_image.get_fdata()

    # Crop the volume to the precomputed size
    volume_data = volume_data[min_x-1:max_x+1, min_y-1:max_y+1, min_z-1:max_z+1]

    # Get the dimensions of the volume
    depth, height, width = volume_data.shape

    # Calculate the central slice indices for each dimension
    central_sagittal_slice = depth // 2
    central_coronal_slice = height // 2
    central_axial_slice = width // 2

    # Create a subplot with central slices for each dimension
    plt.figure(figsize=(12, 4))
    
    # Sagittal slice (YZ plane)
    plt.subplot(1, 3, 1)
    plt.imshow(volume_data[central_sagittal_slice, :, :].T, cmap='gray', origin='lower')
    plt.title(f'Sagittal Slice {central_sagittal_slice}')
    plt.axis('off')

    # Coronal slice (XZ plane)
    plt.subplot(1, 3, 2)
    plt.imshow(volume_data[:, central_coronal_slice, :].T, cmap='gray', origin='lower')
    plt.title(f'Coronal Slice {central_coronal_slice}')
    plt.axis('off')

    # Axial slice (XY plane)
    plt.subplot(1, 3, 3)
    plt.imshow(volume_data[:, :, central_axial_slice], cmap='gray', origin='lower')
    plt.title(f'Axial Slice {central_axial_slice}')
    plt.axis('off')

    # Adjust the layout and save the image as PNG
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()



# Recursively iterate through subdirectories
for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file == 'orig_nu_noskull_mni_prealigned_rigid_affine_no_skullWarped.nii':
            file_path = os.path.join(root, file)
            dest_path = os.path.join(dest_folder, root.split('\\')[-2] + '_' + root.split('\\')[-1] + '.png')
            save_central_slices_as_png(file_path, dest_path)
            

