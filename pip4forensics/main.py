import getopt
import sys
import good_usage
import get_package_info
import check_package

if len(sys.argv[1:]) is 0:
    good_usage.good_usage()
else:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:c:hd", ["search=", "check=", "help", "debug"])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            good_usage.good_usage()
            sys.exit()
        elif opt in ("-d", "--debug"):
            global _debug
            _debug = 1
        elif opt in ("-s", "--search"):
            get_package_info.search_package(package=arg)
            sys.exit()
        elif opt in ("-c", "--check"):
            check_package.check_package(package=arg)
            sys.exit()