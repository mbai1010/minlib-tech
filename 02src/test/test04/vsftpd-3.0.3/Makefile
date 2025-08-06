# Makefile for systems with GNU tools
MUSL_PREFIX=/home/gwu-sys-lab/Desktop/01Research/06minlib_related_test/07Comparison/05musl_libc/musl-1.2.2/install

OPENSSL_PREFIX = /home/gwu-sys-lab/Desktop/01Research/06minlib_related_test/07Comparison/05OpenSSL_musl/openssl-3.0.13/install
OPENSSL_INCLUDE = $(OPENSSL_PREFIX)/include
OPENSSL_LIB = $(OPENSSL_PREFIX)/lib64

XCRYPT_PREFIX   = /home/gwu-sys-lab/Desktop/01Research/06minlib_related_test/07Comparison/05libxcrypt/libxcrypt
XCRYPT_LIB      = $(XCRYPT_PREFIX)/install/lib

CC 	=	$(MUSL_PREFIX)/bin/musl-gcc
INSTALL	=	install
IFLAGS  = -I$(OPENSSL_INCLUDE) -idirafter dummyinc
#CFLAGS = -g

CFLAGS	=	-O2 -fPIE -fstack-protector --param=ssp-buffer-size=4 \
	-Wall -W -Wshadow -Werror -Wformat-security -Wno-error=enum-conversion -Wno-error=deprecated-declarations\
	-D_FORTIFY_SOURCE=2 -I$(OPENSSL_INCLUDE) -I$(XCRYPT_PREFIX) -DVSF_BUILD_SSL -DVSF_NO_PAM \
	#-pedantic -Wconversion

LIBS	=	-lssl -lcrypto -lcrypt -lc
LINK	=	-Wl,-s
LDFLAGS	=	-fPIE -pie -Wl,-z,relro -Wl,-z,now -L$(OPENSSL_LIB) -L$(XCRYPT_LIB) -L$(MUSL_PREFIX)/lib -Wl,-rpath,\$$ORIGIN

OBJS	=	main.o utility.o prelogin.o ftpcmdio.o postlogin.o privsock.o \
		tunables.o ftpdataio.o secbuf.o ls.o \
		postprivparent.o logging.o str.o netstr.o sysstr.o strlist.o \
    banner.o filestr.o parseconf.o secutil.o \
    ascii.o oneprocess.o twoprocess.o privops.o standalone.o hash.o \
    tcpwrap.o ipaddrparse.o access.o features.o readwrite.o opts.o \
    ssl.o sslslave.o ptracesandbox.o ftppolicy.o sysutil.o sysdeputil.o \
    seccomp_dummy.o


.c.o:
	$(CC) -c $*.c $(CFLAGS) $(IFLAGS)

vsftpd: $(OBJS) 
	$(CC) -o vsftpd $(OBJS) $(LINK) $(LDFLAGS) $(LIBS)

install:
	if [ -x /usr/local/sbin ]; then \
		$(INSTALL) -m 755 vsftpd /usr/local/sbin/vsftpd; \
	else \
		$(INSTALL) -m 755 vsftpd /usr/sbin/vsftpd; fi
	if [ -x /usr/local/man ]; then \
		$(INSTALL) -m 644 vsftpd.8 /usr/local/man/man8/vsftpd.8; \
		$(INSTALL) -m 644 vsftpd.conf.5 /usr/local/man/man5/vsftpd.conf.5; \
	elif [ -x /usr/share/man ]; then \
		$(INSTALL) -m 644 vsftpd.8 /usr/share/man/man8/vsftpd.8; \
		$(INSTALL) -m 644 vsftpd.conf.5 /usr/share/man/man5/vsftpd.conf.5; \
	else \
		$(INSTALL) -m 644 vsftpd.8 /usr/man/man8/vsftpd.8; \
		$(INSTALL) -m 644 vsftpd.conf.5 /usr/man/man5/vsftpd.conf.5; fi
	if [ -x /etc/xinetd.d ]; then \
		$(INSTALL) -m 644 xinetd.d/vsftpd /etc/xinetd.d/vsftpd; fi

clean:
	rm -f *.o *.swp vsftpd

