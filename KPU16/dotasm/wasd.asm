ldi r1 16
ldi r2 16

ldi r3 1
ldi r4 0
ldi r6 255
ldi r7 100


setpixel r1 r2 r6
.loop
    
    gettime r8
    mod r8 r8 r7
    jc z .work
    jump .loop
    .work

    mov r9 r1
    mov r10 r2
    
    key  r5 'w'
    cmp r5 r4
    jc z .continuew
    sub r2 r2 r3
    .continuew

    key  r5 's'
    cmp r5 r4
    jc z .continues
    add r2 r2 r3
    .continues

    key  r5 'a'
    cmp r5 r4
    jc z .continuea
    sub r1 r1 r3
    .continuea

    key  r5 'd'
    cmp r5 r4
    jc z .continued
    add r1 r1 r3
    .continued


    setpixel r1 r2 r6
    cmp r1 r9
    jc z .checky
    cmp r2 r10
    jc z .checkx


    jump .flip
.checky
    cmp r2 r10
    jc z .flip
    jump .reset
    jump .flip
.checkx
    cmp r1 r9
    jc z .flip
    jump .reset
    jump .flip
.flip
    dispflip
    jump .loop
.reset
    setpixel r9 r10 r4
    jump .flip
