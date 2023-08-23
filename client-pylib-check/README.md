The `ENABLE_PYLIB_CHECK-refactory-v3.cpp` contains a full refactory in c++20.

### How to Install the new version
1. Before `app->Initialize(hInstance);` add (or keep):

	```cpp
	#ifdef ENABLE_PYLIB_CHECK
		if (!__CheckPyLibFiles())
			return false;
	#endif
	```

2. Replace the old code inside `Client\UserInterface\UserInterface.cpp` with the one inside `ENABLE_PYLIB_CHECK-refactory-v3.cpp`.

### How to Load via Json

1. Set this constant as true: `constexpr bool PyLibTableLoadFromJson = true;`
2. Add the generated `pylibfilestable.json` in root eix/epk

