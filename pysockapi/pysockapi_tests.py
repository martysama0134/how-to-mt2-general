### PORT
# Text (BYTE)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 13000))
con.send("@")
repr(con.recv(1024))

# MarkLogin (BYTE DWORD DWORD)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 13000))
con.send("d22223333")
repr(con.recv(1024))

# ServerStateCheck (BYTE)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 13000))
con.send("\xce")
repr(con.recv(1024))

# Pong (BYTE)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 13000))
con.send("\xfe")
repr(con.recv(1024))

# Handshake (BYTE DWORD DWORD long)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 13000))
con.send("\xff")
repr(con.recv(1024))

# KeyAgreement (BYTE WORD WORD BYTE[256])
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 13000))
con.send("\xfb2233"+("4"*256))
repr(con.recv(1024))

### P2P_PORT
# Shutdown (BYTE)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\x05")
repr(con.recv(1024))

# Shout (BYTE, BYTE empire, char[512+1] text)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\x08"+"\x00"+"smth".ljust(512+1))
repr(con.recv(1024))

# BlockChat (BYTE, char[24+1] nick, long duration)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\x16"+"martytest\0".ljust(24+1)+"\0\0\0\0")
repr(con.recv(1024))

# Notice (BYTE, long len, &char[len] text)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\x04"+"\xff\0\0\0"+"omg\0".ljust(255))
repr(con.recv(1024))

# XmasWarpSanta (BYTE, BYTE channel, long mapindex)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\x11"+"\x01"+")\0\0\0")
repr(con.recv(1024))

# Transfer (BYTE, char[24+1] nick, long x, long y)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\x10"+"martytest\0".ljust(24+1)+"\xb8\xb1\x0e\x00"+"\x54\x3e\x04\x00")
repr(con.recv(1024))

# WarpCharacter (BYTE, DWORD pid, long x, long y)
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\r"+"\x01\0\0\0"+"\xb8\xb1\x0e\x00"+"\x54\x3e\x04\x00")
repr(con.recv(1024))

# Relay (BYTE, char[24+1] whom, long size, &)
#		-> (BYTE header, WORD len, BYTE type, char[24+1] who) #29
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 21103))
con.send("\x03"+"martytest\0".ljust(24+1)+"(\0\0\0"+'"'+"\x0b\0\0\0"+"\x0f"+"martytes2\0".ljust(24+1)+"abcd\0".ljust(9))
repr(con.recv(1024))

### DB_PORT (BYTE header, DWORD handle, DWORD size)
# HEADER_GD_DELETE_AWARDID
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 20000))
con.send("\x8a"+"\0\0\0\0"+"\x04\0\0\0"+"\x01\0\0\0")
repr(con.recv(1024))

# HEADER_GD_DELETE_AWARDID
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
con.connect(("1.2.3.4", 20000))
con.send("\x1e"+"\0\0\0\0"+"\x04\0\0\0"+"\x01\0\0\0")
repr(con.recv(1024))












