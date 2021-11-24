from setuptools import setup

setup(
    name='Vaccinchat Reviewer',
    version='1.0',
    long_description=__doc__,
    packages=['reviewer'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Click',
        'playsound',
        'pygobject',
        'python-dotenv',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'review = reviewer.cli:review',
        ],
    },
)

