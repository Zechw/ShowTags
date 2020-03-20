from setuptools import setup

setup(
    name='ShowTags',
    install_requires=['gitpython'],
    entry_points={
        'console_scripts': [
            'showtags=main:main'
        ]
    }
)
