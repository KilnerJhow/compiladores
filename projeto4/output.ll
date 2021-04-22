@glob1 =  global float 0x40139999a0000000
define i32 @main() {
	%g =  alloca float, align 4
	store i32 4, i32* %g, align 4
	%h =  alloca float, align 4
	%0 = load float, float* @glob1, align 4
	%1 = fadd float 0, %g
	store float 0x4021ccccc0000000, float* %1, align 4
	
}

