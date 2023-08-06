from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
 name='complimenter',
 version='1.0',
 description='Create random compliments',
 long_description = long_description,
 long_description_content_type = "text/markdown",
 keywords = ['generator', 'compliments'],
 author='Mohd Sabahat',
 author_email='mohdsabahat123@gmail.com',
 py_modules=['compliment'],
 python_requires=">=3.6",
    classifiers = [
        'Programming Language :: Python :: 3',
    ],
)
