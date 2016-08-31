from setuptools import setup, find_packages

import os


setup(
    name="ptpchat-server",
    version=os.environ.get('VERSION', '0'),

    description="Ptpchat Server",
    author="Matthew Uzzell"

    install_requires=[
    ],
    scripts=[],
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['*.tac', '*.xml', '*.cfg']},
    packages=find_packages(),
    entry_points={
        'console_scripts': [
        ],
    },

    keywords=[
        # Use keywords if you'll be adding your package to the
    ],

    classifiers=[
        'Development Status :: 5 - production',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
