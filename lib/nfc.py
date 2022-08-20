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

    def read_all(self, file=None):
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

    def write_all(self, file=None, dictionary=None, dump=None):
        out_file = '/tmp/card.write'
        if isinstance(file, str):
            out_file = file
        elif isinstance(dictionary, dict):
            with open(out_file, 'wb') as writing:
                for sector in dictionary:
                    for block in dictionary[sector]:
                        writing.write(binascii.unhexlify(''.join(block.split())))
        elif isinstance(dump, str):
            with open(out_file, 'wb') as writing:
                writing.write(binascii.unhexlify(''.join(dump.split())))
        else:
            print("Error. Add Logging and exceptions...")
            return False
        os.system('nfc-mfclassic w a u ' + out_file)
        if file is None:
            os.system('rm /tmp/card.write')
        return True


    def write_block(self,sector, block, msg):
        if not isinstance(sector, int) or not isinstance(block, int) or not isinstance(msg, str):
            print("Sector has to be a `int`, Block has to be `int`, Message has to be a `str`")
            return False
        hex_string = binascii.hexlify(msg)
        if len(hex_string) is not 32:  # aggiungere possibilità di padding per valori inferiori
            print("32 hex values are needed")
            return False
        self.hexdict[]


card = Card()
print(card.hexdict[7][0])
card.hexdict[7][0] = '00000000007700000000000000000000'
card.write()
card2 = Card()
print(card2.hexdict[7][0])
