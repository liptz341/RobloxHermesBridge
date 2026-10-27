-- Place this script in a Roblox Studio Plugin or run it via Command Bar / Server Script (with HttpService enabled)
-- Hermes Roblox Bridge Client v1.0

local HttpService = game:GetService("HttpService")
local ServerURL = "http://localhost:5000"

print("[Hermes Plugin] Bridge connected. Polling for commands from Hermes...")

task.spawn(function()
    while true do
        pcall(function()
            local response = HttpService:GetAsync(ServerURL .. "/poll")
            local data = HttpService:JSONDecode(response)
            
            if data and data.action and data.action ~= "none" then
                print("[Hermes] Received action:", data.action)
                local success, result = pcall(function()
                    if data.action == "print" then
                        print(data.message)
                        return "Printed: " .. tostring(data.message)
                    elseif data.action == "create_part" then
                        local part = Instance.new("Part")
                        part.Name = data.name or "HermesPart"
                        part.Size = Vector3.new(data.sizeX or 4, data.sizeY or 1, data.sizeZ or 2)
                        part.Position = Vector3.new(data.posX or 0, data.posY or 5, data.posZ or 0)
                        part.BrickColor = BrickColor.new(data.color or "Bright red")
                        part.Anchored = true
                        part.Parent = workspace
                        return "Created part: " + part.Name
                    elseif data.action == "run_code" then
                        local fn, err = loadstring(data.code)
                        if fn then
                            return tostring(fn())
                        else
                            return "Compile Error: " .. tostring(err)
                        end
                    end
                    return "Unknown action"
                end)
                
                -- Send result back
                local resultData = HttpService:JSONEncode({
                    action = data.action,
                    success = success,
                    result = tostring(result)
                })
                HttpService:PostAsync(ServerURL .. "/result", resultData)
            end
        end)
        task.wait(1) -- poll every 1 second
    end
end)
