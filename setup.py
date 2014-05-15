from setuptools import find_packages, setup


install_requires = [
    "Trac >= 0.11"
    ]

setup(
    name='TracInventarisPlugin', 
    version='1.0',
    author = 'Koen Vandaele',
    author_email = 'koen.vandaele@rwo.vlaanderen.be',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = {
        'trac.plugins': [
            'trac-inventaris = inventaris',
        ],
    },
    install_requires=install_requires,
)