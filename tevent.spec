%define teventmajor	0
%define beta %nil
%define official 0
%global _python_bytecompile_build 0
# For the python module
%global _disable_ld_no_undefined 1


# Unofficial builds are extracted from the samba4 source tarball using
# cd samba-4.$VERSION
# mkdir -p tevent-%version/lib
# cp -a lib/tevent/* tevent-%version/
# cp -a lib/talloc tevent-%version/lib/
# cp -a lib/replace tevent-%version/lib/
# cp -a buildtools tevent-%version
# tar cf tevent-%version.tar tevent-%version

%define libtevent %mklibname tevent %teventmajor
%define teventdevel %mklibname -d tevent
%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} \
rm -Rf $GNUPGHOME \

Name: tevent
URL: https://tevent.samba.org/
License: GPLv3
Version:	0.15.0
%if "%beta" != ""
Release:	0.%{beta}1
%else
Release:	1
%endif
Group: System/Libraries
Summary: Samba4's event management library
Source0: https://www.samba.org/ftp/tevent/tevent-%{version}.tar.gz
%if %official
Source1: https://www.samba.org/ftp/tevent/tevent-%{version}.tar.asc
Source2: samba-pubkey.asc
%endif
BuildRequires: talloc-devel >= 2.0.6 python-talloc %{_lib}pytalloc-util-devel
BuildRequires: pkgconfig(libtirpc)
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(cmocka) >= 1.1.3

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
Provides: tevent-devel = %{EVRD}
Requires: %libtevent = %{EVRD}

%description -n %teventdevel
Development files for Samba4's event management library

%package -n python-tevent
Group: Development/Python
Summary: Python module for Samba4's event management library

%description -n python-tevent
Python module for Samba4's event management library

%prep
%if %official
VERIFYSOURCE=%{SOURCE0}
VERIFYSOURCE=${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE

%check_sig %{SOURCE2} %{SOURCE1} $VERIFYSOURCE

rm -f $VERIFYSOURCE
%endif

%setup -q
%autopatch -p1

%build
%setup_compile_flags
./configure --prefix=%{_prefix} --libdir=%{_libdir} --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

%make

%install
%makeinstall_std

%files -n %libtevent
%{_libdir}/libtevent.so.%{teventmajor}*

%files -n %teventdevel
%{_libdir}/libtevent.so
%{_includedir}/tevent.h
%{_libdir}/pkgconfig/tevent.pc

%files -n python-tevent
%{py_platsitedir}/_tevent*.so
%{py_platsitedir}/tevent.py
