from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='dammy',
    version='0.1.2',
    description='Simplify database population with dummy data',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPL-3.0',
    packages=['dammy'],
    package_dir={'dammy': 'dammy'},
    package_data={'dammy': ['data/*.json']},
    author='Ibon',
    author_email='ibonescartin@protonmail.com',
    keywords=['dummy-data', 'database', 'sql', 'dummy', 'data', 'population'],
    url='https://github.com/ibonn/dammy',
    download_url='https://pypi.org/project/dammy/',
    project_urls={
        "Documentation": "https://readthedocs.org/projects/dammy/",
        "Source Code": "https://github.com/ibonn/dammy"
    },
    include_package_data=True
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
