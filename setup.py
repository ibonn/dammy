from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='dammy',
    version='0.1.3',
    description='Generate fake data for any purpose',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPL-3.0',
    packages=['dammy'],
    package_dir={'dammy': 'dammy'},
    package_data={'dammy': ['data/*.json']},
    author='Ibon',
    author_email='ibonescartin@gmail.com',
    keywords=['dummy-data', 'fake', 'mock', 'database', 'sql', 'dummy', 'test', 'data', 'population'],
    url='https://github.com/ibonn/dammy',
    download_url='https://pypi.org/project/dammy/',
    project_urls={
        "Documentation": "https://readthedocs.org/projects/dammy/",
        "Source Code": "https://github.com/ibonn/dammy"
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Mocking',
        'Topic :: Utilities'
    ],
    include_package_data=True
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
