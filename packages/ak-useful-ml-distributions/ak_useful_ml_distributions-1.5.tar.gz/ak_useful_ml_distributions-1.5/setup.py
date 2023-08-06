from setuptools import setup

with open("README.md") as fh:
    long_description = fh.read()

setup(name='ak_useful_ml_distributions',
      author='Andrew Kalil',
      author_email='andrew_kalil@hotmail.com',
      version='1.5',
      description='Distribution Classes for Machine Learning',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['ak_useful_ml_distributions'],
      zip_safe=False)
