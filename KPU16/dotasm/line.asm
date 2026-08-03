
print 'enter slope of line'
read r10  # m
print 'enter y intercept of line'
read r11   # c

ldi r1 0          
ldi r4 1          
ldi r5 32        
ldi r6 31         
ldi r7 255       
ldi r8 0          

.loop
    # y = mx + c
    mult r2 r1 r10
    add  r2 r2 r11

    sub  r2 r6 r2
    cmp r2 r8
    jc n .next

    cmp r2 r5
    jc n .draw
    jump .next

.draw
    setpixel r1 r2 r7
    dispflip

.next
    add r1 r1 r4

    cmp r1 r5
    jc n .loop

# a while loop to keep display awake
.disp
    jump .disp
