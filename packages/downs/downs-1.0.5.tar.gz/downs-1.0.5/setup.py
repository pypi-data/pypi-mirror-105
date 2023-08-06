import os
import setuptools

def rd(pth):
	return open(os.path.join(os.path.abspath(os.path.dirname(__file__)),pth)).read()

setuptools.setup(
    name='downs',
    version='1.0.5',
    description='Multithreaded Download Tool.',
    long_description=rd('README.rst'),
    py_modules=['downs'],
	packages=setuptools.find_packages(),

    author='userElaina',
    author_email='userElaina@google.com',
    url='https://github.com/userElaina',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        "Source": "https://github.com/userelaina/downs",
    },
    keywords='download thread',
    python_requires='>=3.6',
)