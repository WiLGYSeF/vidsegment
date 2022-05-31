import setuptools

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='vidsegment',
    version='0.0.1',
    author='wilgysef',
    author_email='wilgysef@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    project_urls={
        'Bug Tracker': '',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['vidsegment=vidsegment.__main__:main_args']
    }
)
