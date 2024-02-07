from setuptools import setup, find_packages

setup(
    name='p1radup',
    version='2.0.2',
    packages=find_packages(),
    install_requires=[
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'p1radup = p1radup.p1radup:main',
        ],
    },
    author='Tarek Bouali',
    author_email='contact@tarekbouali.com',
    description='This tool is designed to process a list of URLs from an input file, remove duplicate query parameters, and save the modified URLs to an output file.',
    url='https://github.com/iambouali/p1radup',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
