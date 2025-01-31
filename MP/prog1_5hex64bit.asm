section .data
    msg1 db 10,13,"enter 5 64 bit numbers"
    len1 equ $-msg1
    msg2 db 10,13,"entered 5 64 bit numbers"
    len2 equ $-msg2

section .bss
    array resd 200
    counter resd 1

section .text
    global _start

_start:
    mov rax,1
    mov rdi,1
    mov rsi,msg1
    mov rdx,len1
    syscall

accept:
    mov byte [counter], 05
    mov rbx, 00

loop1:
    mov rax, 0 ; 0 for read
    mov rdi, 0 ; 0 for keyboard
    mov rsi, array ; move pointer to start of array
    add rsi, rbx
    mov rdx, 17
    syscall
    add rbx, 17 ; to move counter
    dec byte [counter]
    jnz loop1

    mov rax, 1
    mov rdi, 1
    mov rsi, msg2
    mov rdx, len2
    syscall

    mov byte [counter], 05
    mov rbx, 00

loop2:
    mov rax, 1 ; 1 for write
    mov rdi, 1 ; 1 for monitor
    mov rsi, array
    add rsi, rbx
    mov rdx, 17
    syscall
    add rbx, 17
    dec byte [counter]
    jnz loop2

exit:
    syscall
    mov rax, 60
    mov rdi, 0
    syscall
