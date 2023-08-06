a = Dict(1 => 1, 2 => 2, 3 => 3)
a[2].drop()
a[2] = 2
@assert(list(a.keys()) == [1, 3, 2])
