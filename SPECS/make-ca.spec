%if 0%{?!_unitdir:1} == 1
%global _unitdir /usr/lib/systemd/system
%endif

%global certdata_date 20241020
%if 0%{?libresslAPI:1} == 1
%global __openssl %{_bindir}/libressl
%else
%if 0%{?!__openssl:1} == 1
%global __openssl %{_bindir}/openssl
%endif
%endif

Name:     make-ca
Version:  1.14
Release:  %{?repo}0.rc2%{?dist}
Summary:  Maintains PKI certificate store
BuildArch: noarch

Group:    System Administration/Utilities
License:  MIT, GPLv3
URL:      https://github.com/lfs-book/make-ca
Source0:  https://github.com/lfs-book/make-ca/archive/v%{version}/make-ca-%{version}.tar.gz
Source1:  certdata-%{certdata_date}.txt
#Patch0:   make-ca-1.14-libressl.patch
Patch0:   make-ca-1.14-curl.patch

Requires: %{__openssl}
Requires: %{_bindir}/curl
Requires: /bin/mktemp
Requires: %{_bindir}/certutil
Requires: %{_bindir}/trust
Requires: %{_bindir}/md5sum
Requires(post): %{_bindir}/libressl
Requires(post): %{_bindir}/curl
Requires(post): /bin/mktemp
Requires(post): %{_bindir}/certutil
Requires(post): %{_bindir}/trust
Requires(post): %{_bindir}/md5sum
Requires(post): %{_sysconfdir}/make-ca/certdata-dist.txt

%description
This package maintains the PKI certificate bundles needed to establish a chain
of trust between a signed certificate and the certificate authority that signed
the certificate. The trust list can be configured by a system administrator with
root privileges, although in most cases that is not needed.

%package -n pki-certdata
Group: System Administration/Utilities
Summary: A default certdata.txt file from Mozilla.
Version: %{certdata_date}
BuildArch: noarch

%description -n pki-certdata
This package contains a default certdata.txt file that can be
used to generate the initial certificate bundle. The version is
the date the certdata.txt file was retrieved, which is likely
different than the date it was first published.

The file is installed as:
  %{_sysconfdir}/make-ca/certdata-dist.txt 


%prep
%setup -q
%patch 0 -p1
%if 0%{?libresslAPI:1} == 1
sed -i 's?openssl x509?libressl x509?g' copy-trust-modifications
sed -i 's?openssl x509?libressl x509?g' include.h2m
sed -i 's?openssl x509?libressl x509?g' update-mscertsign.sh
sed -i 's?openssl x509?libressl x509?g' README
%endif
sed -i 's?/usr/bin/openssl?%{__openssl}?g' make-ca
sed -i 's?/usr/bin/openssl?%{__openssl}?g' make-ca.conf.dist
cp %{SOURCE1} ./certdata-dist.txt


%build


%install
make install DESTDIR=%{buildroot}
install -d -m755 %{buildroot}%{_sysconfdir}/ssl/certs
install -d -m755 %{buildroot}%{_sysconfdir}/ssl/csr
install -d -m755 %{buildroot}%{_sysconfdir}/ssl/local
install -m644 certdata-dist.txt %{buildroot}%{_sysconfdir}/make-ca

%post
if [ ! -f %{_sysconfdir}/ssl/certdata.txt ]; then
  cp -p %{_sysconfdir}/make-ca/certdata-dist.txt %{_sysconfdir}/ssl/certdata.txt
  # generate initial certificate bundles
  %{_sbindir}/make-ca -r ||:
fi


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/ssl
%dir %{_sysconfdir}/ssl/certs
%dir %{_sysconfdir}/ssl/csr
%dir %{_sysconfdir}/ssl/local
%dir %{_sysconfdir}/make-ca
%attr(0644,root,root) %{_sysconfdir}/make-ca/CS.txt
%attr(0644,root,root) %{_sysconfdir}/make-ca/make-ca.conf.dist
%exclude %{_sysconfdir}/make-ca/mozilla-ca-root.pem
%dir %{_libexecdir}/make-ca
%attr(0700,root,root) %{_libexecdir}/make-ca/copy-trust-modifications
%attr(0755,root,root) %{_sbindir}/make-ca
%attr(0644,root,root) %config(noreplace) %{_unitdir}/update-pki.service
%attr(0644,root,root) %config(noreplace) %{_unitdir}/update-pki.timer
%attr(0644,root,root) %{_mandir}/man8/make-ca.8*
%license LICENSE LICENSE.GPLv3 LICENSE.MIT
%doc CHANGELOG README LICENSE LICENSE.GPLv3 LICENSE.MIT

%files -n pki-certdata
%defattr(0644,root,root)
%dir %{_libexecdir}/make-ca
%{_sysconfdir}/make-ca/certdata-dist.txt


%changelog
* Sun Oct 27 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.14-0.rc2
- Make spec file portable, so it works on systems without /usr/bin/libressl
-   but that do have /usr/bin/openssl
- Remove the proxy switch that does not work with curl
- Separate default certdata.txt file into a different package so it can be
    updated separately as needed or even uninstalled.

* Sun Oct 20 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.14-0.rc1
- Initial RPM spec file for YJL 6.6 (LFS 12.2)
