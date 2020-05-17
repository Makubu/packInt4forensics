def good_usage():
    txt = "\n       dpkg4forensics is a forensic program that help verify if a package has been corrupted." \
          "\n       Please provide the name of the package you want to check\n"
    txt2 = "\n       -s or --search to search a package, -c or --check to check a package, -d or --debug for debug " \
           "mode, -h or --help for help\n "
    print(txt + txt2)