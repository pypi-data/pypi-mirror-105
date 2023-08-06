import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="ZtModTcp",
  version="1.1.0",
  author="ZbChenEF",
  author_email="531047408@qq.com",
  description="A VSR virtual library controller package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
  install_requires=[
      'modbus-tk>=1.1.2',
      'setuptools>=56.0.0'
      ]
)