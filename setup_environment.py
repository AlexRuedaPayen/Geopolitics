import os
import subprocess
import sys
import platform

def get_python_executable():
    """Returns the correct python executable for the current OS and virtual environment."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")  # Windows path
    else:
        return os.path.join("venv", "bin", "python")  # UNIX-like path

def get_pip_executable():
    """Returns the correct pip executable for the current OS and virtual environment."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip.exe")  # Windows path
    else:
        return os.path.join("venv", "bin", "pip")  # UNIX-like path

def create_virtualenv():
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    else:
        print("Virtual environment already exists.")

    # Ensure pip is installed and up-to-date
    subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    pip_executable = get_pip_executable()
    subprocess.check_call([sys.executable, pip_executable, "install", "--upgrade", "pip"])

def install_dependencies():
    """Install dependencies and set up the project in editable mode."""
    pip_executable = get_pip_executable()

    print("Installing project in editable mode...")
    subprocess.check_call([pip_executable, "install", "-e", "."])  # Editable install

    print("Installing dependencies from requirements.txt...")
    subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])

def main():
    """Main entry point to set up the environment."""
    create_virtualenv()
    install_dependencies()
    print("Setup complete!")

if __name__ == "__main__":
    main()
