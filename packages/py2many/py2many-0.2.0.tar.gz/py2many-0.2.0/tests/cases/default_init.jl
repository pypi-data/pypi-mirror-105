struct Rectangle
    height::ST0
    length::ST1
end

function __init__{T0,T1}(self::Rectangle, height::T0, length::T1)
    self.height = height
    self.length = length
end

function main()
    r = Rectangle()
end
