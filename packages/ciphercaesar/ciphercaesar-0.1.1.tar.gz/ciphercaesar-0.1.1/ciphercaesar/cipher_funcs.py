# This program consists of 2 functions which cipher and decipher text.
# And it implements the Cesar encryption technique, so, relatively easy to
# decipher encoded messages

from string import ascii_letters as letters


# ****
# author: Ishan Kashyap
# created: 3/4/2021
# ****


def encrypt(text, key, multi=False):
    """
    This function implements Cesar encryption to encrypt text
    This function encrypts text
    :param key:
    :type text: str
    """
    # if the input is a sequence, then take each element of text and
    # return all of those elements, encrypted, as a list (another sequence)
    if multi:
        return [encrypt(i, key) for i in text]
    # make variable to store cyphered text
    encrypted_text = ""
    # loop through each element in text
    for i in text:
        # if its a letter shift its value
        try:
            # get index of i, shift it, get its mod 26, then find
            # corresponding value and concatenate it to encrypted text
            encrypted_text += letters[(letters.index(i) + key) % len(letters)]
        # other vise don't cipher it
        except ValueError:
            encrypted_text += i
    # finally, return ciphered text
    return encrypted_text


def decrypt(text, key: int, multi=False):
    """
    This function is the inverse of the encrypt function. It decrypts
    text using the key that was used to encrypt it.
    :param text: Text to decrypt
    :param key: key that was used to encrypt text
    :return: decrypted text
    """
    if multi:
        return [decrypt(i, key) for i in text]
    decrypted_text = ""
    for i in text:
        try:
            decrypted_text += letters[letters.index(i) - key % len(letters)]
        except ValueError:
            decrypted_text += i
    return decrypted_text
 