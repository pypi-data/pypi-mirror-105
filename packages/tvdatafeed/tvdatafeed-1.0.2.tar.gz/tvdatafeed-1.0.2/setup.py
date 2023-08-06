from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='tvdatafeed',
    version='1.0.2',
    packages=['tvDatafeed'],
    url='https://www.youtube.com/c/StreamAlpha',
    license='MIT License',
    author='@anojangra',
    author_email='',
    description='TradingView historical data downloader',
    long_description=long_description,
    install_requires=['pandas','selenium','websocket-client','chromedriver-autoinstaller'],
    long_description_content_type="text/markdown",
    keywords=['historical data', 'tradingview', 'stock markets'],
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ]
)
