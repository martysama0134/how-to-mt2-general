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
