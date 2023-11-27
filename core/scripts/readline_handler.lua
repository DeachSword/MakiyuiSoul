--[[======================================
||	filename:       readline_handler
||	owner:          WEDeach
||	description:    readline script
||	version:    	1.0.2
=======================================]]


_G.VarState = {
	ins = nil,
	state = true,
}

-- 解析指令函数
function ParseCommand(command_str)
	local args = {}
	local i = 1

	-- 分割
	local parts = {}
	for part in string.gmatch(command_str, "%S+") do
		table.insert(parts, part)
	end

	-- 主名稱
	args.name = parts[i]
	i = i + 1

	-- 其餘參數
	args.params = {}
	while i <= #parts and string.sub(parts[i], 1, 1) ~= "-" do
		table.insert(args.params, parts[i])
		i = i + 1
	end

	-- 可選參數
	args.options = {}
	while i <= #parts do
		local arg = parts[i]

		if string.sub(arg, 1, 1) == "-" then
			local option = string.sub(arg, 2)

			if i + 1 <= #parts and string.sub(parts[i + 1], 1, 1) ~= "-" then
				-- 有值取值
				local val = parts[i + 1]

				if val == "bT" then
					args.options[option] = true
				elseif val == "bF" then
					args.options[option] = false
				else
					args.options[option] = val
				end
				i = i + 2
			else
				-- 無值以 bool 處理
				args.options[option] = true
				i = i + 1
			end
		else
			break
		end
	end

	return args
end

-- 處理指令
function OnCmd(command_line)
	local parser = ParseCommand(command_line)
	local cmd = parser.name
	local CM = _cmd_hoshizora.Matataku(cmd).Teraseru
	if cmd == "ping" then
		CM("pong")
	elseif cmd == "exit" then
		_G.VarState.state = false
	elseif cmd == "info" then
		local players = {}
		for item in python.iter(self.playerMgr.players) do
			table.insert(
				players, item.player.nickname
			)
		end
		CM("Online(" .. #players .. "): " .. table.concat(players, ', '))
	elseif cmd == "rel" then
		CM("Reload scripts...")
		ScriptMgr.loadScripts()
		_G.VarState.ins = ScriptMgr.getScriptInstance("readline_handler")
	elseif cmd == "exec" then
		pexec(table.concat(parser.params, ' '))
	elseif cmd == "activity" then
		OnActivity(parser)
	else
		if cmd and not cmd:match("^%s*$") then
			cmd_hoshizora("Invalid command: " .. cmd)
		end
	end
end

-- Activity指令
function OnActivity(parser)
	local CM = _cmd_hoshizora.Matataku("Activity").Teraseru
	if #parser.params >= 1 then
		local action = parser.params[1]
		local activity_id = nil
		if #parser.params >= 2 then
			activity_id = tonumber(parser.params[2])
		end

		if action == "add" then
			if activity_id ~= nil then
				local insert = true
				local start_time = 0
				local end_time = 1999999999
				local activity_ids = {}
				if parser.options['insert'] ~= nil then
					insert = parser.options['insert']
				end
				if parser.options['start'] ~= nil then
					start_time = parser.options['insert']
				end
				if parser.options['end'] ~= nil then
					end_time = parser.options['insert']
				end
				if #parser.params >= 2 then
					-- 支持多個
					for i = 2, #parser.params do
						activity_id = tonumber(parser.params[i])
						if activity_id ~= nil then
							table.insert(activity_ids, activity_id)
						end
					end
				end

				for _, value in ipairs(activity_ids) do
					local activity = self.activityMgr.getActivity(value)
					if activity ~= nil then
						CM("Activity [green]" .. value .. "[/] already exists")
					else
						activity = self.activityMgr.newActivity(activity_id, start_time, end_time)
						if insert then
							activity.save()
						end
						self.playerMgr.NotifyActivityChange(python.args { new_activities = { activity } })
						CM("Activity [green]" .. value .. "[/] has been added successfully!")
					end
				end
			else
				CM("[red]activity_id is nil[/]")
			end
		elseif action == "list" then
			local activeOnly = true
			if parser.options['active'] ~= nil then
				activeOnly = parser.options['active']
			end
			local activitys = self.activityMgr.fetchActivityList(python.args { activeOnly = activeOnly })
			local table_data = {
				head = { "#", "activity_id", "start_time", "end_time", "is_active" },
				rows = {}
			}
			for item in python.iter(activitys) do
				table.insert(
					table_data.rows, { item._id, item.activity_id, item.start_time, item.end_time, item.is_active }
				)
			end
			CM(python.args { 123, table = table_data, debug = true, fff = 12 })
		elseif action == "remove" then
			if activity_id ~= nil then
				local activity_ids = {}
				if #parser.params >= 2 then
					-- 支持多個
					for i = 2, #parser.params do
						activity_id = tonumber(parser.params[i])
						if activity_id ~= nil then
							table.insert(activity_ids, activity_id)
						end
					end
				end
				local delete = true
				if parser.options['delete'] ~= nil then
					delete = parser.options['delete']
				end
				for _, value in ipairs(activity_ids) do
					local activity = self.activityMgr.getActivity(value)
					if activity ~= nil then
						CM("Remove activity [green]" .. value .. "[/]...")
						self.playerMgr.NotifyActivityChange(python.args { end_activities = { value } })
						if delete then
							self.activityMgr.removeActivity(value)
						end
					else
						CM("Activity [green]" .. value .. "[/] does not exist!")
					end
				end
			else
				CM("[red]activity_id is nil[/]")
			end
		else
			CM("[red]Invalid parameter: " .. action .. "[/]")
		end
	else
		cmd_hoshizora(
			"Usage: activity <add|list|remove> <activity_id> [start_time] [end_time]"
		)
	end
end
