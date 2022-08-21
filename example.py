"""
Script which will act as a basis
"""

from lib import crypto as crypto
from lib import nfc_lib as nfc
import time

# initiate
card = nfc.Card()
rnd = crypto.get_random_block()
print(rnd)
card.write_block(5, 2, rnd)

for element in card.hexdict:
    for block in element:
        print(len(block))
del card

for i in range(1, 11):
    print('.')
    time.sleep(1)

card = nfc.Card()
if crypto.check_card(card):
    print('The password is correct')
    new_password = crypto.get_random_block()
    status = card.write_block()
    if status:
        print('ok')
    else:
        print('not ok')

