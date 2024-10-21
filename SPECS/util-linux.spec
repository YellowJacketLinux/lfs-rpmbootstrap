Name:     util-linux
Version:  2.40.2
Release:  %{?repo}0.rc1%{?dist}
Summary:  A random collection of Linux utilities

Group:    System Environment/Utilities
License:  GPLv2, GPLv1, GPLv3, LGPLv2.1, MIT, BSD-2-Clause, BSD-3-Clause, BSD-4-Clause-UC, PublicDomain
URL:      https://git.kernel.org/pub/scm/utils/util-linux/util-linux.git/
Source0:  https://www.kernel.org/pub/linux/utils/util-linux/v2.40/util-linux-%{version}.tar.xz
Source1:  util-linux-%{version}-bash-completion.filelist

#BuildRequires:
#Requires:	

%description
Util-Linux is a collection of common utilities needed to use the GNU/Linux
operating system.

%package libs
Summary: util-linux shared libraries
Group:   System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
This package containts the shared libraries that are part of util-linux.

%package devel
Summary: util-linux development files
Group:   Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains the developer header files needed to compile software
that links against the util-linux shared libraries.

%package bash-completion
Summary: bash completion rules
Group:   System Environment/Base
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description bash-completion
This package contains the bash completion rules for util-linux. Unless you
__know__ you do not want this, you should probably install this package.

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%prep
%setup -q
cp %{SOURCE1} ./bash-completion.filelist


%build
%configure \
  --libdir=/%{_lib}     \
  --disable-rpath       \
  --disable-chfn-chsh   \
  --disable-login       \
  --disable-nologin     \
  --disable-su          \
  --disable-setpriv     \
  --disable-runuser     \
  --disable-pylibmount  \
  --disable-liblastlog2 \
  --disable-static      \
  --without-python      \
  ADJTIME_PATH=%{_sharedstatedir}/hwclock/adjtime \
  --docdir=%{_datadir}/doc/%{name}-%{version} \
  --disable-makeinstall-chown \
  --disable-makeinstall-setuid

make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make -k check > %{name}-make.check.log 2>&1 ||:
%else
echo "make check not run at package build" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
# move these into /bin
install -d -m755 %{buildroot}/bin
for binary in dmesg kill more mount umount; do
  mv %{buildroot}%{_bindir}/${binary} %{buildroot}/bin
done
# move these into /sbin
install -d -m755 %{buildroot}/sbin
for binary in agetty fdisk fsck fsck.minix mkfs mkfs.bfs \
              mkfs.minix mkswap swapoff swapon; do
  mv %{buildroot}%{_sbindir}/${binary} %{buildroot}/sbin
done
# package these with %%doc
rm -f %{buildroot}%{_datadir}/doc/%{name}-%{version}/getopt-example.{bash,tcsh}
# .mo files
%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
# /bin and /usr/bin
%attr(0755,root,root) %{_bindir}/cal
%attr(0755,root,root) %{_bindir}/chmem
%attr(0755,root,root) %{_bindir}/choom
%attr(0755,root,root) %{_bindir}/chrt
%attr(0755,root,root) %{_bindir}/col
%attr(0755,root,root) %{_bindir}/colcrt
%attr(0755,root,root) %{_bindir}/colrm
%attr(0755,root,root) %{_bindir}/column
%attr(0755,root,root) /bin/dmesg
%attr(0755,root,root) %{_bindir}/eject
%attr(0755,root,root) %{_bindir}/enosys
%attr(0755,root,root) %{_bindir}/exch
%attr(0755,root,root) %{_bindir}/fadvise
%attr(0755,root,root) %{_bindir}/fallocate
%attr(0755,root,root) %{_bindir}/fincore
%attr(0755,root,root) %{_bindir}/findmnt
%attr(0755,root,root) %{_bindir}/flock
%attr(0755,root,root) %{_bindir}/getopt
%attr(0755,root,root) %{_bindir}/hardlink
%attr(0755,root,root) %{_bindir}/hexdump
%{_bindir}/i386
%attr(0755,root,root) %{_bindir}/ionice
%attr(0755,root,root) %{_bindir}/ipcmk
%attr(0755,root,root) %{_bindir}/ipcrm
%attr(0755,root,root) %{_bindir}/ipcs
%attr(0755,root,root) %{_bindir}/irqtop
%attr(0755,root,root) %{_bindir}/isosize
%attr(0755,root,root) /bin/kill
%attr(0755,root,root) %{_bindir}/last
%{_bindir}/lastb
%{_bindir}/linux32
%{_bindir}/linux64
%attr(0755,root,root) %{_bindir}/logger
%attr(0755,root,root) %{_bindir}/look
%attr(0755,root,root) %{_bindir}/lsblk
%attr(0755,root,root) %{_bindir}/lsclocks
%attr(0755,root,root) %{_bindir}/lscpu
%attr(0755,root,root) %{_bindir}/lsfd
%attr(0755,root,root) %{_bindir}/lsipc
%attr(0755,root,root) %{_bindir}/lsirq
%attr(0755,root,root) %{_bindir}/lslocks
%attr(0755,root,root) %{_bindir}/lslogins
%attr(0755,root,root) %{_bindir}/lsmem
%attr(0755,root,root) %{_bindir}/lsns
%attr(0755,root,root) %{_bindir}/mcookie
%attr(0755,root,root) %{_bindir}/mesg
%attr(0755,root,root) /bin/more
%attr(0755,root,root) %{_bindir}/mountpoint
%attr(0755,root,root) %{_bindir}/namei
%attr(0755,root,root) %{_bindir}/nsenter
%attr(0755,root,root) %{_bindir}/pipesz
%attr(0755,root,root) %{_bindir}/prlimit
%attr(0755,root,root) %{_bindir}/rename
%attr(0755,root,root) %{_bindir}/renice
%attr(0755,root,root) %{_bindir}/rev
%attr(0755,root,root) %{_bindir}/script
%attr(0755,root,root) %{_bindir}/scriptlive
%attr(0755,root,root) %{_bindir}/scriptreplay
%attr(0755,root,root) %{_bindir}/setarch
%attr(0755,root,root) %{_bindir}/setpgid
%attr(0755,root,root) %{_bindir}/setsid
%attr(0755,root,root) %{_bindir}/setterm
%attr(0755,root,root) %{_bindir}/taskset
%attr(0755,root,root) %{_bindir}/uclampset
%attr(0755,root,root) %{_bindir}/ul
%{_bindir}/uname26
%attr(0755,root,root) %{_bindir}/unshare
%attr(0755,root,root) %{_bindir}/utmpdump
%attr(0755,root,root) %{_bindir}/uuidgen
%attr(0755,root,root) %{_bindir}/uuidparse
%attr(0755,root,root) %{_bindir}/waitpid
%attr(0755,root,root) %{_bindir}/wdctl
%attr(0755,root,root) %{_bindir}/whereis
%{_bindir}/x86_64
### NON-STANDARD-PERMS in /bin /usr/bin ###
%attr(4755,root,root) /bin/mount
%attr(4755,root,root) /bin/umount
%attr(2755,root,tty) %{_bindir}/wall
# /sbin and /usr/sbin
%attr(0755,root,root) %{_sbindir}/addpart
%attr(0755,root,root) /sbin/agetty
%attr(0755,root,root) %{_sbindir}/blkdiscard
%attr(0755,root,root) %{_sbindir}/blkid
%attr(0755,root,root) %{_sbindir}/blkpr
%attr(0755,root,root) %{_sbindir}/blkzone
%attr(0755,root,root) %{_sbindir}/blockdev
%attr(0755,root,root) %{_sbindir}/cfdisk
%attr(0755,root,root) %{_sbindir}/chcpu
%attr(0755,root,root) %{_sbindir}/ctrlaltdel
%attr(0755,root,root) %{_sbindir}/delpart
%attr(0755,root,root) /sbin/fdisk
%attr(0755,root,root) %{_sbindir}/findfs
%attr(0755,root,root) /sbin/fsck
%attr(0755,root,root) /sbin/fsck.minix
%attr(0755,root,root) %{_sbindir}/fsfreeze
%attr(0755,root,root) %{_sbindir}/fstrim
%attr(0755,root,root) %{_sbindir}/hwclock
%attr(0755,root,root) %{_sbindir}/ldattach
%attr(0755,root,root) %{_sbindir}/losetup
%attr(0755,root,root) /sbin/mkfs
%attr(0755,root,root) /sbin/mkfs.bfs
%attr(0755,root,root) /sbin/mkfs.minix
%attr(0755,root,root) /sbin/mkswap
%attr(0755,root,root) %{_sbindir}/partx
%attr(0755,root,root) %{_sbindir}/pivot_root
%attr(0755,root,root) %{_sbindir}/readprofile
%attr(0755,root,root) %{_sbindir}/resizepart
%attr(0755,root,root) %{_sbindir}/rfkill
%attr(0755,root,root) %{_sbindir}/rtcwake
%attr(0755,root,root) %{_sbindir}/sfdisk
%attr(0755,root,root) %{_sbindir}/sulogin
%attr(0755,root,root) %{_sbindir}/swaplabel
%attr(0755,root,root) /sbin/swapoff
%attr(0755,root,root) /sbin/swapon
%attr(0755,root,root) %{_sbindir}/switch_root
%attr(0755,root,root) %{_sbindir}/uuidd
%attr(0755,root,root) %{_sbindir}/wipefs
%attr(0755,root,root) %{_sbindir}/zramctl
# man pages
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(0644,root,root) %{_mandir}/man8/*.8*
#
%attr(0644,root,root) %config(noreplace) %{_libdir}/systemd/system/fstrim.service
%attr(0644,root,root) %config(noreplace) %{_libdir}/systemd/system/fstrim.timer
%attr(0644,root,root) %config(noreplace) %{_libdir}/systemd/system/uuidd.service
%attr(0644,root,root) %config(noreplace) %{_libdir}/systemd/system/uuidd.socket
%attr(0644,root,root) %config(noreplace) %{_libdir}/tmpfiles.d/uuidd-tmpfiles.conf
%license COPYING README.licensing
%doc misc-utils/getopt-example.bash
%doc misc-utils/getopt-example.tcsh
%doc AUTHORS COPYING README README.licensing
%doc %{name}-make.check.log

%files libs
%defattr(-,root,root,-)
%attr(0755,root,root) /%{_lib}/libblkid.so.1.1.0
/%{_lib}/libblkid.so.1
%attr(0755,root,root) /%{_lib}/libfdisk.so.1.1.0
/%{_lib}/libfdisk.so.1
%attr(0755,root,root) /%{_lib}/libmount.so.1.1.0
/%{_lib}/libmount.so.1
%attr(0755,root,root) /%{_lib}/libsmartcols.so.1.1.0
/%{_lib}/libsmartcols.so.1
%attr(0755,root,root) /%{_lib}/libuuid.so.1.3.0
/%{_lib}/libuuid.so.1
%license COPYING README.licensing
%doc AUTHORS COPYING README README.licensing

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/blkid
%attr(0644,root,root) %{_includedir}/blkid/blkid.h
%dir %{_includedir}/libfdisk
%attr(0644,root,root) %{_includedir}/libfdisk/libfdisk.h
%dir %{_includedir}/libmount
%attr(0644,root,root) %{_includedir}/libmount/libmount.h
%dir %{_includedir}/libsmartcols
%attr(0644,root,root) %{_includedir}/libsmartcols/libsmartcols.h
%dir %{_includedir}/uuid
%attr(0644,root,root) %{_includedir}/uuid/uuid.h
%{_libdir}/libblkid.so
%{_libdir}/libfdisk.so
%{_libdir}/libmount.so
%{_libdir}/libsmartcols.so
%{_libdir}/libuuid.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%attr(0644,root,root) %{_mandir}/man3/*.3*

%files bash-completion -f bash-completion.filelist


%changelog
* Sun Oct 20 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.40.2-0.rc1
- Initial RPM spec file for YJL 6.6 (LFS 12.2)
