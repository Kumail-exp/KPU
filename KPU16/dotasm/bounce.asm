ldi r1 1          # dx
ldi r2 1          # dy

ldi r5 0          # min
ldi r6 31         # max


#making it random
gettime r3
mod r3 r3 r6          # x
add r4 r3 r3            # y
mod r4 r4 r6

ldi r7 255        # white
ldi r8 -1         # -1
ldi r9 0          # black
ldi r10 100       # delay
.loop
    gettime r11
    mod r11 r11 r10
    jc z .work
    jump .loop

.work
    setpixel r3 r4 r9

    add r3 r3 r1
    add r4 r4 r2

    cmp r5 r3
    jc z .flipx
    cmp r6 r3
    jc z .flipx

.xdone

    cmp r5 r4
    jc z .flipy
    cmp r6 r4
    jc z .flipy

.ydone

    setpixel r3 r4 r7
    dispflip
    jump .loop

.flipx
    mult r1 r1 r8
    jump .xdone

.flipy
    mult r2 r2 r8
    jump .ydone