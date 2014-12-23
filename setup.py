from setuptools import setup, find_packages

setup(
    name="swcpy",
    version="0.1",
    install_requires=["cffi"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
