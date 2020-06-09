import subprocess
import numpy as np
import re


def get_package_info(package=None):
    if package is None:
        raise ValueError("Missing package name")
    cmd = "pip list | egrep \"" + package + "\""
    try:
        byte_out = subprocess.check_output(cmd, shell=True)
        string_out = byte_out.decode("utf-8")
    except subprocess.CalledProcessError as err:
        if err.returncode == 1:
            return None
        else:
            exit(1)
    lines = string_out.split("\n")
    packages_info = []
    for line in lines:
        split_line = re.sub(r"\s+", " ", line)
        split_line = split_line.split(" ")
        if len(split_line) <= 1:
            if len(split_line) == 1 and re.match(r"[^t]+", split_line[0]):
                raise ImportError("Can't find the version of the package, might be not given by pip")
            else:
                continue  # Blank line
        if split_line[0] is "Package":
            continue

        info = [split_line[i] for i in range(2)]
        packages_info.append(info)

    return np.array(packages_info)


def search_package(package=None):
    if package is None:
        raise ValueError("Missing package name")
    info = get_package_info(package=package)
    if info is None:
        str_to_print = "\nThe search for \"" + package + "\" package returned no package\n"
        print(str_to_print)
        return None, 0
    elif len(info[:, 1]) == 1:
        str_to_print = "\nThe search for \"" + package + "\" package returned only 1 package :\n"
    else:
        str_to_print = "\nThe search for \"" + package + "\" package returned " + str(len(info[:, 1])) + " different " \
                                                                                                   "packages:\n "

    print(str_to_print)

    max_size_col = [len("Package name "), 0]

    for pack_info in info:
        for col_ind, col in enumerate(pack_info):
            max_size_col[col_ind] = max(len(col), max_size_col[col_ind])

    print("Package name " + "=" * (max_size_col[1] - len("Package name")) + "  Version ")

    for pack_info in info:
        str_info = ""
        for col_ind, col in enumerate(pack_info):
            str_info = str_info + col + " " * (max_size_col[col_ind] - len(col)) + "  "
        print(str_info)

    return info, len(info[:, 1])
