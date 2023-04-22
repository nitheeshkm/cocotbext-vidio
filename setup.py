"""Setup file to create a PIP package"""

from setuptools import setup

setup(
    name='cocotbext-vidio',
    version='0.0.1',
    description='One stop shop for all your video simulation',
    url='https://github.com/nitheeshkm/pytpg',
    author='Nitheesh Manjunath',
    author_email='nitheesh2013@gmail.com',
    license='MIT License',
    install_requires=['cocotbext.axi',
                      'numpy',
                      'cocotb',
                      ],
    python_requires = '>=3.6',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',  
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Framework :: cocotb"]
)
