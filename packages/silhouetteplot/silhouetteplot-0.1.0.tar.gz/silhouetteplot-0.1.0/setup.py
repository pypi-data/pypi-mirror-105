from setuptools import setup, find_packages

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
    version='0.1.0',
    description='A library to plot silhouette plot of KMeans clustering',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/BharathN96/silhouetteplot',
    author='Bharath N',
    author_email='nbharath96@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['python', 'machine learning', 'KMeans', 'classification', 'silhouette score'],
    packages=find_packages(),
    install_requires=['']
)
