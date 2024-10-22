%global debug_package %{nil}
# ssh-keygen -A
#  TODO: SystemD unit scripts after systemd w/ rpmmacros package

%if 0%{?!_unitdir:1} == 1
%global _unitdir /usr/lib/systemd/system
%endif

%if 0%{?repo:1} == 1
%if "%{repo}" == "1.core."
# disable these features for 1.core. build
%global nokerberos nokerberos
%global nolibedit  nolibedit
%endif
%endif

# for tests
%if 0%{?!__scp:1}
%global __scp %{_bindir}/scp
%endif

Name:     openssh	
Version:  9.9p1
Release:  %{?repo}0.rc3%{?dist}
Summary:  Secure Shell

Group:    System Environment/Utilities
License:  BSD-2-Clause, BSD-3-Clause, ISC-style, and MIT-style
URL:      https://www.openssh.com/
Source0:  https://ftp.usa.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1:  sshd-units-blf12.2.tgz

BuildRequires:  yjl-sysusers
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
# this will work with LibreSSL or OpenSSL
BuildRequires:  pkgconfig(openssl)
%endif
%if 0%{?!nokerberos:1} == 1
BuildRequires:  kerberos5-devel
%endif
%if 0%{?!nolibedit:1} == 1
BuildRequires:  libedit-devel
%endif
%if 0%{?runtests:1} == 1
BuildRequires:  gdb
BuildRequires:  %{__scp}
%endif
BuildRequires:  pkgconfig(zlib)
### These add entropy, extra entropy is never bad but I do not think they
### are necessary as of kernel 5.6 series.
#Requires: net-tools sysstat
#Requires: haveged

%description
OpenSSH is the premier connectivity tool for remote login with the SSH
protocol. It encrypts all traffic to eliminate eavesdropping, connection
hijacking, and other attacks. In addition, OpenSSH provides a large suite
of secure tunneling capabilities, several authentication methods, and
sophisticated configuration options.

%package clients
Group:    System Environment/Utilities
Summary:  OpenSSH clients
Requires: %{name} = %{version}-%{release}

%description clients
This package contains the OpenSSH clients: list

%package server
Group:    System Environment/Daemons
Summary:  OpenSSH server
Requires: %{name} = %{version}-%{release}
Requires(pre):  %{_yjl_sysusers}

%description server
This package contains the OpenSSH server daemon.

%prep
%setup -q
mkdir blfs-sshd-units && cd blfs-sshd-units
tar -zxf %{SOURCE1}


%build
%configure \
  --sysconfdir=/etc/ssh                    \
  --with-privsep-path=/var/lib/sshd        \
  --with-default-path=/usr/bin:/bin        \
  --with-superuser-path=/usr/sbin:/usr/bin:/sbin:/bin \
  --with-zlib=%{_prefix}                   \
%if 0%{?!nokerberos} == 1
  --with-kerberos5=%{_prefix}              \
%endif
%if 0%{?!nolibet} == 1
  --with-libedit                           \
%endif
  --with-xauth=%{_bindir}/xauth            \
  --with-pid-dir=/run
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
echo "PermitRootLogin no" >> %{buildroot}%{_sysconfdir}/ssh/sshd_config
install -m755 contrib/ssh-copy-id %{buildroot}%{_bindir}/
install -m644 contrib/ssh-copy-id.1 %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sharedstatedir}/sshd
mkdir -p %{buildroot}%{_unitdir}
install -m644 blfs-sshd-units/sshdat.service %{buildroot}%{_unitdir}/sshd@.service
install -m644 blfs-sshd-units/sshd.service %{buildroot}%{_unitdir}
install -m644 blfs-sshd-units/sshd.socket  %{buildroot}%{_unitdir}


%check
%if 0%{?runtests:1} == 1
TEST_SSH_UNSAFE_PERMISSIONS=1 \
make -j1 tests > %{name}-make.tests.log 2>&1
%else
echo "tests not run during package build" > %{name}-make.tests.log
%endif

%pre server
%{_yjl_sysusers} --userandgroup \
  -d /var/lib/sshd -s noshell sshd ||:

#%%post
#%%systemd_post sshd.service

#%%preun
#%%systemd_preun sshd.service

#%%postun
#%%systemd_postun_with_restart sshd.service

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(4711,root,root) %{_libexecdir}/ssh-keysign
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*
%license LICENCE
%doc CREDITS LICENCE OVERVIEW PROTOCOL* README* SECURITY.md
%doc %{name}-make.tests.log

%files clients
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/scp
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_libexecdir}/ssh-pkcs11-helper
%attr(0755,root,root) %{_libexecdir}/ssh-sk-helper
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%attr(0644,root,root) %{_mandir}/man8/ssh-pkcs11-helper.8*
%attr(0644,root,root) %{_mandir}/man8/ssh-sk-helper.8*
%license LICENCE
%doc CREDITS LICENCE OVERVIEW PROTOCOL* README* SECURITY.md

%files server
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/sftp-server
%attr(0755,root,root) %{_libexecdir}/sshd-session
%attr(0700,root,sys) %dir %{_sharedstatedir}/sshd
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0644,root,root) %config(noreplace) %{_unitdir}/sshd*
%license LICENCE
%doc CREDITS LICENCE OVERVIEW PROTOCOL* README* SECURITY.md
%doc blfs-sshd-units/blfs-systemd-README

%changelog
* Mon Oct 21 2024 Michael A. Peters <anymouseprophet@gmail.com> - 9.9p1-0.rc3
- Build for YJL 6.6 (LFS 12.2)
-   Need to rebuild after SystemD macros available

* Sat Jun 03 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.3p1-0.rc4
- Rebuild with yjl-sysusers

* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.3p1-0.rc2
- Rebuild with correct %%{_sharedstatedir} macro

* Fri May 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.3p1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
