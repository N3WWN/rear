Summary: Relax and Recover (Rear) is a Linux Disaster Recovery framework
Name: rear
Version: 1.13.0
Release: 1%{?dist}
License: GPLv3
Group: Applications/File
URL: http://rear.github.com/

Source: rear-%{version}.tar.bz2
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch
Requires: binutils
#Requires: cfg2html
#Requires: bacula-mysql
Requires: ethtool
##Requires: genisoimage
Requires: gzip
Requires: iproute
Requires: iputils
#Requires: lsscsi
Requires: mingetty
Requires: mkisofs
Requires: parted
Requires: portmap
### FIXME: Hardcode the OS in /etc/rear/os.conf
###   OS_VENDOR=RedHatEnterpriseServer
###   OS_VERSION=5
##Requires: redhat-lsb
##Requires: rpcbind
### FIXME: Required for Federal Police
#Requires: sg3_utils
Requires: syslinux >= 4.00
Requires: tar
Requires: util-linux

%description
Relax and Recover (abbreviated rear) is a highly modular disaster recovery
framework for GNU/Linux based systems, but can be easily extended to other
UNIX alike systems. The disaster recovery information (and maybe the backups)
can be stored via the network, local on hard disks or USB devices, DVD/CD-R,
tape, etc. The result is also a bootable image that is capable of booting via
PXE, DVD/CD and USB media.

Relax and Recover integrates with other backup software and provides integrated
bare metal disaster recovery abilities to the compatible backup software.

%prep
%setup

echo "30 1 * * * root /usr/sbin/rear checklayout || /usr/sbin/rear mkrescue" >rear.cron

### Add a specific os.conf for RHEL so we do not depend on redhat-lsb
%{?rhel:echo -e "OS_VENDOR=RedHatEnterpriseServer\nOS_VERSION=%{?rhel}" >etc/rear/os.conf}

%build

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__install} -Dp -m0644 rear.cron %{buildroot}%{_sysconfdir}/cron.d/rear
%{__install} -Dp -m0644 etc/udev/rules.d/62-rear-usb.rules %{buildroot}%{_sysconfdir}/udev/rules.d/62-rear-usb.rules

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING README doc/*
%doc %{_mandir}/man8/rear.8*
%config(noreplace) %{_sysconfdir}/cron.d/rear/
%config(noreplace) %{_sysconfdir}/rear/
%config(noreplace) %{_sysconfdir}/udev/rules.d/62-rear-usb.rules
%{_datadir}/rear/
%{_localstatedir}/lib/rear/
%{_sbindir}/rear

%changelog
* Thu Jun 03 2010 Dag Wieers <dag@wieers.com> - 1.7.23-1
- Initial package. (using DAR)