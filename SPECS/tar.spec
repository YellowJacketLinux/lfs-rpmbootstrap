%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     tar
Version:  1.35
Release:  %{?repo}0.rc1%{?dist}
Summary:  Archive and restore files and directies
Requires(preun): %{insinfo}
Requires(post): %{insinfo}
BuildRequires: pkgconfig(libacl)

Group:    System Environment/Utilities
License:  GPLv3
URL:      https://gnu.org/software/tar
Source0:  https://ftp.gnu.org/gnu/tar/tar-%{version}.tar.xz


%description
GNU Tar is a program for creating archives of files and for restoring archives
of file structures. Historically such archives were written to a tape drive,
hence the name Tape ARchive. In modern times, a tape drives are almost never
used.

A tar achive is usually called a "tarball" and extracting the archived files is
usually called "unpacking the tarball". Tar itself does not provide any
compression to the archive but tar is usually used in conjunction with a
separate lossless compression utility such as gzip, bzip2, or xz-utils. With GNU
tar, this compression can be applied at the time the archive is created through
option switches to the tar command.


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
make -C doc install-html docdir=%{_datadir}/doc/tar-%{version} \
  DESTDIR=%{buildroot}
%find_lang %{name}

%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/tar
%attr(0755,root,root) %{_libexecdir}/rmt
%attr(0644,root,root) %{_infodir}/%{name}.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/tar.1*
%attr(0644,root,root) %{_mandir}/man8/rmt.8*
%{_datadir}/doc/tar-%{version}/tar.html
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS ChangeLog COPYING README NEWS THANKS


%changelog
* Sat Oct 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.35-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2)
