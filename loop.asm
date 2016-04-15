cpy r10 1048576

:loop
inc r5
jmp r10 r5 outloop
jmp r22 r23 loop

:outloop
hlt r5