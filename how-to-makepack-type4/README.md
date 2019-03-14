# How-to makepack type4
By using `MakePack.exe` (you need to compile it), you can use this python script to generate type4 packs.
The generated .dat key must be added in the package/ folder server-side.

### EN
1. drag&drop the folder to pack on `MakePackHelper_List.bat`
(it will generate `<foldername>.txt`) [ClickMe](https://i.imgur.com/a5E5u6E.png)

2. drag&drop the folder to pack on `MakePack_Run.bat` [ClickMe](https://i.imgur.com/TPtgR5z.png)
(it will create `Pack/` containing `.dat`, `Index` and the eix epk files [ClickMe](https://i.imgur.com/pEvMWDx.png))

3. upload the `.dat` on `package/` server-side and restart the game

### IT
1. trascina la folder da packare su `MakePackHelper_List.bat`
(creerà `<nomefolder>.txt`) [ClickMe](https://i.imgur.com/a5E5u6E.png)

2. trascina la folder da packare su `MakePack_Run.bat` [ClickMe](https://i.imgur.com/TPtgR5z.png)
(creerà `Pack/` contenente la `.dat`, `Index` e gli eix epk [ClickMe](https://i.imgur.com/pEvMWDx.png))

3. carica la `.dat` su `package/` server-side e riavvia il game

_Note: just change CSHybridEncryptExeNameList to SecurityExtNameList for packing everything in type2 instead of type4_
