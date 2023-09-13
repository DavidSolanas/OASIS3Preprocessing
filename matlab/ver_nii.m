function ver_nii(volume, outputFilename)
    % Get dimensions of the volume
    [~, ~, z_dim] = size(volume);
    
    % Calculate the central slice along the Z-axis
    central_slice = round(z_dim / 2);
    
    % Create a figure
    figure;
    
    % Plot sagittal (Y-X) slices
    subplot(1, 3, 1);
    montage(squeeze(volume(central_slice, :, :)), 'DisplayRange', []);
    title('Sagittal Slices');
    
    % Plot coronal (Z-X) slices
    subplot(1, 3, 2);
    montage(squeeze(volume(:, :, central_slice)'), 'DisplayRange', []);
    title('Coronal Slices');
    
    % Plot axial (Z-Y) slices
    subplot(1, 3, 3);
    montage(permute(volume(:, central_slice, :), [1, 3, 2]), 'DisplayRange', []);
    title('Axial Slices');
    
    % Save the combined figure as a PNG file
    saveas(gcf, outputFilename, 'png');
    
    % Close the figure
    close(gcf);
end

