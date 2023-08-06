from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='quantclean',
    version='0.0.2',
    description='Quantclean is a program that reformats every financial dataset to US Equity TradeBar',
    py_modules=['quantclean'],
    package_dir={'':'src'},
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url='https://github.com/ssantoshp/quantclean',
    author = "Santosh Passoubady",
    author_email = "santoshpassoubady@gmail.com",
    license='MIT',
    install_requires=[
          'pandas_datareader',
          'pandas'
      ],
)
