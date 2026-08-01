println 'Enter a number to find the absolute value of:'
read r1
cmp r1 r2
jc n .neg
display r1
halt
.neg
    sub r1 r3 r1
    print 'absolute value:'
    display r1
    halt