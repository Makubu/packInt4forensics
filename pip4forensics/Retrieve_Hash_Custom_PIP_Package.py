import os
import shutil
import zipfile
import hashlib


# Goal: Compute the sha256 of a file
# Argument: Path to the file
# Return: The sha-256 hash of the file
def sha_256_computation(file_to_hash):  # file_to_hash is a path
    BLOCK_SIZE = 4096
    file_hash = hashlib.sha256()  # Create the hash object
    with open(file_to_hash, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE)  # Read and update hash string value in blocks of 4K
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


# Goal: Extract a whl package in a subdirectory of the current directory
# Arguments: Name of the whl package associated to the package, directory in which we will create folder and unzip files, and directory where
# the legitimate whl packages were previously downloaded
# Return: the directory where the whl package has been extracted
def extract_package_current_directory(package_name_whl, working_directory, download_directory):
    os.chdir(working_directory)
    extraction_folder_name = "/Pip_package_extraction_folder"
    print("You are working in the directory: " + working_directory)
    try:
        os.mkdir(working_directory + extraction_folder_name)
    except OSError:
        print("Could not create extraction folder")
    # Copy pip whl file from Download folder (deb_src) to here for manipulations
    deb_src = download_directory + package_name_whl
    dst_folder = working_directory + extraction_folder_name
    try:
        shutil.copy(deb_src, dst_folder)  # Handle exceptions (eg. no more space)
    except IOError:
        print("Could not copy the package. Package downloaded is not in the right folder")
    print("Whl package successfully copied")
    os.chdir(working_directory + extraction_folder_name)
    new_name_for_unzipping = package_name_whl.replace(".whl", ".zip")
    os.rename(package_name_whl, new_name_for_unzipping)
    # Extract content of whl file
    with zipfile.ZipFile(new_name_for_unzipping, "r") as Whl_Pckg_zip:
        try:
            Whl_Pckg_zip.extractall()
        except Exception as e:
            print("Errors when unzipping the whl package" + e)
    print(os.getcwd())
    return os.getcwd()


# Goal: Compute the hashes of the files present in the package package_name and store them in a file
# Arguments: the package for which we want to extract the hashes for a later comparison, the directory where the extraction was done)
# Returns: The name of the hash file which contains the computed hashes
def compute_hashes_legit_package(package_name, working_directory):
    extracted_interesting_folder = package_name
    hash_file_name="hash_file.txt"
    hash_file = open(hash_file_name, "w")  # Create the file
    hash_file.write("Beginning of Hash File:")
    hash_file.close()
    print("File containing the hashes successfully initialized")
    hash_file = open(hash_file_name, "a")  # Each time append to the file
    # r=root, d=directories, f=files
    for r, d, f in os.walk(working_directory + extracted_interesting_folder):
        for file in f:
            path_of_file = os.path.join(r, file)
            # Compute hash of file + store it hash_file
            hash_of_file = sha_256_computation(path_of_file)
            # Write the file name and the hash in the hash_file
            hash_file.write(file + "\n")  # One line = name of the file
            hash_file.write(hash_of_file + "\n")  # The next line = hash value of the file
            # Then we will just search for a file and take the next line to get its hash value
    hash_file.close()
    print("End of Extraction legitimate files")
    print(hash_file_name)
    return hash_file_name


# Goal: Compute the hashes of the installed packages to compare them with the legitimate ones
# Arguments: The VE path where the packages are installed, the package name, the name of the file which contains the
# hashes of the legitimate packages
# Returns: List of legitimate file, modified files, and non existing files compared to the legitimate package files
def compute_hashes_package_installed(virtual_env_path, package_name, extracted_hash_values_file):
    ve_interesting_folder = package_name
    file_to_list = []
    legitimate_files = []
    corrupted_files = []
    unknown_files = []
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
                    legitimate_files.append(file)
                else:
                    corrupted_files.append(file)
            except ValueError:  # In case file is not in the list of legitimate files
                unknown_files.append(file)
    print("End of Checking\n")
    return legitimate_files, corrupted_files, unknown_files


# Goal: Delete the temporary directories created -> to clean some space
# Arguments: Directory in which we created the extraction folder in the first place
# Returns: Nothing, it's just deleting files
def delete_temp_extraction_directory(working_directory):
    os.chdir(working_directory)
    extraction_folder_name = "/Pip_package_extraction_folder"
    try:
        shutil.rmtree("." + extraction_folder_name)
    except IOError:
        print("Could not clean the directory\n")
    print("Temporary package extraction folder successfully deleted\n")


# Example of use: ( WARNING: Do not change working directory between different functions !)
example_package_name = "/numpy"
example_package_name_whl = "numpy-1.18.4-cp35-cp35m-manylinux1_x86_64.whl"
virtual_env_path_example = "/home/gael/.local/lib/python2.7/site-packages"
working_dir = os.getcwd()
download_dir = working_dir+"/../../Package_PIP_Example/"

extraction_directory = extract_package_current_directory(example_package_name_whl, working_dir, download_dir)
name_file_containing_hashes = compute_hashes_legit_package(example_package_name, extraction_directory)
list_legit_files, list_corrupt_files, list_unknown_file = compute_hashes_package_installed(virtual_env_path_example, example_package_name, name_file_containing_hashes)
print("Legitimate files:")
print(list_legit_files)
print("\n")
print("Corrupted files:")
print(list_corrupt_files)
print("\n")
print("Unknown files:")
print(list_unknown_file)
print("\n")
# delete_temp_extraction_directory(working_dir)


