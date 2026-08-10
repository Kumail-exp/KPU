&width=31
&height=31
&frame_time=30

# player
ldi r1 16
ldi r2 &width

# obstacle reserved
ldi r3 0
ldi r4 0

# frame time
ldi r5 &frame_time

# RNG seed
ldi r6 12345
ldi r8 1 
ldi r9 0


$update_obstacle(x_loc,y_loc,offset){
    load r3 {x_loc}
    load r4 {y_loc}

    getpixel r30 r3 r4
    ldi r0 255
    cmp r0 r30
    jc z .halt
    # set previous pixel to black
    ldi r0 0
    setpixel r3 r4 r0

    # move down
    ldi r0 1
    add r4 r0 r4
    # check again
    getpixel r30 r3 r4
    ldi r0 255
    cmp r0 r30
    jc z .halt
    # draw obstacle
    ldi r0 100
    setpixel r3 r4 r0
    
    
    ldi r0 &height
    ldi r30 1
    add r0 r0 r30
    cmp r4 r0
    jc z .done

    jump .end

.done
    # RNG
    gettime r0
    ldi r30 37
    mult r0 r0 r30
    ldi r30 12345
    add r0 r0 r30
    xor r0 r0 r6
    mov r6 r0
    ldi r3 &width
    mod r3 r0 r3
    # reset Y
    mov r4 {offset}
    jump .end

    .halt
        halt
.end
    store {x_loc} r3
    store {y_loc} r4
}
$update_player(){
    ldi r0 0
    setpixel r1 r2 r0

    key r30 KEY_RIGHT
    add r1 r1 r30
    key r30 KEY_LEFT
    sub r1 r1 r30

    ldi r0 -1
    cmp r1 r0
    jc z .negate
    jump .nocap
    .negate
        ldi r1 0
    .nocap
    ldi r0 &width
    min r1 r1 r0

    ldi r0 255
    setpixel r1 r2 r0
}

.loop
gettime r0
mod r0 r0 r5
jc z .update
jump .loop

.update
    ldi r0 1
    add r8 r8 r0    #frame count
    ldi r0 320
    mod r0 r8 r0
    jc z .diff
    .backfromdiff
    ldi r0 50
    mod r0 r8 r0
    jc z .score
    .backfromscore
    update_player()

    # obstacle 1
    ldi r10 0
    ldi r11 1
    ldi r7 -1
    update_obstacle(r10,r11,r7)
    
    # obstacle 2
    ldi r10 2
    ldi r11 3
    ldi r7 -11
    update_obstacle(r10,r11,r7)

    # obstacle 3
    ldi r10 4
    ldi r11 5
    ldi r7 -21
    update_obstacle(r10,r11,r7)


    dispflip
    jump .loop
.diff
    ldi r0 1
    sub r5 r5 r0
    jump .backfromdiff
.score
    ldi r0 1
    add r9 r9 r0
    print 'score: '
    display r9
    jump .backfromscore