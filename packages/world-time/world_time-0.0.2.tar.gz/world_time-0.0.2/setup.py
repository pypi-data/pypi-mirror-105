import setuptools

setuptools.setup(
    name="world_time",
    version="0.0.2",
    author="SDA",
    author_email="sda@sda.pl",
    description="Be in time",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
