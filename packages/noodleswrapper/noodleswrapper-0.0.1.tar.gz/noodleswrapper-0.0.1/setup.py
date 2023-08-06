import setuptools
from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name = 'noodleswrapper',
    version = '0.0.1',
    author = 'Kabir Ghai',
    author_email = 'KabirGhai18@gmail.com',
    description = 'A wrapper used for meme generating using Discord API',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
     install_requires=[
        'Discord.py>=0.7',
    ],
    python_requires='>=3.7',
    include_package_data = True,
    url = 'https://www.frenchnoodles.xyz/',
    classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
        ],
    packages= setuptools.find_packages(),
)