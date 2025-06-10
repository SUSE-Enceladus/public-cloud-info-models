#
# spec file for package python-pint-models
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define upstream_name pint-models
%if 0%{?suse_version} >= 1600
%define pythons %{primary_python}
%else
%{?sle15_python_module_pythons}
%endif
%global _sitelibdir %{%{pythons}_sitelib}

Name:           python-pint-models
Version:        0.2.0
Release:        0
Summary:        Contains a set of models and utilites for SUSE Pint Server
License:        Apache-2.0
URL:            https://github.com/SUSE-Enceladus/public-cloud-info-models
Source:         pint-models-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  %{pythons}-SQLAlchemy
BuildRequires:  %{pythons}-psycopg2
BuildRequires:  %{pythons}-pip
BuildRequires:  %{pythons}-setuptools
BuildRequires:  %{pythons}-wheel
Requires:       %{pythons}-SQLAlchemy
Requires:       %{pythons}-psycopg2
BuildArch:      noarch

%description
Contains a set of models and utilites for SUSE Pint Server

%prep
%autosetup -n pint-models-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root)
%license LICENSE
%doc CHANGES.md README.md
%{_sitelibdir}/*

%changelog
