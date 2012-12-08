%define major 6
%define major_port 10
%define libname %mklibname gphoto %{major}
%define develname %mklibname gphoto -d

%define extraversion %nil

Summary:	Library to access digital cameras
Name:		libgphoto
Version:	2.5.0
Release:	3
License:	LGPL+ and GPLv2 and (LGPL+ or BSD-like)
Group:		Graphics
URL:		http://sourceforge.net/projects/gphoto/
Source0:	http://downloads.sourceforge.net/project/gphoto/%{name}/%{version}/%{name}2-%{version}%{?extraversion:%extraversion}.tar.bz2
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
Obsoletes:	%{mklibname gphoto 2} < 2.5

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
Provides:	libgphoto-devel = %{version}-%{release}
Conflicts:	gphoto2 <= 2.1.0
Obsoletes:	%{mklibname gphoto 2 -d} < %{version}-%{release}

%description -n %{develname}
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%prep
%setup -q -n %{name}2-%{version}%{?extraversion:%extraversion}
%apply_patches

%build
autoreconf -fi

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


%find_lang libgphoto2-6
%find_lang libgphoto2_port-10
cat libgphoto2-6.lang libgphoto2_port-10.lang > %{name}.lang

# Multiarch setup
%multiarch_binaries %{buildroot}%{_bindir}/gphoto2-config

%multiarch_binaries %{buildroot}%{_bindir}/gphoto2-port-config

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


%changelog
* Sat Sep 01 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-3
+ Revision: 816161
- provide libgphoto-devel

* Tue Aug 28 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.5.0-2
+ Revision: 815958
- Bump release and rebuild.

* Sun Aug 26 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-1
+ Revision: 815798
- update major to 6
- drop patch 13
- update to new version 2.5.0
- drop HAL support
- Patch0: fix format strings error
- Patch1: fix linking
- spec file clean

* Tue May 22 2012 Oden Eriksson <oeriksson@mandriva.com> 2.4.14-1
+ Revision: 800083
- 2.4.14
- various fixes

* Tue Apr 10 2012 Götz Waschk <waschk@mandriva.org> 2.4.11-2
+ Revision: 790265
- update build deps
- remove libtool archives

* Wed Apr 20 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.4.11-1
+ Revision: 656325
- rediffed p0 for new version
- new version 2.4.11
- make building with hal a bcond option

* Sat Apr 16 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.10.1-1
+ Revision: 653294
- update to new version 2.4.10.1
- spec file clean

* Thu Sep 23 2010 Funda Wang <fwang@mandriva.org> 2.4.10-1mdv2011.0
+ Revision: 580773
- br gd
- new version 2.4.10

* Fri May 07 2010 Frederic Crozat <fcrozat@mandriva.com> 2.4.9-3mdv2010.1
+ Revision: 543402
- put back HAL fdi files, needed by KDE4

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.4.9-2mdv2010.1
+ Revision: 539589
- rebuild so that shared libraries are properly stripped again

* Fri Apr 16 2010 Frederik Himpe <fhimpe@mandriva.org> 2.4.9-1mdv2010.1
+ Revision: 535689
- Update to new version 2.4.9
- Rediff string format patch

* Mon Jan 25 2010 Frederik Himpe <fhimpe@mandriva.org> 2.4.8-1mdv2010.1
+ Revision: 496349
- Fix running print-camera-list by setting LD_LIBRARY_PATH so it finds
  the library
- Update to new version 2.4.8
- Remove mtp media player patch integrated upstream

  + Emmanuel Andry <eandry@mandriva.org>
    - check majors
    - drop HAL support (should be safe now, ask ubuntu)

* Tue Jan 19 2010 Frederic Crozat <fcrozat@mandriva.com> 2.4.7-6mdv2010.1
+ Revision: 493566
- Switch to lockdev for serial access, resmgr is obsolete

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.7-5mdv2010.1
+ Revision: 488777
- rebuilt against libjpeg v8

* Tue Oct 13 2009 Frederic Crozat <fcrozat@mandriva.com> 2.4.7-4mdv2010.0
+ Revision: 457029
- Update patch13 to 8192 photos
- Patch14 (SVN): fix media player detection (GNOME bug #597585)

* Thu Oct 08 2009 Frederic Crozat <fcrozat@mandriva.com> 2.4.7-3mdv2010.0
+ Revision: 456122
- Obsoletes/Provides libgphoto-hotplug (not libgphoto2-hotplug)

* Mon Oct 05 2009 Frederic Crozat <fcrozat@mandriva.com> 2.4.7-2mdv2010.0
+ Revision: 454182
- Merge hotplug subpackage in common subpackage
- Create and package udev rules for usage with gvfs
- Update patch0 to fix generated udev rules
- Update patch13 to handle 4096 files in one directory (Fedora)

* Sun Aug 23 2009 Frederik Himpe <fhimpe@mandriva.org> 2.4.7-1mdv2010.0
+ Revision: 419899
- Update to new version 2.4.7
- Rediff string format patch

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-2mdv2010.0
+ Revision: 416621
- rebuilt against libjpeg v7

* Mon May 18 2009 Frederik Himpe <fhimpe@mandriva.org> 2.4.6-1mdv2010.0
+ Revision: 377284
- update to new version 2.4.6

* Wed May 06 2009 Funda Wang <fwang@mandriva.org> 2.4.5-1mdv2010.0
+ Revision: 372358
- New version 2.4.5

* Tue Jan 27 2009 Funda Wang <fwang@mandriva.org> 2.4.4-2mdv2009.1
+ Revision: 334557
- rebuild for new libtool

* Thu Jan 22 2009 Funda Wang <fwang@mandriva.org> 2.4.4-1mdv2009.1
+ Revision: 332552
- New version 2.4.4
- n82 patch fixed upstream
- fix str fmt introduced by new flags

* Wed Oct 01 2008 Olivier Blin <blino@mandriva.org> 2.4.2-3mdv2009.0
+ Revision: 290301
- remove unused udev helpers (check-ptp-camera and check-mtp-device)
- drop udev rules file, the devices are now handled by hal (avoid forking useless check-ptp-camera helper)
- fix generating hal-fdi and udev rules (by using correct gphoto version)

* Fri Aug 29 2008 Olivier Blin <blino@mandriva.org> 2.4.2-2mdv2009.0
+ Revision: 277374
- install udev helpers in /lib/udev (this is the default on x86_64 too now, as per upstream)

* Wed Jul 16 2008 Frederic Crozat <fcrozat@mandriva.com> 2.4.2-1mdv2009.0
+ Revision: 236482
- Release 2.4.2
- Patch14: add support for Nokia N82 mobile phone

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 29 2008 Frederik Himpe <fhimpe@mandriva.org> 2.4.1-2mdv2009.0
+ Revision: 213154
- Remove buildrequires glib-devel (which is actually the old glib 1.2): it
  builds perfectly fine without it.

* Thu May 29 2008 Frederic Crozat <fcrozat@mandriva.com> 2.4.1-1mdv2009.0
+ Revision: 212969
- Release 2.4.1
- Remove patches 10 (no longer needed), 11, 12, 14, 15 (merged upstream)

* Wed Apr 02 2008 Frederic Crozat <fcrozat@mandriva.com> 2.4.0-7mdv2008.1
+ Revision: 191605
- Patch13 (Robin Rosenberg): handle up to 2048 photos per directory (Mdv bug #37307)
- Patch14 (SVN): fix FDI file for latest HAL
- Patch15 (SVN): fix udev rule for recent kernels

* Mon Feb 04 2008 Frederic Crozat <fcrozat@mandriva.com> 2.4.0-6mdv2008.1
+ Revision: 162095
- Patch12: dn't append HAL info for Olympus D-535 (Mdv bug #37307)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 20 2007 Frederic Crozat <fcrozat@mandriva.com> 2.4.0-5mdv2008.1
+ Revision: 110685
- Patch11 (SVN): don't reset USB bus for Canon cameras and increse timeout (Mdv bug #35642)

* Fri Nov 09 2007 Adam Williamson <awilliamson@mandriva.org> 2.4.0-4mdv2008.1
+ Revision: 107202
- more useless comments...
- remove a comment line that was causing an rpmlint error. remove all of these useless comments while we're at it.
- comply with lib policy: move all files except proper versioned shared libraries out of the lib package and into -common and -hotplug
- move check-ptp-camera and check-mtp-device to /%%_lib/udev , where they should be (by setting udevscriptdir variable before configure)

* Fri Aug 03 2007 Adam Williamson <awilliamson@mandriva.org> 2.4.0-3mdv2008.0
+ Revision: 58685
- fix bug #22017: since it basically involves dropping the entire upstream file, turn our patch2 into a source and just install it

* Fri Aug 03 2007 Adam Williamson <awilliamson@mandriva.org> 2.4.0-2mdv2008.0
+ Revision: 58680
- fix group for devel package (#28142)

* Fri Aug 03 2007 Adam Williamson <awilliamson@mandriva.org> 2.4.0-1mdv2008.0
+ Revision: 58513
- fix file list again
- actually we need to specify docdir or else it doesn't get lib64-ified
- drop static headers from file list as they're not generated
- generate HAL FDI file, with a little help from Fedora
- use new upstream method of generating udev rules, with a little help from Debian
- no need to specify docdir any more, default matches our new policy
- drop DCANON_EXPERIMENTAL_20D from cflags as it's now default upstream
- drop unnecessary calls to autotools
- new devel policy
- drop unneeded buildrequires on autotools
- drop already unapplied patches:
  * 20 through 36: merged upstream
  * 37: breaks build if re-applied
  * 38: no longer needed
- rediff patch10
- use Fedora licensing policy (licensing on this package is very complex)
- spec clean
- new release 2.4.0


* Sat Dec 30 2006 Pascal Terjan <pterjan@mandriva.org> 2.3.1-1mdv2007.0
+ Revision: 102789
- list new /lib/udev/check-ptp-camera
- 2.3.1
- New release
- Requires libusb-devel, needed by libgphoto2_port.pc

* Tue Dec 05 2006 Jérôme Soyer <saispo@mandriva.org> 2.3.0-1mdv2007.1
+ Revision: 91301
- New release 2.3.0

* Tue Dec 05 2006 Jérôme Soyer <saispo@mandriva.org> 2.2.1-9mdv2007.1
+ Revision: 91065
- Import libgphoto

* Thu Aug 31 2006 Frederic Crozat <fcrozat@mandriva.com> 2.2.1-9mdv2007.0
- Move plugins .la files to main package, it is required by digikam (Mdv bug #22797)

* Wed Aug 30 2006 Frederic Crozat <fcrozat@mandriva.com> 2.2.1-8mdv2007.0
- Update patch37, fix crash in Mdv bug #24405 (don't close shared connection)

* Wed Aug 30 2006 Till Kamppeter <till@mandriva.com> 2.2.1-7mdv2007.0
- Moved translations into libgphoto-common package.

* Thu Aug 10 2006 Frederic Crozat <fcrozat@mandriva.com> 2.2.1-6mdv2007.0
- Patch38: don't use dbus deprecated api (Mdv bug #24154)

* Wed Aug 09 2006 Till Kamppeter <till@mandriva.com> 2.2.1-5mdv2007.0
- Rebuilt again to adapt to API changes in DBUS.

* Wed Aug 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.2.1-4mdv2007.0
- Patch37: allow bootstrapping package
- Rebuild with latest dbus

* Tue Jul 11 2006 Till Kamppeter <till@mandriva.com> 2.2.1-3mdv2007.0
- Moved unversioned/platform-independent files out of the libgphoto2 package.

* Mon Jul 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.2.1-2mdv2007.0
- fix buildrequires
- fix macro-in-%%changelog
- fix prereq-use

* Sat Jul 01 2006 Till Kamppeter <till@mandriva.com> 2.2.1-1mdv2007.0
- Updated to GPhoto2 2.2.1.
- Added remote capture on Canon EOS 5D and other DIGIC II Canon DSLRs
  (patches 20-22).
- Uncompressed patches.

* Wed May 17 2006 Till Kamppeter <till@mandriva.com> 2.1.99-2mdk
- Fixes for building on 64-bit.

* Fri May 12 2006 Till Kamppeter <till@mandriva.com> 2.1.99-1mdk
- Updated to GPhoto2 2.1.99 (Preview of 2.2.x).
- Introduced %%mkrel.

* Thu Dec 29 2005 Frederic Crozat <fcrozat@mandriva.com> 2.1.6-11mdk
- Fix udev rules to remove .desktop file when device are unplugged

* Tue Dec 27 2005 Olivier Blin <oblin@mandriva.com> 2.1.6-10mdk
- update Patch2 to make device removal possible with udev

* Thu Oct 27 2005 Till Kamppeter <till@mandriva.com> 2.1.6-8mdk
- Activated experimental support for the Canon EOS 20D in Canon (not PTP)
  mode.

* Thu Sep 08 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.1.6-8mdk
- lib64 fixes

* Mon Sep 05 2005 Olivier Blin <oblin@mandriva.com> 2.1.6-7mdk
- rebuild for new udev_import_usermap

* Sat Sep 03 2005 Olivier Blin <oblin@mandriva.com> 2.1.6-6mdk
- libgphoto-hotplug: require udev instead of hotplug

* Sat Sep 03 2005 Olivier Blin <oblin@mandriva.com> 2.1.6-5mdk
- fix BuildRequires: udev_import_usermap is now in udev-tools

* Sun Aug 28 2005 Olivier Blin <oblin@mandriva.com> 2.1.6-4mdk
- don't try to load the inexistent "usbcam" module in udev
- move usbcam script to /etc/udev/agents.d/usb/usbcam
- remove hotplug usermaps

* Fri Aug 26 2005 Olivier Blin <oblin@mandriva.com> 2.1.6-3mdk
- convert usermaps to udev rules

* Thu Aug 18 2005 Frederic Lepied <flepied@mandriva.com> 2.1.6-2mdk
- remove signature of Pentax Optio 450

* Tue Jun 28 2005 Till Kamppeter <till@mandrakesoft.com> 2.1.6-1mdk
- Updated to GPhoto2 2.1.6 (Bug fixes, support for newest camera models).
- Removed patch 1 (fixed upstream).

* Wed Mar 16 2005 Till Kamppeter <till@mandrakesoft.com> 2.1.5-2mdk
- Removed "Requires: libgphoto-hotplug" from the libgphoto2 package
  (bug 14416).
- Let libgphoto2 package own the /usr/lib/gphoto2_port and
  /usr/lib/gphoto2_port/0.5.1 directories (bug 14422).
- Let libgphoto2 package also own the /usr/lib/gphoto2 and
  /usr/lib/gphoto2/2.1.5 directories.
- Added multiarch stuff

* Thu Dec 16 2004 Till Kamppeter <till@mandrakesoft.com> 2.1.5-1mdk
- Updated to GPhoto2 2.1.5.

* Sat Nov 27 2004 Till Kamppeter <till@mandrakesoft.com> 2.1.5-0.rc1.1mdk
- Updated to GPhoto2 2.1.5rc1.

* Fri Oct 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.1.4-3mdk
- Added signature so to recognize Canon IXUS 430.

* Tue Feb 10 2004 Pascal Terjan <pterjan@mandrake.org> 2.1.4-2mdk
- Patch from CVS to fix large file transfers from Canon cameras

* Fri Jan 23 2004 Till Kamppeter <till@mandrakesoft.com> 2.1.4-1mdk
- Updated to GPhoto2 2.1.4.

* Wed Jan 14 2004 Till Kamppeter <till@mandrakesoft.com> 2.1.4-0.pre1.1mdk
- Updated to GPhoto2 2.1.4pre1.

