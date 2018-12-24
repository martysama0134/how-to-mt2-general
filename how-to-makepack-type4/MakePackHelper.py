#! /usr/bin/env python

# Copyright (c) 2013, martysama0134
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of martysama0134 nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__		= "martysama0134 <martysama0134@gmail.com>"
__copyright__	= "Copyright (c) 2014 martysama0134"
__date__		= "2017-05-13"
__license__		= "New BSD License"
__version__		= "4.8.1.0"

import os

drivePaths = (
	"ymir work",
)

listFormat = """FolderName "Pack"
PackName "%s"

List ExcludedPathList
{
}

List ExcludedFileNameList
{
}

List CSHybridEncryptExeNameList
{
	"%s"
}

List FileList
{
	"%s"
}
"""

def MPH_List(packName):
	print "Processing... %s" % packName
	packDir = os.path.join(packName, "")
	packLen = len(packDir)

	packList = []
	extList = set()
	for root, dirs, files in os.walk(packName, topdown=False):
		for name in files:
			tmpFile = os.path.join(root, name)
			# remove the folder directory from the path
			if tmpFile.startswith(packDir):
				tmpFile = tmpFile[packLen:]
			# add d: when needed
			for dPath in drivePaths:
				if tmpFile.startswith(dPath):
					tmpFile = os.path.join("d:"+os.path.sep, tmpFile)
			# get the extension
			tmpExt = os.path.splitext(tmpFile)[-1]
			# remove the dot
			if tmpExt.startswith("."):
				tmpExt = tmpExt[1:]
			# add extension in list
			if tmpExt:
				extList.add(tmpExt)
			# add file in list
			if tmpFile:
				packList.append(tmpFile.replace("\\", "/"))
	# show the pack list
	# for i in packList: print i
	# show the ext list
	# for i in extList: print i
	outFile = "%s.txt" % packName
	with open(outFile, "w") as f:
		f.write(listFormat % (packName, '"\n\t"'.join(extList), '"\n\t"'.join(packList)))

if __name__ == "__main__":
	def Usage():
		print '''Usage: MakePackHelper.py --[extract|list|pack] [pack_name]'''
	import getopt
	import sys
	try:
		optlist, args = getopt.getopt(sys.argv[1:], "e:l:p:", ('extract=','list=','pack='))
		if not optlist: # skip no args
			sys.exit(Usage())
		# process args
		for o, a in optlist:
			if o in ('-e', '--extract'):
				MPH_Extract(a)
			elif o in ('-l', '--list'):
				MPH_List(a)
			elif o in ('-p', '--pack'):
				MPH_Pack(a)
			else:
				sys.exit(Usage())
	except getopt.GetoptError, err:
		sys.exit(err)
#
