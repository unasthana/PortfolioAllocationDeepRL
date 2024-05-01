import subprocess

def install_packages():
    packages = [
        "line_profiler",
        "stable-baselines3",
        "shimmy",
        "pyfolio-reloaded",
        "wrds",
        "swig",
        "git+https://github.com/AI4Finance-Foundation/FinRL.git"
    ]

    # Loop through each package and install it
    for package in packages:
        try:
            # Run pip install command
            subprocess.check_call(["pip", "install", package])
            print(f"Successfully installed {package}")

        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
              print(f"Successfully installed {package}. To use it, you will have to restart runtime.")
            
            else:
              print(f"Failed to install {package}: {e}")
