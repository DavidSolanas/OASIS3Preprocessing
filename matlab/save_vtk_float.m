function save_vtk_float( img, spacing, origin, filename );

fid = fopen( filename, 'w', 'ieee-be' );

% Header parameters
fprintf( fid, '# vtk DataFile Version 3.0 \n' );
fprintf( fid, 'Comments \n' );
fprintf( fid, 'BINARY \n' );
fprintf( fid, 'DATASET STRUCTURED_POINTS \n' );
dim = size( img );
s = size(dim)
if( s(2) == 2 ) 
    dim(3) = 1;
end;
fprintf( fid, 'DIMENSIONS %d %d %d \n', dim(1), dim(2), dim(3) );
% fprintf( fid, 'DIMENSIONS %d %d %d \n', dim(1), dim(2), 1 );
fprintf( fid, 'SPACING %f %f %f \n', spacing(1), spacing(2), spacing(3) );
fprintf( fid, 'ORIGIN %f %f %f \n', origin(1), origin(2), origin(3) );
fprintf( fid, 'POINT_DATA %d \n', prod(dim) );
fprintf( fid, 'SCALARS scalars float 1 \n' );
fprintf( fid, 'LOOKUP_TABLE default \n' );

fwrite( fid, img, 'float32' );

fclose( fid );
