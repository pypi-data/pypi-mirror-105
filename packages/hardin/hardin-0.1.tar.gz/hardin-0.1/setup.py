from setuptools import setup, find_packages


setup(name='hardin',
      version='0.1',
      description='A mini Deep Learning Framework',
      author='Tudor-Andrei Dumitrascu',
      author_email='tudorandrei.dumitrascu@gmail.com',
      url='https://gitlab2.informatik.uni-wuerzburg.de/s421904/hardin',
      license='MIT',
      install_requires=[
          'numpy'
      ],
      packages=['hardin'],
      zip_safe=False)
