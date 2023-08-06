import setuptools
import subprocess
import os

with open('README.md') as f:
    README = f.read()

# if os.environ.get('CI_COMMIT_TAG'):
#     version = os.environ['CI_COMMIT_TAG']
# else:
#     version = os.environ['CI_JOB_ID']
version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

setuptools.setup(
    author="Rahul Kumar",
    author_email="rahulbits2015@gmail.com",
    name='Jaarvis',
    description='Utility code ',
    version=version,
    long_description=README,
    url='https://github.com/RahulnKumar/Rahul-Utils',
    packages=setuptools.find_packages(),
    python_requires=">=3.6.9",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'

    ],
)
