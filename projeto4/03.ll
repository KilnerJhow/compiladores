; ModuleID = 'inputs/03.c'
source_filename = "inputs/03.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @half(i32 %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  %3 = load i32, i32* %2, align 4
  %4 = sdiv i32 %3, 2
  ret i32 %4
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @scalar(i32 %0, i32 %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  store i32 %1, i32* %4, align 4
  %5 = load i32, i32* %4, align 4
  %6 = sub nsw i32 0, %5
  %7 = load i32, i32* %3, align 4
  %8 = mul nsw i32 %7, %6
  store i32 %8, i32* %3, align 4
  %9 = load i32, i32* %4, align 4
  %10 = add nsw i32 %9, 1
  store i32 %10, i32* %4, align 4
  %11 = load i32, i32* %3, align 4
  %12 = load i32, i32* %3, align 4
  %13 = mul nsw i32 %11, %12
  %14 = load i32, i32* %4, align 4
  %15 = add nsw i32 %13, %14
  %16 = load i32, i32* %4, align 4
  %17 = load i32, i32* %3, align 4
  %18 = sub nsw i32 %16, %17
  %19 = load i32, i32* %4, align 4
  %20 = mul nsw i32 %18, %19
  %21 = add nsw i32 %15, %20
  %22 = call i32 @half(i32 %21)
  %23 = add nsw i32 %22, 3
  %24 = sdiv i32 %23, 2
  ret i32 %24
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local float @fscalar(float %0, float %1) #0 {
  %3 = alloca float, align 4
  %4 = alloca float, align 4
  %5 = alloca float, align 4
  store float %0, float* %3, align 4
  store float %1, float* %4, align 4
  %6 = load float, float* %3, align 4
  %7 = load float, float* %4, align 4
  %8 = fadd float %6, %7
  %9 = load float, float* %3, align 4
  %10 = load float, float* %4, align 4
  %11 = fsub float %9, %10
  %12 = fdiv float %8, %11
  %13 = load float, float* %3, align 4
  %14 = load float, float* %4, align 4
  %15 = fmul float %13, %14
  %16 = fmul float %12, %15
  %17 = load float, float* %3, align 4
  %18 = load float, float* %4, align 4
  %19 = fdiv float %17, %18
  %20 = fdiv float %16, %19
  store float %20, float* %5, align 4
  %21 = load float, float* %5, align 4
  ret float %21
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 33, i32* %2, align 4
  store i32 821, i32* %3, align 4
  store i32 1, i32* %4, align 4
  store i32 -1, i32* %5, align 4
  %6 = load i32, i32* %2, align 4
  %7 = load i32, i32* %4, align 4
  %8 = sub nsw i32 %6, %7
  %9 = load i32, i32* %3, align 4
  %10 = call i32 @scalar(i32 %8, i32 %9)
  %11 = load i32, i32* %5, align 4
  %12 = sub nsw i32 %10, %11
  store i32 %12, i32* %3, align 4
  %13 = load i32, i32* %3, align 4
  ret i32 %13
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0-4ubuntu1 "}
