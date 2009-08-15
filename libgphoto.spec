%define name	libgphoto
%define version	2.4.6
%define release	%mkrel 2

%define major		2
%define libname		%mklibname gphoto %{major}
%define develname	%mklibname gphoto -d


%define extraversion %nil

Summary:	Library to access digital cameras
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL+ and GPLv2 and (LGPL+ or BSD-like)
Group:		Graphics
Source0: 	http://heanet.dl.sourceforge.net/sourceforge/gphoto/%{name}%{major}-%{version}%{?extraversion:%extraversion}.tar.bz2
# Taken from the old patch2: do it as a source now as we don't want to
# use any part of the upstream file any more
Source1:	usbcam_agent
Patch0:		libgphoto2-2.4.5-fix-str-fmt.patch
# (fc) 2.4.0-7mdv handle up to 2048 photos per directory (Mdv bug #39710) (Robin Rosenberg)
Patch13: libgphoto2-2.4.0-increaselimit.patch
URL: http://sourceforge.net/projects/gphoto/
BuildRoot: %{_tmppath}/%{name}-buildroot
Obsoletes:	hackgphoto2
Provides:	hackgphoto2
Conflicts:	gphoto2 <= 2.1.0
BuildRequires:	libusb-devel >= 0.1.6 zlib-devel findutils perl
BuildRequires:	libexif-devel resmgr-devel
BuildRequires:	udev-tools
BuildRequires:	libltdl-devel libhal-devel >= 0.5 libjpeg-devel

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
Requires: 	libusb >= 0.1.5
Requires:	%{name}-common >= 2.4.0-3mdv2008.0
Provides:	%{name} = %{version}-%{release}
Conflicts:	gphoto2 <= 2.1.0
Conflicts:	%{libname}-devel < 2.2.1-9mdv2007.0
Conflicts:	%{name}-common <= 2.4.0-3mdv2008.0
Conflicts:	%{name}-hotplug <= 2.4.0-3mdv2008.0
Group:		Graphics

%description -n %{libname}
This library contains all the functionality to access to modern digital
cameras via USB or the serial port.

%package common
Summary:	Non-library files for the "%{libname}" library
Group:		Graphics
Conflicts:	%{libname} <= 2.4.0-3mdv2008.0

%description common
Platform-independent files for the "%{libname}" library

%package -n %{develname}
Summary:	Headers and links to compile against the "%{libname}" library
Requires: 	%{libname} >= %{version}
Requires:	libexif-devel
Requires:	multiarch-utils
Requires:	libusb-devel >= 0.1.11
Provides:	%{name}-devel = %{version}-%{release}
Provides:	gphoto%{major}-devel = %{version}-%{release}
Conflicts:	gphoto2 <= 2.1.0
Obsoletes:	%{mklibname gphoto 2 -d}
Group:		Development/C

%description -n %{develname}
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%package hotplug
Summary:	Hotplug support from libgphoto
Group:		System/Configuration/Hardware
Requires:	udev
Conflicts:	%{libname} <= 2.4.0-3mdv2008.0

%description hotplug
This package contains the scripts necessary for hotplug support.

%prep
%setup -q -n %{name}%{major}-%{version}%{?extraversion:%extraversion}
%patch0 -p0 -b .str
%patch13 -p1 -b .increaselimit

%build

export udevscriptdir=/lib/udev
%configure2_5x --disable-rpath --with-doc-dir=%{_docdir}/%{libname}

%make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall_std

# remove unused udev helpers, this is now handled by hal
rm -f $RPM_BUILD_ROOT/lib/udev/check-ptp-camera \
      $RPM_BUILD_ROOT/lib/udev/check-mtp-device

# Fix up libtool libraries.
find $RPM_BUILD_ROOT -name '*.la' | \
	xargs perl -p -i -e "s|$RPM_BUILD_ROOT||g"

# we should move that into the proper Makefile.am eventually
install -d -m755 %{buildroot}/etc/udev/agents.d/usb
install -m755 %{SOURCE1} %{buildroot}/etc/udev/agents.d/usb/usbcam

# Create HAL FDI file
install -d -m755 %{buildroot}/usr/share/hal/fdi/information/20thirdparty/
	export LIBDIR=%{buildroot}%{_libdir}
	export CAMLIBS=%{buildroot}%{_libdir}/libgphoto2/%{version}
	export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
	%{buildroot}%{_libdir}/libgphoto2/print-camera-list hal-fdi | \
	grep -v "<!-- This file was generated" \
	> %{buildroot}/%{_datadir}/hal/fdi/information/20thirdparty/10-camera-libgphoto2.fdi

%find_lang libgphoto2-2
%find_lang libgphoto2_port-0
cat libgphoto2-2.lang libgphoto2_port-0.lang > %{name}.lang

# Multiarch setup
%multiarch_binaries %buildroot%{_bindir}/gphoto2-config
%multiarch_binaries %buildroot%{_bindir}/gphoto2-port-config

# Don't need to package this
rm -f %{buildroot}%{_docdir}/%{libname}/COPYING

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files hotplug
%defattr(-,root,root)
%{_sysconfdir}/udev/agents.d/usb/usbcam
%{_datadir}/hal/fdi/information/20thirdparty/10-camera-libgphoto2.fdi

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files common -f %{name}.lang
%defattr(-,root,root)
%{_datadir}/libgphoto2
%{_libdir}/libgphoto2
%{_libdir}/libgphoto2_port

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/gphoto2
%{_libdir}/*.la
%{_libdir}/*.so

%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%docdir %{_docdir}/%{libname}
%{_docdir}/%{libname}

%doc ABOUT-NLS ChangeLog HACKING MAINTAINERS TESTERS
