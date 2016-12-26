--[[ ## I usually check the syserr and clean the lines doing:
    # Find:
        ^(.*)martytest \:
    # Replace with:
        (empty)
    [v] Regular expression
]]

-- muhTable = {}
-- for k,v in pairs(_G) begin
	-- sys_err(string.format("%s == %s", type(v), k))
-- end

-- for k,v in pairs(_G) begin
	-- local x = type(v)
	-- if muhTable[x]==nil then muhTable[x] = {} end
	-- table.insert(muhTable[x], k)
-- end

-- table.sort(muhTable["function"])
-- for k,v in ipairs(muhTable["function"]) begin
	-- sys_err(v)
-- end

-- table.sort(muhTable["table"])
-- for k,v in ipairs(muhTable["table"]) begin
	-- sys_err(v)
-- end

local modList = {
	-- "debug",
	-- "io",
	-- "math",
	-- "os",
	-- "string",
	-- "table",
	"affect",
	"arena",
	"ba",
	"building",
	"coroutine",
	"d",
	"dance_event",
	"ds",
	"forked",
	"game",
	"guild",
	"highscore",
	"horse",
	"item",
	"marriage",
	"member",
	"mgmt",
	"mining",
	"mob",
	"npc",
	"oh",
	"oxevent",
	"party",
	"pc",
	"pet",
	"q",
	"speedserver",
	"target",
	"village_map",
	-- "dnd",
	-- "mob_rewarp",
}

-- for n,e in ipairs(modList) begin
	-- for k,v in pairs(_G[e]) begin
		-- if type(v) == "function" then
			-- sys_err(string.format("%s.%s", e, k))
		-- end
	-- end
-- end

for n,e in ipairs(modList) begin
	local tmpList = {}
	for k,v in pairs(_G[e]) begin
		if type(v) == "function" then
			table.insert(tmpList, string.format("%s.%s", e, k))
		end
	end
	table.sort(tmpList)
	for num,elem in ipairs(tmpList) begin
		sys_err(elem)
	end
end
