read r1
ldi r2 2
ldi r3 1
.loop
    ldi r5 1
    cmp r1 r5
    jc n .end
    cmp r1 r2
    jc n .end
    mod r0 r1 r2
    jc z .factor
    jump .nofactor
    .factor
        display r2
        div r1 r1 r2
        jump .loop
    .nofactor
        add r2 r2 r3
        jump .loop
.end
    halt