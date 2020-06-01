import os
import shutil
import zipfile

# For later improvements, do functions f("name of the packet")
# 1) Function for extraction
# 2) Function for computing the hashes and putting them in a file
# 3) Function for checking the hashes
# For the moment consider Python VirtualEnv = ~/.local

''' Function for Extraction '''

package_name = "numpy-1.18.4-cp35-cp35m-manylinux1_x86_64.whl"

working_directory = os.getcwd()
extraction_folder_name = "/Pip_package_extraction_folder"
print("You are working in the directory: " + working_directory)
os.mkdir(working_directory + extraction_folder_name)  # Handle exceptions (eg. no more space)

# Copy pip whl file from Download folder (deb_src) to here for manipulations
deb_src = working_directory + "/../../Package_PIP_Example/" + package_name
dst_folder = working_directory + extraction_folder_name
shutil.copy(deb_src, dst_folder)  # Handle exceptions (eg. no more space)
print("Whl package successfully copied")
os.chdir(working_directory + extraction_folder_name)
new_name_for_unzipping = package_name.replace(".whl", ".zip")
os.rename(package_name, new_name_for_unzipping)

# Extract content of whl file
with zipfile.ZipFile(new_name_for_unzipping, "r") as Whl_Pckg_zip:
    Whl_Pckg_zip.extractall()

''' Compute hashes extracted file'''
extracted_interesting_folder = "numpy"  # Will need to use Regex to get the right name out of the zip folder
hash_file = open("hash_file.txt", "w")
hash_file.write("Beginning of Hash File\n")
hash_file.close()
# r=root, d=directories, f = files
for r, d, f in os.walk(working_directory + extraction_folder_name + extracted_interesting_folder):
    for file in f:
        path_of_file = os.path.join(r, file)
        # Compute hash of file + store it hash_file







# Delete these temporary files to keep some space
os.chdir(working_directory)
shutil.rmtree("./Debian_package_extraction_folder")

