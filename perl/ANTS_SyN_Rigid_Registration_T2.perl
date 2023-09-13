#!/usr/bin/perl

use strict;
use warnings;
use File::Find;
use File::Basename;
use File::Spec;

# Define the root folder containing multiple subfolders with T2w volumes
my $root_folder = "/path/to/root/folder";

# Define the common template files
my $dim = 3;
my $data = "/home/monica/T1T2Atlas/icbm152_ext55_model_sym_2020";
my $f = "$data/mni_icbm152_t2_tal_nlin_sym_55_ext.nii";
my $mask = "$data/mni_icbm152_t1_tal_nlin_sym_55_ext_mask.nii";

# Common variables for transformation and registration
my $ccradius = 4; # Declare the $ccradius variable here

# Function to process each volume
sub process_volume {
    my $volume_file = $_;
    my $volume_folder = $File::Find::dir;

    return unless $volume_file =~ /\.nii\.gz$/; # Process only .nii.gz files

    # Remove both .nii and .gz extensions from the $volume_file
    my ($volume_name, $volume_dirs, $file_ext) = fileparse($volume_file, qr/\.(nii|gz)$/);

    my @dirs = File::Spec->splitdir($volume_folder);
    my $last_dir = $dirs[-1];
    return unless $last_dir eq "T2w"; # Process only files in "T2w" subdirectories

    my $output_folder = File::Spec->catdir($volume_folder, ".."); # Output folder will be the parent directory
    my $outputname = "${volume_name}_rigid_affine_"; # Output file will have the prefix _rigid_affine_

    my $m = File::Spec->catfile($volume_folder, $volume_file);

    print("Processing $m\n");

    my $ccradius = 4;
    my $metricRigid = "CC[$f,$m,1.0,$ccradius]";

    my $ridigconvergence = "[100x50x25,1e-6,10]";
    my $rigidshrinkfactors = "12x8x4";
    my $rigidsmoothingsigmas = "4x3x2vox";
    my $transformRigid = "Rigid[0.1] --metric $metricRigid --convergence $ridigconvergence --shrink-factors $rigidshrinkfactors --smoothing-sigmas $rigidsmoothingsigmas";

    $ccradius = 4;
    my $metricAffine = "CC[$f,$m,1.0,$ccradius]";

    my $affineconvergence = "[100x50x25,1e-6,10]";
    my $affineshrinkfactors = "12x8x4";
    my $affinesmoothingsigmas = "4x3x2vox";
    my $transformAffine = "Affine[0.1] --metric $metricAffine --convergence $affineconvergence --shrink-factors $affineshrinkfactors --smoothing-sigmas $affinesmoothingsigmas";

    my $syngradientstep = 0.1;
    my $synupdatefield = 3;
    my $syntotalfield = 0;

    $ccradius = 4;
    my $metricSyN = "CC[$f,$m,1.0,$ccradius]";

    my $synconvergence = "[50x50x50,1e-6,10]";
    my $synshrinkfactors = "4x2x1";
    my $synsmoothingsigmas = "3x2x1vox";
    my $transformSyN = "SyN[$syngradientstep, $synupdatefield, $syntotalfield] --metric $metricSyN --convergence $synconvergence --shrink-factors $synshrinkfactors --smoothing-sigmas $synsmoothingsigmas";


    system("/home/davidpet/antsRegistration --verbose 1 --float 1 --dimensionality $dim --output [$output_folder/$outputname,${output_folder}/${outputname}Warped.nii] --interpolation Linear --use-histogram-matching 0 --transform $transformRigid --transform $transformAffine");
}

# Traverse through the root folder and its subdirectories to process each volume
find(\&process_volume, $root_folder);
