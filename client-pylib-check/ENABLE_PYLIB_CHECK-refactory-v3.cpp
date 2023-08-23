#ifdef ENABLE_PYLIB_CHECK
#include <algorithm>
#include <filesystem>
#include <iostream>
#include <string>
#include <vector>
#include <fmt/format.h> // Assuming you have fmt library installed

constexpr bool PyLibCheckForce = false; // Throw an error if the file is missing
constexpr int PrintLevel = 0;

template <class... Args>
void PrintMe(int level, const Args&... Arguments)
{
	if (PrintLevel >= level)
		TraceError(Arguments...);
}

typedef struct PyLibFiles_s
{
	std::string fileName;
	size_t stSize;
	DWORD dwCRC32;
} PyLibFiles_t;

std::vector<PyLibFiles_t> PyLibFilesTable = {
	{ "lib/abc.pyc", 6187, 3834771731 },
	{ "lib/bisect.pyc", 3236, 3116899751 },
	{ "lib/codecs.pyc", 36978, 2928014693 },
	{ "lib/collections.pyc", 26172, 385366131 },
	{ "lib/copy.pyc", 13208, 1091298715 },
	{ "lib/copy_reg.pyc", 5157, 536292604 },
	{ "lib/fnmatch.pyc", 3732, 4270526278 },
	{ "lib/functools.pyc", 6193, 3257285433 },
	{ "lib/genericpath.pyc", 3303, 1652596334 },
	{ "lib/hashlib.pyc", 6864, 249833099 },
	{ "lib/heapq.pyc", 13896, 2948659214 },
	{ "lib/keyword.pyc", 2169, 2178546341 },
	{ "lib/linecache.pyc", 3235, 4048207604 },
	{ "lib/locale.pyc", 49841, 4114662314 },
	{ "lib/ntpath.pyc", 11961, 2765879465 },
	{ "lib/os.pyc", 25769, 911432770 },
	{ "lib/pyexpat.pyd", 127488, 2778492911 },
	{ "lib/pyexpat_d.pyd", 194560, 2589182738 },
	{ "lib/random.pyc", 25491, 4021547204 },
	{ "lib/re.pyc", 13178, 1671609387 },
	{ "lib/shutil.pyc", 19273, 1873281015 },
	{ "lib/site.pyc", 20019, 3897044925 },
	{ "lib/sre_compile.pyc", 11107, 1620746411 },
	{ "lib/sre_constants.pyc", 6108, 3900811275 },
	{ "lib/sre_parse.pyc", 19244, 1459430047 },
	{ "lib/stat.pyc", 2791, 1375966108 },
	{ "lib/string.pyc", 19656, 1066063587 },
	{ "lib/struct.pyc", 234, 3060853334 },
	{ "lib/sysconfig.pyc", 17571, 1529083148 },
	{ "lib/traceback.pyc", 11703, 3768933732 },
	{ "lib/types.pyc", 2530, 920695307 },
	{ "lib/UserDict.pyc", 9000, 1431875928 },
	{ "lib/warnings.pyc", 13232, 3752454002 },
	{ "lib/weakref.pyc", 16037, 2124701469 },
	{ "lib/_abcoll.pyc", 22339, 2365844594 },
	{ "lib/_locale.pyc", 49841, 4114662314 },
	{ "lib/_weakrefset.pyc", 10490, 1576811346 },
	{ "lib/__future__.pyc", 4431, 2857792867 },
};

bool checkPyLibDir()
{
	bool HasHack = false;

	for (const auto& fileInfo : PyLibFilesTable)
	{
		// Check if the file exists
		if (!std::filesystem::exists(fileInfo.fileName))
		{
			if constexpr (PyLibCheckForce)
			{
				PrintMe(0, "File not found: {}", fileInfo.fileName.c_str());
				HasHack = true;
				break;
			}
			PrintMe(1, "File not found: {}", fileInfo.fileName.c_str());
			continue;
		}

		const auto dwFileSize = GetFileSize(fileInfo.fileName.c_str());
		const auto dwCrc32 = GetFileCRC32(fileInfo.fileName.c_str());

		if (fileInfo.stSize != dwFileSize)
		{
			PrintMe(1, "wrong size %zu==%u", fileInfo.stSize, dwFileSize);
			PrintMe(0, "wrong size %zu for %s", dwFileSize, fileInfo.fileName.c_str());
			HasHack = true;
			break;
		}
		else if (fileInfo.dwCRC32 != dwCrc32)
		{
			PrintMe(1, "wrong crc32 %u==%u", fileInfo.dwCRC32, dwCrc32);
			PrintMe(0, "wrong crc32 %u for %s", dwCrc32, fileInfo.fileName.c_str());
			HasHack = true;
			break;
		}
		else
		{
			PrintMe(1, "right size %zu==%u", fileInfo.stSize, dwFileSize);
			PrintMe(1, "right crc32 %u==%u", fileInfo.dwCRC32, dwCrc32);
		}
	}

	return HasHack;
}

bool __CheckPyLibFiles()
{
	PrintMe(1, "__CheckPyLibFiles processing");
	if (checkPyLibDir())
		return false;
	return true;
}
#endif