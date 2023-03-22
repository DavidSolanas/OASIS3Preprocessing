import os
import sys
import shutil

def remove_empty_folders():
    folder = './OASIS3'
    for session_folder in os.listdir(folder):
        session_path = os.path.join(folder, session_folder)

        for anat in os.listdir(session_path):
            anat_path = os.path.join(session_path, anat)
            if 'anat' in anat:
                shutil.rmtree(anat_path)
            else:
                # remove T1w, T2w folder if empty
                if len(os.listdir(anat_path)) == 0:
                    print(anat_path)
                    shutil.rmtree(anat_path)


def remove_folders_with_one_scan_type():
    folder = './OASIS3'
    for session_folder in os.listdir(folder):
        session_path = os.path.join(folder, session_folder)
        scan_folders = os.listdir(session_path)
        if len(scan_folders) == 1:
            # remove folder since it only has 1 scan type
            shutil.rmtree(session_path)
            



def usage_message():
    print('Usage: python remove_unused_folders.py <type>')
    print('<type>:')
    print('\t1 for OASIS empty folders.')
    print('\t2 for OASIS folders with just one scan type.')

if __name__ == "__main__":
    if  len(sys.argv) < 2:
        print('Error: Wrong number of parameters, expected 2.')
        usage_message()
        exit()

    try:
        type = int(sys.argv[1])
    except Exception as e:
        print(e)
        usage_message()
        exit(1)

    if type == 1:
        remove_empty_folders()
    else:
        remove_folders_with_one_scan_type()