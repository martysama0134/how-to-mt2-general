
Before `app->Initialize(hInstance);` add:

```cpp
#ifdef ENABLE_PYLIB_CHECK
	if (!__CheckPyLibFiles())
		return false;
#endif
```

The `ENABLE_PYLIB_CHECK-refactory-v3.cpp` contains a full refactory in c++20.
