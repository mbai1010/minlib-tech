#!/bin/bash
builddir=`dirname "$0"`
GCONV_PATH="${builddir}/iconvdata"

usage () {
cat << EOF
Usage: $0 [OPTIONS] <program> [ARGUMENTS...]

  --tool=TOOL  Run with the specified TOOL. It can be strace, rpctrace,
               valgrind or container. The container will run within
               support/test-container.
EOF

  exit 1
}

toolname=default
while test $# -gt 0 ; do
  case "$1" in
    --tool=*)
      toolname="${1:7}"
      shift
      ;;
    --*)
      usage
      ;;
    *)
      break
      ;;
  esac
done

if test $# -eq 0 ; then
  usage
fi

case "$toolname" in
  default)
    exec   env GCONV_PATH="${builddir}"/iconvdata LOCPATH="${builddir}"/localedata LC_ALL=C  "${builddir}"/elf/ld-linux-x86-64.so.2 --library-path "${builddir}":"${builddir}"/math:"${builddir}"/elf:"${builddir}"/dlfcn:"${builddir}"/nss:"${builddir}"/nis:"${builddir}"/rt:"${builddir}"/resolv:"${builddir}"/mathvec:"${builddir}"/support:"${builddir}"/crypt:"${builddir}"/nptl ${1+"$@"}
    ;;
  strace)
    exec strace  -EGCONV_PATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/iconvdata  -ELOCPATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/localedata  -ELC_ALL=C  /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf/ld-linux-x86-64.so.2 --library-path /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/math:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/dlfcn:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nss:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nis:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/rt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/resolv:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/mathvec:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/support:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/crypt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nptl ${1+"$@"}
    ;;
  rpctrace)
    exec rpctrace  -EGCONV_PATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/iconvdata  -ELOCPATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/localedata  -ELC_ALL=C  /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf/ld-linux-x86-64.so.2 --library-path /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/math:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/dlfcn:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nss:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nis:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/rt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/resolv:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/mathvec:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/support:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/crypt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nptl ${1+"$@"}
    ;;
  valgrind)
    exec env GCONV_PATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/iconvdata LOCPATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/localedata LC_ALL=C valgrind  /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf/ld-linux-x86-64.so.2 --library-path /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/math:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/dlfcn:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nss:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nis:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/rt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/resolv:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/mathvec:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/support:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/crypt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nptl ${1+"$@"}
    ;;
  container)
    exec env GCONV_PATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/iconvdata LOCPATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/localedata LC_ALL=C  /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf/ld-linux-x86-64.so.2 --library-path /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/math:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/dlfcn:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nss:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nis:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/rt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/resolv:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/mathvec:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/support:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/crypt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nptl /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/support/test-container env GCONV_PATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/iconvdata LOCPATH=/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/localedata LC_ALL=C  /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf/ld-linux-x86-64.so.2 --library-path /home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/math:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/elf:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/dlfcn:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nss:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nis:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/rt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/resolv:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/mathvec:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/support:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/crypt:/home/gwu-sys-lab/Desktop/01Research/04minlib/minlib-tech/02src/test/test04/04glibc/build/nptl ${1+"$@"}
    ;;
  *)
    usage
    ;;
esac
