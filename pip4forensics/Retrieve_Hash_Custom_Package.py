import os
import shutil
import subprocess
import tarfile


# Used this function for compatibility issues (subprocess.run) don't work for all Python versions
def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)
    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE
    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr


# For later improvements, do functions f("name of the packet")
# Function for extraction
# Function for computing the hashes and putting them in a file (V1 = check only those in md5sums) (V2 = compute all of the files in data.tar.xz)
# Function for checking the hashes

working_directory = os.getcwd()
print(working_directory)
os.mkdir(working_directory + "/Debian_package_extraction_folder")  # Handle exceptions (eg. no more space)

# Copy deb file from Download folder (deb_src) to here for manipulations
deb_src = working_directory + "/../Example_Package/cheese-common_3.34.0-1_all.deb"
dst_folder = working_directory + "/Debian_package_extraction_folder"
shutil.copy(deb_src, dst_folder)  # Handle exceptions (eg. no more space)

# Extract deb content (ar archive and other archives after) -> md5sums + paths which interest us
os.chdir(working_directory + "/Debian_package_extraction_folder")
deb_extraction = run(["ar", "-x", "cheese-common_3.34.0-1_all.deb"])  # Handle the exceptions
print("Deb Extraction Terminated")
control_xz_extraction = run(["tar", "-xf", "control.tar.xz", "./md5sums"])  # Handle the exceptions
print("Theoretical md5sums Extraction Terminated")

# Now will compare theoretical md5 with ones in the system


# Delete these temporary files to keep some space
# os.chdir(working_directory)
# shutil.rmtree("./Debian_package_extraction_folder")
