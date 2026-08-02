#rock-1
# paper-2
#scissor-3


ldi r6 0
.main
    println 'enter number of choice:'
    println '1- rock'
    println '2- paper'
    println '3- scissor'
    
    read r1
    gettime r2
    ldi r20 3
    mod r2 r2 r20
    ldi r10 1
    add r2 r2 r10
    print 'bot chose:'
    display r2
    #draw 
    cmp r1 r2
    jc z .draw
    
    #player win
    sub r3 r1 r2
    ldi r20 1
    cmp r3 r20
    jc z .player
    ldi r20 2
    sub r20 r6 r20
    cmp r3 r20
    jc z .player

    #bot win
    sub r3 r1 r2
    ldi r20 1
    sub r20 r6 r20
    cmp r3 r20
    jc z .bot
    ldi r20 2
    cmp r3 r20
    jc z .bot

.draw
    println 'its a draw'
    halt


.player
    println 'player won'
    halt

.bot
    println 'bot won'
    halt