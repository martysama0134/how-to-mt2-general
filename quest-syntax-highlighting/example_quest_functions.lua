
local function dumpFunctions(tbl, done, preStr)
	local functions = {}
	local done = done or {tbl}
	local preStr = preStr or ""

	for k, v in pairs(tbl) do
		local path = ""
		if preStr == "" then
			path = k
		else
			path = string.format("%s.%s", preStr, k)
		end

		if type(v) == "function" then
			table.insert(functions, path)
		elseif type(v) == "table" then
			local currentTableAlreadyDone = false
			for _, tbl in ipairs(done) do
				if tbl == v then
					currentTableAlreadyDone = true
					break
				end
			end

			if not currentTableAlreadyDone then
				table.insert(done, v)

				for _, functionName in ipairs(dumpFunctions(v, done, path)) do
					table.insert(functions, functionName)
				end
			end
		end
	end

	return functions
end

local functions = dumpFunctions(_G)
table.sort(functions)

local outFile = assert(io.open("quest_functions", "w"))
for _, functionName in ipairs(functions) do
	outFile:write(functionName.."\n")
end
assert(outFile:close())
