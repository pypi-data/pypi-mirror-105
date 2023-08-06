import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dynoxhost",  # Replace with your own username
    version="1.0.1",
    author="tovade",
    author_email="support@tovade.ml",
    description="The official python package for dynoxhost",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dynox-Host/dynoxhost.py",
    project_urls={
        "Bug Tracker": "https://github.com/Dynox-Host/dynoxhost.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
