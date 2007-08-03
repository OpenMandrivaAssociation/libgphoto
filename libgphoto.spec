##### GENERAL STUFF #####

%define name	libgphoto
%define version	2.4.0
%define release	%mkrel 2

%define major		2
%define libname		%mklibname gphoto %{major}
%define develname	%mklibname gphoto -d

# Enable debug mode
%define debug 0

%define extraversion %nil

Summary:	Library to access digital cameras
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL+ and GPLv2 and (LGPL+ or BSD-like)
Group:		Graphics


##### SOURCE FILES #####

Source: http://heanet.dl.sourceforge.net/sourceforge/gphoto/%{name}%{major}-%{version}%{?extraversion:%extraversion}.tar.bz2

##### PATCHES #####

# Support for dynamic
Patch2: libgphoto2-2.1.6-dynamic.patch

# Remove signatures for Pentax Optio 450
Patch10: libgphoto2-2.4.0-pentax.patch

##### ADDITIONAL DEFINITIONS #####

Url: http://sourceforge.net/projects/gphoto/
BuildRoot: %{_tmppath}/%{name}-buildroot
Obsoletes:	hackgphoto2
Provides:	hackgphoto2
Conflicts:	gphoto2 <= 2.1.0
BuildRequires:	glib-devel libusb-devel >= 0.1.6 zlib-devel findutils perl
BuildRequires:	libexif-devel
BuildRequires:	udev-tools
BuildRequires:	libltdl-devel libhal-devel >= 0.5 libjpeg-devel



##### SUB-PACKAGES #####

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
Requires:	%{name}-common >= 2.2.1-7mdv2007.0
Provides:	%{name} = %{version}-%{release}
Conflicts:	gphoto2 <= 2.1.0
Conflicts:	%{libname}-devel < 2.2.1-9mdv2007.0
Group:		Graphics

%description -n %{libname}
This library contains all the functionality to access to modern digital
cameras via USB or the serial port.

%package common
Summary:	Platform-independent files for the "%{libname}" library
Group:		Graphics
Conflicts:	%{libname} <= 2.2.1-6mdv2007.0

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

%description hotplug
This package contains the scripts necessary for hotplug support.



##### PREP #####

%prep

%setup -q -n %{name}%{major}-%{version}%{?extraversion:%extraversion}

%patch2 -p1 -b .dynamic
%patch10 -p1 -b .pentax

##### BUILD #####

%build

%if %debug
export DONT_STRIP=1
CFLAGS="`echo %optflags |sed -e 's/-O3/-g/'`" CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/'`"
%endif
%configure2_5x --disable-rpath --with-doc-dir=%{_docdir}/%{libname}

%make

##### INSTALL #####

%install
rm -rf ${RPM_BUILD_ROOT}

%if %debug
export DONT_STRIP=1
%endif

%makeinstall_std

# Fix up libtool libraries.
find $RPM_BUILD_ROOT -name '*.la' | \
	xargs perl -p -i -e "s|$RPM_BUILD_ROOT||g"

# we should move that into the proper Makefile.am eventually
install -d -m755 %{buildroot}/etc/udev/agents.d/usb
install -m755 packaging/linux-hotplug/usbcam.console %{buildroot}/etc/udev/agents.d/usb/usbcam

# Create HAL FDI file
install -d -m755 %{buildroot}/usr/share/hal/fdi/information/20thirdparty/
	export LIBDIR=%{buildroot}%{_libdir}
	export CAMLIBS=%{buildroot}%{_libdir}/libgphoto2/2.4.0
	export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
	%{buildroot}%{_libdir}/libgphoto2/print-camera-list hal-fdi | \
	grep -v "<!-- This file was generated" \
	> %{buildroot}/%{_datadir}/hal/fdi/information/20thirdparty/10-camera-libgphoto2.fdi

# Create udev rules file
install -d -m755 %{buildroot}/etc/udev/rules.d/
	export LIBDIR=%{buildroot}%{_libdir}
	export CAMLIBS=%{buildroot}%{_libdir}/libgphoto2/2.4.0
	export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
	%{buildroot}%{_libdir}/libgphoto2/print-camera-list udev-rules mode 0660 \
	> %{buildroot}/etc/udev/rules.d/90-libgphoto2.rules

%find_lang libgphoto2-2
%find_lang libgphoto2_port-0
cat libgphoto2-2.lang libgphoto2_port-0.lang > %{name}.lang

# Multiarch setup
%multiarch_binaries %buildroot%{_bindir}/gphoto2-config
%multiarch_binaries %buildroot%{_bindir}/gphoto2-port-config

# Don't need to package this
rm -f %{_docdir}/%{libname}/COPYING

##### PRE/POST INSTALL SCRIPTS #####

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

##### CLEAN UP #####

%clean
rm -rf $RPM_BUILD_ROOT


##### FILE LISTS FOR ALL BINARY PACKAGES #####

##### libgphoto-hotplug
%files hotplug
%defattr(-,root,root)
%{_sysconfdir}/udev/rules.d/90-libgphoto2.rules
%{_sysconfdir}/udev/agents.d/usb/usbcam
%{_datadir}/hal/fdi/information/20thirdparty/10-camera-libgphoto2.fdi

##### libgphoto2
%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*
# Here are only ".so" and no ".so.XXX" packages, so the ".so" have to be in
# the main package
%dir %{_libdir}/libgphoto2/*
%dir %{_libdir}/libgphoto2_port/*
%{_libdir}/libgphoto2/*/*.so
%{_libdir}/libgphoto2/*/*.la
%{_libdir}/libgphoto2_port/*/*.so
%{_libdir}/libgphoto2_port/*/*.la
%{_libdir}/udev/check-ptp-camera
%{_libdir}/udev/check-mtp-device

##### libgphoto-common
%files common -f %{name}.lang
%defattr(-,root,root)
%{_datadir}/libgphoto2

##### libgphoto-devel
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
