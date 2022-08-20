"""
Module to perform nfc mifareclassic operations
"""
import os  # TODO: replace os functions with modern way
import binascii

class Card:
    """
    Class defining a Card object
    """

    def __init__(self, file=None):
        self.hexdump, self.hexmap, self.hexdict = self.read(file)

    def read(self, file=None):
        if isinstance(file, str):
            with open(file, 'rb') as pointer:
                hexdump = pointer.read().hex()
        else:
            os.system('nfc-mfclassic r a u /tmp/card.read')
            with open('/tmp/card.read', 'rb') as reading:
                hexdump = reading.read().hex()
            os.system('rm /tmp/card.read')
        hexmap = map(''.join, zip(*[iter(hexdump)]*32))
        hexdict = {}
        sector = 1
        block = 1
        for hexstr in hexmap:
            if hexdict.get(sector) is None:
                hexdict[sector] = []
            hexdict[sector].append(hexstr)
            if block == 4:
                block = 1
                sector += 1
            else:
                block += 1
        return hexdump, hexmap, hexdict

    def write(self, file=None):
        if not isinstance(file, str):
            file = '/tmp/card.write'
            with open(file, 'wb') as writing:
                for sector in self.hexdict:
                    for block in self.hexdict[sector]:
                        writing.write(binascii.unhexlify(''.join(block.split())))
        os.system('nfc-mfclassic w a u ' + file)


card = Card()
print(card.hexdict)
card.write()
print(card.read())
