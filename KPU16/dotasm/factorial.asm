println 'Enter a number to find the factorial of:'
read r1
ldi r2 1
ldi r3 1
ldi r4 1

.loop
    cmp r1 r4
    jc n .end
    mult r3 r3 r4
    add r4 r4 r2
    jump .loop

.end
    print 'factorial: '
    display r3
    halt