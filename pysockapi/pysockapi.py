#!/usr/local/bin/python2.7
import getopt	#getopt.getopt
import os		#os.path.exists
import socket	#socket.socket, socket.connect, socket.send, socket.recv, socket.close
import sys		#sys.exit
import time		#time.sleep

class PySockModule:
	def __init__(self):
		#con-data
		self.HOSTPORT=None
		self.ADMINPWD=None
		self.COMMAND=None
		#default-data
		self.dftHOSTPORT=("123.456.78.90",13000)
		self.dftADMINPWD="SHOWMETHEMONEY"
		self.dftCOMMAND=("NOTICE /!\\ ",)
		#cleanlist
		self.NOWAY=(0,"0","",None)
		#file
		self.PYSOCK_HLPFILE="pysock_hlp.txt"
		self.PYSOCK_CMDFILE="pysock_cmd.txt"
		self.PYSOCK_CONFILE="pysock_con.txt"
		#args
		self.PYSOCK_SHRTARG='c:df:ghr:s:'
		self.PYSOCK_LONGARG=('command=','default','file=','get','help','raw=','set=')

		#analyze argv
		try:
			self.optlist, self.args = getopt.getopt(sys.argv[1:],self.PYSOCK_SHRTARG,self.PYSOCK_LONGARG)
		except getopt.GetoptError, err:
			print str(err)
			sys.exit(2)
		#analyze optlist
		self.ArgAnalyze(self.optlist)

	def Docs():
		"""\
		Intro
		\tPySock is a simple program that uses socket connection
		\t\tto send a little query to a metin2 server (using adminpage)


		ArgvList:
		#(-c or --command) send command
		\t./pysock.py -c "<command>"
		#(-g or --get) get con-data from con-file (pysock_con.txt) and send a command
		\t./pysock.py -g -c "<command>"
		#(-f or --file) send command from file
		\t./pysock.py -f "<file>"
		\t\tExample:\t./pysock.py -f "mysock_cmd.txt"
		#(-h or --help) help
		\t./pysock.py -h
		#(-s or --set) set con-data to con-file (pysock_con.txt) and send a command
		\t./pysock.py -s "<host>:<port>:<pwd>"
		\t\tExample:\t./pysock.py -s "123.456.78.90:13000:SHOMETHEMONEY" -c "NOTICE 1;NOTICE 2;NOTICE 3"
		#(-r or --raw) raw mode
		\t./pysock.py -r "<host:port> <adminpwd> <command>"
		\t\tExample:\t./pysock.py -r "123.456.78.90:13000 SHOWMETHEMONEY NOTICE 1;NOTICE 2;USER_COUNT"

		CommandList:
		#block_chat %s %d
		\tBLOCK_CHAT <nick> <duration>
		\t\tExample:\tBLOCK_CHAT [GA]LoLLo 1h
		#block_exception
		\tBLOCK_EXCEPTION
		#check_client
		\tCHECK_CLIENT
		#close_passpod
		\tCLOSE_PASSPOD
		#dc %s
		\tDC <account>
		\t\tExample:\tDC tuoaccount
		#event %s %d
		\tEVENT <eventflag> <value>
		\t\tExample:\tEVENT xmas_tree 4
		#notice %s
		\tNOTICE <message>
		\t\tExample:\tNOTICE This is a test
		#is_passpod_up
		\tIS_PASSPOD_UP
		#is_server_up
		\tIS_SERVER_UP
		#priv_empire %d %d %d %d
		\tPRIV_EMPIRE <empire> <type> <value> <duration>
		\t\tempire\t0-3  0==all, 1==red, 2==yellow, 3==blue)
		\t\ttype\t1:item_drop, 2:gold_drop, 3:gold10_drop, 4:exp
		\t\tvalue\tpercent
		\t\tdur.\thour
		\t\tExample:\tPRIV_EMPIRE 0 4 200 72h
		#profile
		\tPROFILE
		#reload &%s
		\tRELOAD <&type>
		\t\ttype\tdefault:general, a:admin, c:cube, f:fish, p:player, q:quest, s:string
		#reload_crc
		\tRELOAD_CRC
		#shutdown
		\tSHUTDOWN
		#shutdown_only
		\tSHUTDOWN_ONLY
		#unknown
		\tUNKNOWN
		#user_count
		\tUSER_COUNT

		Created by martysama0134 - 2012 - All rights reserved
		"""

	def SendPacket(self, HOSTPORT=None, ADMINPWD=None, COMMAND=None):
		if(HOSTPORT in self.NOWAY): HOSTPORT=self.dftHOSTPORT
		if(ADMINPWD in self.NOWAY): ADMINPWD=self.dftADMINPWD
		if(COMMAND in self.NOWAY): COMMAND=self.dftCOMMAND
		try:
			#connect
			con=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
			con.connect(HOSTPORT)
			#send
			CMDSEND="@%s\n@%s\n" % (ADMINPWD,"\n@".join(COMMAND))
			print CMDSEND
			con.send(CMDSEND)
			#receive
			print repr(con.recv(1024))#escape
			time.sleep(0.1)#required
			#close
			con.close()
			print "<Pysock> Socket inviato con successo"
		except socket.error:
			assert False, "<Pysock> Socket failed, con-data maybe wrong (%s, %s, %s)"%(HOSTPORT[0], HOSTPORT[1], ADMINPWD)

	def ArgAnalyze(self, optlist):
		for o, a in optlist:
			#help
			if o in ('-h', '--help'):
				try:
					help(self.Docs)
					#print self.Docs.__doc__
				except KeyboardInterrupt:
					pass
				sys.exit()
			#send command from arg
			elif o in ('-c', '--command'):
				#analyze string-arg
				try:
					self.COMMAND=a.split(";")
				except IndentationError, err:
					assert False, "<Pysock> Except %s" % (err,)
				self.SendPacket(self.HOSTPORT, self.ADMINPWD, self.COMMAND)
			#load default con-data
			elif o in ('-d', '--default'):
				self.HOSTPORT=self.dftHOSTPORT
				self.ADMINPWD=self.dftADMINPWD
				self.COMMAND=self.dftCOMMAND
			#load command from file
			elif o in ('-f', '--file'):
				#analyze string-arg
				if(os.path.exists(a)):
					#read file
					self.COMMAND=open(a,"r").read().split("\n")
					#send
					self.SendPacket(self.HOSTPORT, self.ADMINPWD, self.COMMAND)
				else:
					assert False, "<Pysock> File %s not found" % (a,)
			#load con-data from file
			elif o in ('-g', '--get'):
				#analyze string-arg
				if(os.path.exists(self.PYSOCK_CONFILE)):
					#read file
					self.CONREAD=open(self.PYSOCK_CONFILE,"r").read()
					#set con-data
					try:
						self.CONAN=self.CONREAD.split(":",2)
						#set con-data
						self.HOSTPORT=(self.CONAN[0],int(self.CONAN[1]))
						self.ADMINPWD=self.CONAN[2].replace("\n","").replace("\r","")
					except IndentationError, err:
						assert False, "<Pysock> Except %s" % (err,)
				else:
					assert False, "<Pysock> File %s not found" % (self.PYSOCK_CONFILE,)
			#create a manual string
			elif o in ('-r', '--raw'):
				#analyze string-arg
				try:
					a=a.split(" ",2)
				except IndentationError, err:
					assert False, "<Pysock> Except %s" % (err,)
				#set data
				myHOSTPORT=a[0].split(":",1)
				self.HOSTPORT=(myHOSTPORT[0],int(myHOSTPORT[1]))
				self.ADMINPWD=a[1]
				self.COMMAND=a[2].split(";")
				#send
				self.SendPacket(self.HOSTPORT, self.ADMINPWD, self.COMMAND)
			#save your data connection
			elif o in ('-s', '--set'):
				#analyze string-arg
				try:
					self.CONAN=a.split(":",2)
				except IndentationError, err:
					assert False, "<Pysock> Except %s" % (err,)
				#save hostport
				f1=open(self.PYSOCK_CONFILE,"w")
				f1.write(a)
				del f1
				#set con-data
				self.HOSTPORT=(self.CONAN[0],int(self.CONAN[1]))
				self.ADMINPWD=self.CONAN[2]
			#invalid args
			else:
				assert False, "<Pysock> Unhandled %s option" % (o,)

avvia=PySockModule
avvia()
