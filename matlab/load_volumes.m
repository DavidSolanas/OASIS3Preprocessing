function load_volumes(currentPath, session_id)
    % Check if the current directory contains the specified NIfTI files
    if exist(fullfile(currentPath, 'orig_nu_noskull_mni_prealigned_rigid_affine_no_skullWarped.nii'), 'file')

        % Load NIfTI files
        orig = load_nii(fullfile(currentPath, 'orig_nu_noskull_mni.nii.gz'));
        orig = orig.img;
        
        atlas = './T1T2Atlas/mni_icbm152_t1_tal_nlin_sym_55_ext_skull_strip.nii';

        if contains(session_id, 'T2w')
            atlas = './T1T2Atlas/mni_icbm152_t2_tal_nlin_sym_55_ext_skull_strip.nii';
        end

        atlas_volume = load_nii(atlas);
        atlas_volume = atlas_volume.img;

        warped = load_nii(fullfile(currentPath, 'orig_nu_noskull_mni_prealigned_rigid_affine_no_skullWarped.nii'));
        warped = warped.img;
        %warped = permute(warped, [1,3,2]);
        %warped = flipdim(warped, 3);

        % Perform operations on loaded data
        output_dir = '/home/david/Documentos/tfm/dataset/OASIS3_images/';

        %ver_nii(atlas_volume, [output_dir, session_id, '_atlasVol']);
        %ver_nii(warped, [output_dir, session_id, '_warped']);
        ver_nii(warped - atlas_volume, [output_dir, session_id, '_rigidWarped_atlas']);
    else
        disp(['Skipping folder "', currentSubdir, '" as required NIfTI files are not present.']);
    end
end

