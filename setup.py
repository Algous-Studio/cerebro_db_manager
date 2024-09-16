import sys
from setuptools import setup, find_packages

f = open('README.md')
readme = f.read().strip()


setup(
    name='cerebro_db_manager',
    version='0.1.0',
    description='Cerebro Production Tracking Python API Wrapper',
    long_description=readme,
    author='Algous',
    author_email='info@algousstudio.ru',
    url='https://github.com/Algous-Studio/cerebro_db_manager',
    packages=find_packages(exclude=('tests',)),
    py_modules=['settings'],
    install_requires=[
        'psycopg2',
        'Pillow>=8.0.0',
    ],
    zip_safe=False,
    python_requires=">=3.7.0",
    classifiers=[
        "Development Status :: 5 - Production/Dev",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)