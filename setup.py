import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid',
    'requests',
]

test_requires = [
    'WebTest==1.4.3',
    'mock==1.0.1',
]

testing_extras = test_requires + [
    'nose==1.2.1',
    'coverage==3.6',
]


setup(
    name='pyramid_sna',
    version='0.3.2',
    description='Pyramid Social Network Authentication',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pyramid",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Lorenzo Gil Sanchez',
    author_email='lorenzo.gil.sanchez@gmail.com',
    url='https://github.com/lorenzogil/pyramid_sna',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires + test_requires,
    extras_require={
        'testing': testing_extras,
    },
    test_suite="pyramid_sna",
)
