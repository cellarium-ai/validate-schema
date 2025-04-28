from setuptools import setup

with open("requirements.txt") as fh:
    requirements = fh.read().splitlines()

setup(
    name="cellarium-schema",
    version="0.0.1",
    url="https://github.com/cellarium-ai/validate-schema",
    license="BSD 3-Clause",
    author="Cellarium Lab",
    author_email="sfleming@broadinstitute.org",
    description="Tool for applying and validating (cellxgene-like) integration schema to single cell datasets",
    long_description="Tool for applying and validating (cellxgene-like) integration schema to single cell datasets",
    install_requires=requirements,
    python_requires=">=3.10",
    packages=["cellarium_schema"],
    package_dir={"cellarium_schema": "cellarium_schema"},
    package_data={"cellarium_schema": ["gencode_files/*.gz"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    entry_points={"console_scripts": ["cellarium-schema = cellarium_schema.cli:schema_cli"]},
)
