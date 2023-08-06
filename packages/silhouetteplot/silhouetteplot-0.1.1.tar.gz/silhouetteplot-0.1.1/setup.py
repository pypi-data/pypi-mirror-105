from setuptools import setup, find_packages
from os import path

version = "0.1.1"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='silhouetteplot',
    version=version,
    description='A library to plot silhouette plot of KMeans clustering',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/BharathN96/silhouetteplot',
    author='Bharath N',
    author_email='nbharath96@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['python', 'machine learning', 'KMeans', 'classification', 'silhouette score'],
    packages=find_packages(),
    install_requires=['']
)
