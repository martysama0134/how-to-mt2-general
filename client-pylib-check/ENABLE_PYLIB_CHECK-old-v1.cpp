// martysama0134 - 2014
#ifdef ENABLE_PYLIB_CHECK
#define PRINT_LEVEL 0
#define PRINTME(level, ...) if(PRINT_LEVEL>=level) TraceError(__VA_ARGS__);
#define PYFOLD "./lib"
// #define PYFORCE

typedef struct PyLibFiles_s
{
	std::string sFileName;
	size_t stSize;
	DWORD dwCRC32;
} PyLibFiles_t;

PyLibFiles_t PyLibFilesTable[] =
{
#if PY_VERSION_HEX==0x020706f0
	{ PYFOLD"/abc.pyc", 6187, 3834771731},
	{ PYFOLD"/bisect.pyc", 3236, 3116899751},
	{ PYFOLD"/codecs.pyc", 36978, 2928014693},
	{ PYFOLD"/collections.pyc", 26172, 385366131},
	{ PYFOLD"/copy.pyc", 13208, 1091298715},
	{ PYFOLD"/copy_reg.pyc", 5157, 536292604},
	{ PYFOLD"/encodings/aliases.pyc", 8803, 3888310600},
	{ PYFOLD"/encodings/cp949.pyc", 2009, 1824094431},
	{ PYFOLD"/encodings/__init__.pyc", 4510, 2926961588},
	{ PYFOLD"/fnmatch.pyc", 3732, 4270526278},
	{ PYFOLD"/functools.pyc", 6193, 3257285433},
	{ PYFOLD"/genericpath.pyc", 3303, 1652596334},
	{ PYFOLD"/heapq.pyc", 13896, 2948659214},
	{ PYFOLD"/keyword.pyc", 2169, 2178546341},
	{ PYFOLD"/linecache.pyc", 3235, 4048207604},
	{ PYFOLD"/locale.pyc", 49841, 4114662314},
	{ PYFOLD"/ntpath.pyc", 11961, 2765879465},
	{ PYFOLD"/os.pyc", 25769, 911432770},
	{ PYFOLD"/pyexpat.pyd", 127488, 2778492911},
	{ PYFOLD"/pyexpat_d.pyd", 194560, 2589182738},
	{ PYFOLD"/re.pyc", 13178, 1671609387},
	{ PYFOLD"/shutil.pyc", 19273, 1873281015},
	{ PYFOLD"/site.pyc", 20019, 3897044925},
	{ PYFOLD"/sre_compile.pyc", 11107, 1620746411},
	{ PYFOLD"/sre_constants.pyc", 6108, 3900811275},
	{ PYFOLD"/sre_parse.pyc", 19244, 1459430047},
	{ PYFOLD"/stat.pyc", 2791, 1375966108},
	{ PYFOLD"/string.pyc", 19656, 1066063587},
	{ PYFOLD"/sysconfig.pyc", 17571, 1529083148},
	{ PYFOLD"/traceback.pyc", 11703, 3768933732},
	{ PYFOLD"/types.pyc", 2530, 920695307},
	{ PYFOLD"/UserDict.pyc", 9000, 1431875928},
	{ PYFOLD"/warnings.pyc", 13232, 3752454002},
	{ PYFOLD"/weakref.pyc", 16037, 2124701469},
	{ PYFOLD"/xml/dom/domreg.pyc", 3506, 2127674645},
	{ PYFOLD"/xml/dom/expatbuilder.pyc", 36698, 316034696},
	{ PYFOLD"/xml/dom/minicompat.pyc", 4144, 747596376},
	{ PYFOLD"/xml/dom/minidom.pyc", 74704, 1543233763},
	{ PYFOLD"/xml/dom/nodefilter.pyc", 1243, 3805409468},
	{ PYFOLD"/xml/dom/xmlbuilder.pyc", 18659, 4118801318},
	{ PYFOLD"/xml/dom/__init__.pyc", 7337, 343751384},
	{ PYFOLD"/xml/parsers/expat.pyc", 326, 2425747752},
	{ PYFOLD"/xml/parsers/__init__.pyc", 353, 1691127318},
	{ PYFOLD"/xml/__init__.pyc", 1117, 3531597556},
	{ PYFOLD"/_abcoll.pyc", 22339, 2365844594},
	{ PYFOLD"/_locale.pyc", 49841, 4114662314},
	{ PYFOLD"/_weakrefset.pyc", 10490, 1576811346},
	{ PYFOLD"/__future__.pyc", 4431, 2857792867},
#elif PY_VERSION_HEX==0x020203f0
#else
#error "unknown python version"
#endif
};

bool checkPyLibDir(const string szDirName)
{
	bool HasHack = false;

	char szDirNamePath[MAX_PATH];
	sprintf(szDirNamePath, "%s\\*", szDirName.c_str());

	WIN32_FIND_DATA f;
	HANDLE h = FindFirstFile(szDirNamePath, &f);

	if (h == INVALID_HANDLE_VALUE) { return HasHack; }

	do
	{
		if (HasHack)
			break;
		const char * name = f.cFileName;

		if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0) { continue; }

		if (f.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY)
		{
			char filePath[MAX_PATH];
			sprintf(filePath, "%s%s%s", szDirName.c_str(), "\\", name);
			PRINTME(1, "sub %s", filePath);
            checkPyLibDir(filePath);
		}
		else
		{
			// start processing file
			PRINTME(1, "starting %s", name);
			std::string sName(name);
			std::string sPathName(szDirName+"/"+name);
			// change \\ to /
			std::replace(sPathName.begin(), sPathName.end(), '\\', '/');
			PRINTME(1, "path %s", sPathName.c_str());
			// lower file name
			std::transform(sName.begin(), sName.end(), sName.begin(), ::tolower);
			{
				PRINTME(1, "verify %s", sName.c_str());
				bool isPyLibFound = false;
				for (PyLibFiles_t *i1=std::begin(PyLibFilesTable), *e1=std::end(PyLibFilesTable); i1<e1; i1++)
				{
					if (!i1->sFileName.compare(sPathName))
					{
						PRINTME(1, "found %s==%s", i1->sFileName.c_str(), sName.c_str());
						DWORD dwCrc32 = GetFileCRC32(sPathName.c_str());
						// assert(dwCrc32);
						DWORD dwFileSize = f.nFileSizeLow;
						if (i1->stSize!=dwFileSize)
						{
							PRINTME(1, "wrong size %u==%u", i1->stSize, dwFileSize);
							HasHack = true;
							PRINTME(0, "wrong size %u for %s", dwFileSize, sPathName.c_str());
							return HasHack;
						}
						else if (i1->dwCRC32 != dwCrc32)
						{
							PRINTME(1, "wrong crc32 %u==%u", i1->dwCRC32, dwCrc32);
							HasHack = true;
							PRINTME(0, "wrong crc32 %u for %s", dwCrc32, sPathName.c_str());
							return HasHack;
						}
						PRINTME(1, "right size %u==%u", i1->stSize, dwFileSize);
						PRINTME(1, "right crc32 %u==%u", i1->dwCRC32, dwCrc32);
						PRINTME(2, "{ \"%s\", %u, %u},", sPathName.c_str(), dwFileSize, dwCrc32);
						isPyLibFound = true;
						break;
					}
				}
				// block ambiguous pyc/d files
				if (!isPyLibFound)
				{
					PRINTME(1, "not found %s", sName.c_str());
#ifdef PYFORCE
					HasHack = true;
					PRINTME(0, "ambiguous file for %s", sPathName.c_str());
					return HasHack;
#endif
				}
				PRINTME(1, "skipping file(%s) hack(%u) found(%u)", sName.c_str(), HasHack, isPyLibFound);
			}
		}

	} while (FindNextFile(h, &f));
	FindClose(h);
	return HasHack;
}

bool __CheckPyLibFiles()
{
	PRINTME(1, "__CheckPyLibFiles processing "PYFOLD);
	if (checkPyLibDir(PYFOLD))
		return false;
	return true;
}
#endif