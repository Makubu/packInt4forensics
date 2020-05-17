import subprocess
import numpy as np
import re


def get_package_info(package=None):
    if package is None:
        raise ValueError("Missing package name")
    cmd = "dpkg -l | egrep \"^[iruph][icunfh]" + r"[\s]*[^\s]*" + package + "\""
    try:
        byte_out = subprocess.check_output(cmd, shell=True)
        string_out = byte_out.decode("utf-8")
    except subprocess.CalledProcessError as err:
        if err.returncode == 1:
            return None
        else:
            raise err
    lines = string_out.split("\n")
    packages_info = []
    for line in lines:
        split_line = re.sub(r"\s+", " ", line)
        split_line = split_line.split(" ")
        if len(split_line) <= 1:
            if re.match(r"^[iruph][icunfh]", split_line[0]) is not None:
                raise ImportError("Can't find the version of the packet, might be not given by dpkg")
            else:
                continue  # Blank line

        info = [split_line[i] for i in range(4)]
        desc = ""
        for word in range(len(split_line[4:])):
            desc = desc + " " + split_line[4 + word]

        info.append(re.sub(r"^\s+", "", desc))
        packages_info.append(info)

    return np.array(packages_info)


def search_package(package=None):
    if package is None:
        raise ValueError("Missing package name")
    info = get_package_info(package=package)
    if info is None:
        str_to_print = "\nThe search for " + package + " package returned no package\n"
        print(str_to_print)
        return None, 0
    elif len(info[:, 1]) == 1:
        str_to_print = "\nThe info for " + package + " package returned only 1 package :\n"
    else:
        str_to_print = "\nThe info for " + package + " package returned " + str(len(info[:, 1])) + " different " \
                                                                                                   "packages:\n "

    print(str_to_print)

    max_size_col = [0, 0, 0, 0, 0]

    for pack_info in info:
        for col_ind, col in enumerate(pack_info):
            max_size_col[col_ind] = max(len(col), max_size_col[col_ind])

    max_size_col[0] = len("install info ==")
    max_size_col[3] = len("Arch =")

    print("Install info  ==" + " Package name " + "=" * (max_size_col[1] - len("Package name")) + " Version " + "=" * (
            max_size_col[2] - len("Version")) + " Arch == " + "Description ")

    for pack_info in info:
        str_info = ""
        for col_ind, col in enumerate(pack_info):
            str_info = str_info + col + " " * (max_size_col[col_ind] - len(col)) + "  "
        print(str_info)

    return info, len(info[:, 1])
