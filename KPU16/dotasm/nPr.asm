
$fact(num,out){
        ldi {out} 1
        ldi r4 1
        ldi r2 1

    .loop
        cmp {num} r4
        jc n .end

        mult {out} {out} r4
        add r4 r4 r2
        jump .loop

    .end
}
read r5          
read r6          
fact(r5,r7)    
sub r8 r5 r6     
fact(r8,r9)
div r10 r7 r9
display r10
halt