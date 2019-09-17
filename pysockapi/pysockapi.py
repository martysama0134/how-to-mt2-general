#!/usr/local/bin/python2.7
#!/usr/bin/env python

# Copyright (c) 2013, martysama0134
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of martysama0134 nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import socket	# socket.socket, socket.connect, socket.send, socket.recv, socket.close
import time		# time.sleep
"""PySockAPI Module
It's a simple module that uses socket connection to send commands to a metin2 server (via adminpage)

Usage:
	>>> from pysockapi import SOCKAPI
	>>> m_sock = SOCKAPI(host="localhost", pwd="SHOWMETHEMONEY", type="PORT")
	>>> m_sock.Send(cmd=("EVENT xmas_tree 4",), ret=False)

	Or:
	>>> import pysockapi
	>>> m_sock = SOCKAPI(host="localhost", pwd="SHOWMETHEMONEY", type="P2P_PORT")
	>>> m_sock.Send(cmd=SOCKAPI2_SHUTDOWN, ret=False)

Info: (adminpage via PORT ports)
	### NO IP/PASSWORD REQUIRED
	#is_server_up (it returns YES or NO if the server is shutdowned)
		IS_SERVER_UP
	#is_passpod_up (it returns YES or NO if passpod is used)
		IS_PASSPOD_UP
	#user_count (it returns the count of the players on) (nb: it requires validation if adminpageip is not empty)
		USER_COUNT
	#check_p2p_connections (it returns the count of the current desc connections)
		CHECK_P2P_CONNECTIONS
	#packet_info (it generates a profile_log.txt file and returns OK)
		PACKET_INFO
	#profile (it generates a profile.txt file and returns OK)
		PROFILE
	#delete_awardid %11d (it deletes an item_award id)
		DELETE_AWARDID <award_id>
			Example:	DELETE_AWARDID 4810

	### YES IP/PASSWORD REQUIRED
	#notice %43s (it sends a notice to all the games)
		NOTICE <message>
			Example:	NOTICE This is a test
	#close_passpod (it closes passpod)
		CLOSE_PASSPOD
	#open_passpod (it opens passpod)
		OPEN_PASSPOD
	#shutdown (it performs a shutdown of all the game in 10 secs)
		SHUTDOWN
	#shutdown_only (it performs a shutdown of the relative game in 10 secs)
		SHUTDOWN_ONLY
	#dc %30s (it /dc crashes all the players inside the relative <account_name>) [LOGIN_MAX_LEN=30]
		DC <account_name>
			Example:	DC youraccount
	#reload_crc (it reloads the CRC file and returns OK)
		RELOAD_CRC
	#check_client_version (it performs a clientversion check to all the online players and returns OK)
		CHECK_CLIENT_VERSION
	#reload &%c (it performs a classic /reload)
		RELOAD <&type>
			type	default:general, a:admin, f:fishing, p:player, q:quest, s:string, u:usercount
			Example:	RELOAD p
	#event %s %d (it performs a classic /event <name> <value> and returns CHANGE or FAIL)
		EVENT <eventflag> <value>
			Example:	EVENT xmas_tree 4
	#block_chat %s %d (it performs a classic /block_chat <nick> <duration> and returns '' or FAIL)
		BLOCK_CHAT <nick> <duration>
			Example:	BLOCK_CHAT [GA]LoLLo 1h
	#priv_empire %d %d %d %d (it performs a classic /priv_empire <empire> <type> <value> <duration> and returns SUCCESS or FAIL)
		PRIV_EMPIRE <empire> <type> <value> <duration>
			empire	0-3 0==all, 1==red, 2==yellow, 3==blue)
			type	1:item_drop, 2:gold_drop, 3:gold10_drop, 4:exp
			value	percent
			dur.	hour
			Example:	PRIV_EMPIRE 0 4 200 72h
	#block_exception %s %d (it inserts/deletes <login_name> into/from account.block_exception based on the <rule_id>)
		BLOCK_EXCEPTION <login_name> <rule_id>
			rule_id	1:add, 2: del

"""
__author__		= "martysama0134"
__copyright__	= "Copyright (c) 2013 martysama0134"
__date__		= "2012-10-08"
__license__		= "New BSD License"
__version__		= "3.0"

class PySockAPIError(Exception): pass

# default-data
dftHOSTPORT =	("127.0.0.1", 13000)
dftADMINPWD =	"SHOWMETHEMONEY"
dftCOMMAND =	("NOTICE /!\\ ",)
# file
dftCONFILE =	"pysockapi_con.txt"

class SOCKAPI:
	def __init__(self, host = dftHOSTPORT, pwd = dftADMINPWD, type = "PORT"):
		#con-data
		self.HOSTPORT = host
		self.ADMINPWD = pwd
		self.APITYPE = type

	def Send(self, cmd = dftCOMMAND, ret = True):
		try:
			#connect
			con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
			con.connect(self.HOSTPORT)
			if self.APITYPE=="PORT":
				#send
				CMDSEND = "@%s\n@%s\n" % (self.ADMINPWD, "\n@".join(cmd))
				# CMDSEND = "@".join(cmd)
				print CMDSEND
				con.send(CMDSEND)
				#receive
				# print repr(con.recv(1024))#escape
				print con.recv(1024)[15:]
				time.sleep(0.1)#required
				#close
				con.close()
				print "<Pysock> Socket inviato con successo"
			elif self.APITYPE=="P2P_PORT":
				#send
				CMDSEND = cmd
				print CMDSEND
				con.send(CMDSEND)
				#receive
				print repr(con.recv(1024))#escape
				# print con.recv(1024)[15:]
				time.sleep(0.1)#required
				#close
				con.close()
				print "<Pysock> Socket inviato con successo"
		except socket.error:
			raise PySockAPIError, "Socket failed, con-data maybe wrong (%s, %s, %s)"%(self.HOSTPORT[0], self.HOSTPORT[1], self.ADMINPWD)

if __name__ == "__main__":
	def Usage():
		print '''Usage:
	#(-c or --command) send command
		./pysock.py -c "<command>"
	#(-g or --get) get con-data from con-file (pysock_con.txt) and send a command
		./pysock.py -g -c "<command>"
	#(-f or --file) send command from file (1.)
		./pysock.py -f "<file>"
	#(-h or --help) help
		./pysock.py -h
	#(-s or --set) set con-data to con-file (pysock_con.txt) and send a command (2.)
		./pysock.py -s "<host>:<port>:<pwd>"
	#(-r or --raw) raw mode (3.)
		./pysock.py -r "<host:port> <adminpwd> <command>"

Examples:
	1. # ./pysock.py -f "mysock_cmd.txt"
	2. # ./pysock.py -s "123.456.78.90:13000:SHOWMETHEMONEY" -c "NOTICE 1;NOTICE 2;NOTICE 3"
	3. # ./pysock.py -r "173.194.35.6:13003 SHOWMETHEMONEY NOTICE 1;NOTICE 2;USER_COUNT"
'''

	import getopt	# getopt.getopt
	import os		# os.path.exists
	import sys		# sys.exit
	# args
	PYSOCK_SHRTARG = 'c:df:ghr:s:'
	PYSOCK_LONGARG = ('command=', 'default', 'file=', 'get', 'help', 'raw=', 'set=')

	sys_exit = sys.exit
	# analyze argv
	try:
		optlist, args = getopt.getopt(sys.argv[1:], PYSOCK_SHRTARG, PYSOCK_LONGARG)
	except getopt.GetoptError, err:
		sys_exit(err)

	OP_HOSTPORT = None
	OP_ADMINPWD = None
	OP_COMMAND = None

	# analyze optlist
	for o, a in optlist:
		# help
		if o in ('-h', '--help'):
			sys_exit(Usage())
		# send command from arg
		elif o in ('-c', '--command'):
			# analyze string-arg
			try:
				OP_COMMAND = a.split(";")
			except IndentationError, err:
				raise PySockAPIError, "Except %s"%err
		# load default con-data
		elif o in ('-d', '--default'):
			OP_HOSTPORT = dftHOSTPORT
			OP_ADMINPWD = dftADMINPWD
			OP_COMMAND = dftCOMMAND
		# load command from file
		elif o in ('-f', '--file'):
			# analyze string-arg
			if os.path.exists(a):
				# read file
				tmp = open(a, "r"); OP_COMMAND = tmp.read().split("\n"); tmp.close(); del tmp
			else:
				raise PySockAPIError, "File %s not found"%a
		# load con-data from file
		elif o in ('-g', '--get'):
			# analyze string-arg
			if os.path.exists(dftCONFILE):
				# read file
				tmp = open(dftCONFILE, "r"); conread = tmp.read(); tmp.close(); del tmp
				# set con-data
				try:
					conan = conread.split(":", 2)
					#set con-data
					OP_HOSTPORT = (conan[0], int(conan[1]))
					OP_ADMINPWD = conan[2].replace("\n", "").replace("\r", "")
				except IndentationError, err:
					raise PySockAPIError, "Except %s"%err
			else:
				raise PySockAPIError, "File %s not found"%dftCONFILE
		# create a manual string
		elif o in ('-r', '--raw'):
			# analyze string-arg
			try:
				a = a.split(" ", 2)
			except IndentationError, err:
				raise PySockAPIError, "Except %s"%err
			# set data
			tmpHOSTPORT = a[0].split(":", 1)
			OP_HOSTPORT = (tmpHOSTPORT[0], int(tmpHOSTPORT[1]))
			OP_ADMINPWD = a[1]
			OP_COMMAND = a[2].split(";")
		# save your data connection
		elif o in ('-s', '--set'):
			# analyze string-arg
			try:
				conan = a.split(":", 2)
			except IndentationError, err:
				raise PySockAPIError, "Except %s"%err
			# save hostport
			f1 = open(dftCONFILE, "w")
			f1.write(a)
			del f1
			# set con-data
			OP_HOSTPORT = (conan[0], int(conan[1]))
			OP_ADMINPWD = conan[2]
		# invalid args
		else:
			raise PySockAPIError, "Unhandled %s option"%o

	if (not OP_HOSTPORT) or (not OP_ADMINPWD) or (not OP_COMMAND):
		sys_exit(Usage())

	sock = SOCKAPI(OP_HOSTPORT, OP_ADMINPWD)
	sock.Send(OP_COMMAND)

	time.sleep(0.1)
	#
#


















