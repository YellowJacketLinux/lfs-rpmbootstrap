%define kernelabi 6.6.56

# I need to investigate whether or not it is safe to strip
%global debug_package %{nil}
%global __strip /bin/true

%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif
%if 0%{!?__sed:1} == 1
%global __sed %{_bindir}/sed
%endif

Name:		glibc
Version:	2.40
Release:	%{?repo}0.rc3%{?dist}
Summary:	The GNU C Library

Group:		System Environment/Libraries
License:	GPLv2, LGPLv2.1
URL:		https://www.gnu.org/software/libc/
Source0:	https://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
Patch0:		https://www.linuxfromscratch.org/patches/lfs/12.2/%{name}-%{version}-fhs-1.patch

BuildRequires: kernel-abi-headers = %{kernelabi}
BuildRequires: %{__sed}
Requires: libidn2
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}
# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

%description
The GNU C Library project provides the core libraries for the GNU system and
GNU/Linux systems, as well as many other systems that use Linux as the kernel.
These libraries provide critical APIs including ISO C11, POSIX.1-2008, BSD,
OS-specific APIs and more. These APIs include such foundational facilities as
open, read, write, malloc, printf, getaddrinfo, dlopen, pthread_create, crypt,
login, exit and more.

The GNU C Library is designed to be a backwards compatible, portable, and high
performance ISO C library. It aims to follow all relevant standards including
ISO C11, POSIX.1-2008, and IEEE 754-2008.

%package utils
Group:  System Environment/Libraries
License: GPLv3
Summary: GLibC Utilities
Requires: %{name} = %{version}-%{release}
Requires: tzdata

%description utils
This package contains several system utilities that are part of the GNU C
Library distribution.

%package devel
Group:  Development/Libraries
License: GPLv3
Summary: Development files for the GNU C Library
Requires: kernel-abi-headers = %{kernelabi}

%description devel
This package contains the header files and related files that are necessary to
compile software that link against the GNU C Library. 

%package static
Group:  Development/Libraries
License:  GPLv3
Summary:  Static libraries for the GNU C Library
Requires: %{name}-devel = %{version}-%{release}

%description static
This package contains the GLibC static libraries. They are only needed to
compile software that staticly links against GLibC.

%prep
%setup -q
%patch 0 -p1


%build
mkdir build && cd build

echo "rootsbindir=%{_sbindir}" > configparms

../configure --prefix=%{_prefix} \
             --disable-werror \
             --enable-kernel=4.19 \
             --enable-stack-protector=strong \
             --disable-nscd \
             libc_cv_slibdir=%{_libdir}

make %{?_smp_mflags}

%check
cd build
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1 ||:
%else
echo "make check not run during packaging" > %{name}-make.check.log
%endif


%install
cd build
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/ld.so.conf
%{__sed} '/test-installation/s@$(PERL)@echo not running@' -i ../Makefile
make install DESTDIR=%{buildroot}

mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}/%{_lib}/
# fix broken symlinks
rm -f %{buildroot}%{_libdir}/libBrokenLocale.so
ln -sf libBrokenLocale.so.1 %{buildroot}/%{_lib}/libBrokenLocale.so
rm -f %{buildroot}%{_libdir}/libanl.so
ln -sf libanl.so.1 %{buildroot}/%{_lib}/libanl.so
rm -f %{buildroot}%{_libdir}/libc_malloc_debug.so
ln -sf libc_malloc_debug.so.0 %{buildroot}/%{_lib}/libc_malloc_debug.so
rm -f %{buildroot}%{_libdir}/libmvec.so
ln -sf libmvec.so.1 %{buildroot}/%{_lib}/libmvec.so
rm -f %{buildroot}%{_libdir}/libnss_compat.so
ln -sf libnss_compat.so.2 %{buildroot}/%{_lib}/libnss_compat.so
rm -f %{buildroot}%{_libdir}/libnss_db.so
ln -sf libnss_db.so.2 %{buildroot}/%{_lib}/libnss_db.so
rm -f %{buildroot}%{_libdir}/libnss_hesiod.so
ln -sf libnss_hesiod.so.2 %{buildroot}/%{_lib}/libnss_hesiod.so
rm -f %{buildroot}%{_libdir}/libresolv.so
ln -sf libresolv.so.2 %{buildroot}/%{_lib}/libresolv.so
rm -f %{buildroot}%{_libdir}/libthread_db.so
ln -sf libthread_db.so.1 %{buildroot}/%{_lib}/libthread_db.so
mv %{buildroot}%{_libdir}/libmemusage.so %{buildroot}/%{_lib}/
mv %{buildroot}%{_libdir}/libpcprofile.so %{buildroot}/%{_lib}/
# fix ld.so link
rm -f %{_buildroot}%{_bindir}/ld.so
ln -sf ../../%{_lib}/ld-linux-x86-64.so.2 %{buildroot}%{_bindir}/ld.so
mkdir -p %{buildroot}/lib64
ln -sf ../lib/ld-linux-x86-64.so.2 %{buildroot}/lib64/
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_sbindir}/ldconfig %{buildroot}/sbin/
mv %{buildroot}%{_sbindir}/sln %{buildroot}/sbin/

%{__sed} '/RTLDLIST=/s@/usr@@g' -i %{buildroot}%{_bindir}/ldd

make localedata/install-locales DESTDIR=%{buildroot}

### FIXME ###
#localedef -i C -f UTF-8 C.UTF-8
#localedef -i ja_JP -f SHIFT_JIS ja_JP.SJIS 2> /dev/null || true

cat > %{buildroot}%{_sysconfdir}/nsswitch.conf << "EOF"
# Begin %{_sysconfdir}/nsswitch.conf

passwd: files systemd
group: files systemd
shadow: files systemd

hosts: mymachines resolve [!UNAVAIL=return] files myhostname dns
networks: files

protocols: files
services: files
ethers: files
rpc: files

# End %{_sysconfdir}/nsswitch.conf
EOF

cat >> %{buildroot}%{_sysconfdir}/ld.so.conf << "EOF"
# Add an include directory
include %{_sysconfdir}/ld.so.conf.d/*.conf

EOF
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d

cd ..
%find_lang libc

%post
/sbin/ldconfig
%{insinfo} %{_infodir}/libc.info %{_infodir}/dir ||:

%postun -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libc.info %{_infodir}/dir ||:
fi

%files -f libc.lang
%defattr(-,root,root,-)
%doc CONTRIBUTED-BY COPYING* LICENSES MAINTAINERS NEWS README
%doc Rules SECURITY.md
%license COPYING* LICENSES 
%attr(0755,root,root) /%{_lib}/ld-linux-x86-64.so.2
%attr(0755,root,root) /%{_lib}/libBrokenLocale.so.1
%attr(0755,root,root) /%{_lib}/libanl.so.1
%attr(0755,root,root) /%{_lib}/libc.so.6
%attr(0755,root,root) /%{_lib}/libc_malloc_debug.so.0
%attr(0755,root,root) /%{_lib}/libdl.so.2
%attr(0755,root,root) /%{_lib}/libm.so.6
%attr(0755,root,root) /%{_lib}/libmemusage.so
%attr(0755,root,root) /%{_lib}/libmvec.so.1
%attr(0755,root,root) /%{_lib}/libnsl.so.1
%attr(0755,root,root) /%{_lib}/libnss_compat.so.2
%attr(0755,root,root) /%{_lib}/libnss_db.so.2
%attr(0755,root,root) /%{_lib}/libnss_dns.so.2
%attr(0755,root,root) /%{_lib}/libnss_files.so.2
%attr(0755,root,root) /%{_lib}/libnss_hesiod.so.2
%attr(0755,root,root) /%{_lib}/libpcprofile.so
%attr(0755,root,root) /%{_lib}/libpthread.so.0
%attr(0755,root,root) /%{_lib}/libresolv.so.2
%attr(0755,root,root) /%{_lib}/librt.so.1
%attr(0755,root,root) /%{_lib}/libthread_db.so.1
%attr(0755,root,root) /%{_lib}/libutil.so.1
/lib64/ld-linux-x86-64.so.2
%dir %{_libdir}/audit
%attr(0755,root,root) %{_libdir}/audit/sotruss-lib.so
%dir %{_libdir}/gconv
%attr(0755,root,root) %{_libdir}/gconv/*.so
%config(noreplace) %attr(0644,root,root) %{_libdir}/gconv/gconv-modules
%dir %{_libdir}/gconv/gconv-modules.d
%config(noreplace) %attr(0644,root,root) %{_libdir}/gconv/gconv-modules.d/gconv-modules-extra.conf
%{_datadir}/i18n/locales
%{_infodir}/libc.info*
%exclude %{_infodir}/dir
%doc build/%{name}-make.check.log

%files utils
%defattr(-,root,root,-)
%doc CONTRIBUTED-BY COPYING* LICENSES MAINTAINERS NEWS README
%doc Rules SECURITY.md
%license COPYING* LICENSES
%config(noreplace) %{_sysconfdir}/ld.so.conf
%dir %{_sysconfdir}/ld.so.conf.d
%config(noreplace) %{_sysconfdir}/nsswitch.conf
%config(noreplace) %{_sysconfdir}/rpc
%exclude %{_sysconfdir}/ld.so.cache
%attr(0755,root,root) /sbin/ldconfig
%attr(0755,root,root) /sbin/sln
%{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%{_libdir}/locale/locale-archive
%{_libexecdir}/getconf
%{_datadir}/i18n/charmaps
%{_sharedstatedir}/nss_db
%{_datadir}/locale/locale.alias

%files devel
%defattr(-,root,root,-)
%doc CONTRIBUTED-BY COPYING* LICENSES MAINTAINERS NEWS README
%doc Rules SECURITY.md
%license COPYING* LICENSES
%{_includedir}/*.h
%{_includedir}/arpa
%{_includedir}/bits
%{_includedir}/finclude
%{_includedir}/gnu
%{_includedir}/net
%{_includedir}/netash
%{_includedir}/netatalk
%{_includedir}/netax25
%{_includedir}/neteconet
%{_includedir}/netinet
%{_includedir}/netipx
%{_includedir}/netiucv
%{_includedir}/netpacket
%{_includedir}/netrom
%{_includedir}/netrose
%{_includedir}/nfs
%{_includedir}/protocols
%{_includedir}/rpc
%{_includedir}/scsi
%{_includedir}/sys
%{_libdir}/Mcrt1.o
%{_libdir}/Scrt1.o
%{_libdir}/crt1.o
%{_libdir}/crti.o
%{_libdir}/crtn.o
%{_libdir}/gcrt1.o
%{_libdir}/grcrt1.o
/%{_lib}/libBrokenLocale.so
/%{_lib}/libanl.so
%{_libdir}/libc.so
/%{_lib}/libc_malloc_debug.so
#%%{_libdir}/libcrypt.so
%{_libdir}/libm.so
/%{_lib}/libmvec.so
/%{_lib}/libnss_compat.so
/%{_lib}/libnss_db.so
/%{_lib}/libnss_hesiod.so
/%{_lib}/libresolv.so
/%{_lib}/libthread_db.so
%{_libdir}/rcrt1.o

%files static
%defattr(-,root,root,-)
%doc CONTRIBUTED-BY COPYING* LICENSES MAINTAINERS NEWS README
%doc Rules SECURITY.md
%license COPYING* LICENSES
%attr(0644,root,root) %{_libdir}/libBrokenLocale.a
%attr(0644,root,root) %{_libdir}/libanl.a
%attr(0644,root,root) %{_libdir}/libc.a
%attr(0644,root,root) %{_libdir}/libc_nonshared.a
#%%attr(0644,root,root) %%{_libdir}/libcrypt.a
%attr(0644,root,root) %{_libdir}/libdl.a
%attr(0644,root,root) %{_libdir}/libg.a
%attr(0644,root,root) %{_libdir}/libm-%{version}.a
%attr(0644,root,root) %{_libdir}/libm.a
%attr(0644,root,root) %{_libdir}/libmcheck.a
%attr(0644,root,root) %{_libdir}/libmvec.a
%attr(0644,root,root) %{_libdir}/libpthread.a
%attr(0644,root,root) %{_libdir}/libresolv.a
%attr(0644,root,root) %{_libdir}/librt.a
%attr(0644,root,root) %{_libdir}/libutil.a

%changelog
* Sun Oct 20 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.40-0.rc3
- Explicity provide rtld(GNU_HASH)

* Fri Oct 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.40-0.rc2
- Initial spec file for YJL 6.6 (LFS 12.2). Quite likely needs a lot of work.
