from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Bitkub-Api',
    version='0.0.2',
    description='A Non-official very basic Bitkub API',
    url='',
    author='Chayanon Promchaiya',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='bitkub_api',
    packages=find_packages(),
    install_requires=['requests']
)