from setuptools import setup, find_packages

setup(
    name="flow_analysis",
    version="0.1.0",
    author="Brendan Foley",
    author_email="brendanfoley1214@gmail.com",
    description="A package for flow cytometry data analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bfoley12/flow_analysis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "polars",
        "matplotlib",
        "seaborn",
        "FlowIO"
    ],
    include_package_data=True,
)
