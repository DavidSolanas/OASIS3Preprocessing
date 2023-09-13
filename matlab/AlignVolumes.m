% Define the parent directory containing the folders with NIfTI files
parentDir = '/home/david/Documentos/tfm/dataset/OASIS3_processed';

% List all subdirectories (folders) in the parent directory
subdirs = dir(parentDir);
subdirs = subdirs([subdirs.isdir]); % Keep only directories
subdirs = subdirs(~ismember({subdirs.name}, {'.', '..'})); % Remove '.' and '..'

% Loop through each subdirectory
for subdirIndex = 1:length(subdirs)
    currentSubdir = subdirs(subdirIndex).name;
    currentPath = fullfile(parentDir, currentSubdir);
    
    % Check if the current subject directory contains T1w and T2w subdirectories
    t1Dir = fullfile(currentPath, 'T1w');
    t2Dir = fullfile(currentPath, 'T2w');
    
    if ~exist(t1Dir, 'dir') || ~exist(t2Dir, 'dir')
        disp(['Skipping subject "', currentSubject, '" as T1w or T2w directories are missing.']);
        continue;
    end

    flipdimvolumes(t1Dir, [currentSubdir, '_T1w'])
    flipdimvolumes(t2Dir, [currentSubdir, '_T2w'])
    
end