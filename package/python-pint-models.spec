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
%{?sle15_python_module_pythons}

Name:           python-pint-models
Version:        0.0.1
Release:        0
Summary:        Contains a set of models and utilites for SUSE Pint Server
License:        Apache-2.0
URL:            https://github.com/SUSE-Enceladus/public-cloud-info-models
Source:         pint-models-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module SQLAlchemy}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module wheel}
Requires:       python-SQLAlchemy
BuildArch:      noarch
%python_subpackages

%description
Contains a set of models and utilites for SUSE Pint Server.

%prep
%autosetup -n pint-models-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files %{python_files}
%defattr(-,root,root)
%license LICENSE
%doc CHANGES.md README.md
%{python_sitelib}/*

%changelog

