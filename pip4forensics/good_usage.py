def good_usage():
    txt = "\nPip4forensics description:" \
          "\n       pip4forensics is a forensic program that help verify if a package has been corrupted." \
          "\n       Please provide the name of the package you want to check\n"
    txt2 = "\nCommands:   " \
           "\n       -s or --search to search a package" \
           "\n       -c or --check to check a package" \
           "\n       -h or --help for help" \
           "\n\nOptions:" \
           "\n       -k or --keep, keeps all the computed hashes and legitimate files in the working directory " \
           "\n       -l or --list, print all the legitimate and local unknown files " \
           "\n       --diff to compute the diffs of the corrupted files if any were to be found " \
           "\n       -d or --directory to indicate the directory where to download the package to check, extract it " \
           "and compute the hashes. NOTE: This directory, if it already exists, will be emptied in a first step, " \
           "if you want to indicate an already existing package, use -p option " \
           "\n       -p or --package to indicate the legitimate package to compare with the installed package, " \
           "and thus to avoid downloading the package" \
           "\n       -D or --Debug for debug mode\n"
    print(txt + txt2)
