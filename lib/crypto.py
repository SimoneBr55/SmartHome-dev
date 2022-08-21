"""
Module to handle crypto
"""

import os
import binascii
from .nfc_lib import Card

# random choice, just to test it
pass_sector = 5
pass_block = 2


def get_random_block():
    rnd = binascii.b2a_hex(os.urandom(16))
    with open('/root/next_pass', 'wb') as crypto_file:
        cr = crypto_file.write(rnd)
    return rnd


def check_card(card: Card):
    current = card.hexdict[pass_sector][pass_block]
    with open('/root/next_pass', 'rb') as crypto_file:
        password = crypto_file.read()
    if current == password:
        print('Passed')
        return True
    else:
        print('Wrong')
        return False
