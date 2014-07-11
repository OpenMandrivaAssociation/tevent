%define teventmajor	0
%define beta %nil
%define official 0

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
URL: http://tevent.samba.org/
License: GPLv3
Version: 0.9.20
# Shipped in samba4 without internal version:
Epoch: 1
%if "%beta" != ""
Release: 0.%beta.1
%else
Release: 7
%endif
Group: System/Libraries
Summary: Samba4's event management library
Source0: http://www.samba.org/ftp/tevent/tevent-%{version}.tar.gz
%if %official
Source1: http://www.samba.org/ftp/tevent/tevent-%{version}.tar.asc
Source2: samba-pubkey.asc
%endif
Patch1: samba4-fix-tevent-link-order.patch
BuildRequires: talloc-devel >= 2.0.6 python-talloc pkgconfig(pytalloc-util) >= 2.0.6

%track
prog %name = {
	url = http://www.samba.org/ftp/tevent/
	regex = %name-(__VER__)\.tar\.gz
	version = %version
}

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
#patch1 -p3 -b .linkorder

%build
export PYTHONDIR=%{py_platsitedir}
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
#%{_includedir}/tevent_internal.h
%{_libdir}/pkgconfig/tevent.pc

%files -n python-tevent
%{py_platsitedir}/_tevent.so
%{py_platsitedir}/tevent.py
