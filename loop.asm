cpy r10 4096
cpy r16 10

:loop
inc r5
jmp r10 r5 outloop
jmp r22 r23 loop

:outloop
outn r5
outb r16 1
hlt r5