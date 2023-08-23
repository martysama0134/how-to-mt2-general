### How to Install it
Before `app->Initialize(hInstance);` add:

```cpp
#ifdef ENABLE_PYLIB_CHECK
	if (!__CheckPyLibFiles())
		return false;
#endif
```

The `ENABLE_PYLIB_CHECK-refactory-v3.cpp` contains a full refactory in c++20. Replace the old code inside `Client\UserInterface\UserInterface.cpp`.
