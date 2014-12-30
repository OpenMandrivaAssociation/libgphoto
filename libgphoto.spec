%define extraversion %nil
%define sname gphoto2
%define major 6
%define majport 12
%define libname %mklibname %{sname}_ %{major}
%define libport %mklibname %{sname}_port %{majport}
%define devname %mklibname gphoto -d


Summary:	Library to access digital cameras
Name:		libgphoto
Version:	2.5.6
Release:	1
License:	LGPL+ and GPLv2 and (LGPL+ or BSD-like)
Group:		Graphics
Url:		http://sourceforge.net/projects/gphoto/
Source0:	http://downloads.sourceforge.net/project/gphoto/%{name}/%{version}/%{name}2-%{version}%{?extraversion:%extraversion}.tar.bz2

BuildRequires:	findutils
BuildRequires:	perl
BuildRequires:	gd-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	libtool-devel
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(lockdev)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	systemd
Requires:		lockdev

%description
The gPhoto2 project is a universal, free application and library
framework that lets you download images from several different
digital camera models, including the newer models with USB
connections. Note that
a) for some older camera models you must use the old "gphoto" package.
b) for USB mass storage models you must use the driver in the kernel

This package contains the library that digital camera applications
can use.

Frontends (GUI and command line) are available separately.

%package -n %{libname}
Summary:	Library to access to digital cameras
Group:		Graphics
Provides:	%{name} = %{version}-%{release}
Suggests:	%{name}-common = %{EVRD}
Obsoletes:	%{_lib}gphoto6 < 2.5.1.1-2

%description -n %{libname}
This library contains all the functionality to access to modern digital
cameras via USB or the serial port.

%package -n %{libport}
Summary:	Library to access to digital cameras
Group:		Graphics
Conflicts:	%{_lib}gphoto6 < 2.5.1.1-2

%description -n %{libport}
This library contains all the functionality to access to modern digital
cameras via USB or the serial port.

%package common
Summary:	Non-library files for the "%{libname}" library
Group:		Graphics

%description common
Platform-independent files for the "%{libname}" library

%package -n %{devname}
Summary:	Headers and links to compile against the "%{libname}" library
Group:		Development/C
Requires:	%{name}-common >= %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libport} >= %{version}-%{release}
Requires:	multiarch-utils
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%prep
%setup -qn lib%{sname}-%{version}%{?extraversion:%extraversion}
%apply_patches

%build
autoreconf -fi

export udevscriptdir=/lib/udev
%configure \
	--disable-static \
	--disable-rpath \
	--with-doc-dir=%{_docdir}/%{libname} \
	--disable-resmgr \
	--disable-baudboy \
	--disable-ttylock

%make

%install
%makeinstall_std

# obsolete with recent udev or hal
rm -f %{buildroot}/lib/udev/check-ptp-camera \
      %{buildroot}/lib/udev/check-mtp-device


# # Output udev rules for device identification; this is used by GVfs gphoto2
# backend and others.
#
# Btw, since it's /lib/udev, never e.g. /lib64/udev, we hardcode the path
#
mkdir -p %{buildroot}/lib/udev/rules.d
LD_LIBRARY_PATH=%{buildroot}/%{_libdir} %{buildroot}%{_libdir}/libgphoto2/print-camera-list udev-rules version 136 > %{buildroot}/lib/udev/rules.d/40-libgphoto2.rules

%find_lang libgphoto2-6
%find_lang libgphoto2_port-12
cat libgphoto2-6.lang libgphoto2_port-12.lang > %{name}.lang

# Multiarch setup
%multiarch_binaries %{buildroot}%{_bindir}/gphoto2-config

%multiarch_binaries %{buildroot}%{_bindir}/gphoto2-port-config

# Don't need to package this
rm -f %{buildroot}%{_docdir}/%{libname}/COPYING

%files -n %{libname}
%{_libdir}/libgphoto2.so.%{major}*

%files -n %{libport}
%{_libdir}/libgphoto2_port.so.%{majport}*

%files common -f %{name}.lang
%{_datadir}/libgphoto2
%{_libdir}/libgphoto2
%{_libdir}/libgphoto2_port
/lib/udev/rules.d/40-libgphoto2.rules

%files -n %{devname}
%{_bindir}/*
%{_includedir}/gphoto2
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*
%docdir %{_docdir}/%{libname}
%{_docdir}/%{libname}
%doc ABOUT-NLS ChangeLog HACKING MAINTAINERS TESTERS

