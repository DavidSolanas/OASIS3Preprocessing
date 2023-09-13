import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Define the root folder path
root_folder = './OASIS3_final/test'

# Initialize variables to store volume data
total_volume = None
num_volumes = 0




# Initialize variables to store minimum and maximum indices for each dimension
min_x, max_x = float('inf'), 0
min_y, max_y = float('inf'), 0
min_z, max_z = float('inf'), 0

# Background value
background_value = 0

# Function to compute minimum and maximum indices for each dimension
def compute_min_max_indices(data):
    global min_x, max_x, min_y, max_y, min_z, max_z

    # Get the dimensions of the data
    x, y, z = data.shape

    # Iterate through the data to find the min and max indices
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if data[i, j, k] != background_value:
                    min_x = min(min_x, i)
                    max_x = max(max_x, i)
                    min_y = min(min_y, j)
                    max_y = max(max_y, j)
                    min_z = min(min_z, k)
                    max_z = max(max_z, k)


            



average_volume = nib.load('avg_val.nii')
average_volume = average_volume.get_fdata()
print(average_volume.shape)

compute_min_max_indices(average_volume)

# Compute the safe crop size
crop_size_x = max_x - min_x + 1
crop_size_y = max_y - min_y + 1
crop_size_z = max_z - min_z + 1

print(f"Safe crop size: ({crop_size_x}, {crop_size_y}, {crop_size_z})")
print(f"Safe crop dims: (xmin: {min_x} xmax:{max_x}, ymin: {min_y} ymax:{max_y}, zmin: {min_z} zmax:{max_z})")



average_volume = average_volume[min_x-1:max_x+1, min_y-1:max_y+1, min_z-1:max_z+1]
print(average_volume.shape)

# Display the average volume as an image
plt.imshow(average_volume[:, :, average_volume.shape[2] // 2], cmap='gray')
plt.title('Average Volume')
plt.colorbar()
plt.show()


# Display the average volume as an image
plt.imshow(average_volume[:, average_volume.shape[1] // 2, :], cmap='gray')
plt.title('Average Volume')
plt.colorbar()
plt.show()

# Display the average volume as an image
plt.imshow(average_volume[average_volume.shape[0] // 2, :, :], cmap='gray')
plt.title('Average Volume')
plt.colorbar()
plt.show()
