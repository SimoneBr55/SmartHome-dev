"""
Script which will act as a basis
"""

import lib.crypto as crypto
import lib.nfc as nfc


card = nfc.Card()
if crypto.check_card(card):
    print('The password is correct')
    new_password = crypto.get_random_block()
    status = card.write_block()
    if status:
        print('ok')
    else:
        print('not ok')

