%global libzsharedv 1.3.1

Name:     zlib
Version:  1.3.1
Release:  %{?repo}0.rc3%{?dist}
Summary:	A compression library

Group:    System Environment/Libraries
License:  Zlib
URL:      https://zlib.net/
Source0:  https://zlib.net/%{name}-%{version}.tar.gz

#BuildRequires:	

%description
zlib is a massively spiffy yet delicately unobtrusive compression library. It
is free software that also is not patent encumbered.

Note that zlib is not related to the Linux zlibc compressing File-I/O library.

%package devel
Summary:  Developer files for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the library header files and the pkg-config file that are
necessary to compile software that links against the zlib library.

%prep
%setup -q


%build
./configure --prefix=%{_prefix} 
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log

%install
make install DESTDIR=%{buildroot}
#install -m755 -d %{buildroot}%{_libdir}
#sed -i 's?libdir=.*?libdir=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/zlib.pc
#sed -i 's?^sharedlibdir=%{_prefix}?sharedlibdir=?' %{buildroot}/%{_lib}/pkgconfig/zlib.pc
#mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}/
#rm -f %{buildroot}/%{_lib}/libz.so
#ln -s ../../%{_lib}/libz.so.1.2.13 %{buildroot}%{_libdir}/libz.so
# just in case we ever package the static library
#mv %{buildroot}/%{_lib}/libz.a %{buildroot}%{_libdir}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libz.so.%{libzsharedv}
%{_libdir}/libz.so.1
%license LICENSE
%doc ChangeLog LICENSE README FAQ
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/libz.a
%{_libdir}/libz.so
%attr(0644,root,root) %{_includedir}/zconf.h
%attr(0644,root,root) %{_includedir}/zlib.h
%attr(0644,root,root) %{_libdir}/pkgconfig/zlib.pc
%attr(0644,root,root) %{_mandir}/man3/zlib.3*
%license LICENSE

%changelog
* Mon Oct 21 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.3.1-0.rc3
- Don't use /lib for now as it breaks OpenSSH build

* Sun Oct 20 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.3.1-0.rc1
- Build for YJL 6.6 (LFS 12.2)

* Fri Apr 21 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.2.13-0.rc4
- Fix mis-labeled license tag.

* Tue Apr 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.2.13-0.rc3
- Rebuild with now packaged gcc

* Fri Mar 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.2.13-0.rc2
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
