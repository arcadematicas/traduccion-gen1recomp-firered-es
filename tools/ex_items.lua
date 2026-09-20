local f=io.open(arg[1],"rb") local d=f:read("*a") f:close()
local items = assert(loadstring(d))()
for k,v in pairs(items.items) do
  if type(v)=="table" then
    local desc = (v.description or ""):gsub("\n","\\n")
    io.write(tostring(k),"\t",tostring(v.name),"\t",desc,"\n")
  end
end
