0x1000:	jg	0x1047
0x1002:	add	dword ptr [rcx], r8d
0x1006:	add	dword ptr [rax], eax
0x1008:	add	byte ptr [rax], al
0x100a:	add	byte ptr [rax], al
0x100c:	add	byte ptr [rax], al
0x100e:	add	byte ptr [rax], al
0x1010:	add	al, byte ptr [rax]
0x1012:	sub	byte ptr [rax], al
0x1014:	add	dword ptr [rax], eax
0x1016:	add	byte ptr [rax], al
0x1018:	int3	
0x1019:	add	eax, dword ptr [rcx]
0x101b:	add	byte ptr [rax + rax], dh
0x101e:	add	byte ptr [rax], al
0x1020:	movabs	al, byte ptr [0x340500040000001b]
0x1029:	add	byte ptr [rax], ah
0x102b:	add	byte ptr [rcx], cl
0x102d:	add	byte ptr [rax], ch
0x102f:	add	byte ptr [rsi], bl
0x1031:	add	byte ptr [rip + 0x100], bl
0x1037:	jo	0xfe9
