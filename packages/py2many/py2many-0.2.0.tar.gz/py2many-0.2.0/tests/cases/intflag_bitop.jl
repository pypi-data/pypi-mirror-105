using SuperEnum

@se Permissions begin
    R = 1
    W = 2
    X = 16

end

a = (Permissions.R | Permissions.W)
function main()
    if (a & Permissions.R)
        println(join(["R"], " "))
    end
end
