function load_volumes(currentPath, session_id)
    % Check if the current directory contains the specified NIfTI files
    if exist(fullfile(currentPath, 'orig_nu_noskull_mni_rigid_affine_no_skullWarped.nii'), 'file')

        % Load NIfTI files
        nii = load_nii(fullfile(currentPath, 'orig_nu_noskull_mni.nii.gz'));
        orig = nii.img;
        orig = permute(orig, [1, 3, 2]);
        orig = flipdim(orig, 2);
        save_nii(make_nii(orig), fullfile(currentPath, 'orig_nu_noskull_mni_prealigned.nii'));
        
    else
        disp(['Skipping folder "', currentSubdir, '" as required NIfTI files are not present.']);
    end
end

