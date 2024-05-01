import warnings
warnings.filterwarnings('ignore')

import threading
import subprocess

def install_package(package):
    try:
        subprocess.check_call(["pip", "install", package])
        print(f"Successfully installed {package}")
    
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
          print(f"Successfully installed {package}. To use it, you will have to restart runtime.")
        
        else:
          print(f"Failed to install {package}: {e}")

def manage_threads(packages):
    threads = [threading.Thread(target=install_package, args=(package,)) for package in packages]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def run_install_packages():
    packages = [
    "line_profiler",
    "stable-baselines3",
    "shimmy",
    "pyfolio-reloaded",
    "wrds",
    "swig",
    "git+https://github.com/AI4Finance-Foundation/FinRL.git"]

    manage_threads(packages)
