img = load_nii('/home/david/Documentos/tfm/dataset/OASIS3_processed/OAS30001_d0129/T1w/orig_nu_noskull_mni.nii.gz');
img = img.img;

save_vtk_float( img, [1.0, 1.0, 1.0], [0.0, 0.0, 0.0], '/home/david/Documentos/tfm/dataset/OASIS3_processed/OAS30001_d0129/T1w/orig_nu_noskull_mni.vtk' )