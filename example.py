"""
Script which will act as a basis
"""

import lib.crypto as crypto
import lib.nfc as nfc
import time

# initiate
card = nfc.Card()
rnd = crypto.get_random_block()
card.write_block(5, 2, rnd)

del card

for i in range(1, 11):
    print('.')
    time.sleep(1)



crypto.get_random_block()
card = nfc.Card()
if crypto.check_card(card):
    print('The password is correct')
    new_password = crypto.get_random_block()
    status = card.write_block()
    if status:
        print('ok')
    else:
        print('not ok')

