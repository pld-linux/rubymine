Summary:	The Most Intelligent Ruby and Rails IDE
Name:		rubymine
Version:	2016.2.5
Release:	1
# TODO: figure out what's the licensing and redistribution
License:	?
Group:		Development/Tools
Source0:	https://download.jetbrains.com/ruby/RubyMine-%{version}.tar.gz
# NoSource0-md5:	23d377c3ddf2514ad0543a2e41c1df8b
NoSource:	0
Source1:	%{name}.desktop
Patch0:		pld.patch
URL:		https://www.jetbrains.com/ruby/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	desktop-file-utils
Requires:	jre >= 1.6
Requires:	which
Suggests:	cvs
Suggests:	git-core
Suggests:	subversion
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't strip fsnotifier, it's size is checked for "outdated binary"
# https://bugs.archlinux.org/task/34703
# http://git.jetbrains.org/?p=idea/community.git;a=blob;f=platform/platform-impl/src/com/intellij/openapi/vfs/impl/local/FileWatcher.java;h=004311b96a35df1ffc2c87baba78a8b2a8809f7d;hb=376b939fd6d6ec4c12191a5f90503d9d62c501da#l173
%define		_noautostrip	.*/fsnotifier.*

# use /usr/lib, 64bit files do not conflict with 32bit files (64 suffix)
# this allows to install both arch files and to use 32bit jdk on 64bit os
%define		_appdir		%{_prefix}/lib/%{name}

%description
JetBrains RubyMine is a commercial IDE for Ruby and Ruby on Rails
built on JetBrains' IntelliJ IDEA platform.

RubyMine provides intelligent code completion for Ruby and Ruby on
Rails code, on-the-fly code analysis and refactoring support for both
plain Ruby projects and web applications built with Ruby on Rails.

%prep
%setup -qn RubyMine-%{version}

# keep only single arch files (don't want to pull 32bit deps by default),
# if you want to mix, install rpm from both arch
%ifarch %{ix86}
rm bin/fsnotifier64
rm bin/libyjpagent-linux64.so
rm bin/rubymine64.vmoptions
rm bin/libbreakgen64.so
%endif
%ifarch %{x8664}
rm bin/fsnotifier
rm bin/libyjpagent-linux.so
rm bin/rubymine.vmoptions
rm bin/libbreakgen.so
%endif
rm -r lib/libpty/{macosx,win}
rm bin/fsnotifier-arm
%patch0 -p1
chmod a+rx bin/*.so bin/fsnotifier*
mv bin/rubymine.png .
mv bin/RMlogo.svg .

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -l build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -p rubymine.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -p RMlogo.svg $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.svg
cp -a$l bin help lib license plugins rb rubystubs* $RPM_BUILD_ROOT%{_appdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln -s %{_appdir}/bin/rubymine.sh $RPM_BUILD_ROOT%{_bindir}/rubymine

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_appdir}
%{_appdir}/help
%{_appdir}/lib
%{_appdir}/license
%{_appdir}/plugins
%{_appdir}/rb
%{_appdir}/rubystubs*
%dir %{_appdir}/bin
%{_appdir}/bin/rubymine*.vmoptions
%{_appdir}/bin/idea.properties
%{_appdir}/bin/log.xml
%attr(755,root,root) %{_appdir}/bin/rubymine.sh
%attr(755,root,root) %{_appdir}/bin/rinspect.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier*
%attr(755,root,root) %{_appdir}/bin/libyjpagent-linux*.so
%attr(755,root,root) %{_appdir}/bin/libbreakgen*.so
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_pixmapsdir}/%{name}.svg
