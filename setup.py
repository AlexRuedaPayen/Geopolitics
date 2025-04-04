from setuptools import setup, find_packages

def read_requirements():
    """Read dependencies from requirements.txt"""
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="Geopolitics",  # Change this to your project name
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),  # Install dependencies listed in requirements.txt
    entry_points={
        "console_scripts": [
            "run-dashboard = scripts.dashboard:app.run_server"
        ],
    },
)
