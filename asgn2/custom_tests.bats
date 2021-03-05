load harness

@test "custom-1" {
  check 'x := 1 ; y := 2 ; z := x' '{x → 1, y → 2, z → 1}'
}

@test "custom-2" {
  check 'if true then x := 10 else y := 10' '{x → 10}'
}

@test "custom-3" {
  check 'if true then if true then a := 1 else b := 2 else x := 0' '{a → 1}'
}

@test "custom-4" {
  check 'while x < 10 do x := x + 1' '{x → 10}'
}

@test "custom-5" {
  check 'if ( true ∨ true ) then x := z + y else x := 10 ; skip ; skip ; z := 10' '{x → 0}'
}
