println 'enter base:'
read r1
println 'enter power:'
read r2
ldi r3 1
ldi r4 1
.loop
    mult r3 r3 r1
    sub r2 r2 r4
    jc z .end
    jump .loop
.end
    print 'exponent'
    display r3
    halt