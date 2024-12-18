Name:     gdb
Version:  15.2
Release:  %{?repo}0.rc1%{?dist}
Summary:  GNU Project Debugger

Group:    Development/Utilities
License:  GPLv2 GPLv3 LGPLv2 LGPLv3
URL:      https://www.sourceware.org/gdb/
Source0:  https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz

BuildRequires:  expat-devel
BuildRequires:  liblzma-devel
BuildRequires:  mpfr-devel
BuildRequires:  gmp-devel
BuildRequires:  readline-devel
BuildRequires:  libzstd-devel
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  elfutils-devel
BuildRequires:  libstdc++-devel
BuildRequires:  dejagnu
%if %{?python3_ABI:1}%{!?python3_ABI:0}
# Non-Standard Macro
Requires: %{python3_ABI}
%else
Requires: %{python3_sitearch}
%endif
Requires: python3-six

%description
GDB, the GNU Project debugger, allows you to see what is going on
`inside' another program while it executes -- or what another program
was doing at the moment it crashed.

%prep
%setup -q


%build
mkdir build && cd build
../configure --prefix=%{_prefix} \
  --with-system-readline         \
  --with-python=%{python3}
make %{?_smp_mflags}

# after we have Doxygen
# make -C gdb/doc doxy

%check
cd build/gdb/testsuite
%if 0%{?runtests:1} == 1
make site.exp
echo  "set gdb_test_timeout 120" >> site.exp
runtest > %{name}-runtest.log 2>&1 ||:
%else
echo "make check not run during packaging" > %{name}-runtest.log
%endif

%install
cd build
make -C gdb install DESTDIR=%{buildroot}

# after we have Doxygen
# cp -Rv gdb/doc/doxy /usr/share/doc/gdb-15.2

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gcore
%attr(0755,root,root) %{_bindir}/gdb
%attr(0755,root,root) %{_bindir}/gdb-add-index
%attr(0755,root,root) %dir %{_includedir}/gdb
%attr(0644,root,root) %{_includedir}/gdb/jit-reader.h
%{_datadir}/gdb
%attr(0644,root,root) %{_infodir}/annotate.info*
%attr(0644,root,root) %{_infodir}/gdb.info*
%attr(0644,root,root) %{_infodir}/stabs.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/gcore.1*
%attr(0644,root,root) %{_mandir}/man1/gdb-add-index.1*
%attr(0644,root,root) %{_mandir}/man1/gdb.1*
%attr(0644,root,root) %{_mandir}/man1/gdbserver.1*
%attr(0644,root,root) %{_mandir}/man5/gdbinit.5*
%license COPYING COPYING.LIB COPYING3 COPYING3.LIB
%doc ChangeLog gdb/README COPYING COPYING.LIB COPYING3 COPYING3.LIB
%doc build/gdb/testsuite/%{name}-runtest.log


%changelog
* Mon Oct 21 2024 Michael A. Peters <anymouseprophet@gmail.com> - 15.2-0.rc1
- Build for YJL 6.6 (LFS 12.2)

* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 13.1-0.rc2
- Fix BuildRequires, tabs to spaces, conditionally run tests.

* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 13.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
