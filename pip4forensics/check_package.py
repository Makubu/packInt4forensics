import os
import re
import shutil
import subprocess
import get_package_info
import Retrieve_Hash_Custom_PIP_Package
import numpy as np
from colorama import Fore, Style, Back, init


def find_check_package(package=None):
    found_package = None
    package_info = get_package_info.get_package_info(package=package)

    if package_info is None:
        print("\nThere is no package matching the search for \"" + package + "\" \n")
        return None
    elif len(package_info[:, 0]) == 1:  # number of package found
        package_version = package_info[0][1]
        found_package = (package, package_version)
        return found_package
    else:
        is_in_package_list = package in package_info[:, 0]

        if not is_in_package_list:
            print("\nMore than one package were found for " + package + " " + "package, please write the full name "
                                                                              "of the package within the following "
                  + str(len(package_info[:, 0])) + " packages:\n ")
        else:
            print("\nThe package " + package + " has been found but several packages can match this name, please "
                                               "confirm the full name of the package you want to check within the "
                                               "following "
                  + str(len(package_info[:, 0])) + " packages:\n\n ")
        max_len = 0
        for package_name in package_info[:, 0]:
            max_len = max(max_len, len(package_name))
        str_to_print = ""
        for pack_ind, package_name in enumerate(package_info[:, 0]):
            if pack_ind % 2 == 0:
                str_to_print = package_name + " " * (max_len - len(package_name) + 2)
                if pack_ind == len(package_info[:, 0]) - 1:
                    print(str_to_print)
            else:
                str_to_print = str_to_print + package_name
                print(str_to_print)
        print("")
        print(">> ", end='')
        new_package = input()
        if is_in_package_list:
            if new_package == package:
                index = np.where(package_info[:, 0] == package)[0][0]
                package_version = package_info[index][1]
                found_package = (package, package_version)
                return found_package
            else:
                found_package = find_check_package(package=new_package)
                return found_package
        else:
            found_package = find_check_package(package=new_package)
            return found_package


def download_pip_package(package_name, package_version=None, download_dir='download_dir',
                         already_downloaded_package=None):
    if already_downloaded_package is not None:
        return os.getcwd() + "/" + already_downloaded_package

    try:
        os.makedirs(download_dir)
    except FileExistsError as err:
        pass

    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    try:
        os.chdir(download_dir)
        subprocess.check_call('pip download --no-deps ' + package_name + '==' + package_version, shell=True)
        os.chdir('../')
    except Exception:
        print("A problem occurred while downloading the package " + package_name + " in version " + package_version)
        return None
    return os.getcwd() + "/" + download_dir + "/" + os.listdir(download_dir)[0]


def check_package(package=None, download_dir='download_dir', already_downloaded_package=None, debug=False, keep=False,
                  diff=False, listing=False):
    package_info = find_check_package(package)
    if package_info is None:
        return 0
    package_name, package_version = package_info[0], package_info[1]

    cmd = "pip show " + package_name + " | egrep \"^Location\""
    byte_out = subprocess.check_output(cmd, shell=True)
    string_out = byte_out.decode("utf-8")
    package_location = re.sub(r"\s", "", string_out.split(" ")[1])

    print("\nThe check for packet " + package_version + " at version " + str(
        package_version) + " has started\n")

    legitimate_package = download_pip_package(package_name, package_version, download_dir, already_downloaded_package)

    if debug:
        print("Legitimate package downloaded at " + legitimate_package)

    extraction_directory = Retrieve_Hash_Custom_PIP_Package.extract_package_current_directory(package_name,
                                                                                              legitimate_package,
                                                                                              debug=debug)

    hash_file_name = Retrieve_Hash_Custom_PIP_Package.compute_hashes_legit_package(extraction_directory)

    legit_files, corrupted_files, unknown_file, path_to_corrupted_files = Retrieve_Hash_Custom_PIP_Package.compute_hashes_package_installed(
        package_location, package_name, hash_file_name, extraction_directory, debug=debug)

    if diff:
        Retrieve_Hash_Custom_PIP_Package.compute_differences(package_location, package_name, corrupted_files,
                                                             path_to_corrupted_files, debug=debug)

    if not keep:
        Retrieve_Hash_Custom_PIP_Package.delete_temp_extraction_directory(debug=debug)

    if debug or listing:
        print(Fore.GREEN)
        print("Legitimate files:")
        if len(legit_files) == 0:
            print('None')
        else:
            print(*legit_files, sep = ", ")

        print(Fore.RED)
        print("Corrupted files:")
        if len(corrupted_files) == 0:
            print('None')
        else:
            print(*corrupted_files, sep = ", ")

        print(Fore.YELLOW)
        print("Unknown files:")
        if len(unknown_file) == 0:
            print('None')
        else:
            print(*unknown_file, sep = ", ")

    init(autoreset=True)
    if len(corrupted_files) > 0:
        print(Fore.RED + Back.LIGHTWHITE_EX + "\nRESULTS: Some corrupted files were found :")
        print(corrupted_files)
    else:
        print(Fore.GREEN + Style.BRIGHT +Back.LIGHTBLACK_EX + "\nRESULTS: No corrupted file has been found" + Style.RESET_ALL + "\n")

    return 0
