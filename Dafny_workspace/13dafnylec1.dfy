method double(x:int) return (y:int)
requires x >= 2
ensures y >= x + 2
//ensures y == x + x // more precise spec
{
    y := x + x;
}

method CallDouble()
{
    var z:int;
    z := double(7); // dafny only knows the ensure line => z >= 7 + 2
    assert z == 14;
}