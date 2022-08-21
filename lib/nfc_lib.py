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

    def read_all(self, file=None):  # maybe static
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

    def write_all(self, file=None, dictionary=None, dump=None):  # maybe static
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
            print("This means that i have to write the self.dict")
            with open(out_file, 'wb') as writing:
                for sector in self.hexdict:
                    for block in self.hexdict[sector]:
                        writing.write(binascii.unhexlify(''.join(block.split())))
        os.system('nfc-mfclassic w a u ' + out_file)
        if file is None:
            os.system('rm ' + out_file)
        return True

    def write_block(self, sector, block, msg):
        if not isinstance(sector, int) or not isinstance(block, int) or not isinstance(msg, str):
            print("Sector has to be a `int`, Block has to be `int`, Message has to be a `str`")
            return False
        msg = msg.encode('ascii')
        hex_string = binascii.hexlify(msg)
        if len(hex_string) != 32:  # add padding possibility for hexstrings with lt 32 hexchars
            print("32 hex values are needed")
            return False
        self.hexdict[sector][block] = hex_string
        self.write_all()
        return True
