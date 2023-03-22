import os
import shutil

if __name__ == "__main__":
    folder = './OASIS3/'
    for patient_folder in os.listdir(folder):
        patient_path = os.path.join(folder, patient_folder)

        for session_folder in os.listdir(patient_path):
            session_path = os.path.join(patient_path, session_folder)
            print(session_path)
            shutil.move(session_path, folder)

        # all sessions moved, remove patient folder  
        shutil.rmtree(patient_path)
