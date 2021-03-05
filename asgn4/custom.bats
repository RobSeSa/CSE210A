load harness

@test "custom-1" {
  check 'y := 1' '⇒ skip, {y → 1}'
}

@test "custom-2" {
  check 'skip ; y := 1' '⇒ y := 1, {}
⇒ skip, {y → 1}'
}

@test "custom-3" {
  check 'a := 1; b := 2 ; c := a ; a := b' '⇒ skip; b := 2; c := a; a := b, {a → 1}
⇒ b := 2; c := a; a := b, {a → 1}
⇒ skip; c := a; a := b, {a → 1, b → 2}
⇒ c := a; a := b, {a → 1, b → 2}
⇒ skip; a := b, {a → 1, b → 2, c → 1}
⇒ a := b, {a → 1, b → 2, c → 1}
⇒ skip, {a → 2, b → 2, c → 1}'
}

@test "custom-4" {
  check 'if false then y := 1 else y := 0' '⇒ y := 0, {}
⇒ skip, {y → 0}'
}

@test "custom-5" {
  check 'while x < 2 do x := x + 1' '⇒ x := (x+1); while (x<2) do { x := (x+1) }, {}
⇒ skip; while (x<2) do { x := (x+1) }, {x → 1}
⇒ while (x<2) do { x := (x+1) }, {x → 1}
⇒ x := (x+1); while (x<2) do { x := (x+1) }, {x → 1}
⇒ skip; while (x<2) do { x := (x+1) }, {x → 2}
⇒ while (x<2) do { x := (x+1) }, {x → 2}
⇒ skip, {x → 2}'
}

