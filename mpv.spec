Summary:	Video player based on MPlayer/mplayer2
Name:		mpv
Version:	0.9.2
Release:	1
License:	GPL v2
Group:		X1//Applications/Multimedia
Source0:	https://github.com/mpv-player/mpv/archive/v%{version}.tar.gz
# Source0-md5:	ed1384e703f7032e531731842e4da4f7
Source1:	http://ftp.waf.io/pub/release/waf-1.8.7
# Source1-md5:	190ebc5141720b72c533aa015bd19a76
URL:		http://mpv.io/
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libwayland-EGL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	curl-devel
BuildRequires:	docutils
BuildRequires:	enca-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	lcms2-devel
BuildRequires:	libass-devel >= 0.12
BuildRequires:	libbluray-devel
BuildRequires:	libcdio-paranoia-devel
BuildRequires:	libdvdnav-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libquvi-devel
BuildRequires:	libsmbclient-devel
BuildRequires:	libva-devel
BuildRequires:	libxkbcommon-devel
BuildRequires:	lua-devel
BuildRequires:	mpg123-libs-devel
BuildRequires:	pkg-config
#BuildRequires:	pulseaudio-devel
BuildRequires:	v4l-utils-devel
BuildRequires:	wayland-devel
BuildRequires:	xorg-libX11-devel
BuildRequires:	xorg-libXScrnSaver-devel
BuildRequires:	xorg-libXext-devel
BuildRequires:	xorg-libXinerama-devel
BuildRequires:	xorg-libXrandr-devel
BuildRequires:	xorg-libXv-devel
BuildRequires:	zlib-devel
%requires_eq	ffmpeg-libs
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mpv is a free and open-source general-purpose video player.

%package -n zsh-completion-%{name}
Summary:	Zsh auto-complete site functions
Group:		Documentation
Requires:	zsh

%description -n zsh-completion-%{name}
Zsh auto-complete site functions.


%prep
%setup -q

install %{SOURCE1} waf
chmod +x waf

%{__sed} -i 's/vendor-completions/site-functions/' wscript_build.py

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
./waf configure \
	--confdir=%{_sysconfdir}/mpv	\
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--enable-cdda	    \
	--enable-zsh-comp
./waf -v build

%install
rm -rf $RPM_BUILD_ROOT

./waf -v install \
	--destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc README.md RELEASE_NOTES etc/{example,input}.conf DOCS/{edl-mpv,encoding}.rst
%dir %{_sysconfdir}/mpv
%{_sysconfdir}/mpv/encoding-profiles.conf
%attr(755,root,root) %{_bindir}/mpv
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/mpv.png
%{_mandir}/man1/mpv.1*

%files -n zsh-completion-%{name}
%attr(755,root,root)
%{_datadir}/zsh/site-functions/_mpv

