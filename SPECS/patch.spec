Name:     patch
Version:  2.7.6
Release:  %{?repo}0.rc1%{?dist}
Summary:  Apply a diff to an original file

Group:    System Environment/Utilities
License:  GPLv3
URL:      https://savannah.gnu.org/projects/patch
Source0:  https://ftp.gnu.org/gnu/patch/patch-%{version}.tar.xz


%description
This is GNU patch, which applies diff files to original files.

This version of patch has many changes made by the Free Software Foundation.
They add support for:
 * handling arbitrary binary data and large files
 * the unified context diff format that GNU diff can produce
 * merging into files instead of creating reject files
 * making GNU Emacs-style backup files
 * improved interaction with RCS and SCCS
 * the GNU conventions for option parsing and configuring and compilation.
 * better POSIX compliance
They also fix some bugs.


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


%files
%defattr(-,root,root,-)
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS ChangeLog COPYING README
%attr(0755,root,root) %{_bindir}/patch
%attr(0755,root,root) %{_mandir}/man1/patch.1*


%changelog
* Sat Oct 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.13-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2)
