import os
import shutil
import zipfile
import hashlib
import difflib
import main
import tarfile


# Goal: Compute the sha256 of a file
# Argument: Path to the file
# Return: The sha-256 hash of the file
def sha_256_computation(file_to_hash):
    BLOCK_SIZE = 4096
    file_hash = hashlib.sha256()
    with open(file_to_hash, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


# Goal: Extract a whl package in a subdirectory of the current directory
# Arguments: Name of the whl package associated to the package, directory in which we will create folder and unzip files, and directory where
# the legitimate whl packages were previously downloaded
# Return: the directory where the whl package has been extracted
def extract_package_current_directory(package_name, package_name_whl, debug = False):
    orcwd = os.getcwd()
    extraction_folder_name = "Pip_package_extraction_folder"
    try:
        os.mkdir(extraction_folder_name)
    except OSError:
        for filename in os.listdir(extraction_folder_name):
            file_path = os.path.join(extraction_folder_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                exit(1)
    except PermissionError as e:
        print(e)

    os.chdir(extraction_folder_name)



    if package_name_whl.endswith("tar.gz"):
        tar = tarfile.open(package_name_whl, "r:gz")
        tar.extractall()
        tar.close()
    elif package_name_whl.endswith("tar"):
        tar = tarfile.open(package_name_whl, "r:")
        tar.extractall()
        tar.close()
    else:
        with zipfile.ZipFile(package_name_whl, "r") as Whl_Pckg_zip:
            try:
                Whl_Pckg_zip.extractall()
            except Exception as e:
                print("Errors when unzipping the whl package" + e)


    extraction_folder_path = os.getcwd()
    os.chdir(orcwd)
    return extraction_folder_path


# Goal: Compute the hashes of the files present in the package package_name and store them in a file
# Arguments: the package for which we want to extract the hashes for a later comparison, the directory where the extraction was done)
# Returns: The name of the hash file which contains the computed hashes
def compute_hashes_legit_package(extraction_directory, debug = False):
    ordir = os.getcwd()
    os.chdir(extraction_directory)
    hash_file_name="hash_file.txt"
    hash_file = open(hash_file_name, "w")
    hash_file.write("Beginning of Hash File:")
    hash_file.close()
    if debug:
        print("File containing the hashes successfully initialized")
    hash_file = open(hash_file_name, "a")
    # r=root, d=directories, f=files
    for r, d, f in os.walk('./'):
        for file in f:
            path_of_file = os.path.join(r, file)
            # Compute hash of file + store it hash_file
            hash_of_file = sha_256_computation(path_of_file)
            # Write the file name and the hash in the hash_file
            hash_file.write(file + "\n")  # One line = name of the file
            hash_file.write(hash_of_file + "\n")  # The next line = hash value of the fileue
    hash_file.close()
    if debug:
        print("End of Extraction legitimate files")
    os.chdir(ordir)
    return hash_file_name


# Goal: Compute the hashes of the installed packages to compare them with the legitimate ones
# Arguments: The VE path where the packages are installed, the package name, the name of the file which contains the
# hashes of the legitimate packages, and the directory where the hash file is located
# Returns: List of legitimate file, modified files, and non existing files compared to the legitimate package files, also
# an additional list with the path of the corrupted files in the virtual environment
def compute_hashes_package_installed(virtual_env_path, package_name, extracted_hash_values_file, extraction_directory, debug=False):
    ordir = os.getcwd()
    os.chdir(extraction_directory)
    ve_interesting_folder = package_name
    file_to_list = []
    legitimate_files = []
    corrupted_files = []
    unknown_files = []
    corrupted_files_path = []
    try:
        with open(extracted_hash_values_file, 'rt') as my_hash_file:
            for line in my_hash_file:
                file_to_list.append(line.rstrip('\n'))
    except EnvironmentError:
        print("Error when reading the hash_file")

    for r_ve, d_ve, f_ve in os.walk(virtual_env_path + "/" + ve_interesting_folder):
        for file in f_ve:
            path_of_file = os.path.join(r_ve, file)
            hash_of_file = sha_256_computation(path_of_file)
            # Compare the hash of the file with the one in hash_file
            try:
                index_file_in_hash_file_list = file_to_list.index(file)
                hash_legit_file = file_to_list[index_file_in_hash_file_list + 1]
                if hash_of_file == hash_legit_file:
                    legitimate_files.append(file)
                else:
                    corrupted_files.append(file)
                    corrupted_files_path.append(path_of_file)
            except ValueError:  # In case file is not in the list of legitimate files
                unknown_files.append(file)
    if debug:
        print("End of Checking\n")
    os.chdir(ordir)
    return legitimate_files, corrupted_files, unknown_files, corrupted_files_path


# Goal: Delete the temporary directories created -> to clean some space
# Arguments: Directory in which we created the extraction folder in the first place
# Returns: Nothing, it's just deleting files
def delete_temp_extraction_directory(debug=False):
    extraction_folder_name = "/Pip_package_extraction_folder"
    try:
        shutil.rmtree("." + extraction_folder_name)
    except IOError:
        print("Could not clean the directory\n")
    if debug:
        print("Temporary package extraction folder successfully deleted\n")


def lists_content_print(leg_list, corr_list, unk_list):
    print("Legitimate files:")
    print(leg_list)
    print("")
    print("Corrupted files:")
    print(corr_list)
    print("")
    print("Unknown files:")
    print(unk_list)

def compute_differences(virtual_environment, package_name, corr_list, corr_list_path, debug=False):
    ordir = os.getcwd()
    package_name_stripped = package_name.replace("/", "_")
    difference_folder_name = "Diff_of_corrupted_packages_" + package_name_stripped
    files_not_differenced=[]


    try:
        os.mkdir(difference_folder_name)
    except OSError:
        for filename in os.listdir(difference_folder_name):
            file_path = os.path.join(difference_folder_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                exit(1)
    except PermissionError as e:
        print(e)

    os.chdir(difference_folder_name)
    for file_name_position in range(len(corr_list)):
        file_containing_differences = open(corr_list[file_name_position], "w")
        file_containing_differences.write("Beginning of Diff File:\n")
        file_containing_differences.close()
        Corrupted_file = corr_list_path[file_name_position]
        Legitimate_file = Corrupted_file.replace(virtual_environment, "/Pip_package_extraction_folder")
        file_containing_differences = open(corr_list[file_name_position], "a")
        try:
            with open(Legitimate_file) as Legit_file:
                Legit_file_content = Legit_file.read()
            with open(Corrupted_file) as Corrupt_file:
                Corrupt_file_content = Corrupt_file.read()
            for line in difflib.unified_diff(Legit_file_content, Corrupt_file_content, fromfile=Legitimate_file, tofile=Corrupted_file, lineterm='\n'):
                file_containing_differences.write(line)
        except EnvironmentError:
            file_containing_differences.write("Could not see the diff for this file -> not same locations (often it is just already done elsewhere) \n")
        file_containing_differences.close()
    if debug:
        print("Creation of the different Diff Files was successful \n")


# Example of use:
# Need only a starting defined working_dir. Then no need to specify anymore
def test():
    example_package_name = "/numpy"
    example_package_name_whl = "numpy-1.18.4-cp35-cp35m-manylinux1_x86_64.whl"
    virtual_env_path_example = "/home/gael/.local/lib/python2.7/site-packages"
    working_dir = os.getcwd()
    download_dir = working_dir+"/../../Package_PIP_Example/"

    extraction_directory = extract_package_current_directory(example_package_name_whl, download_dir)
    name_file_containing_hashes = compute_hashes_legit_package(example_package_name, extraction_directory)
    list_legit_files, list_corrupt_files, list_unknown_file, path_to_corrupted_files = compute_hashes_package_installed(virtual_env_path_example, example_package_name, name_file_containing_hashes, extraction_directory)
    # lists_content_print(list_legit_files, list_corrupt_files, list_unknown_file)
    compute_differences(virtual_env_path_example, example_package_name, list_corrupt_files, path_to_corrupted_files, working_dir)
    # A new folder is created in the current directory, which contains for each file the difference between the legitimate one and the one in the virtual environment.
    delete_temp_extraction_directory(working_dir)


