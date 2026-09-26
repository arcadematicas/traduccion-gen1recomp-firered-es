-- Clasifica scripts/text.lua (gen3 0.3.x) reconstruyendo EN con los nombres de
-- token que usa el corpus (poke-corpus). Salida: clave<TAB>complejo<TAB>EN
local path = arg[1]
local f = io.open(path, "rb")
local data = f:read("*a"); f:close()
local t = assert(loadstring(data, path))()

local B_TXT = {
  [0x00]="B_BUFF1",[0x01]="B_BUFF2",[0x02]="B_COPY_VAR_1",[0x03]="B_COPY_VAR_2",
  [0x04]="B_COPY_VAR_3",[0x05]="B_PLAYER_MON1_NAME",[0x06]="B_OPPONENT_MON1_NAME",
  [0x07]="B_PLAYER_MON2_NAME",[0x08]="B_OPPONENT_MON2_NAME",[0x09]="B_LINK_PLAYER_MON1_NAME",
  [0x0A]="B_LINK_OPPONENT_MON1_NAME",[0x0B]="B_LINK_PLAYER_MON2_NAME",[0x0C]="B_LINK_OPPONENT_MON2_NAME",
  [0x0D]="B_ATK_NAME_WITH_PREFIX_MON1",[0x0E]="B_ATK_PARTNER_NAME",[0x0F]="B_ATK_NAME_WITH_PREFIX",
  [0x10]="B_DEF_NAME_WITH_PREFIX",[0x11]="B_EFF_NAME_WITH_PREFIX",[0x12]="B_ACTIVE_NAME_WITH_PREFIX",
  [0x13]="B_SCR_ACTIVE_NAME_WITH_PREFIX",[0x14]="B_CURRENT_MOVE",[0x15]="B_LAST_MOVE",
  [0x16]="B_LAST_ITEM",[0x17]="B_LAST_ABILITY",[0x18]="B_ATK_ABILITY",[0x19]="B_DEF_ABILITY",
  [0x1A]="B_SCR_ACTIVE_ABILITY",[0x1B]="B_EFF_ABILITY",[0x1C]="B_TRAINER1_CLASS",
  [0x1D]="B_TRAINER1_NAME",[0x1E]="B_LINK_PLAYER_NAME",[0x1F]="B_LINK_PARTNER_NAME",
  [0x20]="B_LINK_OPPONENT1_NAME",[0x21]="B_LINK_OPPONENT2_NAME",[0x22]="B_LINK_SCR_TRAINER_NAME",
  [0x23]="B_PLAYER_NAME",[0x24]="B_TRAINER1_LOSE_TEXT",[0x25]="B_TRAINER1_WIN_TEXT",
  [0x26]="B_26",[0x27]="B_PC_CREATOR_NAME",[0x28]="B_ATK_PREFIX1",[0x29]="B_DEF_PREFIX1",
  [0x2A]="B_ATK_PREFIX2",[0x2B]="B_DEF_PREFIX2",[0x2C]="B_ATK_PREFIX3",[0x2D]="B_DEF_PREFIX3",
  [0x2E]="B_TRAINER2_LOSE_TEXT",[0x2F]="B_TRAINER2_WIN_TEXT",[0x30]="B_BUFF3",
}

local SIMPLE = { text=true, nl=true, para=true, scroll=true, eos=true,
                 player=true, rival=true, strvar=true, bph=true, tag=true }

local function esc(s)
  local out = {}
  for i = 1, #s do
    local b = s:byte(i)
    if b == 10 then out[#out+1]="\\n" elseif b == 9 then out[#out+1]="\\t"
    elseif b == 13 then out[#out+1]="\\r"
    elseif b < 32 or b == 127 then out[#out+1]=string.format("\\%03d", b)
    else out[#out+1]=s:sub(i,i) end
  end
  return table.concat(out)
end

local function rebuild(cmds)
  local out = {}
  for _, c in ipairs(cmds) do
    local ty = c.t
    if ty == "text" then out[#out+1] = esc(c.s or "")
    elseif ty == "nl" then out[#out+1] = "\\n"
    elseif ty == "para" then out[#out+1] = "\\c"
    elseif ty == "scroll" then out[#out+1] = "\\r"
    elseif ty == "player" then out[#out+1] = "[PLAYER]"
    elseif ty == "rival" then out[#out+1] = "[RIVAL]"
    elseif ty == "strvar" then out[#out+1] = "[STR_VAR_" .. tostring(c.n) .. "]"
    elseif ty == "bph" then out[#out+1] = "[" .. (B_TXT[c.code] or ("B_"..tostring(c.code))) .. "]"
    elseif ty == "tag" then
      local inner = tostring(c.tag or ""):gsub("^{", ""):gsub("}$", "")
      out[#out+1] = "[" .. inner .. "]"
    elseif ty == "eos" then -- nada
    elseif ty == "ph" then out[#out+1] = "[" .. tostring(c.name or c.code or "PH") .. "]"
    else out[#out+1] = "{" .. tostring(ty) .. "}" end
  end
  return table.concat(out)
end

local keys = {}
for k in pairs(t) do keys[#keys+1] = k end
table.sort(keys)
for _, k in ipairs(keys) do
  local v = t[k]
  if type(v) == "table" then
    local complex = 0
    for _, c in ipairs(v) do if not SIMPLE[c.t] then complex = 1; break end end
    io.write(k, "\t", tostring(complex), "\t", rebuild(v), "\n")
  end
end
