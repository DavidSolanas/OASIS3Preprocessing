import argparse
from PIL import Image
import os
import numpy as np

def guardar_cortes_axiales(dir_path, dir_salida):
    """
    Itera por las subcarpetas en el directorio especificado, carga los volúmenes NIfTI y
    guarda los cortes axiales centrales de cada par de volúmenes en una imagen separada.

    Args:
        dir_path (str): Ruta del directorio que contiene las subcarpetas con los volúmenes NIfTI.
        dir_salida (str): Ruta del directorio de salida donde se guardarán las imágenes.

    Returns:
        None
    """
    # Iterar por cada subcarpeta
    for subcarpeta in os.listdir(dir_path):
        # Ruta completa de la subcarpeta
        subcarpeta_path = os.path.join(dir_path, subcarpeta)
        # Verificar si la subcarpeta es en realidad una carpeta
        if os.path.isdir(subcarpeta_path):
            # Ruta completa del fichero NIfTI dentro de la subcarpeta
            data_path = os.path.join(subcarpeta_path, "data.npy")
            # Cargar el volumen NIfTI usando la librería nibabel
            volumen = np.load(data_path)
            # Obtener el corte axial central del primer volumen (posición 0)
            corte_axial_0 = volumen[0, :, volumen.shape[2]//2, :]
            # Obtener el corte axial central del segundo volumen (posición 1)
            corte_axial_1 = volumen[1, :, volumen.shape[2]//2, :]
            # Normalizar los valores de intensidad del corte a [0, 255]
            corte_axial_0 = np.interp(corte_axial_0, (corte_axial_0.min(), corte_axial_0.max()), (0, 255)).astype(np.uint8)
            corte_axial_1 = np.interp(corte_axial_1, (corte_axial_1.min(), corte_axial_1.max()), (0, 255)).astype(np.uint8)
            # Crear una imagen PIL con cada corte y guardarla como un archivo separado
            img_corte_axial_0 = Image.fromarray(corte_axial_0)
            img_corte_axial_1 = Image.fromarray(corte_axial_1)
            nombre_archivo = f"cortes_axiales_{subcarpeta}.jpg"
            ruta_archivo = os.path.join(dir_salida, subcarpeta, nombre_archivo)
            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
            imagen_final = Image.new("RGB", (img_corte_axial_0.width*2, img_corte_axial_0.height))
            imagen_final.paste(img_corte_axial_0, (0, 0))
            imagen_final.paste(img_corte_axial_1, (img_corte_axial_0.width, 0))
            imagen_final.save(ruta_archivo)


if __name__ == "__main__":
    # Parsear los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description='Obtener los cortes axiales centrales de los volúmenes NIfTI en una carpeta y guardarlos como imágenes.')
    parser.add_argument('--dir_path', type=str, help='Ruta del directorio que contiene las subcarpetas con los volúmenes NIfTI.')
    parser.add_argument('--dir_salida', type=str, help='Ruta del directorio de salida donde se guardarán las imágenes.')
    args = parser.parse_args()

    # Llamar a la función para procesar los volúmenes y guardar los cortes axiales
    guardar_cortes_axiales(args.dir_path, args.dir_salida)