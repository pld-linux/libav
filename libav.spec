# NOTE: don't send it to Th unless you resolve libraries (incl. sonames) conflict with ffmpeg
# libav is a fork of ffmpeg; as of Dec 2012 they are not 100% compatible
# (e.g. libav didn't drop some deprecated APIs); ffmpeg 1.0.x seems more powerful than libav 0.8.x.
#
# How to deal with ffmpeg/opencv chicken-egg problem:
#	1. make-request -r --without opencv ffmpeg.spec
#	2. make-request -r opencv.spec
#	3. bump release of ffmpeg.spec
#	4. make-request -r ffmpeg.spec
#
# Conditional build:
%bcond_with	nonfree		# non free options of package (currently: faac)
%bcond_with	fdk_aac		# AAC de/encoding via libfdk_aac (requires nonfree)
%bcond_without	bs2b		# BS2B audio filter support
%bcond_with	cuda		# NVIDIA CUDA code [BR: cuda.h]
%bcond_without	dcadec		# DCA decoding via libdcadec
%bcond_without	frei0r		# frei0r video filtering
%bcond_without	hdcd		# HDCD decoding filter
%bcond_without	ilbc		# iLBC de/encoding via WebRTC libilbc
%bcond_without	kvazaar		# Kvazaar HEVC encoder support
%bcond_with	mfx		# MFX hardware acceleration support
%bcond_with	npp		# NVIDIA Performance Primitives-based code (requires nonfree) [BR: libnppc+libnppi, npp.h]
%bcond_with	nvenc		# NVIDIA NVENC support
%bcond_without	omx		# OpenMAX IL support
%bcond_with	openh264	# OpenH264 H.264 encoder
%bcond_without	opencv		# OpenCV video filtering
%bcond_without	pulseaudio	# PulseAudio input support
%bcond_without	snappy		# Snappy compression support (needed for hap encoding)
%bcond_without	x264		# x264 encoder
%bcond_without	x265		# H.265/HEVC x265 encoder
%bcond_without	va		# VAAPI (Video Acceleration API)
%bcond_with	vpx		# VP8, a high-quality video codec [not ready for 1.4+?]
%bcond_without	wavpack		# wavpack encoding support
%bcond_without	webp		# WebP encoding support
%bcond_without	doc		# don't build docs

%ifnarch %{ix86} %{x8664} %{arm}
%undefine	with_x265
%endif
%ifarch i386 i486
%undefine	with_x265
%endif
Summary:	libav - Open Source audio and video processing tools
Summary(pl.UTF-8):	libav - narzędzia do przetwarzania dźwięku i obrazu o otwartych źródłach
Name:		libav
Version:	12.3
Release:	0.1
# LGPL or GPL, chosen at configure time (GPL version is more featured)
# (some filters, x264, x265, xavs, xvid, x11grab)
# using v3 allows Apache-licensed libs (opencore-amr, libvo-*enc)
License:	GPL v3+ with LGPL v3+ parts
Group:		Libraries
Source0:	https://libav.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	753ec26481b0582eb737383bd8a350a5
Patch0:		%{name}-opencv24.patch
Patch1:		%{name}-omx-libnames.patch
Patch2:		%{name}-x264.patch
URL:		https://libav.org/
# libomxil-bellagio-devel or limoi-core-devel (just headers, library is dlopened at runtime)
%{?with_omx:BuildRequires:	OpenMAX-IL-devel}
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	bzip2-devel
%{?with_dcadec:BuildRequires:	dcadec-devel >= 0.2.0}
%{?with_nonfree:BuildRequires:	faac-devel}
%{?with_fdk_aac:BuildRequires:	fdk-aac-devel}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
%{?with_frei0r:BuildRequires:	frei0r-devel}
%ifarch ppc
# require version with altivec support fixed
BuildRequires:	gcc >= 5:3.3.2-3
%endif
BuildRequires:	gnutls-devel
BuildRequires:	jack-audio-connection-kit-devel
%{?with_kvazaar:BuildRequires:	kvazaar-devel >= 0.8.1}
BuildRequires:	lame-libs-devel >= 3.98.3
%{?with_bs2b:BuildRequires:	libbs2b-devel}
BuildRequires:	libcdio-paranoia-devel >= 0.90-2
BuildRequires:	libdc1394-devel >= 2
BuildRequires:	libgsm-devel
%{?with_hdcd:BuildRequires:	libhdcd-devel}
BuildRequires:	libraw1394-devel >= 2
BuildRequires:	librtmp-devel
BuildRequires:	libtheora-devel >= 1.0-0.beta3
BuildRequires:	libtool >= 2:1.4d-3
%{?with_va:BuildRequires:	libva-devel >= 1.0.3}
BuildRequires:	libvdpau-devel >= 0.2
BuildRequires:	libvorbis-devel
%{?with_vpx:BuildRequires:	libvpx-devel >= 1.3.0}
%{?with_webp:BuildRequires:	libwebp-devel}
# X264_BUILD >= 118
%{?with_x264:BuildRequires:	libx264-devel >= 0.1.3-1.20111212_2245}
# X265_BUILD >= 57
%{?with_x265:BuildRequires:	libx265-devel >= 1.3}
# libxcb xcb-shm xcb-xfixes xcb-shape
BuildRequires:	libxcb-devel >= 1.4
%{?with_mfx:BuildRequires:	mfx_dispatch-devel}
%ifarch %{ix86}
%ifnarch i386 i486
BuildRequires:	nasm
%endif
%endif
#%{?with_nvenc:BuildRequires:	NVIDIA-NVENC-API} compat/nvenc/nvEncodeAPI.h
BuildRequires:	opencore-amr-devel
%{?with_opencv:BuildRequires:	opencv-devel}
%{?with_openh264:BuildRequires:	openh264-devel >= 1.3}
BuildRequires:	openjpeg-devel >= 1.5
BuildRequires:	opus-devel
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpmbuild(macros) >= 1.470
BuildRequires:	schroedinger-devel
%{?with_snappy:BuildRequires:	snappy-devel}
BuildRequires:	speex-devel >= 1:1.2-rc1
BuildRequires:	tar >= 1:1.22
%{?with_doc:BuildRequires:	tetex}
%{?with_doc:BuildRequires:	texi2html}
%{?with_doc:BuildRequires:	texinfo}
BuildRequires:	twolame-devel
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
%{?with_vpx:Requires:	libvpx >= 1.3.0}
%{?with_ilbc:Requires:	webrtc-libilbc}
Requires:	xvid >= 1:1.1.0
Obsoletes:	libav-avserver
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
%{?with_dcadec:Requires:	dcadec-devel >= 0.2.0}
%{?with_nonfree:Requires:	faac-devel}
%{?with_fdk_aac:Requires:	fdk-aac-devel}
Requires:	fontconfig-devel
Requires:	freetype-devel
Requires:	jack-audio-connection-kit-devel
%{?with_kvazaar:Requires:	kvazaar-devel >= 0.8.1}
Requires:	lame-libs-devel >= 3.98.3
%{?with_bs2b:Requires:	libbs2b-devel}
Requires:	libcdio-paranoia-devel >= 0.90-2
Requires:	libdc1394-devel >= 2
Requires:	libgsm-devel
%{?with_hdcd:Requires:	libhdcd-devel}
Requires:	libraw1394-devel >= 2
Requires:	librtmp-devel
Requires:	libtheora-devel >= 1.0-0.beta3
%{?with_va:Requires:	libva-devel >= 1.0.3}
Requires:	libvorbis-devel
%{?with_vpx:Requires:	libvpx-devel >= 1.3.0}
%{?with_webp:Requires:	libwebp-devel}
%{?with_x264:Requires:	libx264-devel >= 0.1.3-1.20110625_2245}
%{?with_x265:Requires:	libx265-devel >= 1.3}
%{?with_mfx:Requires:	mfx_dispatch-devel}
Requires:	opencore-amr-devel
%{?with_openh264:Requires:	openh264-devel >= 1.3}
%{?with_opencv:Requires:	opencv-devel}
Requires:	openjpeg-devel >= 1.5
Requires:	opus-devel
Requires:	schroedinger-devel
%{?with_snappy:Requires:	snappy-devel}
Requires:	speex-devel >= 1:1.2-rc1
Requires:	twolame-devel
Requires:	vo-aacenc-devel
Requires:	vo-amrwbenc-devel
%{?with_wavpack:Requires:	wavpack-devel}
%{?with_ilbc:Requires:	webrtc-libilbc-devel}
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
	%{!?with_cuda:--disable-cuda} \
	--enable-gnutls \
	--enable-gpl \
	--enable-version3 \
	%{?with_frei0r:--enable-frei0r} \
	%{?with_bs2b:--enable-libbs2b} \
	--enable-libcdio \
	--enable-libdc1394 \
	%{?with_dcadec:--enable-libdcadec} \
	--enable-libfontconfig \
	--enable-libfreetype \
	--enable-libgsm \
	%{?with_hdcd:--enable-libhdcd} \
	%{?with_ilbc:--enable-libilbc} \
	%{?with_kvazaar:--enable-libkvazaar} \
	%{?with_mfx:--enable-libmfx} \
	--enable-libmp3lame \
	--enable-libopencore-amrnb \
	--enable-libopencore-amrwb \
	%{?with_opencv:--enable-libopencv} \
	%{?with_openh264:--enable-libopenh264} \
	--enable-libopenjpeg \
	--enable-libopus \
	%{?with_pulseaudio:--enable-libpulse} \
	--enable-librtmp \
	--enable-libschroedinger \
	%{?with_snappy:--enable-libsnappy} \
	--enable-libspeex \
	--enable-libtheora \
	--enable-libtwolame \
	--enable-libvo-aacenc \
	--enable-libvo-amrwbenc \
	--enable-libvorbis \
	%{?with_vpx:--enable-libvpx} \
	%{?with_wavpack:--enable-libwavpack} \
	%{?with_webp:--enable-libwebp} \
	%{?with_x264:--enable-libx264} \
	%{?with_x265:--enable-libx265} \
	--enable-libxavs \
	--enable-libxcb \
	--enable-libxvid \
	%{!?with_nvenc:--disable-nvenc} \
	%{?with_omx:--enable-omx} \
	--enable-pthreads \
	--enable-shared \
	--enable-swscale \
	%{?with_va:--enable-vaapi} \
	--enable-vdpau \
%ifnarch %{ix86} %{x8664}
	--disable-mmx \
%endif
%ifarch i386 i486
	--disable-mmx \
%endif
%if %{with nonfree}
	--enable-nonfree \
	--enable-libfaac \
	%{?with_fdk_aac:--enable-libfdk-aac} \
	%{?with_npp:--enable-libnpp} \
%endif
	--enable-runtime-cpudetect

%{__make} \
	V=1

# CC_O to add -c to commandline. makefile should be patched
%{__make} tools/qt-faststart V=1 CC_O='-c -o $@'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/libav

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

%files
%defattr(644,root,root,755)
%doc CREDITS Changelog LICENSE README.md doc/{APIchanges,RELEASE_NOTES} %{?with_doc:doc/*.html}
%attr(755,root,root) %{_libdir}/libavcodec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavcodec.so.57
%attr(755,root,root) %{_libdir}/libavdevice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavdevice.so.56
%attr(755,root,root) %{_libdir}/libavfilter.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavfilter.so.6
%attr(755,root,root) %{_libdir}/libavformat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavformat.so.57
%attr(755,root,root) %{_libdir}/libavresample.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavresample.so.3
%attr(755,root,root) %{_libdir}/libavutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libavutil.so.55
%attr(755,root,root) %{_libdir}/libswscale.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libswscale.so.4

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
