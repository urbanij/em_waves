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
    description='TODO',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy==1.18.1",
        "matplotlib==3.1.3",
        "scipy==1.4.1",
   ],
   keywords="electromagnetic waves, ",
   python_requires=">=3.7",
)
