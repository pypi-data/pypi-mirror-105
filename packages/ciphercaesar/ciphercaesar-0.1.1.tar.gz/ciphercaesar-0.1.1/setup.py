import setuptools


with open("README.md") as file:
    long_description2 = file.read()

setuptools.setup(
  name = 'ciphercaesar',         # How you named your package folder (MyLib)
  packages = ['ciphercaesar'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Package to Cipher text',   # Give a short description about your library
  long_description = long_description2,
  long_description_content_type = "text/markdown",
  author = 'Ishan Kashyap',                   # Type in your name
  author_email = 'ishan.kashyap@sahyadrischool.org',      # Type in your E-Mail
  url = 'https://github.com/ishan090/ciphercaesar',   # Provide either the link to your github or to your website
  keywords = ['cipher', 'monoalphabetic', "caesar"],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3'
  ]
)
