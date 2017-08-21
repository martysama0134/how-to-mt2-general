If you have issues in displaying the WorldEditor such as a bigger an cut-off UI, you have to do the following things:

1. Turn on the external manifest loading by running [Enable External Manifest.reg](./Enable External Manifest.reg).

1. Put the [WorldEditor_MfcRelease_vc100_v24.exe.manifest](./WorldEditor_MfcRelease_vc100_v24.exe.manifest) manifest file beside the program.

	_Note: The note must be called the same as the program.exe with the .manifest in the end.


Extra:

After that, you may also have a little problem in Windows 10 if you changed the DPI settings inside the control panel.

You can solve it by going to **Home -> Screen -> Scale and layout** to 100%.

[![Result Label](http://i.imgur.com/QKRtdq7.png)](http://i.imgur.com/QKRtdq7.png)
