from setuptools import setup, find_packages

setup(
    name='sitf',
    version='1.1.0',
    description="Sort Images by day's wise into to the folders",
    author='Shatak Gurukar',
    author_email='shatakgurukar@gmail.com',
    packages=find_packages(include=['sitfproject', 'sitfproject.*']),    
    entry_points={
        'console_scripts': ['sitf=sitfproject.sitf:main']
    },
    install_requires=[
        'image'        
    ],
    python_requires='>=3.6'
)