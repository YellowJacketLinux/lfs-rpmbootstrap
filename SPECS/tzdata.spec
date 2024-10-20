%if 0%{!?__zic:1} == 1
%global __zic %{_sbindir}/zic
%endif

Name:		tzdata
Version:	2024b
Release:	%{?repo}0.rc2%{?dist}
Summary:	Timezone data
BuildArch: noarch

Group:		System Environment/Base
License:	Public Domain
URL:		  https://www.iana.org/time-zones
Source0:	https://data.iana.org/time-zones/releases/tzdata2024b.tar.gz

BuildRequires: %{__zic}

%description
This package contains rules for time zones throughout the world.

%prep
%setup -c


%build


%install
ZONEINFO=%{_datadir}/zoneinfo
%{__install} -d %{buildroot}/${ZONEINFO}

for tz in etcetera southamerica northamerica europe africa antarctica \
          asia australasia backward; do
  %{__zic} -L /dev/null   -d %{buildroot}/${ZONEINFO}     ${tz}
  %{__zic} -L /dev/null   -d %{buildroot}/$ZONEINFO/posix ${tz}
  %{__zic} -L leapseconds -d %{buildroot}/$ZONEINFO/right ${tz}
done

%{__install} -m644 zone.tab %{buildroot}/${ZONEINFO}
%{__install} -m644 zone1970.tab %{buildroot}/${ZONEINFO}
%{__install} -m644 zone.tab %{buildroot}/${ZONEINFO} 

%{__zic} -d %{buildroot}/${ZONEINFO} -p America/New_York
unset ZONEINFO

%files
%defattr(-,root,root,-)
%doc README LICENSE SECURITY theory.html
%{_datadir}/zoneinfo



%changelog
* Fri Oct 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2024b-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2)
