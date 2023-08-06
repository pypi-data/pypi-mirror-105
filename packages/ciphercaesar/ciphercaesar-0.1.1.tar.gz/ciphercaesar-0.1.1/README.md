# ciphercaesar
A ciphering lib for python. Uses Caesar encryption to encrypt messages. Can also cipher text from sequences.


## Installation
Installing ciphercaesar via pip

### Windows:
```sh
$ pip install ciphercaesar
```

### MacOS or Linux:
```sh
$ pip3 install ciphercaesar
```


## Usage
This is a really simple project with ease of opperation in mind. Simply import or its specific functions explicitly:

```python
import ciphercaesar
```
or
```python
from ciphercaesar import encrypt, decrypt
```
and that is it (just like most of the other packages). Now you will be able to access its 2 functions: encrypt and decrypt.

### Example with a String
Both of these functions take in 3 params, the *last one being optional*.

An example use could be
```python
from ciphercaesar import encrypt, decrypt

print("Encrypting 'Hello World!':", encrypt("Hello World!", 5))
```

And by executing this piece of code, you would get the following output
```
Encrypting 'Hello World!': Mjqqt btwqi!
```

### Example with an Interable

You could also use both of these functions on *interables* by using the 3rd param

```python
print(decrypt(["Mjqqt", "btwqi!"], 5, multi=True))
```
Now the first param, **text** is a list and the 3rd param is set to True. This set of params would now return a list of strings, instead of a single string.

This I found, was quite useful in decrypting and encrypting a table row by row. And the output of the code is shown below

```
['Hello', 'World!']
```


## Note
Note that this is this project's alpha release and one may encounter some bugs, if any bugs are found, please report them.
As this encryption algorithm is quite simple, it is recommended that it shouldn't be used for anything more than a little fun and to represent better encryption just for a mild presentation
