%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     gzip
Version:  1.13
Release:  %{?repo}0.rc1%{?dist}
Summary:  GNU compression utility

Group:    System Environment/Utilities
License:  GPLv3
URL:      https://www.gnu.org/software/gzip
Source0:  https://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.xz

#BuildRequires:
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
gzip (GNU zip) is a compression utility designed to be a replacement
for 'compress'. Its main advantages over compress are much better
compression and freedom from patented algorithms.  The GNU Project
uses it as the standard compression program for its system.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make test not run during package build." > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}

%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%files
%defattr(-,root,root,-)
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS ChangeLog COPYING README THANKS
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_infodir}/%{name}.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/*.1*


%changelog
* Sat Oct 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.13-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2)
