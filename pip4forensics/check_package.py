import get_package_info
import numpy as np
import subprocess
import re


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
        print(is_in_package_list)
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


def check_package(package=None):
    package_info = find_check_package(package)
    if package_info is None:
        return 0
    package_name, package_version = package_info[0], package_info[1]

    cmd = "pip show " + package_name + " | egrep \"^Location\""
    byte_out = subprocess.check_output(cmd, shell=True)
    string_out = byte_out.decode("utf-8")
    package_location = re.sub(r"\s", "", string_out.split(" ")[1])

    print("\nThe check for packet " + package_version + " at version " + str(
        package_version) + " located in " + package_location + " has started")

    return 0
