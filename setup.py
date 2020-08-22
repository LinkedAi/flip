import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

about = {}
with open('flip/__about__.py') as fp:
    exec(fp.read(), about)

setuptools.setup(
      name=about['__title__'],
      version=about['__version__'],
      license=about['__license__'],
      author=about['__author__'],
      author_email=about['__email__'],
      description=about['__description__'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      url=about['__github__'],
      packages=setuptools.find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
      ],
      install_requires=requirements,
      python_requires='>=3.7'
)
