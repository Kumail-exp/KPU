ldi r10 1     
ldi r9 0       # left mouse button
ldi r5 43
ldi r6 24

.loop
    mbutton r8 r9
    cmp r8 r10
    jc n .loop

    mousex r1
    mousey r2

    div r1 r1 r5
    div r2 r2 r6

    ldi r3 255
    setpixel r1 r2 r3

    dispflip
    jump .loop