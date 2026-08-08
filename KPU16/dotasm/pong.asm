&height=31
&width=31
# paddle
ldi r1 16
ldi r2 3 #length of the paddle
#ball
ldi r8 10 #x
ldi r9 16 #y
ldi r10 1 #vx
ldi r11 -1 #vy
$drawpaddle(i,colour){
    ldi {i} 0
    .loop
        add r30 r1 {i}
        setpixel r30 r4 {colour}
        add {i} {i} r3
        cmp {i} r2
        jc z .end
        jump .loop

    .end
}
$drawball(colour){
    setpixel r8 r9 {colour}

    ldi r0 0
    load r30 r0
    
    ldi r0 1
    load r31 r0
    
    ldi r0 0
    setpixel r30 r31 r0
}
$event_handle(){
    ldi r0 0
    ldi r30 0
    key r30 KEY_LEFT
    add r30 r30 r0
    jc z .upkey
    sub r1 r1 r3
    #erasing the extra
    add r30 r1 r2
    ldi r0 0
    setpixel r30 r4 r0
    .upkey
    ldi r30 0
    key r30 KEY_RIGHT
    add r30 r30 r0
    jc z .end
    add r1 r1 r3
    #erasing the extra
    # idk why it requires two erasing but thats okayy
    sub r30 r1 r2
    add r30 r30 r3
    ldi r0 0
    setpixel r30 r4 r0
    add r30 r30 r3
    setpixel r30 r4 r0
    .end
}
$ball_move(){
    ldi r0 0
    store r0 r8
    ldi r0 1
    store r0 r9

    add r8 r8 r10
    add r9 r9 r11


}
$handle_collisions(){
    # calculate next Y
    add r30 r9 r11
    # calculate next X
    add r31 r8 r10
    # check for paddle
    getpixel r15 r31 r30
    cmp r15 r5
    jc z .pedalhit
    ldi r0 -1
    cmp r30 r0
    jc z .reversey


    ldi r0 -1
    cmp r31 r0
    jc z .reversex

    ldi r0 &width
    add r0 r0 r3
    cmp r31 r0
    jc z .reversex

    jump .done

    .reversey
        mult r11 r11 r13
        jump .done
    .pedalhit
        mult r11 r11 r13
        # incrementing score
        add r14 r14 r3
        jump .done
    .reversex
        mult r10 r10 r13

    .done
}
ldi r3 1

ldi r4 &height
sub r4 r4 r3
ldi r5 255
ldi r7 25
ldi r12 100
ldi r13 -1
ldi r14 0
.loop
    ldi r0 3
    store r0 r14

    gettime r0
    mod r0 r0 r7
    jc z .update
    jump .loop

    .update
    gettime r0
    mod r0 r0 r12
    jc z .ballupdate
    .backfromball
    event_handle()
    drawpaddle(r6,r5)
    handle_collisions()
    drawball(r5)
    dispflip
    ldi r0 3
    load r0 r0
    cmp r0 r14
    jc z .loop
    display r14
    jump .loop

.ballupdate
    ball_move()
    # cheking for fall
    ldi r0 &height
    cmp r0 r9
    jc n .end
    jump .backfromball

.end
    halt