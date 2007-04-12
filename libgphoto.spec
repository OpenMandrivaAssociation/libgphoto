##### GENERAL STUFF #####

%define major	2
%define libname	%mklibname gphoto %{major}

# Enable debug mode
%define debug 0

#define extraversion rc1
%define extraversion %nil

Summary:	Library to access digital cameras
Name:		libgphoto
Version:	2.3.1
Release:	%mkrel 1
License:	LGPL
Group:		Graphics


##### SOURCE FILES #####

Source: http://heanet.dl.sourceforge.net/sourceforge/gphoto/%{name}%{major}-%{version}%{?extraversion:%extraversion}.tar.bz2
#Source: http://sourceforge.net/projects/gphoto/%{name}2-cvs20030829.tar.bz2

##### PATCHES #####

# Support for dynamic
Patch2: libgphoto2-2.1.6-dynamic.patch

# Remove signatures for Pentax Optio 450
Patch10: libgphoto2-2.1.6-pentax.patch

# Remote capture on Canon EOS 5D and other DIGIC II Canon DSLRs
Patch20: http://www.booyaka.com/~paul/libgphoto2/eos5d/a01_start_end_remote_control.patch
Patch21: http://www.booyaka.com/~paul/libgphoto2/eos5d/a02_add_capture_size_class.patch
Patch22: http://www.booyaka.com/~paul/libgphoto2/eos5d/a03_add_eos_5d_usb_id.patch
Patch23: b01_add_canon_usb_dialogue_full.patch
Patch24: b02_add_canon_control_dialogue.patch
Patch25: b03_add_get_release_params.patch
Patch26: c01_add_set_release_params.patch
Patch27: d01_add_secondary_image_support.patch
Patch28: e01_return_photographic_status.patch
Patch29: f01_fast_camera_identify.patch
Patch30: f02_hub_svn_changelog.patch
Patch31: h01_fix_warnings.patch
Patch32: h02_svn_changelog.patch
Patch33: i01_fix_canon_usb_dialogue_full_debug.patch
Patch34: i02_svn_changelog.patch
Patch35: j01_fix_non_20d_compile_failure.patch
Patch36: j02_svn_changelog.patch
# (fc) 2.2.1-4mdv allow bootstrapping package
Patch37: libgphoto2-2.2.1-bootstrap.patch
# (fc) 2.2.1-6mdv don't use deprecated dbus api
Patch38: libgphoto2-2.2.1-deprecated.patch

##### ADDITIONAL DEFINITIONS #####

Url: http://sourceforge.net/projects/gphoto/
BuildRoot: %{_tmppath}/%{name}-buildroot
Obsoletes:	hackgphoto2
Provides:	hackgphoto2
Conflicts:	gphoto2 <= 2.1.0
BuildRequires:	glib-devel libusb-devel >= 0.1.6 zlib-devel findutils perl
BuildRequires:	libexif-devel
BuildRequires:  autoconf2.5 automake
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

This package contains the library that digital camera applications can use

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

%package -n %{libname}-devel
Summary:	Headers and links to compile against the "%{libname}" library
Requires: 	%{libname} >= %{version}
Requires:	libexif-devel
Requires:	multiarch-utils
Requires:	libusb-devel >= 0.1.11
Provides:	%{name}-devel = %{version}-%{release}
Provides:	gphoto%{major}-devel = %{version}-%{release}
Conflicts:	gphoto2 <= 2.1.0
Group:		Graphics

%description -n %{libname}-devel
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%package hotplug
Summary:	Hotplug support from libgphoto
Group:		System/Configuration/Hardware
Requires:	udev
#PreReq:		%{libname}

%description hotplug
This package contains the scripts necessary for hotplug support.



##### PREP #####

%prep

export WANT_AUTOCONF_2_5=1

%setup -q -n %{name}%{major}-%{version}%{?extraversion:%extraversion}
#setup -q -n %{name}%{major}

%patch2 -p1 -b .dynamic
%patch10 -p1 -b .pentax

# Needed for CVS version
#./autogen.sh

autoconf
cd libgphoto2_port
autoconf
cd ..



##### BUILD #####

%build

export WANT_AUTOCONF_2_5=1

# update config.{sub,guess}, ltmain.sh scripts
cd libgphoto2_port
libtoolize --copy --force
cd ..

%if %debug
export DONT_STRIP=1
CFLAGS="`echo %optflags |sed -e 's/-O3/-g/'` -DCANON_EXPERIMENTAL_20D" CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/'`" \
%else
CFLAGS="%optflags -DCANON_EXPERIMENTAL_20D" \
%endif
%configure2_5x --with-doc-dir=%{_docdir}/%{name}-%{version} --disable-rpath

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

# convert usermaps to udev rules
mkdir -p $RPM_BUILD_ROOT/etc/udev/rules.d
/usr/sbin/udev_import_usermap --no-modprobe usb %{buildroot}%{_libdir}/libgphoto2/print-usb-usermap | uniq | sed -e 's/SYSFS{idProduct}=="0*\([^"]\+\)", SYSFS{idVendor}=="0*\([^"]\+\)"/ENV{PRODUCT}=="\2\/\1\/*"/g' -e 's/SYSFS{bInterfaceClass}=="06"/ENV{INTERFACE}=="6\/*\/*"/g' > $RPM_BUILD_ROOT/etc/udev/rules.d/70-libgphoto2.rules
rm -f %{buildroot}%{_libdir}/libgphoto2/print-usb-usermap

%find_lang libgphoto2-2
%find_lang libgphoto2_port-0
cat libgphoto2-2.lang libgphoto2_port-0.lang > %{name}.lang

# Install documentation
cp -a ABOUT-NLS AUTHORS COPYING ChangeLog HACKING INSTALL MAINTAINERS NEWS README TESTERS %{buildroot}/usr/share/doc/lib*gphoto*-%{version}/

# Multiarch setup
%multiarch_binaries %buildroot%{_bindir}/gphoto2-config
%multiarch_binaries %buildroot%{_bindir}/gphoto2-port-config



##### PRE/POST INSTALL SCRIPTS #####

%post -n %{libname}
# register libraries
/sbin/ldconfig

%postun -n %{libname}
# unregister libraries
/sbin/ldconfig

##### CLEAN UP #####

%clean
rm -rf $RPM_BUILD_ROOT


##### FILE LISTS FOR ALL BINARY PACKAGES #####

##### libgphoto-hotplug
%files hotplug
%defattr(-,root,root)
%{_sysconfdir}/udev/rules.d/70-libgphoto2.rules
%{_sysconfdir}/udev/agents.d/usb/usbcam

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

##### libgphoto-common
%files common -f %{name}.lang
%defattr(-,root,root)
%{_datadir}/libgphoto2

##### libgphoto2-devel
%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/gphoto2
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/libgphoto2/*/*.a
%{_libdir}/libgphoto2_port/*/*.a

%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%docdir %{_docdir}/lib*gphoto*-%{version}
%{_docdir}/lib*gphoto*-%{version}


##### CHANGELOG #####


