from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ColorPrintX',
    version='0.0.1',
    description='Aviv\'s way to print with colors ez',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.TXT').read(),
    url='',
    author='aviv05423',
    author_email='avivb60@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='color, print, colorful, printer, prints, bold, underline',
    packages=find_packages(),
    install_requires=['']
)
