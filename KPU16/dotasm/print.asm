ldi r1 0
ldi r2 1
ldi r3 127
.loop
    println r1
    add r1 r1 r2
    cmp r1 r3 
    jc z .end
    jump .loop
.end
    halt