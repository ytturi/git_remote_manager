from setuptools import setup, find_packages


setup(
    name='git_remote_manager',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/ytturi/git_remote_manager',
    license='GNU',
    author='Ytturi',
    author_email='ytturi@protonmail.com',
    description='Manage remote repositories',
    install_requires=[
        'fabric',
        'osconf',
        'click',
        'tqdm'
    ]
)