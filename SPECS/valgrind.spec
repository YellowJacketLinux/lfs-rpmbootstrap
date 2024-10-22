# SEE README_DEVELOPERS
%global debug_package %{nil}
%global __strip /bin/true

%if 0%{?!__which:1} == 1
%global __which %{_bindir}/which
%endif
%if 0%{?!__sed:1} == 1
%global __sed %{_bindir}/sed
%endif

Name:     valgrind
Version:  3.23.0
Release:  %{?repo}0.rc1%{?dist}
Summary:  Framework for building dynamic analysis tools

Group:    Development/Utilities
License:  GPLv2 GFDL1.2
URL:      https://valgrind.org/
Source0:  https://sourceware.org/pub/valgrind/valgrind-3.23.0.tar.bz2

BuildRequires: %{__sed}
%if 0%{?runtests:1} == 1
BuildRequires: docbook-xml
BuildRequires: gdb
BuildRequires: %{__which}
%endif
#Requires:	

%description
Valgrind is an instrumentation framework for building dynamic analysis tools.
There are Valgrind tools that can automatically detect many memory management
and threading bugs, and profile your programs in detail. You can also use
Valgrind to build new tools.

The Valgrind distribution currently includes seven production-quality tools: a
memory error detector, two thread error detectors, a cache and branch-prediction
profiler, a call-graph generating cache and branch-prediction profiler, and two
different heap profilers. It also includes an experimental SimPoint basic block
vector generator.

%prep
%setup -q
sed -i 's|/doc/valgrind||' docs/Makefile.in
# note to self, above works but is dirty

%build
./configure --prefix=%{_prefix} --datadir=%{_datadir}/doc/%{name}-%{version}
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
%if 0%{?runtests:1} == 1
make regtest > %{name}-make.regtest.log 2>&1 ||:
%else
echo "make regtest not during package build" > %{name}-make.regtest.log
%endif

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/callgrind_annotate
%attr(0755,root,root) %{_bindir}/callgrind_control
%attr(0755,root,root) %{_bindir}/cg_annotate
%attr(0755,root,root) %{_bindir}/cg_diff
%attr(0755,root,root) %{_bindir}/cg_merge
%attr(0755,root,root) %{_bindir}/ms_print
%attr(0755,root,root) %{_bindir}/valgrind
%attr(0755,root,root) %{_bindir}/valgrind-di-server
%attr(0755,root,root) %{_bindir}/valgrind-listener
%attr(0755,root,root) %{_bindir}/vgdb
%dir %{_includedir}/valgrind
%attr(0644,root,root) %{_includedir}/valgrind/*.h
%dir %{_includedir}/valgrind/vki
%attr(0644,root,root) %{_includedir}/valgrind/vki/*.h
%dir %{_libdir}/valgrind
%attr(0644,root,root) %{_libdir}/valgrind/*.a
%attr(0644,root,root) %{_prefix}/lib/pkgconfig/valgrind.pc
%dir %{_libexecdir}/valgrind
%attr(0644,root,root) %{_libexecdir}/valgrind/*.xml
%attr(0644,root,root) %{_libexecdir}/valgrind/*.so
%attr(0644,root,root) %{_libexecdir}/valgrind/*.py
%attr(0644,root,root) %{_libexecdir}/valgrind/default.supp
%attr(0644,root,root) %{_libexecdir}/valgrind/dh_view.*
%attr(0755,root,root) %{_libexecdir}/valgrind/cachegrind-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/callgrind-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/dhat-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/drd-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/exp-bbv-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/getoff-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/helgrind-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/lackey-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/massif-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/memcheck-amd64-linux
%attr(0755,root,root) %{_libexecdir}/valgrind/none-amd64-linux
%dir %{_datadir}/doc/%{name}-%{version}/html
%attr(0644,root,root) %{_datadir}/doc/%{name}-%{version}/html/*.html
%attr(0644,root,root) %{_datadir}/doc/%{name}-%{version}/html/*.css
%dir %{_datadir}/doc/%{name}-%{version}/html/images
%attr(0644,root,root) %{_datadir}/doc/%{name}-%{version}/html/images/*.png
%attr(0644,root,root) %{_datadir}/doc/%{name}-%{version}/valgrind_manual.*
%attr(0644,root,root) %{_mandir}/man1/*.1*
%license COPYING COPYING.DOCS
%doc %{name}-make.regtest.log
%doc AUTHORS COPYING COPYING.DOCS NEWS README README_PACKAGERS



%changelog
* Tue Oct 22 2024 Michael A. Peters <anymouseprophet@gmail.com> - 3.23.0-0.rc1
- Initial RPM spec file for YJL 6.6 (LFS 12.2)
