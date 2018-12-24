# How to manually debug crashes with VisualStudio

1. Go to Debug -> Options and Settings... [ClickMe](https://i.imgur.com/N6l5hUE.png)

	Go inside Debugging -> General [ClickMe](https://i.imgur.com/tzlVBdA.png)

	[v] Show disassembly if source is not available

2. On UserInterface -> Properties [ClickMe](https://i.imgur.com/LSi4xHl.png)

	Go inside Linker -> Debugging [ClickMe](https://i.imgur.com/vf6Y6yU.png)
	
	* Generate Debug Info -> Yes (/DEBUG)
	* ~Map Exports -> Yes (/MAPINFO:EXPORTS)~ _(not required)_
	* Debuggable Assembly -> Yes (/ASSEMBLYDEBUG)

3. Compile and execute the launcher.

4. Debug -> Attach to Process... [ClickMe](https://i.imgur.com/Mskhvaq.png)

	metin2client.exe -> Attach [ClickMe](https://i.imgur.com/50WDcYa.png)

5. When you will get a crash (or "??????") you will get the Call Stack [ClickMe](https://i.imgur.com/LGXpzz5.png)

6. To disable all: [ClickMe](https://i.imgur.com/aV29aB0.png)

	On UserInterface -> Properties

	Go inside Linker -> Debugging
	
	* Generate Debug Info -> No
	* Map Exports -> No
	* Debuggable Assembly -> No (/ASSEMBLYDEBUG:DISABLE)

_Note: Whether the target is set on Release or Debug, it's irrelevant_
