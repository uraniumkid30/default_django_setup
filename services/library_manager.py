import os
import pkg_resources


def clean_requrements_for_production():
    """for new version of pip to avoid conflict"""
    re_pattern: str = "==\w+.+.+"
    dump_data: list = []
    with open("requirements/base.txt") as package_file:
        packages = package_file.read()
        packages = packages.splitlines()
        for package in packages:
            dump_data.append(package.split("==")[0])
    with open("requirements/base.txt", "w") as package_file:
        for package in dump_data:
            package_file.write(f"{package}\n")


def update_requirements():
    LIBRARY_MANAGER: str = os.environ.get('LIBRARY_MANAGER', "PIP")
    if LIBRARY_MANAGER == "PIP":
        list_of_packages: list = [tuple(str(ws).split()) for ws in pkg_resources.working_set]
        all_packages: dict = dict(sorted(list_of_packages, key=lambda x: (x[0].lower(), x)))
        packages_available: list = []
        try:
            with open("requirements/base.txt", "r") as package_file:
                for _package in package_file:
                    packages_available.append(_package.replace("\n", ""))

            if len(all_packages.items()) > len(packages_available):
                with open("requirements/base.txt", "w") as package_file:
                    for _package, _version in all_packages.items():
                        package_file.write(f"{_package}\n")
                with open("requirements/development.txt", "w") as package_file:
                    for _package, _version in all_packages.items():
                        package_file.write(f"{_package}=={_version}\n")
        except FileNotFoundError as err:
            print(f"Error {err}")
