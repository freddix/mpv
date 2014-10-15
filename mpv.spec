Summary:	Video player based on MPlayer/mplayer2
Name:		mpv
Version:	0.6.1
Release:	2
License:	GPL v2
Group:		X1//Applications/Multimedia
Source0:	https://github.com/mpv-player/mpv/archive/v%{version}.tar.gz
# Source0-md5:	a6060358a47a5a7cfc1123b8f74dd5ab
Source1:	https://waf.googlecode.com/files/waf-1.7.15
# Source1-md5:	2ba0e10baf44db334e3baa39e59688db
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
BuildRequires:	libass-devel
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
BuildRequires:	pulseaudio-devel
BuildRequires:	v4l-utils-devel
BuildRequires:	wayland-devel
BuildRequires:	xorg-libX11-devel
BuildRequires:	xorg-libXScrnSaver-devel
BuildRequires:	xorg-libXext-devel
BuildRequires:	xorg-libXinerama-devel
BuildRequires:	xorg-libXrandr-devel
BuildRequires:	xorg-libXv-devel
BuildRequires:	zlib-devel
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
	--nocache	    \
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

