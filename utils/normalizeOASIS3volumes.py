import os
import nibabel as nib
import numpy as np
from scipy.interpolate import interpn


####################################################################
# El orden de ejecución de las funciones es según están definidas:
#    1: Crop
#    2: Resize
#    3: MinMax Norm
####################################################################



def _1_cropOASIS3(img: np.ndarray) -> np.ndarray:
    # Precomputed crop for OASIS3 processed volumes
    min_x = 14
    max_x = 179
    min_y = 16
    max_y = 221
    min_z = 60
    max_z = 242

    img =  img[min_x-1:max_x+1, min_y-1:max_y+1, min_z-1:max_z+1]
    return img


def _2_resizeOASIS3(img: np.ndarray, shape=(128, 128, 128)) -> np.ndarray:
    xx = np.arange(shape[1]) 
    yy = np.arange(shape[0])
    zz = np.arange(shape[2])

    xx = xx * img.shape[1] / shape[1]
    yy = yy * img.shape[0] / shape[0] 
    zz = zz * img.shape[2] / shape[2]

    grid = np.rollaxis(np.array(np.meshgrid(xx, yy, zz)), 0, 4)

    sample = np.stack((grid[:, :, :, 1], grid[:, :, :, 0], grid[:, :, :, 2]), 3)
    xxx = np.arange(img.shape[1])
    yyy = np.arange(img.shape[0])
    zzz = np.arange(img.shape[2])  

    img = img[0:img.shape[0],0:img.shape[1],0:img.shape[2]]

    img = interpn((yyy, xxx, zzz), img, sample, method='linear', bounds_error=False, fill_value=0)

    return img


def _3_normalizeOASIS3(img: np.ndarray) -> np.ndarray:
    # Normalize the values to be in the range of 0-1
    img_norm = (img - img.min()) / (img.max() - img.min())

    # Scale the values to be in the range of 0-255 (este paso solo para CycleGAN3D, para Voxelmorph dejar entre [0-1])
    #img_scaled = img_norm * 255
    return img_norm


if __name__ == '__main__':
    # Ruta de la carpeta principal
    carpeta_principal = 'path/to/test/images'

    # Recorre las subcarpetas
    for root, _, _ in os.walk(carpeta_principal):
        # Verifica si la subcarpeta contiene "T1w" y "T2w"
        if "T1w" in root or "T2w" in root:
            # Ruta al archivo "volumen.nii.gz"
            archivo_nii = os.path.join(root, 'orig_nu_noskull_mni_prealigned_rigid_affine_no_skullWarped.nii.gz')
            
            if os.path.exists(archivo_nii):
                try:
                    # Carga el archivo NIfTI utilizando nibabel
                    imagen_nii = nib.load(archivo_nii)
                    # Haz lo que necesites con la imagen (por ejemplo, acceder a sus datos)
                    img = imagen_nii.get_fdata()
                    img = _1_cropOASIS3(img)
                    img = _2_resizeOASIS3(img)
                    img = _3_normalizeOASIS3(img)
                    # Puedes realizar operaciones en 'datos' aquí

                    # Imprime la información de la imagen
                    img_type = "T1w" if "T1w" in root else "T2w"

                    # Create a NIfTI image object
                    nifti_image = nib.Nifti1Image(img, affine=None)  # You can specify the affine transformation if needed

                    # Define the output file path
                    output_file = os.path.join(root, f'real{img_type}.nii.gz')  # Specify the desired file name and path

                    # Save the NIfTI image to a file
                    nib.save(nifti_image, output_file)
                    
                except nib.filebasedimages.ImageFileError:
                    print(f"Error al cargar el archivo: {archivo_nii}")
