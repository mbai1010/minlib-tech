$(common-objpfx)string/rtld-memcmp-avx2-movbe-rtm.os: \
 ../sysdeps/x86_64/multiarch/memcmp-avx2-movbe-rtm.S \
 $(common-objpfx)libc-modules.h \
 ../include/libc-symbols.h \
 $(common-objpfx)config.h \
 ../sysdeps/generic/libc-symver.h ../sysdeps/generic/symbol-hacks.h \
 /usr/lib/gcc/x86_64-linux-gnu/11/include/cet.h \
 ../sysdeps/x86_64/multiarch/memcmp-avx2-movbe.S
$(common-objpfx)libc-modules.h:
../include/libc-symbols.h:
$(common-objpfx)config.h:
../sysdeps/generic/libc-symver.h:
../sysdeps/generic/symbol-hacks.h:
/usr/lib/gcc/x86_64-linux-gnu/11/include/cet.h:
../sysdeps/x86_64/multiarch/memcmp-avx2-movbe.S:
