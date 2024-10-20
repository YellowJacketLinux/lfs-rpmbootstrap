Name:     texinfo
Version:  7.1
Release:  %{?repo}0.rc1%{?dist}
Summary:  Text documentation system
BuildRequires: perl
BuildRequires: libunistring-devel

Group:    System Environment/Documentation
License:  GPLv3
URL:      https://www.gnu.org/software/texinfo/
Source0:  https://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz

%description
Texinfo is a documentation system that uses a single source to produce
many forms of output:
- a PDF or DVI document (via the TeX typesetting system) with the normal
  features of a book, including sectioning, cross references, indices, etc.
- an Info file with analogous features
- a plain text (ASCII) file
- HTML output suitable for use with a web browser
- an EPUB 3 e-book
- a LaTeX file, which can then be used to create a PDF
- a Docbook file

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%find_lang texinfo
%find_lang texinfo_document
cat texinfo_document.lang >> texinfo.lang

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log
%else
echo "make check not run during packaging" > %{name}-make.check.log
%endif

%post
for doc in info-stnd texi2any_api texi2any_internals texinfo; do
  %{_bindir}/install-info %{_infodir}/${doc}.info %{_infodir}/dir ||:
done

%preun
if [ $1 = 0 ]; then
for doc in info-stnd texi2any_api texi2any_internals texinfo; do
  %{_bindir}/install-info --delete %{_infodir}/${doc}.info %{_infodir}/dir ||:
done
fi

%files -f texinfo.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/info
%attr(0755,root,root) %{_bindir}/install-info
%attr(0755,root,root) %{_bindir}/pdftexi2dvi
%attr(0755,root,root) %{_bindir}/pod2texi
%attr(0755,root,root) %{_bindir}/texi2any
%attr(0755,root,root) %{_bindir}/texi2dvi
%attr(0755,root,root) %{_bindir}/texi2pdf
%attr(0755,root,root) %{_bindir}/texindex
%{_bindir}/makeinfo
%{_libdir}/texinfo
%dir %{_infodir}
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/info-stnd.info*
%attr(0644,root,root) %{_infodir}/texi2any_api.info*
%attr(0644,root,root) %{_infodir}/texi2any_internals.info*
%attr(0644,root,root) %{_infodir}/texinfo.info*
%attr(0644,root,root) %{_mandir}/man1/info.1*
%attr(0644,root,root) %{_mandir}/man1/install-info.1*
%attr(0644,root,root) %{_mandir}/man1/makeinfo.1*
%attr(0644,root,root) %{_mandir}/man1/pdftexi2dvi.1*
%attr(0644,root,root) %{_mandir}/man1/pod2texi.1*
%attr(0644,root,root) %{_mandir}/man1/texi2any.1*
%attr(0644,root,root) %{_mandir}/man1/texi2dvi.1*
%attr(0644,root,root) %{_mandir}/man1/texi2pdf.1*
%attr(0644,root,root) %{_mandir}/man1/texindex.1*
%attr(0644,root,root) %{_mandir}/man5/info.5*
%attr(0644,root,root) %{_mandir}/man5/texinfo.5*
%{_datadir}/texinfo
%doc AUTHORS COPYING ChangeLog* README*
%license COPYING
%doc %{name}-make.check.log

%changelog
* Sat Oct 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 7.1-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2)
