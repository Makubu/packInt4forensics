import subprocess
import numpy as np
import re


def get_package_version(package=None):
    if package is None:
        raise ValueError("Missing package name")
    cmd = "dpkg -l | egrep \"^[iruph][icunfh]" + r"[\s]*[^\s]*" + package + "\""
    byte_out = subprocess.check_output(cmd, shell=True)
    string_out = byte_out.decode("utf-8")
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

