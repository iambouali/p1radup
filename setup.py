from setuptools import setup

setup(
    name='p1radup',
    version='1.0.0',
    scripts=['p1radup/p1radup.py'],
    install_requires=[
        'termcolor',
    ],
    author='Tarek Bouali',
    author_email='contact@tarekbouali.com',
    description='This script identifies duplicate query parameters within each URL and retains only the first occurrence of each parameter for a given hostname.',
    url='https://github.com/iambouali/p1radup',  # Replace with your GitHub repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
