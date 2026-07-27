read r1
cmp r1 r2
jc n .neg
display r1
halt
.neg
    sub r1 r0 r1
    display r1
    halt