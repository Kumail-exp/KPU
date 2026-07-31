#rock-1
# paper-2
#scissor-3


ldi r6 0
.loop
    read r1
    gettime r2
    ldi r0 3
    mod r2 r2 r0
    ldi r10 1
    add r2 r2 r10
    display r2
    #draw 
    cmp r1 r2
    jc z .draw
    
    #player win
    sub r3 r1 r2
    ldi r0 1
    cmp r3 r0
    jc z .player
    ldi r0 2
    sub r0 r6 r0
    cmp r3 r0
    jc z .player

    #bot win
    sub r3 r1 r2
    ldi r0 1
    sub r0 r6 r0
    cmp r3 r0
    jc z .bot
    ldi r0 2
    cmp r3 r0
    jc z .bot

.draw
    ldi r0 'd'
    println r0
    halt


.player
    ldi r0 'p'
    println r0
    halt

.bot
    ldi r0 'b'
    println r0
    halt