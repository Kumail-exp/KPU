ldi r1 0      
ldi r2 0      

.loop
    mousex r3
    mousey r4

    cmp r3 r1
    jc z .check_y

.changed
    mov r1 r3
    mov r2 r4
    display r3
    display r4
    ldi r5 10
    print r5
    jump .loop

.check_y
    cmp r4 r2
    jc z .loop

    jump .changed