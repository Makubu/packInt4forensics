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

# Compute hashes extracted file and put them in a text file
extracted_interesting_folder = "/numpy"  # Will need to use Regex to get the right python name out of the zip folder
hash_file = open("hash_file.txt", "w")  # Create the file
hash_file.write("Beginning of Hash File:\n")
hash_file.close()
print("File containing the hashes successfully initialized\n")
hash_file = open("hash_file.txt", "a")  # Each time append to the file
# r=root, d=directories, f=files
for r, d, f in os.walk(working_directory + extraction_folder_name + extracted_interesting_folder):
    for file in f:
        path_of_file = os.path.join(r, file)
        # Compute hash of file + store it hash_file
        hash_of_file = sha_256_computation(path_of_file)
        # print("File Name: " + file + "\n" + "File Hash : " + hash_of_file + "\n")
        # Write the file name and the hash in the hash_file
        hash_file.write(file + "\n")  # One line = name of the file
        hash_file.write(hash_of_file + "\n")  # The next line = hash value of the file
        # Then we will just search for a file and take the next line to get its hash value
hash_file.close()
print("End of Extraction legitimate files \n\n\n\n\n")

# Compute the hashes of the package installed on the system
virtual_env_path = "/home/gael/.local/lib/python2.7/site-packages"  # Need to handle different Virtual Environments
ve_interesting_folder = "/numpy"  # Also will have to use some Regex to have the right name
extracted_hash_values_file = "hash_file.txt"  # Will need to pass this as a parameter for final function

file_to_list = []
with open(extracted_hash_values_file, 'rt') as my_hash_file:
    for line in my_hash_file:
        file_to_list.append(line.rstrip('\n'))

for r_ve, d_ve, f_ve in os.walk(virtual_env_path + ve_interesting_folder):
    for file in f_ve:
        path_of_file = os.path.join(r_ve, file)
        hash_of_file = sha_256_computation(path_of_file)
        # print("File Name: " + file + "\n" + "File Hash : " + hash_of_file + "\n")
        # Compare the hash of the file with the one in hash_file
        try:
            index_file_in_hash_file_list = file_to_list.index(file)
            hash_legit_file = file_to_list[index_file_in_hash_file_list + 1]
            if hash_of_file == hash_legit_file:
                print("File: " + file + " is legitimate\n")
            else:
                print("File: " + file + " was corrupted\n")
        except ValueError:  # In case file is not in the list of legitimate files
            print("File: " + file + " is malicious. It doesn't exist in legitimate pip package\n")

print("End of Checking\n")

# Delete these temporary files to keep some space
os.chdir(working_directory)
shutil.rmtree("." + extraction_folder_name)
print("Temporary package extraction folder successfully deleted\n")
