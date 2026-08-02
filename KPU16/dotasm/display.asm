ldi r5 32     
ldi r4 1        
ldi r7 4 # every four boxes flip it
ldi r8 0 # frame count
ldi r1 0       
ldi r2 0        

.loop
    add r8 r8 r4
    ldi r3 255
    setpixel r1 r2 r3

    add r1 r1 r4

    cmp r1 r5
    jc n .cont

    ldi r1 0
    add r2 r2 r4

.cont
    mod r10 r8 r7
    jc z .flip
    jump .loop
.flip
    dispflip
    jump .loop