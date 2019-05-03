This is a revised version of an old thread. Following this How-To, you will have a better customizable solution for the aspect of your quests.

You will be able to choice amongst: quest icon, text color, blink effect (like whisper buttons)

### How To
You just need to replace 2 little things:

In interfaceModule.py, replace BINARY_RecvQuest with:
[Python] interfaceModule.codepart.py - Pastebin.com

In questlib.lua, replace send_letter_ex with:
[Lua] questlib.codepart.lua - Pastebin.com

### Explanation:
- the 2° argument of send_letter_ex will support multiple parameters:

	- green|blue|purple|golden|fucsia|aqua and so on (you can add them in BINARY_RecvQuest by adding new colors 0xFF+#HEX; Color Picker Online)
	- blink (the quest will flash like the whisper messages)
	- ex (a dummy tag to separate it from "info" and "item")

- the 3° argument is the name of the icon to choose, which the current availables are:

	- scroll_open.tga
	- scroll_open_green.tga
	- scroll_open_blue.tga
	- scroll_open_purple.tga
	- scroll_open_golden.tga

### Examples:

_Note: As you can imagine, the only limitation is that the color in N won't appear. (it will require additional code and work, so just forget it)_

### Download:
Add metin2_patch_new_questicon in your client.
