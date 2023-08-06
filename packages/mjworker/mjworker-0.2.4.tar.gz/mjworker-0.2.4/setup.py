from setuptools import setup, find_packages
from codecs import open
from os import path
 
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mjworker',
    version='0.2.4',
    author='huyan',
    description='agent application for mj-monitor',
    author_email='lixiuhu_lee@163.com',
    url='https://gitlab.dataenlighten.com/devops/monitor',
    py_modules=['mjworker'],
    packages=find_packages(),
    install_requires=[
        'Click',
        'psutil',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        mjworker=mjworker.worker:cli
    ''',
)