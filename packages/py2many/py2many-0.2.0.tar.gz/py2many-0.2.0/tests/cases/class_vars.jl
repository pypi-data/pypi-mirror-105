struct A
    B::ST0
end

B = "FOO"
function main()
    @assert(A::B == "FOO")
end
