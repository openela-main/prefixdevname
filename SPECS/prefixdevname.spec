Name:           prefixdevname
Version:        0.1.0
Release:        6%{?dist}
Summary:        Udev helper utility that provides network interface naming using user defined prefix

License:        MIT
URL:            https://www.github.com/msekletar/prefixdevname
Source0:        https://github.com/msekletar/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz

Patch0001:      0001-udev-assign-new-name-to-the-interface-directly-and-d.patch
Patch0002:      0002-dracut-introduce-new-dracut-module-prefixdevname-too.patch
Patch0003:      0003-core-don-t-rename-interfaces-that-already-have-the-n.patch
Patch0004:      0004-core-if-interface-already-has-name-in-expected-forma.patch
Patch0005:      0005-core-don-t-assign-names-to-virtual-network-devices.patch

Patch0999:      0999-sema-fix-cast-needed-to-build-with-rust-1.26.patch

ExclusiveArch: %{rust_arches}

BuildRequires:  rust-toolset
BuildRequires:  git
BuildRequires:  systemd-devel

%description
This package provides udev helper utility that tries to consistently name all ethernet NICs using
user defined prefix (e.g. net.ifnames.prefix=net produces NIC names net0, net1, ...). Utility is
called from udev rule and it determines NIC name and writes out configuration file for udev's
net_setup_link built-in (e.g. /etc/systemd/network/71-net-ifnames-prefix-net0.link).

%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%ifarch s390 s390x ppc %{power64} aarch64
%patch999 -p1 -b .cast
%endif

%cargo_prep -V 1

%build
%cargo_build

%install
%make_install

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{_prefix}/lib/udev/%{name}
%{_prefix}/lib/udev/rules.d/*.rules
%dir %{_prefix}/lib/dracut/modules.d/71%{name}
%{_prefix}/lib/dracut/modules.d/71%{name}/*
%dir %{_prefix}/lib/dracut/modules.d/71%{name}-tools
%{_prefix}/lib/dracut/modules.d/71%{name}-tools/*

%changelog
* Wed Dec 19 2018 Michal Sekletár <msekleta@redhat.com> - 0.1.0-6
- rebuild with non-SCL toolset

* Mon Nov 05 2018 Michal Sekletár <msekleta@redhat.com> - 0.1.0-5
- if interface has name in expected format print it to stdout (#1643515)
- don't assign names to virtual devices (#1644294)

* Fri Sep 21 2018 Michal Sekletár <msekleta@redhat.com> - 0.1.0-4
- never rename interfaces that already have names in expected format (#1631650)

* Wed Sep 12 2018 Michal Sekletár <msekleta@redhat.com> - 0.1.0-3
- dracut: introduce new dracut module that includes prefixdevname to initrd.img

* Tue Aug 14 2018 Michal Sekletár <msekleta@redhat.com> - 0.1.0-2
- udev: assign new name to the interface directly by assigning to NAME

* Wed Aug 08 2018 Michal Sekletar <msekleta@redhat.com> - 0.1.0-1
- initial package
