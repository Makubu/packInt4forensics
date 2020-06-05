import os
import shutil
import zipfile
import hashlib


# For later improvements, do functions f("name of the packet")
# 1) Function for extraction
# 2) Function for computing the hashes and putting them in a file
# 3) Function for checking the hashes
# For the moment consider Python VirtualEnv = ~/.local

def sha_256_computation(file_to_hash):  # file_to_hash is a path
    BLOCK_SIZE = 4096
    file_hash = hashlib.sha256()  # Create the hash object
    with open(file_to_hash, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE)  # Read and update hash string value in blocks of 4K
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


''' Function for Extraction '''

package_name = "numpy-1.18.4-cp35-cp35m-manylinux1_x86_64.whl"

working_directory = os.getcwd()
extraction_folder_name = "/Pip_package_extraction_folder"
print("You are working in the directory: " + working_directory + "\n")
os.mkdir(working_directory + extraction_folder_name)  # Handle exceptions (eg. no more space)

# Copy pip whl file from Download folder (deb_src) to here for manipulations
deb_src = working_directory + "/../../Package_PIP_Example/" + package_name
dst_folder = working_directory + extraction_folder_name
shutil.copy(deb_src, dst_folder)  # Handle exceptions (eg. no more space)
print("Whl package successfully copied\n")
os.chdir(working_directory + extraction_folder_name)
new_name_for_unzipping = package_name.replace(".whl", ".zip")
os.rename(package_name, new_name_for_unzipping)

# Extract content of whl file
with zipfile.ZipFile(new_name_for_unzipping, "r") as Whl_Pckg_zip:
    Whl_Pckg_zip.extractall()

# Compute hashes extracted file
extracted_interesting_folder = "/numpy"  # Will need to use Regex to get the right python name out of the zip folder
hash_file = open("hash_file.txt", "w")
hash_file.write("Beginning of Hash File\n")
hash_file.close()
print("File containing the hashes successfully initialized\n")
# r=root, d=directories, f=files
for r, d, f in os.walk(working_directory + extraction_folder_name + extracted_interesting_folder):
    for file in f:
        path_of_file = os.path.join(r, file)
        # Compute hash of file + store it hash_file
        hash_of_file = sha_256_computation(path_of_file)
        print("File Name: " + file + "\n" + "File Hash : " + hash_of_file + "\n")
        # Write the file name and the hash in the hash_file
print("End of Extraction legitimate files \n\n\n\n\n")

# Compute the hashes of the package installed on the system
virtual_env_path = "/home/gael/.local/lib/python2.7/site-packages"  # Need to handle different Virtual Environments
ve_interesting_folder = "/numpy"  # Also will have to use some Regex to have the right name

for r_ve, d_ve, f_ve in os.walk(virtual_env_path + ve_interesting_folder):
    for file in f_ve:
        path_of_file = os.path.join(r_ve, file)
        hash_of_file = sha_256_computation(path_of_file)
        print("File Name: " + file + "\n" + "File Hash : " + hash_of_file + "\n")
print("End of Extraction system package files \n\n\n\n\n")

# Delete these temporary files to keep some space
os.chdir(working_directory)
shutil.rmtree("." + extraction_folder_name)
print("Temporary package extraction folder successfully deleted\n")
