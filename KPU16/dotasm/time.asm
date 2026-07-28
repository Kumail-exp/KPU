ldi r4 1000
gettime r2
ldi r5 0
ldi r6 1
.loop
    gettime r1
    sub r3 r1 r2
    cmp r4 r3
    jc c .loop
    add r5 r5 r6
    display r5
    mov r2 r1 
    jump .loop