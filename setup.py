from setuptools import setup, find_packages

setup(
    name="FabricCLI",  
    version="0.0.1",
    packages=find_packages(),  
    install_requires=[
        "click",  
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "fabric=fabric_cli.main:main",  
        ],
    },
    author="Danny de Bree",
    author_email="d.debree@rubicon.nl",
    description="A CLI tool for managing Microsoft Fabric",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    ##url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
