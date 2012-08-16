%define major 2
%define major_port 0
%define libname %mklibname gphoto %{major}
%define develname %mklibname gphoto -d

%define extraversion %nil

Summary:	Library to access digital cameras
Name:		libgphoto
Version:	2.5.0
Release:	1
License:	LGPL+ and GPLv2 and (LGPL+ or BSD-like)
Group:		Graphics
URL:		http://sourceforge.net/projects/gphoto/
Source0:	http://downloads.sourceforge.net/project/gphoto/%{name}/%{version}/%{name}%{major}-%{version}%{?extraversion:%extraversion}.tar.bz2
Patch0:		libgphoto2-2.5.0-fix-format-errors.patch
Patch1:		libgphoto2-2.5.0-fix-linking.patch
Obsoletes:	hackgphoto2 < %{version}
Provides:	hackgphoto2
Conflicts:	gphoto2 <= 2.1.0
BuildRequires:	libusb-devel >= 0.1.6
BuildRequires:	zlib-devel
BuildRequires:	findutils
BuildRequires:	perl
BuildRequires:	libexif-devel
BuildRequires:	lockdev-devel
BuildRequires:	udev-devel
BuildRequires:	libtool-devel
BuildRequires:	libjpeg-devel
BuildRequires:	gd-devel
BuildRequires:	gettext-devel

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
Requires:	libusb >= 0.1.5
Requires:	%{name}-common = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
Conflicts:	gphoto2 <= 2.1.0
Conflicts:	%{libname}-devel < 2.2.1-9mdv2007.0
Conflicts:	%{name}-common <= 2.4.0-3mdv2008.0
Conflicts:	%{name}-hotplug <= 2.4.0-3mdv2008.0

%description -n %{libname}
This library contains all the functionality to access to modern digital
cameras via USB or the serial port.

%package common
Summary:	Non-library files for the "%{libname}" library
Group:		Graphics
Conflicts:	%{libname} <= 2.4.0-3mdv2008.0
Obsoletes:	%{name}-hotplug <= 2.4.7-2mdv2010.0
Provides:	%{name}-hotplug = %{version}-%{release}

%description common
Platform-independent files for the "%{libname}" library

%package -n %{develname}
Summary:	Headers and links to compile against the "%{libname}" library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Requires:	libexif-devel
Requires:	multiarch-utils
Requires:	libusb-devel >= 0.1.11
Provides:	%{name}-devel = %{version}-%{release}
Provides:	gphoto%{major}-devel = %{version}-%{release}
Conflicts:	gphoto2 <= 2.1.0
Obsoletes:	%{mklibname gphoto 2 -d} < %{version}-%{release}

%description -n %{develname}
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%prep
%setup -q -n %{name}%{major}-%{version}%{?extraversion:%extraversion}
%apply_patches

%build
export udevscriptdir=/lib/udev
%configure2_5x \
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


%find_lang libgphoto2-2
%find_lang libgphoto2_port-0
cat libgphoto2-2.lang libgphoto2_port-0.lang > %{name}.lang

# Multiarch setup
%multiarch_binaries %buildroot%{_bindir}/gphoto2-config

%multiarch_binaries %buildroot%{_bindir}/gphoto2-port-config

# Don't need to package this
rm -f %{buildroot}%{_docdir}/%{libname}/COPYING

# cleanup
rm -f %{buildroot}%{_libdir}/*.la

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/*.so.%{major_port}*

%files common -f %{name}.lang
%{_datadir}/libgphoto2
%{_libdir}/libgphoto2
%{_libdir}/libgphoto2_port
/lib/udev/rules.d/40-libgphoto2.rules

%files -n %{develname}
%{_bindir}/*
%{_includedir}/gphoto2
%{_libdir}/*.so

%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%docdir %{_docdir}/%{libname}
%{_docdir}/%{libname}

%doc ABOUT-NLS ChangeLog HACKING MAINTAINERS TESTERS
