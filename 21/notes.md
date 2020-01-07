# Notes

## Part 1

    .................
    .................
    .@...,...........
    #####.###########
      ABCD

- If there is a hole directly in front of me, I have to jump. Otherwise,
  if there will be a hole in front of me and I can safely land, jump.

- A == False is hole directly in front, so I must jump (i.e. Not(A))
- A jump takes 4 spaces, so D must be True where we land
- If there's a hole in B or C (Or(Not(B), Not(C))) and D is ground (D)

- Logically:

      !A || ((!B || !C) && D)

- To convert this into Springcode, we need to take small pieces, store them in
  `T`, and then go from there:

      NOT B T
      NOT C J
      OR J T
      AND D T
      NOT A J
      OR T J

- It works!

## Part 2

    .................
    .................
    .@...,...........
    #####.###########
      ABCDEFGHI

- Same constraints as Part 1, but now we have additional information up to I
  away
- If we jump at @, D must be True
- If we jump at A (B is False), E must be True -- B == !E 
- If we jump at B (C is False), F must be True -- C == !F 
- If we jump at C (D is False), G must be True -- D == !G
- If we jump at D (E is False), H must be True -- E == !H 
- If we jump at E (F is False), I must be True -- F == !I  

- Logically:

      !A || ((!B || !C) && D && (E || H))
             (-T-)
                  (-J-)
             (----T---)
             (------T------)   
                                (J)
                                (---J---)
            (-------------J-------------)
      (-T-)

      NOT B T
      NOT C J
      OR J T
      AND D T
      NOT E J
      NOT J J
      OR H J
      AND T J
      NOT A T
      OR T J

