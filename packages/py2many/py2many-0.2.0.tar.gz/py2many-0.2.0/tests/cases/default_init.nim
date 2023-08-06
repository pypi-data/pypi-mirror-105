import tables
type
    Rectangle = object
        height: ST0
        length: ST1
proc __init__(self: Rectangle, height: T, length: T) =
    self.height = height
    self.length = length


proc main() =
    let r = Rectangle()

