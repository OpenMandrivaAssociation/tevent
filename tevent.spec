%define teventmajor	0
%define epoch 1

%define libtevent %mklibname tevent %teventmajor
%define teventdevel %mklibname -d tevent

Name: tevent
URL: http://tevent.samba.org/
License: GPLv3
Version: 0.9.8
# Shipped in samba4 without internal version:
Epoch: %epoch
Release: %mkrel 3
Group: System/Libraries
Summary: Samba4's event management library
Source: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz
Source1: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz.asc
Patch1: samba4-fix-tevent-link-order.patch
BuildRequires: talloc-devel
BuildRoot: %{_tmppath}/%{name}-root

%description
Tevent is an event system based on the talloc memory management library. It is
the core event system used in Samba. Tevent has support for many event types,
including timers, signals, and the classic file descriptor events. Tevent also
provide helpers to deal with asynchronous code providing the tevent_req (Tevent
Request) functions. 

%package -n %libtevent
Group: System/Libraries
Summary: Samba4's event management library

%description -n %libtevent
Samba4's event management library

%package -n %teventdevel
Group: Development/C
Summary: Development files for Samba4's event management library
Provides: tevent-devel = %{epoch}:%{version}-%{release}
Requires: %libtevent = %{epoch}:%{version}-%{release}

%description -n %teventdevel
Development files for Samba4's event management library

%prep
%setup -q
%patch1 -p3 -b .linkorder

%build
%configure
%make

%install
rm -Rf %{buildroot}
%makeinstall_std
ln -s libtevent.so.%{teventmajor} %{buildroot}/%{_libdir}/libtevent.so

%clean
rm -Rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libtevent} -p /sbin/ldconfig
%postun -n %{libtevent} -p /sbin/ldconfig
%endif

%files -n %libtevent
%defattr(-,root,root)
%{_libdir}/libtevent.so.%{teventmajor}*

%files -n %teventdevel
%defattr(-,root,root)
%{_libdir}/libtevent.so
%{_libdir}/libtevent.a
%{_includedir}/tevent.h
#%{_includedir}/tevent_internal.h
%{_libdir}/pkgconfig/tevent.pc
