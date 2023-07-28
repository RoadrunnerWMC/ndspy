import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ndspy',
    version='4.1.0',
    author='RoadrunnerWMC',
    author_email='roadrunnerwmc@gmail.com',
    description='Python library that can help you read, modify and create many types of files used in Nintendo DS games.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RoadrunnerWMC/ndspy',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ndspy_codeCompression = ndspy.codeCompression:main',
            'ndspy_lz10 = ndspy.lz10:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
)