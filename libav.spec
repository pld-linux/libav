# TODO: avserver no longer supports daemon mode, so adjust init script
# NOTE: don't send it to Th unless you resolve libraries (incl. sonames) conflict with ffmpeg
# libav is a fork of ffmpeg; as of Dec 2012 they are not 100% compatible
# (e.g. libav didn't drop some deprecated APIs); ffmpeg 1.0.x seems more powerful than libav 0.8.x.
#
# How to deal with ffmpeg/opencv checken-egg problem:
#	1. make-request -r --without opencv ffmpeg.spec
#	2. make-request -r opencv.spec
#	3. bump release of ffmpeg.spec
#	4. make-request -r ffmpeg.spec
#
# Conditional build:
%bcond_with	nonfree		# non free options of package (currently: faac)
%bcond_with	fdk_aac		# AAC de/encoding via libfdk_aac (requires nonfree)
%bcond_without	frei0r		# frei0r video filtering
%bcond_without	ilbc		# iLBC de/encoding via WebRTC libilbc
%bcond_without	opencv		# OpenCV video filtering
%bcond_without	pulseaudio	# PulseAudio input support
%bcond_without	x264		# x264 encoder
%bcond_without	va		# VAAPI (Video Acceleration API)
%bcond_without	vpx		# VP8, a high-quality video codec
%bcond_without	wavpack		# wavpack encoding support
%bcond_without	webp		# WebP encoding support
%bcond_without	doc		# don't build docs

Summary:	libav - Open Source audio and video processing tools
Summary(pl.UTF-8):	libav - narzędzia do przetwarzania dźwięku i obrazu o otwartych źródłach
Name:		libav
Version:	10.4
Release:	0.1
# LGPL or GPL, chosen at configure time (GPL version is more featured)
# (some filters, x264, xavs, xvid, x11grab)
# using v3 allows Apache-licensed libs (opencore-amr, libvo-*enc)
License:	GPL v3+ with LGPL v3+ parts
Group:		Libraries
Source0:	http://libav.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	218bdfa1b2ff56c2a3daa2501c2e893f
Source1:	avserver.init
Source2:	avserver.sysconfig
Source3:	avserver.conf
Patch0:		%{name}-opencv24.patch
Patch1:		%{name}-avserver.patch
URL:		http://libav.org/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	bzip2-devel
%{?with_nonfree:BuildRequires:	faac-devel}
%{?with_fdk_aac:BuildRequires:	fdk-aac-devel}
BuildRequires:	freetype-devel
%{?with_frei0r:BuildRequires:	frei0r-devel}
%ifarch ppc
# require version with altivec support fixed
BuildRequires:	gcc >= 5:3.3.2-3
%endif
BuildRequires:	gnutls-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	lame-libs-devel >= 3.98.3
BuildRequires:	libcdio-paranoia-devel >= 0.90-2
BuildRequires:	libdc1394-devel >= 2
BuildRequires:	libgsm-devel
BuildRequires:	libraw1394-devel >= 2
BuildRequires:	librtmp-devel
BuildRequires:	libtheora-devel >= 1.0-0.beta3
BuildRequires:	libtool >= 2:1.4d-3
%{?with_va:BuildRequires:	libva-devel >= 1.0.3}
BuildRequires:	libvdpau-devel >= 0.2
BuildRequires:	libvorbis-devel
%{?with_vpx:BuildRequires:	libvpx-devel >= 0.9.6}
%{?with_webp:BuildRequires:	libwebp-devel}
# X264_BUILD >= 118
%{?with_x264:BuildRequires:	libx264-devel >= 0.1.3-1.20111212_2245}
%ifarch %{ix86}
%ifnarch i386 i486
BuildRequires:	nasm
%endif
%endif
BuildRequires:	opencore-amr-devel
%{?with_opencv:BuildRequires:	opencv-devel}
BuildRequires:	openjpeg-devel >= 1.5
BuildRequires:	opus-devel
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpmbuild(macros) >= 1.470
BuildRequires:	schroedinger-devel
BuildRequires:	speex-devel >= 1:1.2-rc1
BuildRequires:	tar >= 1:1.22
%{?with_doc:BuildRequires:	tetex}
%{?with_doc:BuildRequires:	texi2html}
%{?with_doc:BuildRequires:	texinfo}
BuildRequires:	vo-aacenc-devel
BuildRequires:	vo-amrwbenc-devel
%{?with_wavpack:BuildRequires:	wavpack-devel}
%{?with_ilbc:BuildRequires:	webrtc-libilbc-devel}
BuildRequires:	xavs-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xvid-devel >= 1:1.1.0
BuildRequires:	xz
BuildRequires:	yasm
BuildRequires:	zlib-devel
%{?with_vpx:Requires:	libvpx >= 0.9.6}
%{?with_ilbc:Requires:	webrtc-libilbc}
Requires:	xvid >= 1:1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%define		specflags	-fno-strict-aliasing

# -fomit-frame-pointer is always needed on x86 due to lack of registers (-fPIC takes one)
%define		specflags_ia32	-fomit-frame-pointer
# -mmmx is needed to enable <mmintrin.h> code.
%define		specflags_i586	-mmmx
%define		specflags_i686	-mmmx
%define		specflags_ppc	-fPIC

%description
Libav provides cross-platform tools and libraries to convert,
manipulate and stream a wide range of multimedia formats and
protocols.

%description -l pl.UTF-8
Projekt libav udostępnia wieloplatformowe narzędzia i biblioteki do
konwersji, modyfikowania oraz nadawania strumieni przy użyciu
szerokiego zakresu formatów i protokołów multimedialnych.

%package devel
Summary:	libav header files
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek libav
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# Libs.private from *.pc (unreasonably they are all the same)
Requires:	SDL-devel >= 1.2.1
Requires:	alsa-lib-devel
Requires:	bzip2-devel
%{?with_nonfree:Requires:	faac-devel}
%{?with_fdk_aac:Requires:	fdk-aac-devel}
Requires:	freetype-devel
Requires:	jack-audio-connection-kit-devel
Requires:	lame-libs-devel >= 3.98.3
Requires:	libcdio-paranoia-devel >= 0.90-2
Requires:	libdc1394-devel >= 2
Requires:	libgsm-devel
Requires:	libraw1394-devel >= 2
Requires:	librtmp-devel
Requires:	libtheora-devel >= 1.0-0.beta3
%{?with_va:Requires:	libva-devel >= 1.0.3}
Requires:	libvorbis-devel
%{?with_vpx:Requires:	libvpx-devel >= 0.9.6}
%{?with_webp:Requires:	libwebp-devel}
%{?with_x264:Requires:	libx264-devel >= 0.1.3-1.20110625_2245}
Requires:	opencore-amr-devel
%{?with_opencv:Requires:	opencv-devel}
Requires:	openjpeg-devel >= 1.5
Requires:	opus-devel
Requires:	schroedinger-devel
Requires:	speex-devel >= 1:1.2-rc1
Requires:	vo-aacenc-devel
Requires:	vo-amrwbenc-devel
%{?with_wavpack:Requires:	wavpack-devel}
%{?with_ilbc:Requires:	webrtc-libilbc}
Requires:	xavs-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXfixes-devel
Requires:	xvid-devel >= 1:1.1.0
Requires:	zlib-devel

%description devel
libav header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek libav.

%package static
Summary:	libav static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libav
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libav static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki libav.

%package tools
Summary:	libav video and audio conversion tools
Summary(pl.UTF-8):	Narzędzia libav do konwersji obrazu i dźwięku
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description tools
libav command line tools to convert one video file format to another.

%description tools -l pl.UTF-8
Narzędzia linii poleceń libav do konwersji filmów z jednego formatu do
innego.

%package avplay
Summary:	avplay - SDL-based media player
Summary(pl.UTF-8):	avplay - odtwarzacz mediów oparty na SDL
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description avplay
avplay is a very simple and portable media player using the libav
libraries and the SDL library. It is mostly used as a test bench for
the various APIs of libav.

%description avplay -l pl.UTF-8
avplay to bardzo prosty i przenośny odtwarzacz mediów używający
bibliotek libav oraz biblioteki SDL. Jest używany głównie do
testowania różnych API libav.

%package avserver
Summary:	avserver video server
Summary(pl.UTF-8):	avserver - serwer strumieni obrazu
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.0.10

%description avserver
avserver is a streaming server for both audio and video. It supports
several live feeds, streaming from files and time shifting on live
feeds (you can seek to positions in the past on each live feed,
provided you specify a big enough feed storage in avserver.conf).

%description avserver -l pl.UTF-8
avserver to serwer strumieni dla dźwięku i obrazu. Obsługuje kilka
źródeł na żywo, przekazywanie strumieni z plików i przesuwanie w
czasie dla źródeł na żywo (można przeskakiwać na położenia w
przeszłości dla każdego źródła na żywo, pod warunkiem odpowiednio
dużej przestrzeni na dane skonfigurowanej w avserver.conf).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# package the grep result for mplayer, the result formatted as ./mplayer/configure
cat <<EOF > libav-avconfig
#! /bin/sh
_libavdecoders_all="`sed -n 's/^[^#]*DEC.*(.*, *\(.*\)).*/\1_decoder/p' libavcodec/allcodecs.c | tr '[a-z]' '[A-Z]'`"
_libavencoders_all="`sed -n 's/^[^#]*ENC.*(.*, *\(.*\)).*/\1_encoder/p' libavcodec/allcodecs.c | tr '[a-z]' '[A-Z]'`"
_libavparsers_all="`sed -n 's/^[^#]*PARSER.*(.*, *\(.*\)).*/\1_parser/p' libavcodec/allcodecs.c | tr '[a-z]' '[A-Z]'`"
_libavbsfs_all="`sed -n 's/^[^#]*BSF.*(.*, *\(.*\)).*/\1_bsf/p' libavcodec/allcodecs.c | tr '[a-z]' '[A-Z]'`"
_libavdemuxers_all="`sed -n 's/^[^#]*DEMUX.*(.*, *\(.*\)).*/\1_demuxer/p' libavformat/allformats.c | tr '[a-z]' '[A-Z]'`"
_libavmuxers_all="`sed -n 's/^[^#]*_MUX.*(.*, *\(.*\)).*/\1_muxer/p' libavformat/allformats.c | tr '[a-z]' '[A-Z]'`"
_libavprotocols_all="`sed -n 's/^[^#]*PROTOCOL.*(.*, *\(.*\)).*/\1_protocol/p' libavformat/allformats.c | tr '[a-z]' '[A-Z]'`"
EOF
cat <<'EOF' >> libav-avconfig

case "$1" in
--decoders)
	echo $_libavdecoders_all
	;;
--encoders)
	echo $_libavencoders_all
	;;
--parsers)
	echo $_libavparsers_all
	;;
--bsfs)
	echo $_libavbsfs_all
	;;
--demuxers)
	echo $_libavdemuxers_all
	;;
--muxers)
	echo $_libavmuxers_all
	;;
--protocols)
	echo $_libavprotocols_all
	;;
*)
	cat <<USAGE
Usage: $0 [OPTION]
Options:
  --decoders
  --encoders
  --parsers
  --bsfs
  --demuxers
  --muxers
  --protocols
USAGE
	exit 1;;
esac

exit 0
EOF

%build
# notes:
# - it's not autoconf configure
# - --disable-debug, --disable-optimizations, tune=generic causes not to override our optflags
# - openssl is not enabled (gnutls is instead)
./configure \
	--arch=%{_target_base_arch} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--shlibdir=%{_libdir} \
	--mandir=%{_mandir} \
	--extra-cflags="-D_GNU_SOURCE=1 %{rpmcppflags} %{rpmcflags}" \
	--extra-ldflags="%{rpmcflags} %{rpmldflags}" \
	--cc="%{__cc}" \
	--disable-debug \
	--disable-optimizations \
	--enable-avfilter \
	--enable-gnutls \
	--enable-gpl \
	--enable-version3 \
	%{?with_frei0r:--enable-frei0r} \
	--enable-libcdio \
	--enable-libdc1394 \
	%{?with_fdk_aac:--enable-libfdk-aac} \
	--enable-libfreetype \
	--enable-libgsm \
	%{?with_ilbc:--enable-libilbc} \
	--enable-libmp3lame \
	--enable-libopencore-amrnb \
	--enable-libopencore-amrwb \
	%{?with_opencv:--enable-libopencv} \
	--enable-libopenjpeg \
	--enable-libopus \
	%{?with_pulseaudio:--enable-libpulse} \
	--enable-librtmp \
	--enable-libschroedinger \
	--enable-libspeex \
	--enable-libtheora \
	--enable-libvo-aacenc \
	--enable-libvo-amrwbenc \
	--enable-libvorbis \
	%{?with_vpx:--enable-libvpx} \
	%{?with_wavpack:--enable-libwavpack} \
	%{?with_webp:--enable-libwebp} \
	%{?with_x264:--enable-libx264} \
	--enable-libxavs \
	--enable-libxvid \
	--enable-pthreads \
	--enable-shared \
	--enable-swscale \
	%{?with_va:--enable-vaapi} \
	--enable-vdpau \
	--enable-x11grab \
%ifnarch %{ix86} %{x8664}
	--disable-mmx \
%endif
%ifarch i386 i486
	--disable-mmx \
%endif
%if %{with nonfree}
	--enable-nonfree \
	--enable-libfaac \
%endif
	--enable-runtime-cpudetect

%{__make} \
	V=1

# CC_O to add -c to commandline. makefile should be patched
%{__make} tools/qt-faststart V=1 CC_O='-c -o $@'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},/etc/{sysconfig,rc.d/init.d}} \
	$RPM_BUILD_ROOT%{_includedir}/libav \
	$RPM_BUILD_ROOT/var/{cache,log}/avserver

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	V=1

cp -a config.h $RPM_BUILD_ROOT%{_includedir}/libav
cp -a libavutil/intreadwrite.h $RPM_BUILD_ROOT%{_includedir}/libavutil
cp -a libavutil/bswap.h $RPM_BUILD_ROOT%{_includedir}/libavutil
cp -a libavutil/common.h $RPM_BUILD_ROOT%{_includedir}/libavutil
cp -a libavutil/mem.h $RPM_BUILD_ROOT%{_includedir}/libavutil
for a in libavutil/*/bswap.h; do
	install -D $a $RPM_BUILD_ROOT%{_includedir}/$a
done
cp -a libavformat/riff.h $RPM_BUILD_ROOT%{_includedir}/libavformat
cp -a libavformat/avio.h $RPM_BUILD_ROOT%{_includedir}/libavformat

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/avserver
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/avserver
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/avserver.conf
mv -f $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/avserver
install -p tools/qt-faststart $RPM_BUILD_ROOT%{_bindir}/avqt-faststart

# install as libav-avconfig to avoid with possible programs looking for
# libav-config and expecting --libs output from it which is not implemented
# simple to do (by querying pkgconfig), but why?
install -p libav-avconfig $RPM_BUILD_ROOT%{_bindir}/libav-avconfig

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/libav/*.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%pre avserver
%groupadd -g 167 ffserver
%useradd -g ffserver -u 167 ffserver

%post avserver
/sbin/chkconfig --add avserver
%service avserver restart

%preun avserver
if [ "$1" = 0 ]; then
	%service avserver stop
	/sbin/chkconfig --del avserver
fi

%postun avserver
if [ "$1" = 0 ]; then
	%userremove ffserver
	%groupremove ffserver
fi

%files
%defattr(644,root,root,755)
%doc CREDITS Changelog LICENSE README doc/{APIchanges,RELEASE_NOTES} %{?with_doc:doc/*.html}
%attr(755,root,root) %{_libdir}/libavcodec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavcodec.so.55
%attr(755,root,root) %{_libdir}/libavdevice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavdevice.so.54
%attr(755,root,root) %{_libdir}/libavfilter.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavfilter.so.4
%attr(755,root,root) %{_libdir}/libavformat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavformat.so.55
%attr(755,root,root) %{_libdir}/libavresample.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavresample.so.1
%attr(755,root,root) %{_libdir}/libavutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavutil.so.53
%attr(755,root,root) %{_libdir}/libswscale.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libswscale.so.2

%files devel
%defattr(644,root,root,755)
%doc doc/optimization.txt
%attr(755,root,root) %{_bindir}/libav-avconfig
%attr(755,root,root) %{_libdir}/libavcodec.so
%attr(755,root,root) %{_libdir}/libavdevice.so
%attr(755,root,root) %{_libdir}/libavfilter.so
%attr(755,root,root) %{_libdir}/libavformat.so
%attr(755,root,root) %{_libdir}/libavresample.so
%attr(755,root,root) %{_libdir}/libavutil.so
%attr(755,root,root) %{_libdir}/libswscale.so
%{_includedir}/libav
%{_includedir}/libavcodec
%{_includedir}/libavdevice
%{_includedir}/libavfilter
%{_includedir}/libavformat
%{_includedir}/libavresample
%{_includedir}/libavutil
%{_includedir}/libswscale
%{_pkgconfigdir}/libavcodec.pc
%{_pkgconfigdir}/libavdevice.pc
%{_pkgconfigdir}/libavfilter.pc
%{_pkgconfigdir}/libavformat.pc
%{_pkgconfigdir}/libavresample.pc
%{_pkgconfigdir}/libavutil.pc
%{_pkgconfigdir}/libswscale.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libavcodec.a
%{_libdir}/libavdevice.a
%{_libdir}/libavfilter.a
%{_libdir}/libavformat.a
%{_libdir}/libavresample.a
%{_libdir}/libavutil.a
%{_libdir}/libswscale.a

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avconv
%attr(755,root,root) %{_bindir}/avprobe
%attr(755,root,root) %{_bindir}/avqt-faststart
%dir %{_datadir}/avconv
%{_datadir}/avconv/*.avpreset
%{?with_doc:%{_mandir}/man1/avconv.1*}
%{?with_doc:%{_mandir}/man1/avprobe.1*}

%files avplay
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avplay
%{?with_doc:%{_mandir}/man1/avplay.1*}

%files avserver
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/avserver.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/avserver
%attr(755,root,root) %{_sbindir}/avserver
%attr(754,root,root) /etc/rc.d/init.d/avserver
%{?with_doc:%{_mandir}/man1/avserver.1*}
%dir %attr(770,root,ffserver) /var/cache/avserver
%dir %attr(770,root,ffserver) /var/log/avserver
