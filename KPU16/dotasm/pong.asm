&height=31
&width=31
# paddle
ldi r1 16
ldi r2 3 #length of the paddle


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
$event_handle(){
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
ldi r3 1

ldi r4 &height
sub r4 r4 r3
ldi r5 255
ldi r7 25
.loop
    gettime r0
    mod r0 r0 r7
    jc z .update
    jump .loop
    .update
    event_handle()

    drawpaddle(r6,r5)
    
    dispflip
    jump .loop