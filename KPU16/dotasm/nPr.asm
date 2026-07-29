
#ts is to demonstrate that actually there is no multi handling of macros yet

$fact1(num,out){
    ldi {out} 1
    ldi r4 1
    ldi r2 1

.loop1
    cmp {num} r4
    jc n .end1

    mult {out} {out} r4
    add r4 r4 r2
    jump .loop1

.end1
}
$fact2(num,out){
    ldi {out} 1
    ldi r4 1
    ldi r2 1

.loop2
    cmp {num} r4
    jc n .end2

    mult {out} {out} r4
    add r4 r4 r2
    jump .loop2

.end2
}
read r5          
read r6          
fact1(r5,r7)    
sub r8 r5 r6     
fact2(r8,r9)
div r10 r7 r9
display r10
halt