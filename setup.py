import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    # indirect dependencies
    'Beaker==1.6.4',            # required by pyramid_beaker
    'Chameleon==2.11',          # required by pyramid
    'Mako==0.7.3',              # required by pyramid
    'PasteDeploy==1.5.0',       # required by pyramid
    'repoze.lru==0.6',          # required by pyramid
    'translationstring==1.1',   # required by pyramid
    'venusian==1.0a8',          # required by pyramid
    'WebOb==1.2.3',             # required by pyramid
    'zope.interface==4.0.5',    # required by pyramid

    # direct dependencies
    'pyramid==1.4',
    'pyramid_beaker==0.7',
    'requests==1.2.0',
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
    version='0.1',
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
