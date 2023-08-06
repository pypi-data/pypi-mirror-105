a = ("a")
b = Dict(a => "a")
@assert("a" == b[a])
