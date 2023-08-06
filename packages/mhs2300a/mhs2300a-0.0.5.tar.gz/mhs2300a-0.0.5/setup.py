from setuptools import setup, find_packages


setup(
    name="mhs2300a",
    version='0.0.5',
    description='Python module for controlling inexpensive MHS-2300A signal generators',
    author="Ferrer, Manuel",
    py_modules=["mhs2300a"],
    package_dir={'':'src'},
    install_requires=[
        'pyserial>=3.5',
        'cached-property>= 1.5.2',
    ],
    classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            ],
)

