ldi r3 1
ldi r5 0
.loop
    mov r5 r2
    key r2 KEY_UP
    cmp r2 r3
    jc z .pressed
    jump .loop

.pressed
    cmp r5 r2
    jc z .loop
    println 'up'
    jump .loop