#!/bin/bash

# Directorio principal que contiene los subdirectorios
DIRECTORIO_PRINCIPAL="/home/david/TFM/dataset/OASIS3_processed"


# Crear un array para almacenar los nombres de directorios que ya han sido procesados
declare -A directorios_procesados

# Recorre los subdirectorios dentro del directorio principal
for subdirectorio in $DIRECTORIO_PRINCIPAL/*; do
  if [ -d "$subdirectorio" ]; then # Verifica si el elemento es un directorio
    # Obtiene el nombre actual del subdirectorio
    nombre_actual=$(basename "$subdirectorio")
    
    # Extrae el PATID, SESID y TYPE del nombre actual
    patid=$(echo "$nombre_actual" | awk -F '_' '{print $5}')
    sesid=$(echo "$nombre_actual" | awk -F '_' '{print $7}')
    type=$(echo "$nombre_actual" | awk -F '_' '{print $8}')
    
    # Genera el nuevo nombre del subdirectorio
    nuevo_nombre="${patid}_${sesid}_${type}"
    
    # Renombra el subdirectorio
    mv "$subdirectorio" "$DIRECTORIO_PRINCIPAL/$nuevo_nombre"
    
    echo "El subdirectorio $nombre_actual se ha renombrado a $nuevo_nombre"
    
    # Verifica si el directorio actual ya ha sido procesado
    if [[ ! -z ${directorios_procesados["$patid$sesid"]} ]]; then
      # Si el directorio ya ha sido procesado, mueve el directorio actual a la carpeta correspondiente
      mv "${DIRECTORIO_PRINCIPAL}/${nuevo_nombre}/orig_nu_noskull.nii.gz" "${DIRECTORIO_PRINCIPAL}/${patid}_${sesid}/${type}"
      mv "${DIRECTORIO_PRINCIPAL}/${nuevo_nombre}/orig_nu.nii.gz" "${DIRECTORIO_PRINCIPAL}/${patid}_${sesid}/${type}"
      
      echo "1. El directorio $nuevo_nombre ha sido movido a ${patid}_${sesid}/${type}"
    else
      # Si el directorio no ha sido procesado, crea un directorio nuevo para agrupar los directorios con mismo PATID y SESID
      mkdir "${DIRECTORIO_PRINCIPAL}/${patid}_${sesid}"
      
      # Crea dos directorios dentro del nuevo directorio para los directorios con mismo PATID y SESID pero distinto TYPE
      mkdir "${DIRECTORIO_PRINCIPAL}/${patid}_${sesid}/T1w"
      mkdir "${DIRECTORIO_PRINCIPAL}/${patid}_${sesid}/T2w"
      
      # Mueve el directorio actual a la carpeta correspondiente
      mv "${DIRECTORIO_PRINCIPAL}/${nuevo_nombre}/orig_nu_noskull.nii.gz" "${DIRECTORIO_PRINCIPAL}/${patid}_${sesid}/${type}"
      mv "${DIRECTORIO_PRINCIPAL}/${nuevo_nombre}/orig_nu.nii.gz" "${DIRECTORIO_PRINCIPAL}/${patid}_${sesid}/${type}"
      
      echo "2. El directorio $nuevo_nombre ha sido movido a ${patid}_${sesid}/${type}"
      
      # Marca el directorio como procesado en el array
      directorios_procesados["$patid$sesid"]=1
	fi
	rm -rf "${DIRECTORIO_PRINCIPAL}/${nuevo_nombre}"
  fi
done






