Name:           wormsofprey
Version:        0.4.3
Release:        6%{?dist}
Summary:        Team based bomb / scorched like game
Group:          Amusements/Games
License:        GPLv2+
URL:            http://wormsofprey.org/
Source0:        http://wormsofprey.org/download/wop-%{version}-src.tar.bz2
Source1:        %{name}.desktop
Source2:        %{name}.png
Patch0:         wop-0.4.3-gcc43.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  SDL_image-devel SDL_mixer-devel SDL_net-devel SDL_ttf-devel
BuildRequires:  zlib-devel imake desktop-file-utils
Requires:       %{name}-data >= 20051221

%description
Each player controls a team of worms and the purpose is to ellimate all the
other worms, for which each worm has a number of different weapons at his
disposal. Features: Multi-player with one player per computer, Completely new
graphics, Low bandwidth usage, Different game modes (death match, team play),
Ropes can be attached to any object, Rope can be released, Any number of ropes
and Multiple moving goals.


%prep
%setup -q -n wop-%{version}
%patch0 -p1
sed -i 's|^CXXFLAGS ?= .*|CXXFLAGS ?= %{optflags}|' sdlwidgets/Makefile \
  src/Makefile
sed -i 's|data = ./data|data = %{_datadir}/%{name}|' woprc
sed -i 's|\r||' ChangeLog
iconv -f ISO-8859-1 -t UTF-8 REVIEWS > REVIEWS.tmp
touch -r REVIEWS REVIEWS.tmp
mv REVIEWS.tmp REVIEWS


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m 644 woprc $RPM_BUILD_ROOT/%{_sysconfdir}
install -m 755 bin/wop $RPM_BUILD_ROOT/%{_bindir}/%{name}

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor dribble           \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
install -p -m 644 %{SOURCE2} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README README-COMMAND-LINE-OPTIONS.txt REVIEWS
%config(noreplace) %{_sysconfdir}/woprc
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png


%changelog
* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr  1 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4.3-5
- Fix building with gcc 4.4

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.4.3-4
- rebuild for new F11 features

* Fri Jul 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4.3-3
- Release bump for rpmfusion

* Thu Mar 20 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4.3-2%{?dist}
- Fix building with gcc 4.3

* Wed Aug  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4.3-1%{?dist}
- Initial Fedora Extras package
