;Factorial calculation program in DLX assembly


   .data

n   1   5
f   1   1
;Start f at 1 for if we get n = 0

    .text

    ;Check if less than 0?

    ;Check if zero, go to exit
    BEQZ n exit
    ;If not zero, it continues
;Make some vars to use
    ADDI R1, R0, 1 ;R1 = 1? //i
    ;R2 is set in the loop, its j
    ADDI R3, R0, 1 ;R3 = 1? //prevresult
    ;R4 is used for jump condition
n_loop
;Loop for amount of n
    ;If i isn't <= n then branch down past This
    SLEUI R4, R1, n ; (i <= n)
    BEQZ R4 end_n_loop ;If !(i<=n) leave loop
    ;Else, continue loop
    ADDI R3, f, 0 ;R3 = f

    JAL j_loop ;Multiply prevresult by i

    ;Ending of main loop
    ADDI R1, R1, 1 ;i++
    ;back to beggining
    J n_loop
end_n_loop

exit

;All of this is multiply func
start_j
    ADDI R2, R0, 1 ;R2 = 1? //j = 1
j_loop
    ;Multiply prevresult(R3) by i(R1)
    ;By looping for (int j = 1; j < i; j++) adding R3 to f

    ;If j = i, branch
    SGEU R4, R2, R1 ;(j >= i)
    BNEZ R4, R31 ;Ending loop if condition
    ADD f, f, R3 ;result += prevresult
    ADDI R2, R2, 1 ;j++
    J j_loop
end_j_loop