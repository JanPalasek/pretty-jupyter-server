import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pretty-jupyter-server',
    author="Jan Palasek",
    version='0.1a',
    description="Web server for Pretty Jupyter online demo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={
        "": "src"
    },
    packages=setuptools.find_packages("src")
)
