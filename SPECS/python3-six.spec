%global dnlhash 71/39/171f1c67cd00715f190ba0b100d606d440a28c93c7714febeca8b79af85e

Name:     python3-six
Version:  1.16.0
Release:  %{?repo}0.rc1%{?dist}
Summary:  Python wheel packaging standard 
BuildArch:  noarch

Group:    Development/Python
License:  MIT
URL:      https://github.com/benjaminp/six
Source0:  https://files.pythonhosted.org/packages/%{dnlhash}/six-%{version}.tar.gz

%if 0%{?python3_API:1} == 1
# Non-Standard Macro
Requires: %{python3_API}
%endif

%description
Six is a Python 2 and 3 compatibility library. It provides utility functions for
smoothing over the differences between the Python versions with the goal of
writing Python code that is compatible on both Python versions. See the
documentation for more information on what is provided.

Six supports Python 2.7 and 3.3+. It is contained in only one Python file, so it
can be easily copied into your project. (The copyright and license notice must be
retained.)


%prep
%setup -q -n six-%{version}


%build
#PYTHONPATH=src %%{__pip3} wheel -w dist --no-build-isolation --no-deps $PWD
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py build --executable="%{python3} -s"


%install
#DESTDIR=%%{buildroot} %%{__pip3} install --no-index --find-links=dist wheel
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py install -O1 --skip-build --root %{buildroot}


%files
%defattr(-,root,root,-)
%{python3_sitelib}/six.py
%{python3_sitelib}/six-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/__pycache__/*.pyc
%license LICENSE
%doc LICENSE README.rst


%changelog
* Mon Oct 21 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.16.0-0.rc1
- Initial package for YJL 6.6 (LFS 12.2)
