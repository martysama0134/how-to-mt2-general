###### [How-To] Notepad++ Syntax Highlighting Metin2 Quests Lua

---
## How to "install" it?
Open *%appdata%\Notepad++\langs.xml* and replace the `<Language name="lua" ...>` section with this: [langs.m2luaonly.xml](https://github.com/martysama0134/how-to-mt2-general/raw/master/quest-syntax-highlighting/langs.m2luaonly.xml)

After that, restart notepad++, and it's done.

Result:
[![Result Label](http://i.imgur.com/ijAVxHg.png)](http://i.imgur.com/ijAVxHg.png)

Note:
In [example_dumplist.lua](./example_dumplist.lua) you can find some examples to make some function list dumps as well via quest. (dumping only metin2 methods)
In [example_quest_functions.lua](./example_quest_functions.lua) you can find an example to make the whole function list currently in use, ideal for generating quest_functions.
