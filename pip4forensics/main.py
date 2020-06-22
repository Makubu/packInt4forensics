import getopt
import sys
import good_usage
import get_package_info
import check_package

download_dir = 'download_dir'
already_downloaded_package = None
keep = False
debug = False
diff = False
listing=False

if __name__ == '__main__':

    if len(sys.argv[1:]) is 0:
        good_usage.good_usage()
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "s:c:d:p:hDkzl", ["search=", "check=", "directory=", "package=", "help", "Debug", "keep", "diff", "list"])
        except getopt.GetoptError:
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-d", "--directory"):
                download_dir = arg
            elif opt in ("-p", "--package"):
                already_downloaded_package = arg
            elif opt in ("-D", "--Debug"):
                debug = True
            elif opt in ("-k", "--keep"):
                keep = True
            elif opt in ("-l", "--list"):
                listing = True
            elif opt in "--diff":
                diff = True

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                good_usage.good_usage()
                sys.exit(0)
            elif opt in ("-s", "--search"):
                get_package_info.search_package(package=arg)
                sys.exit(0)
            elif opt in ("-c", "--check"):
                check_package.check_package(package=arg, download_dir=download_dir, already_downloaded_package=already_downloaded_package, debug = debug, keep=keep, diff=diff, listing=listing)
                sys.exit(0)