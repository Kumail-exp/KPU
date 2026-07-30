$intro(n){

    ldi {n} 't'
    print {n}

    ldi {n} 'h'
    print {n}
    
    ldi {n} 'i'
    print {n}
    
    ldi {n} 'n'
    print {n}
    
    ldi {n} 'k'
    print {n}

    ldi {n} 32
    print {n}
    
    ldi {n} 'a'
    print {n}
    
    ldi {n} 32
    print {n}
    
    ldi {n} 'n'
    print {n}

    ldi {n} 'u'
    print {n}
    
    ldi {n} 'm'
    print {n}
    
    ldi {n} 'b'
    print {n}
    
    ldi {n} 'e'
    print {n}

    ldi {n} 'r'
    println {n}

    ldi {n} '1'
    print {n}
    
    ldi {n} '-'
    print {n}

    ldi {n} 'r'
    print {n}
    
    ldi {n} 'i'
    print {n}
    
    ldi {n} 'g'
    print {n}
    
    ldi {n} 'h'
    print {n}

    ldi {n} 't'
    println {n}
    
    ldi {n} '2'
    print {n}
    
    ldi {n} '-'
    print {n}
    
    ldi {n} 'l'
    print {n}

    ldi {n} 'o'
    print {n}
    
    ldi {n} 'w'
    print {n}
    
    ldi {n} 'e'
    print {n}
    
    ldi {n} 'r'
    println {n}

    ldi {n} '3'
    print {n}
    
    ldi {n} '-'
    print {n}
    
    ldi {n} 'h'
    print {n}
    
    ldi {n} 'i'
    print {n}

    ldi {n} 'g'
    print {n}
    
    ldi {n} 'h'
    print {n}
    
    ldi {n} 'e'
    print {n}
    
    ldi {n} 'r'
    println {n}

    ldi {n} 32
    println {n}
}
$guessed(n){
    ldi {n} 'G'
    print {n}
    ldi {n} 'u'
    print {n}
    ldi {n} 'e'
    print {n}
    ldi {n} 's'
    print {n}
    ldi {n} 's'
    print {n}
    ldi {n} '-'
    print {n}
    ldi {n} '>'
    print {n}
}
$win(n){
    ldi {n} 'I'
    print {n}
    ldi {n} 32
    print {n}
    ldi {n} 'W'
    print {n}
    ldi {n} 'I'
    print {n}
    ldi {n} 'N'
    print {n}
    ldi {n} '!'
    println {n}
}


ldi r1 0
ldi r2 100
intro(r0)
.loop
    add r3 r1 r2
    ldi r0 2
    div r3 r3 r0
    guessed(r0)
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
.done
    win(r0)
    halt
.low
    mov r2 r3
    jump .loop