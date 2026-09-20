local function load(p) local f=io.open(p,"rb") local d=f:read("*a") f:close() return assert(loadstring(d))() end
local items = load(arg[1])
local desc = load(arg[2])
local function dump(tag, t)
  for k,v in pairs(t) do
    if type(v)=="string" and #v>3 and not v:match("^%?+$") then
      io.write(tag,"\t",tostring(k),"\t",v:gsub("\n","\\n"),"\n")
    end
  end
end
dump("ITEM", items.items)
if desc.ABILITIES then dump("ABILITY", desc.ABILITIES) end
if desc.MOVES then dump("MOVE", desc.MOVES) end
for k,v in pairs(desc) do if type(v)=="table" and k~="ABILITIES" and k~="MOVES" then dump("OTHER_"..k, v) end end
