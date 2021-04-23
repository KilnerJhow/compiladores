define i32 @square(i32 %0) {
	%x = alloca i32, align 4
	store i32 %0, i32* %x, align 4
	%1 = load i32, i32* %x, align 4
	%2 = mul i32 %1, %1
	ret i32 %2
	
}

define void @splash(i32 %0) {
	%k = alloca i32, align 4
	store i32 %0, i32* %k, align 4
	ret void
	
}

define float @ResDiv(float %0, float %1) {
	%k1 = alloca float, align 4
	store float %0, float* %k1, align 4
	%k2 = alloca float, align 4
	store float %1, float* %k2, align 4
	
	%k3 = alloca float, align 4
	%2 = load float, float* %k1, align 4
	%3 = load float, float* %k2, align 4
	%4 = fadd float %2, %3
	%5 = load float, float* %k1, align 4
	%6 = load float, float* %4, align 4
	%7 = fdiv float %5, %6
	ret float %k3
	
}

define i32 @main() {
	%a = alloca i32, align 4
	store i32 8, i32* %a, align 4
	%b = alloca i32, align 4
	store i32 2, i32* %b, align 4
	call void @splash (i32 8)
	%k1 = alloca float, align 4
	store float 0x4079000000000000, float* %k1, align 4
	%k2 = alloca float, align 4
	store float 0x4072c00000000000, float* %k2, align 4
	%k = alloca float, align 4
	%1 = call float @ResDiv (float 0x4079000000000000, float 0x4072c00000000000)
	%c = alloca i32, align 4
	store i32 4, i32* %c, align 4
	call i32 @square (i32 2)
	ret i32 %2
	
}

