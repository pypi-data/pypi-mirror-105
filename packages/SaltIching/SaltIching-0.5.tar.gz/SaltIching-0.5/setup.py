from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='SaltIching',
      version='0.5',
      description='A python package for Iching',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/royalsaltmerchant/salt-iching',
      author='Royal Salt Merchant',
      author_email='jumpingafterrain@gmail.com',
      license='MIT',
      packages=['iching'],
      zip_safe=False,
      include_package_data=True,
      entry_points = {
        'console_scripts': [
              'random=iching.command_line:random',
              ],
      }),
      
      