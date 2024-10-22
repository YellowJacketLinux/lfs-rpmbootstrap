## FIXME - as it, it works, but I think it needs
#   a postun (or preun?) scriplet that uses
#   xmlcatalog --del rather than owning the
#   catalog files, and a few other things, to be
#   a robust package that plays well with others.

%if 0%{?!__xmlcatalog:1} == 1
%global __xmlcatalog %{_bindir}/xmlcatalog
%endif

Name:     docbook-xml
Version:  4.5
Release:	%{?repo}0.rc1%{?dist}
Summary:  General purpose XML and SGML document type
BuildArch: noarch

Group:    Applications/Publishing
License:  Unspecified
URL:      https://docbook.org/
Source0:  https://www.docbook.org/xml/4.5/docbook-xml-4.5.zip

Requires(post): %{__xmlcatalog}

%description
DocBook is a schema (available in several languages including RELAX NG, SGML and
XML DTDs, and W3C XML Schema) maintained by the DocBook Technical Committee of
OASIS. It is particularly well suited to books and papers about computer
hardware and software (though it is by no means limited to these applications).

Because it is a large and robust schema, and because its main structures
correspond to the general notion of what constitutes a "book," DocBook has been
adopted by a large and growing community of authors writing books of all kinds.
DocBook is supported "out of the box" by a number of commercial tools, and there
is rapidly expanding support for it in a number of free software environments.
These features have combined to make DocBook a generally easy to understand,
widely useful, and very popular schema. Dozens of organizations are using
DocBook for millions of pages of documentation, in various print and online
formats, worldwide.


%prep
%setup -c


%build


%install
install -d -m755 %{buildroot}%{_datadir}/xml/docbook/xml-dtd-4.5
install -d -m755 %{buildroot}%{_sysconfdir}/xml
touch %{buildroot}%{_sysconfdir}/xml/docbook
touch %{buildroot}%{_sysconfdir}/xml/catalog
cp -af docbook.cat *.dtd ent/ *.mod \
    %{buildroot}%{_datadir}/xml/docbook/xml-dtd-4.5


%post
if [ ! -e %{_sysconfdir}/xml/docbook ]; then
    %{__xmlcatalog} --noout --create %{_sysconfdir}/xml/docbook ||:
fi
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.5//EN" \
    "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/calstblx.dtd" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/soextblx.dtd" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/dbpoolx.mod" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/dbhierx.mod" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML HTML Tables V4.5//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/htmltblx.mod" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/dbnotnx.mod" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/dbcentx.mod" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5/dbgenent.mod" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5" \
    %{_sysconfdir}/xml/docbook ||:
%{__xmlcatalog} --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5" \
    %{_sysconfdir}/xml/docbook ||:
if [ ! -e %{_sysconfdir}/xml/catalog ]; then
    %{__xmlcatalog} --noout --create %{_sysconfdir}/xml/catalog ||:
fi
%{__xmlcatalog} --noout --add "delegatePublic" \
    "-//OASIS//ENTITIES DocBook XML" \
    "file://%{_sysconfdir}/xml/docbook" \
    %{_sysconfdir}/xml/catalog ||:
%{__xmlcatalog} --noout --add "delegatePublic" \
    "-//OASIS//DTD DocBook XML" \
    "file://%{_sysconfdir}/xml/docbook" \
    %{_sysconfdir}/xml/catalog ||:
%{__xmlcatalog} --noout --add "delegateSystem" \
    "http://www.oasis-open.org/docbook/" \
    "file://%{_sysconfdir}/xml/docbook" \
    %{_sysconfdir}/xml/catalog ||:
%{__xmlcatalog} --noout --add "delegateURI" \
    "http://www.oasis-open.org/docbook/" \
    "file://%{_sysconfdir}/xml/docbook" \
    %{_sysconfdir}/xml/catalog ||:
for DTDVERSION in 4.1.2 4.2 4.3 4.4; do
  %{__xmlcatalog} --noout --add "public" \
    "-//OASIS//DTD DocBook XML V$DTDVERSION//EN" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" \
    %{_sysconfdir}/xml/docbook ||:
  %{__xmlcatalog} --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5" \
    %{_sysconfdir}/xml/docbook ||:
  %{__xmlcatalog} --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file://%{_datadir}/xml/docbook/xml-dtd-4.5" \
    %{_sysconfdir}/xml/docbook ||:
  %{__xmlcatalog} --noout --add "delegateSystem" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file://%{_sysconfdir}/xml/docbook" \
    %{_sysconfdir}/xml/catalog ||:
  %{__xmlcatalog} --noout --add "delegateURI" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file://%{_sysconfdir}/xml/docbook" \
    %{_sysconfdir}/xml/catalog ||:
done

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/xml
%ghost %{_sysconfdir}/xml/docbook
%ghost %{_sysconfdir}/xml/catalog
%dir %{_datadir}/xml
%dir %{_datadir}/xml/docbook
%dir %{_datadir}/xml/docbook/xml-dtd-%{version}
%attr(0644,root,root) %{_datadir}/xml/docbook/xml-dtd-%{version}/*.cat
%attr(0644,root,root) %{_datadir}/xml/docbook/xml-dtd-%{version}/*.dtd
%attr(0644,root,root) %{_datadir}/xml/docbook/xml-dtd-%{version}/*.mod
%dir %{_datadir}/xml/docbook/xml-dtd-%{version}/ent
%attr(0644,root,root) %{_datadir}/xml/docbook/xml-dtd-%{version}/ent/README
%attr(0644,root,root) %{_datadir}/xml/docbook/xml-dtd-%{version}/ent/*.ent
%doc README 



%changelog
* Tue Oct 22 2024 Michael A. Peters <anymouseprophet@gmail.com> - 4.5-0.rc1
- Initial RPM spec file for YJL 6.6 (LFS 12.2)
