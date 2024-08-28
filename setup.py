from setuptools import setup

setup(
    name='setup_security_tools',
    version='0.1',
    py_modules=['setup_security_tools'],
    entry_points={
        'console_scripts': [
            'setup-security-tools = setup_security_tools:main',
        ],
    },
    install_requires=[],
)
