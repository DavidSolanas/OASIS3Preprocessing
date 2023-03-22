import os
import shutil

if __name__ == "__main__":
    folder = './OASIS3'
    for session_folder in os.listdir(folder):
        session_path = os.path.join(folder, session_folder)
        print(session_path)

        if not os.path.exists(os.path.join(session_path, 'T1w')):
            os.mkdir(os.path.join(session_path, 'T1w'))

        if not os.path.exists(os.path.join(session_path, 'T2w')):
            os.mkdir(os.path.join(session_path, 'T2w'))

        for anat in os.listdir(session_path):
            if not 'anat' in anat:
                continue
            anat_path = os.path.join(session_path, os.path.join(anat, 'NIFTI'))
            filename = os.listdir(anat_path)[0]
            if 'acq-TSE' in filename:
                print(filename)
            else:
                scan = 'T1w'
                if 'T1w' in filename:
                    scan = 'T1w'
                else:
                    scan = 'T2w'

                shutil.copy(os.path.join(anat_path, filename), os.path.join(session_path, scan))
        
        # remove T1w, T2w folder if empty
        #if len(os.listdir(os.path.join(session_path, 'T1w'))) == 0:
        #    shutil.rmtree(os.path.join(session_path, 'T1w'))

        #if len(os.listdir(os.path.join(session_path, 'T2w'))) == 0:
        #    shutil.rmtree(os.path.join(session_path, 'T2w'))
