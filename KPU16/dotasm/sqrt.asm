print 'enter a number to square root:'
read r1
ldi r2 0
ldi r3 1

.loop
    add r2 r2 r3
    mult r5 r2 r2
    cmp r1 r5
    jc n .end
    jump .loop

.end
    sub r2 r2 r3
    display r2
    halt