# Intro
This python script automatically generates random xtea keys (into a file called `xtea_keys_gen.txt`) and the relative array code for the `EterPack.cpp` as well.

The result will be like [this](https://i.imgur.com/U8cYOPy.png) (the keys get changed every time you run the script)


# Extra
If you already have a string and need to convert it into numbers or vice versa:

```python
# string to int
>>> import struct
>>> struct.unpack("IIII", "b99eb0026f69810563989b2879181a00".decode('hex'))
(45129401, 92367215, 681285731, 1710201)
>>> struct.unpack("IIII", "22b8b40464b26e1faeea1800a6f6fb1c".decode('hex'))
(78952482, 527348324, 1632942, 486274726)
# int to string
>>> import struct
>>> struct.pack("IIII", 45129401, 92367215, 681285731, 1710201).encode('hex')
'b99eb0026f69810563989b2879181a00'
>>> struct.pack("IIII", 78952482, 527348324, 1632942, 486274726).encode('hex')
'22b8b40464b26e1faeea1800a6f6fb1c'
```
