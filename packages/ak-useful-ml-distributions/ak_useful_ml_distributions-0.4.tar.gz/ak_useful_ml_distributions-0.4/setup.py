from setuptools import setup

with open(file='README.md', mode='r') as readme_handle:
    long_description = readme_handle.read()

setup(name='ak_useful_ml_distributions',
      author='Andrew Kalil',
      author_email='andrew_kalil@hotmail.com',
      version='0.4',
      description='Distribution Classes for Machine Learning',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['ak_useful_ml_distributions'],
      zip_safe=False)
