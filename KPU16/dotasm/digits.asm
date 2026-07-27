read r1
ldi r2 10
ldi r4 0
ldi r5 1

.loop
    cmp r1 r0
    jc z .prep
    mod r3 r1 r2
    store r4 r3
    add r4 r4 r5
    div r1 r1 r2
    jump .loop

.prep
    sub r4 r4 r5
    jump .disp

.disp
    load r6 r4
    display r6
    sub r4 r4 r5
    jc n .end
    jump .disp

.end
    halt