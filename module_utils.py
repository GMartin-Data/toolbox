import pkg_resources
import subprocess
import sys


def check_package_health(package_name):
    """
    Comprehensive package health check using pkg_resources
    """
    try:
        # Get the distribution
        dist = pkg_resources.get_distribution(package_name)

        print(f"Package Information for {package_name}:")
        print(f"Version: {dist.version}")
        print(f"Location: {dist.location}")

        # Check dependencies
        print("\nDependencies:")
        for req in dist.requires():
            try:
                dep_dist = pkg_resources.get_distribution(req.project_name)
                print(f"✓ {req.project_name} {dep_dist.version}")
            except pkg_resources.DistributionNotFound:
                print(f"✗ Missing: {req.project_name}")

        # Check for any available resources
        print("\nAvailable Resources:")
        try:
            resources = pkg_resources.resource_listdir(package_name, "")
            for resource in resources:
                print(f"- {resource}")
        except (pkg_resources.ResourceManager.ResourceError, TypeError):
            print("No resources found")

    except pkg_resources.DistributionNotFound:
        print(f"Package {package_name} is not installed")


def install_if_missing(package: str) -> None:
    """
    Check an environment, to see if a given package is installed.
    If not, installs it to its latest version.
    """
    try:
        installed_version = pkg_resources.get_distribution(package).version
        print(f"{package} is already installed (version {installed_version})")
    except pkg_resources.DistributionNotFound:
        # Install the package and capture the output
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-qU", package])
        # Get and display the newly installed version
        new_version = pkg_resources.get_distribution(package).version
        print(f"Successfully installed {package} (version {new_version})")
