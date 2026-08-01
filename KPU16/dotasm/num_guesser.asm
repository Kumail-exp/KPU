.start
ldi r1 0
ldi r2 100
println 'enter a number between 1 to 100.'
println '1-if guessed corectly'
println '2-if smaller'
println '3-if bigger'
.loop
    cmp r1 r2
    jc z .cheat
    add r3 r1 r2
    ldi r0 2
    div r3 r3 r0
    print 'computer guessed:'
    display r3
    read r4
    ldi r0 1
    cmp r0 r4
    jc z .done
    ldi r0 2
    cmp r0 r4
    jc z .low
    mov r1 r3
    jump .loop
.cheat
    println 'the number is out of limit or you are telling me wrong instructions,cheater'
    jump .start
.done
    println 'yay i guessed correctly the number is '
    display r3
    halt
.low
    mov r2 r3
    jump .loop