def good_usage():
    txt = "\nPip4forensics description:" \
          "\n       pip4forensics is a forensic program that help verify if a package has been corrupted." \
          "\n       Please provide the name of the package you want to check\n"
    txt2 = "\nCommands:   " \
           "\n       -s or --search to search a package" \
           "\n       -c or --check to check a package" \
           "\n       -h or --help for help" \
           "\n\nOptions:" \
           "\n       -d or --directory to indicate the directory where to download the package to check" \
           "\n       -p or --package to indicate the legitimate package to compare with the installed package, " \
           "and thus to avoid downloading the package" \
           "\n       -D or --Debug for debug mode\n"
    print(txt + txt2)
