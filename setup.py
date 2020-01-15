from setuptools import setup, find_packages

from flask_memory_profiler import __version__ as version

setup(
    name='Flask-Memory-Profiler',
    version=version,
    packages=find_packages(),
    long_description=open('README.md').read(),
    url='http://github.com/waxisien/flask-memory-profiler',
    license="MIT",
    install_requires=[
        'Flask>=1.0',
        'psutil',
    ],
)
