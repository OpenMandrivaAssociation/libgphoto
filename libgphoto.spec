# wine uses libgphoto
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define extraversion %nil
%define sname gphoto2
%define major 6
%define majport 12
%define libname %mklibname %{sname}_ %{major}
%define libport %mklibname %{sname}_port %{majport}
%define devname %mklibname gphoto -d
%define lib32name %mklib32name %{sname}_ %{major}
%define lib32port %mklib32name %{sname}_port %{majport}
%define dev32name %mklib32name gphoto -d

Summary:	Library to access digital cameras
Name:		libgphoto
Version:	2.5.26
Release:	1
License:	LGPL+ and GPLv2 and (LGPL+ or BSD-like)
Group:		Graphics
Url:		http://sourceforge.net/projects/gphoto/
Source0:	http://downloads.sourceforge.net/project/gphoto/%{name}/%{version}/%{name}2-%{version}%{?extraversion:%extraversion}.tar.bz2
Patch0:		libgphoto2-2.5.8-compile.patch

BuildRequires:	findutils
BuildRequires:	perl
BuildRequires:	gd-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	libtool-devel
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(systemd)

%if %{with compat32}
BuildRequires:	devel(libltdl)
BuildRequires:	devel(libexif)
BuildRequires:	devel(libudev)
BuildRequires:	devel(libusb-1.0)
BuildRequires:	devel(libz)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libwebp)
BuildRequires:	devel(libgd)
%endif

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
Platform-independent files for the "%{libname}" library.

%package -n %{devname}
Summary:	Headers and links to compile against the "%{libname}" library
Group:		Development/C
Requires:	%{name}-common >= %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libport} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Library to access to digital cameras (32-bit)
Group:		Graphics

%description -n %{lib32name}
This library contains all the functionality to access to modern digital
cameras via USB or the serial port.

%package -n %{lib32port}
Summary:	Library to access to digital cameras (32-bit)
Group:		Graphics

%description -n %{lib32port}
This library contains all the functionality to access to modern digital
cameras via USB or the serial port.

%package -n %{dev32name}
Summary:	Headers and links to compile against the "%{lib32name}" library (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} >= %{version}-%{release}
Requires:	%{lib32port} >= %{version}-%{release}

%description -n %{dev32name}
This package contains all files which one needs to compile programs using
the "%{lib32name}" library.
%endif

%prep
%autosetup -n lib%{sname}-%{version}%{?extraversion:%extraversion} -p1
autoreconf -fi

export udevscriptdir=/lib/udev

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	udevscriptdir="/lib/udev" \
	--with-drivers=all
cd ..
%endif

mkdir build
cd build
%configure \
	udevscriptdir="/lib/udev" \
	--disable-static \
	--disable-rpath \
	--with-doc-dir=%{_docdir}/%{libname} \
	--with-drivers=all

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libgphoto2_port/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libgphoto2_port/libtool

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

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

# Don't need to package this
rm -f %{buildroot}%{_docdir}/%{libname}/COPYING
rm -f %{buildroot}%{_datadir}/libgphoto2_port/*/vcamera/README.txt

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
%{_docdir}/%{libname}
%doc ABOUT-NLS ChangeLog MAINTAINERS TESTERS
%optional %doc %{_docdir}/libgphoto2
%optional %doc %{_docdir}/libgphoto2_port

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libgphoto2.so.%{major}*
%{_prefix}/lib/libgphoto2

%files -n %{lib32port}
%{_prefix}/lib/libgphoto2_port.so.%{majport}*
%{_prefix}/lib/libgphoto2_port

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%endif
