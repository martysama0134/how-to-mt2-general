#! /usr/bin/env python
"""Sequence Generator
	This python script automatically generates a new sequence table
"""
__author__		= "martysama0134"
__copyright__	= "Copyright (c) 2018 martysama0134"
__date__		= "2018-02-09"
__license__		= "New BSD License"
__url__			= "https://github.com/martysama0134/how-to-mt2-general/tree/master/sequence-generator"
__version__		= "1.0.0"

from random import randrange
def genKey():
	return randrange(0x0,0xfe)

def genLine():
	return " ".join(["0x%x," % genKey() for i in range(16)])

if __name__ == "__main__":
	with open("seq_gen.txt", "w") as seqFile:
		seqFile_write = seqFile.write
		seqFile_write("{\n")
		for i in range(2048):
			seqFile_write("\t%s\n" % genLine())
		seqFile_write("}\n")
#
