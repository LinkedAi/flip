from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

setup(name='flip',
      version='0.1.1',
      license='GPL-3.0',
      author='Linked AI Inc',
      author_email='d@linkedai.co',
      description='Generate thousands of new 2D images from a small batch of objects and backgrounds.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/LinkedAi/flip',
      packages=['flip'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
      ],
      install_requires=requirements,
      python_requires='>=3.7')
