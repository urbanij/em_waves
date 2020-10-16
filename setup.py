from setuptools import setup

setup(
    name='em_waves',
    version='0.0.1',
    author='Francesco Urbani',
    author_email='francescourbanidue@gmail.com',
    packages=['em_waves'],
    scripts=[],
    url='https://github.com/urbanij/em_waves',
    license='LICENSE.txt',
    description="Simulation of electromagnetic wave hitting an interface with a different medium.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy>=1.19.2",
        "matplotlib>=3.3.2",
   ],
   keywords="electromagnetic waves, ",
   python_requires=">=3.7",
)
