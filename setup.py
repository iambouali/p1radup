from setuptools import setup, find_packages

setup(
    name='p1radup',
    version='1.0.5',
    packages=find_packages(),
    install_requires=[
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'p1radup = p1radup.p1radup',
        ],
    },
    author='Tarek Bouali',
    author_email='contact@tarekbouali.com',
    description='This script identifies duplicate query parameters within each URL and retains only the first occurrence of each parameter for a given hostname.',
    url='https://github.com/iambouali/p1radup',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
