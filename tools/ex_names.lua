local function load(p) local f=io.open(p,"rb") local d=f:read("*a") f:close() return assert(loadstring(d))() end
local function dump(tag, t, field)
  for k,v in pairs(t) do
    local name = type(v)=="table" and v[field or "name"] or v
    if type(name)=="string" and name~="" and not name:match("^[%?%-]+$") then
      local num = type(k)=="number" and k or 0
      io.write(tag,"\t",num,"\t",name,"\n")
    end
  end
end
dump("MOVE", load(arg[1]))
dump("ABILITY", load(arg[2]))
dump("ITEM", load(arg[3]).items)
