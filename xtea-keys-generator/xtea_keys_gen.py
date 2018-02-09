#! /usr/bin/env python
"""XteaKeys KeyGen
	This python script automatically generates random xtea keys
"""
__author__		= "martysama0134"
__copyright__	= "Copyright (c) 2015 martysama0134"
__date__		= "2015-11-16"
__license__		= "New BSD License"
__url__			= "https://github.com/martysama0134/how-to-mt2-general/tree/master/xtea-keys-generator"
__version__		= "1.1.0"

def swapHex(basestring): # just for eternexus
	asal = [basestring[i:i+2] for i in range(0, len(basestring), 2)]
	asal.reverse()
	return ''.join(asal)

def pad32Hex(keyDataHex, keySplitHex=8):
	return ", ".join([swapHex(keyDataHex[i:i+keySplitHex]) for i in range(0, len(keyDataHex), keySplitHex)])

from random import randrange
def genKey():
	return randrange(0x1fFFffFF,0x6fFFffFF)

if __name__ == "__main__":
	import struct
	# index
	keyIndexInt = (genKey(), genKey(), genKey(), genKey())
	keyIndexHex = struct.pack("IIII", *keyIndexInt).encode('hex')
	# pack
	keyPackInt = (genKey(), genKey(), genKey(), genKey())
	keyPackHex = struct.pack("IIII", *keyPackInt).encode('hex')

	with open("xtea_keys_gen.txt", "w") as keyFile:
		keyFile.write("\n### INDEX KEY\n")
		keyFile.write("Hex:\n")
		keyFile.write("%s [%s]\n" % (pad32Hex(keyIndexHex), keyIndexHex))
		keyFile.write("Int:\n")
		keyFile.write("static DWORD s_adwEterPackKey[] =\n{\n\t%u,\n\t%u,\n\t%u,\n\t%u\n};\n" % keyIndexInt)

		keyFile.write("\n### PACK KEY\n")
		keyFile.write("Hex:\n")
		keyFile.write("%s [%s]\n" % (pad32Hex(keyPackHex), keyPackHex))
		keyFile.write("Int:\n")
		keyFile.write("static DWORD s_adwEterPackSecurityKey[] =\n{\n\t%u,\n\t%u,\n\t%u,\n\t%u\n};\n" % keyPackInt)
#
