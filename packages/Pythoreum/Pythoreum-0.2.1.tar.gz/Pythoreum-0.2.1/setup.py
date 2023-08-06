import setuptools

with open("README.md", 'r') as file:
	long_description = file.read()
setuptools.setup(
     name='Pythoreum',
     version='0.2.1',
     author="Snehashish Laskar",
     author_email="snehashish.laskar@gmail.com",
     description="A simpple Pythogoreus theorum calculator!",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
