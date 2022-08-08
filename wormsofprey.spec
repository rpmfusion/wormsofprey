Name:           wormsofprey
Version:        0.4.3
Release:        23%{?dist}
Summary:        Team based bomb / scorched like game
Group:          Amusements/Games
License:        GPLv2+
URL:            http://wormsofprey.org/
Source0:        http://wormsofprey.org/download/wop-%{version}-src.tar.bz2
Source1:        %{name}.desktop
Source2:        %{name}.png
Patch0:         wop-0.4.3-gcc43.patch
Patch1:         wop-0.4.3-gcc6.patch
BuildRequires:  SDL_image-devel SDL_mixer-devel SDL_net-devel SDL_ttf-devel
BuildRequires:  zlib-devel imake desktop-file-utils gcc-c++
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
%patch1 -p1
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


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc AUTHORS ChangeLog COPYING README README-COMMAND-LINE-OPTIONS.txt REVIEWS
%config(noreplace) %{_sysconfdir}/woprc
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png


%changelog
* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.4.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.4.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.4.3-15
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.4.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul  7 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 0.4.3-10
- Fix building with gcc6 / fix FTBFS

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.4.3-8
- Mass rebuilt for Fedora 19 Features

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.3-7
- Rebuilt for c++ ABI breakage

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
