function show()
let try_dummy = { //unsupported
raise!(Exception("foo")) # unsupported
}
let except!(Exception) = { //unsupported
println(join(["caught"], " "));
}
let try_dummy = { //unsupported
(3/0);
}
let except!(ZeroDivisionError) = { //unsupported
println(join(["OK"], " "));
}
let try_dummy = { //unsupported
raise!(Exception("foo")) # unsupported
}
let except!() = { //unsupported
println(join(["Got it"], " "));
}
end

function main()
show();
end

main()
