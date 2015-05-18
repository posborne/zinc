AC_INIT(zinc, 0.1)

AC_CHECK_TOOL(STRIP, strip, :)
AC_CHECK_TOOL(OBJCOPY, objcopy, :)
AC_CHECK_TOOL(OBJDUMP, objdump, :)

AC_SUBST(host, $host)

AC_ARG_VAR(MCU, [MCU type])

case $MCU in
lpc17xx)
	tgt_cpu=cortex-m3
	;;
stm32f4)
	tgt_cpu=cortex-m4
	;;
stm32l1)
	tgt_cpu=cortex-m3
	;;
k20)
	tgt_cpu=cortex-m4
	;;
tiva_c)
	tgt_cpu=cortex-m4
	;;
*)
	AC_MSG_ERROR([Unknown MCU $MCU])
	;;
esac

tgt_arch=arm
tgt_layout=e-m:e-p:32:32-i1:8:32-i8:8:32-i16:16:32-i64:64-v128:64:128-a:0:32-n32-S64
tgt_os=none
tgt_endian=little
tgt_ptr_width=32

case $tgt_cpu in
cortex-m3)
	tgt_llvm_tgt=thumbv7em-none-eabi
	;;
cortex-m4)
	tgt_llvm_tgt=thumbv7m-none-eabi
	;;
esac

AC_SUBST(tgt_arch, $tgt_arch)
AC_SUBST(tgt_cpu, $tgt_cpu)
AC_SUBST(tgt_layout, $tgt_layout)
AC_SUBST(tgt_llvm_tgt, $tgt_llvm_tgt)
AC_SUBST(tgt_os, $tgt_os)
AC_SUBST(tgt_endian, $tgt_endian)
AC_SUBST(tgt_ptr_width, $tgt_ptr_width)

AC_CONFIG_FILES([Makefile])

if test -n "$host"; then
	AC_CONFIG_FILES([$host.json:target.json.in])
fi

AC_OUTPUT
