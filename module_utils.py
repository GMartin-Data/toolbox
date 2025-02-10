from importlib.metadata import (
    version,                # For getting package version
    metadata,               # For getting package metadata
    requires,               # For getting package dependencies
    PackageNotFoundError,   # For handling missing packages
)
from packaging.requirements import Requirement
import subprocess
import sys


def check_package_info(package_name: str) -> None:
    """
    Modern approach to checking package information.
    """
    try:
        # Get version
        pkg_version = version(package_name)

        # Get package metadata
        pkg_meta = metadata(package_name)

        print(f"Package Information for {package_name}:")
        print(f"Version: {pkg_version}")
        print(f"Summary: {pkg_meta.get('Summary', 'No summary available')}")
        print(f"Home-page: {pkg_meta.get('Home-page', 'No homepage available')}")
        print(f"Author: {pkg_meta.get('Author', 'No author information')}")

        # Get requirements (if available)
        if requires(package_name):
            print("\nDependencies:")
            for req in requires(package_name):
                print(f"- {req}")

    except PackageNotFoundError:
        print(f"Package {package_name} is not installed")

        # Optionally, offer to install it
        response = input(f"Would you like to install {package_name}? (y/n): ")
        if response.lower() == "y":
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package_name]
                )
                print(f"Successfully installed {package_name}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {package_name}")


def get_detailed_requirements(
    package_name: str,
) -> list[dict[str, str | list[str] | None]]:
    """
    Retrieve and parse detailed dependency information for a Python package.

    This function analyzes a package's requirements using importlib.metadata and the
    packaging library to provide comprehensive information about its dependencies.
    It breaks down each requirement into its components: package name, version
    specifications, optional features (extras), and environmental markers.

    Parameters
    ----------
    package_name : str
        The name of the package to analyze. This should be the distribution name
        as it appears in pip (e.g., 'requests', 'boto3', 'pandas').

    Returns
    -------
    list[dict[str, str | list[str] | None]]
        A list of dictionaries, where each dictionary contains detailed information
        about a single requirement with the following keys:
        - 'name': str
            The name of the required package
        - 'specifier': str
            Version constraints (e.g., '>=1.0.0', '==2.1.*')
            Returns 'Any' if no specific version is required
        - 'extras': list[str]
            Optional features or components of the package
            Returns an empty list if no extras are specified
        - 'marker': str | None
            Environment markers (e.g., 'python_version >= "3.7"')
            Returns None if no markers are specified

    Raises
    ------
    importlib.metadata.PackageNotFoundError
        If the specified package is not installed
    packaging.requirements.InvalidRequirement
        If a requirement string cannot be parsed correctly

    Examples
    --------
    >>> reqs = get_detailed_requirements('requests')
    >>> for req in reqs:
    ...     print(f"Package: {req['name']}")
    ...     print(f"Version required: {req['specifier']}")
    Package: urllib3
    Version required: >=1.21.1,<3

    Notes
    -----
    The function uses importlib.metadata.requires(), which might return None for
    packages that don't declare their dependencies in a way that can be read by
    the tool. In such cases, an empty list is returned.

    See Also
    --------
    importlib.metadata.requires : Gets raw requirements strings
    packaging.requirements.Requirement : Parses requirement strings
    """
    if not (package_requires := requires(package_name)):
        return []

    detailed_requirements = []
    for req_string in package_requires:
        req = Requirement(req_string)
        detailed_requirements.append(
            {
                "name": req.name,
                "specifier": str(req.specifier) if req.specifier else "Any",
                "extras": list(req.extras) if req.extras else [],
                "marker": str(req.marker) if req.marker else None,
            }
        )
    return detailed_requirements


def install_if_missing(package: str, upgrade: bool = True) -> str | None:
    """
    Check if a package is installed and install it if missing.

    This function uses modern importlib.metadata.
    It checks if a package is installed, and if not, installs it.
    It can also upgrade existing packages if requested.

    Parameters:
        package: str
            The name of the package to check/install
        upgrade: bool, default=True
            Whether to upgrade the package if it's already installed

    Returns:
        str | None: The version of the installed package, or None if installation failed

    Examples:
        >>> install_if_missing("requests")
        'requests is already installed (version 2.28.1)'
        >>> install_if_missing("non-existent-package")
        'Successfully installed non-existent-package (version 1.0.0)'
    """
    try:
        # Try to get the current version using importlib.metadata
        current_version = version(package)

        if upgrade:
            print(f"Upgrading {package} from version {current_version}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", package]
            )
            # Get the new version after upgrae
            new_version = version(package)
            print(
                f"Successfully upgraded {package} from {current_version} to {new_version}"
            )
            return new_version
        else:
            print(f"{package} is already installed (version {current_version})")
            return current_version

    except PackageNotFoundError:
        print(f"Installing {package}")
        try:
            # Install the package
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            # Get and display the newly installed version
            installed_version = version(package)
            print(f"Successfully installed {package} (version {installed_version})")
            return installed_version

        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {str(e)}")
            return None


def install_requirements(
    requirements: list[str], upgrade: bool = True
) -> dict[str, str | None]:
    """
    Install multiple packages and return their versions.

    Parameters:
        requirements: list[str]
            List of package names to install
        upgrade: bool, default=True
            Whether to upgrade existing packages

    Returns:
        dict[str, Optional[str]]: Mapping of package names to their installed versions
    """
    return {
        package: install_if_missing(package, upgrade=upgrade)
        for package in requirements
    }
