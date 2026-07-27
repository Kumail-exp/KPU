read r1 #base
read r2 #number
ldi r3 0 # log
ldi r4 1
.loop
    div r2 r2 r1
    add r3 r3 r4
    cmp r4 r2
    jc z .end
    jump .loop
.end
    display r3
    halt