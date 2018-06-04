from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='flyonthewall',
    version='0.1a6',
    author='Hunter M. Allen',
    author_email='allenhm@gmail.com',
    license='MIT',
    #packages=find_packages(),
    packages=['flyonthewall'],
    #scripts=['bin/heartbeatmonitor.py'],
    install_requires=['boto3>=1.7.25',
                      'beautifulsoup4>=4.6.0',
                      'requests>=2.13.0',
                      'slackclient>=1.2.1',
                      'wget>=3.2'],
    description='Forum scraper that returns relevant posts and attachments based on keywords provided as argument or in file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hmallen/flyonthewall',
    keywords=['forum', 'scrape'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
