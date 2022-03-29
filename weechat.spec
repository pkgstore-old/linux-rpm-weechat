%ifnarch s390x
%bcond_without check
%else
# some tests fail on s390x
%bcond_with check
%endif

%if 0%{?fedora} || 0%{?rhel} < 8
%bcond_without docs
%else
# TODO: package rubygem-asciidoctor
%bcond_with docs
%endif

%if 0%{?rhel} && 0%{?rhel} < 9
%undefine __cmake_in_source_build
%endif
%global __provides_exclude_from ^%{_libdir}/weechat/plugins/.*$

%if %{?_pkgdocdir:1}0
%if 0%{?rhel}
%global _doc %{name}-%{version}
%else
%global _doc                    %{name}
%endif
%else
%global _doc                    %{name}-%{version}
%global _pkgdocdir              %{_docdir}/%{_doc}
%endif

%global release_prefix          100

Name:                           weechat
Version:                        3.5
Release:                        %{release_prefix}%{?dist}
Summary:                        Portable, fast, light and extensible IRC client
License:                        GPLv3
URL:                            https://weechat.org
Vendor:                         Package Store <https://pkgstore.github.io>
Packager:                       Kitsune Solar <kitsune.solar@gmail.com>

Source0:                        https://weechat.org/files/src/%{name}-%{version}.tar.xz
# Signature
Source900:                      https://weechat.org/files/src/%{name}-%{version}.tar.xz.asc

# /usr/bin/ld: CMakeFiles/charset.dir/charset.o:
# relocation R_X86_64_PC32 against symbol `weechat_charset_plugin'
# can not be used when making a shared object; recompile with -fPIC
Patch0:                         weechat-1.0.1-plugins-fPIC.patch
Patch1:                         weechat-3.4-tests-fPIC.patch
# this fails on too many tests, we want to let them finish anyway
Patch2:                         weechat-3.4-disable-memleak-detection.patch

BuildRequires:                  gcc
%if %{with check}
BuildRequires:                  cpputest-devel
BuildRequires:                  glibc-langpack-en
%endif
%if %{with docs}
BuildRequires:                  asciidoctor
%endif
BuildRequires:                  ca-certificates
BuildRequires:                  cmake
BuildRequires:                  docbook-style-xsl
BuildRequires:                  enchant-devel
BuildRequires:                  gettext
BuildRequires:                  gnutls-devel
%if 0%{?fedora} >= 30 || 0%{?rhel} > 8
BuildRequires:                  guile22-devel
%else
BuildRequires:                  guile-devel
%endif
BuildRequires:                  libcurl-devel
BuildRequires:                  libgcrypt-devel
BuildRequires:                  lua-devel
BuildRequires:                  ncurses-devel
BuildRequires:                  perl-ExtUtils-Embed
BuildRequires:                  perl-devel
BuildRequires:                  pkgconfig
BuildRequires:                  python3-devel
BuildRequires:                  ruby
BuildRequires:                  ruby-devel
BuildRequires:                  source-highlight
BuildRequires:                  tcl-devel
BuildRequires:                  libzstd
%ifarch %{ix86} x86_64 %{arm}
# https://bugzilla.redhat.com/show_bug.cgi?id=1338728
# https://github.com/weechat/weechat/issues/360
%if 0%{?rhel} && 0%{?rhel} < 8
BuildRequires:                  v8-devel
%endif
%endif
BuildRequires:                  zlib-devel
%if 0%{?rhel}
BuildRequires:                  cmake3
%endif

Requires:                       hicolor-icon-theme

%description
WeeChat (Wee Enhanced Environment for Chat) is a portable, fast, light and
extensible IRC client. Everything can be done with a keyboard.
It is customizable and extensible with scripts.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: devel
# -------------------------------------------------------------------------------------------------------------------- #

%package devel
Summary:                        Development files for weechat
Requires:                       %{name}%{?_isa} = %{version}-%{release}
Requires:                       pkgconfig

%description devel
WeeChat (Wee Enhanced Environment for Chat) is a portable, fast, light and
extensible IRC client. Everything can be done with a keyboard.
It is customizable and extensible with scripts.

This package contains include files and pc file for weechat.

# -------------------------------------------------------------------------------------------------------------------- #
# -----------------------------------------------------< SCRIPT >----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

%prep
%autosetup -p1 -n %{name}-%{version}
find doc/ -type f -name 'CMakeLists.txt' \
  -exec %{__sed} -i -e 's#${PROJECT_NAME}#%{_doc}#g' '{}' \;

%{__sed} -i 's/NAMES python3.7/NAMES python%{python3_version}m python%{python3_version}/' cmake/FindPython.cmake


%build
%cmake3                                       \
  -DPREFIX=%{_prefix}                         \
  -DLIBDIR=%{_libdir}                         \
  -DENABLE_ENCHANT=ON                         \
  -DENABLE_PYTHON3=ON                         \
  -DENABLE_PHP=OFF                            \
%if %{with check}
  -DENABLE_TESTS=ON \
%else
  -DENABLE_TESTS=OFF \
%endif
%if %{with docs}
  -DENABLE_DOC=ON                             \
  -DENABLE_MAN=ON                             \
%else
  -DENABLE_DOC=OFF                            \
  -DENABLE_MAN=OFF                            \
%endif
  -DENABLE_JAVASCRIPT=OFF                     \
  -DCA_FILE=/etc/pki/tls/certs/ca-bundle.crt  \
  %{nil}
%cmake_build


%install
%cmake_install

%find_lang %name


%if %{with check}
%ctest -- -V
%endif


%files -f %{name}.lang
%doc AUTHORS.adoc ChangeLog.adoc Contributing.adoc
%doc README.adoc ReleaseNotes.adoc
%license COPYING
%{_bindir}/%{name}-curses
%{_bindir}/%{name}
%{_bindir}/%{name}-headless
%{_libdir}/%{name}
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%if 0%{?fedora} || 0%{?rhel} < 8
%{_pkgdocdir}/weechat_*.html
%{_mandir}/man1/weechat.1*
%{_mandir}/*/man1/weechat.1*
%{_mandir}/man1/%{name}-headless.1*
%{_mandir}/*/man1/%{name}-headless.1*
%endif


%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/weechat-plugin.h
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Mar 29 2022 Package Store <pkgstore@mail.ru> - 3.5-100
- NEW: WeeChat v3.5.
- UPD: Rebuild by Package Store.

* Sun Nov 07 2021 Paul Komkoff <i@stingr.net> - 3.3-1
- update to 3.3

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.2-1
- Update to 3.2
- Reenable s390x build for EPEL8 (#1869383)

* Sat Jun 19 2021 Package Store <kitsune.solar@gmail.com> - 3.2-100
- NEW: v3.2.
- UPD: Move to Package Store.
- UPD: License.

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.1-3
- Rebuilt for Python 3.10

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.1-2
- Perl 5.34 rebuild

* Sun Mar 07 2021 Łukasz Patron <priv.luk@gmail.com> - 3.1-1
- Update to 3.1

* Fri Feb 12 2021 Łukasz Patron <priv.luk@gmail.com> - 3.0.1-1
- Update to 3.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Łukasz Patron <priv.luk@gmail.com> - 3.0-1
- Update to 3.0

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9-3
- F-34: rebuild against ruby 3.0

* Mon Sep 14 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.9-2
- Use guile 2.2 where possible

* Mon Aug 17 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.9-1
- Update to 2.9

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.8-3
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.8-2
- Rebuilt for Python 3.9

* Wed Apr 1 2020 Paul Komkoff <i@stingr.net> - 2.8-1
- Update to 2.8

* Sun Mar 15 2020 Package Store <kitsune.solar@gmail.com> - 2.7.1-101
- UPD: SPEC-file.
- UPD: Only Fedora build.

* Fri Mar 13 2020 Package Store <kitsune.solar@gmail.com> - 2.7.1-100
- NEW: v2.7.1.
- UPD: master-d1bbbb.

* Thu Oct 03 2019 Package Store <kitsune.solar@gmail.com> - 2.6-100
- NEW: v2.6.

* Sat Jun 29 2019 Package Store <kitsune.solar@gmail.com> - 2.5-100
- NEW: v2.5.
- UPD: MARKETPLACE.

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.4-2
- Perl 5.30 rebuild

* Sun Mar 17 2019 Kitsune Solar <kitsune.solar@gmail.com> - 2.4-1
- Update to 2.4.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3-2
- F-30: rebuild against ruby26

* Wed Nov 28 2018 Paul Komkoff <i@stingr.net> - 2.3-1
- Update to 2.3
- Enable python plugin.

* Tue Sep 18 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2-2
- Switch to use python3

* Mon Aug 6 2018 Paul Komkoff <i@stingr.net> - 2.2-2
- Fix epel build (#1505750)

* Wed Jul 18 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2-1
- Update to 2.2 and clean spec

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.1-4
- Perl 5.28 rebuild

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Paul Komkoff <i@stingr.net> - 2.0.1-1
- Update to 2.0.1 (#1528100)

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.9.1-3
- Rebuilt for switch to libxcrypt

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.1-2
- F-28: rebuild for ruby25

* Sat Sep 23 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1 (#1494835)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Paul Komkoff <i@stingr.net> - 1.9-1
- new upstream version 1.9 #1450583

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.1-2
- Perl 5.26 rebuild

* Sun Apr 30 2017 Kevin Fenzi <kevin@scrye.com> - 1.7.1-1
- Update to 1.7.1. Fixes bug #1413366
- Fix for CVE-2017-8073

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6-3
- F-26: rebuild for ruby24

* Sat Nov 26 2016 Paul Komkoff <i@stingr.net> - 1.6-2
- add version constraint for asciidoctor.

* Sun Nov 20 2016 Paul Komkoff <i@stingr.net> - 1.6-1
- new upstream version 1.6 (#1297198)

* Thu Jul 21 2016 Than Ngo <than@redhat.com> - 1.5-2
- Rebuilt for glibc: Revert sendmsg/recvmsg ABI changes

* Sun Jun 05 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.5-1
- update to upstream release 1.5
- temporarily disable v8 on rawhide (25)

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.4-4
- Perl 5.24 rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Vít Ondruch <vondruch@redhat.com> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Sun Jan 10 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.4-1
- update to upstream release 1.4

* Mon Sep 14 2015 Paul Komkoff <i@stingr.net> - 1.3-2
- Trying to fix broken build.

* Sat Sep 05 2015 Paul Komkoff <i@stingr.net> - 1.3-1
- new upstream version (#1254000)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.2-3
- Perl 5.22 rebuild

* Fri May 22 2015 Dan Horák <dan[at]danny.cz> - 1.2-2
- v8 is available only on selected arches (#1221689)

* Sun May 10 2015 Paul Komkoff <i@stingr.net> - 1.2-1
- new upstream version (#1220153)

* Sun Mar 8 2015 Paul Komkoff <i@stingr.net> - 1.1.1-1
- new upstream version (#1181572)

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-3
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Build plugins with -fPIC

* Wed Oct 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0.1-2
- fix default ca-bundle.crt location (#1151748)

* Sun Sep 28 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0.1-1
- update to upstream release 1.0.1

* Sat Sep 20 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0-3
- patch from upstream to fix FTBFS (#1144761)

* Sat Sep 20 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0-2
- add conditionals for versioned/unversioned documentation directory

* Sat Sep 13 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0-1
- update to upstream release 1.0
- add %%{?_isa} to Requires
- add additional BR: asciidoc ca-certificates guile-devel source-highlight
- add man page and docs
- temporarily add cflags when building on rawhide (fedora 21) due to FTBFS

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Tue Apr 29 2014 Vít Ondruch <vondruch@redhat.com> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Apr 09 2014 Russell Golden <niveusluna@niveusluna.org> - 0.4.3-2
- Build and patch for el6
  - This is a _nasty_ hack intended solely to get the binary working.
  - The binary does seem to work whether or not aspell is enabled.

* Sun Feb 16 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.3-1
- update to upstream release 0.4.3

* Mon Nov 11 2013 Paul Komkoff <i@stingr.net> - 0.4.2-4
- enable enchant detection / aspell build.

* Fri Nov 08 2013 Russell Golden <niveusluna@niveusluna.org> - 0.4.2-3
- Forgot to remove the patch1 instruction

* Fri Nov 08 2013 Russell Golden <niveusluna@niveusluna.org> - 0.4.2-2
- Forgot to remove 0.4.1 from the sources file. (Rawhide only.)

* Fri Nov 08 2013 Russell Golden <niveusluna@niveusluna.org> - 0.4.2-1
- rename binary from "weechat-curses" to "weechat" (with symbolic link "weechat-curses" for compatibility)
- add secured data (encryption of passwords or private data), new command /secure, new file sec.conf
- search of regular expression in buffer with text emphasis, in prefixes, messages or both
- add option "scroll_beyond_end" for command /window
- add optional buffer context in bar items (for example to display bitlbee nicklist in a root bar)
- new options weechat.look.hotlist_{prefix|suffix}
- new option weechat.look.key_bind_safe to prevent any key binding error from user
- new option weechat.network.proxy_curl to use a proxy when downloading URLs with curl
- display day change message dynamically
- support of wildcards in IRC commands (de)op/halfop/voice
- new option irc.look.notice_welcome_redirect to redirect channel welcome notices to the channel buffer
- new option irc.look.nick_color_hash: new hash algorithm to find nick colors (variant of djb2)
- add info about things defined by a script in the detailed view of script (/script show)
- support of "enchant" library in aspell plugin
- many bugs fixed.
- no more man page by default

* Sun Aug 04 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.1-3
- add BR: libgcrypt-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.1-1
- update to upstream release 0.4.1
- clean old changelog entries
- fix enchant patch set
- Ruby 2.0 crash now fixed upstream

* Tue Apr 02 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.0-7
- filter out automatically generated Provides that shouldn't be there (#947399)

* Sat Mar 30 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.0-6
- enable _hardened_build as weechat matches the "long running" criteria
- remove redundant PIE patch

* Fri Mar 29 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.0-5
- fix crash with Ruby 2.0

* Wed Mar 13 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.0-4
- rebuild with Ruby 2.0.0
- add patch to properly obtain the version of ruby
- fix bogus dates in older changelog entries

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.0-2
- reimplement enchant support as a separate patch
- implement additional enchant support for displaying spelling suggestions
  in weechat_aspell_get_suggestions(), which is a new function introduced by
  upstream in 0.4.0

* Mon Jan 21 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.4.0-1
- update to upstream release 0.4.0
- add CMAKE options (DPREFIX and DLIBDIR) which negate the need to patch
- remove enchant patches to keep close to upstream

* Sun Dec 02 2012 Paul Komkoff <i@stingr.net> - 0.3.9.2-2
- add zlib-devel dependency for epel6/ppc build

* Sat Dec  1 2012 Paul P. Komkoff Jr <i@stingr.net> - 0.3.9.2-1
- new upstream, long overdue

* Mon Nov 19 2012 Paul P. Komkoff Jr <i@stingr.net> - 0.3.8-4
- fix bz#878025

* Fri Nov 09 2012 Paul P. Komkoff Jr <i@stingr.net> - 0.3.8-3
- fix bz#875181

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Russell Golden <niveusluna@niveusluna.org> - 0.3.8-1
- New upstream version

* Fri Mar 16 2012 Paul P. Komkoff Jr <i@stingr.net> - 0.3.7-1
- new upstream version

* Wed Feb 08 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.6-2
- Rebuilt for Ruby 1.9.3.

* Wed Jan 18 2012 Paul P. Komkoff Jr <i@stingr.net> - 0.3.6-1
- new upstream version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Paul P. Komkoff Jr <i@stingr.net> - 0.3.5-2
- rebuilt

* Thu Jun  2 2011 Paul P. Komkoff Jr <i@stingr.net> - 0.3.5-1
- new upstream version

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 28 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.3.3-2
- fixed cmake config to accept python27

* Wed Aug 25 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.3.3-1
- new upstream version

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri May  7 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.3.2-2
- spec file fix

* Thu May  6 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.3.2-1
- new upstream version
