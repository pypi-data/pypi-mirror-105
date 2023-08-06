from setuptools import setup, find_packages


with open('README.md', encoding='utf8') as readme_file:
    readme = readme_file.read()

setup(
    author='Fernando Perez-Garcia',
    author_email='fernando.perezgarcia.17@ucl.ac.uk',
    python_requires='>=3.6',
    description='A very serious package about Dr. Kerstin Kläser.',
    entry_points={
        'console_scripts': [
            'mr2ct=kerstin.mr2ct:main',
        ],
    },
    install_requires=['Pillow', 'gdown'],
    license='MIT license',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='kerstin',
    name='kerstin',
    packages=find_packages(include=['kerstin', 'kerstin.*']),
    setup_requires=[],
    test_suite='tests',
    tests_require=[],
    url='https://github.com/fepegar/kerstin',
    version='0.1.1',
    zip_safe=False,
)
