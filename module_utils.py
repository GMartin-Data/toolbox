import pkg_resources
import subprocess
import sys


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
