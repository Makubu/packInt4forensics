import get_package_info


def find_check_package(package=None):
    package_info = get_package_info.get_package_info(package=package)
    package_number = len(package_info[:, 1])
    if package_number == 0:
        print("\nPlease provide the name of an installed package \n")
    elif package_number == 1:
        # TODO , package identifié, lancer la vérification du hash
        package_version = package_info[0][2]
        print("TODO, package version is " + package_version)
        exit(0)
    else:

        is_in_package_list = package in package_info[:, 1]
        if not is_in_package_list:
            print("\nMore than one package were found for " + package + " " + "package, please write the full name "
                                                                              "of the package within the following "
                  + str(len(package_info[:,
                            1])) + " packages:\n\n ")
        else:
            print("\nMore than one package were found for " + package + " " + "package, please confirm the full name "
                                                                              "of the package within the following "
                  + str(len(package_info[:,
                            1])) + " packages:\n\n ")
        max_len = 0
        for package_name in package_info[:, 1]:
            max_len = max(max_len, len(package_name))
        str_to_print = ""
        for pack_ind, package_name in enumerate(package_info[:, 1]):
            if pack_ind % 2 == 0:
                str_to_print = package_name + " " * (max_len - len(package_name) + 2)
                if pack_ind == len(package_info[:, 1]) - 1:
                    print(str_to_print)
            else:
                str_to_print = str_to_print + package_name
                print(str_to_print)
        print("")
        new_package = input()
        if is_in_package_list:
            if new_package == package:
                # TODO:trouver version dans la liste des différents paquets
                check_package(package=new_package, version=None)
            else:
                find_check_package(package=new_package)
        else:
            find_check_package(package=new_package)


def check_package(package=None, version=None):
    # TODO
    return 0
