# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name       digester
%define short_name      commons-%{base_name}
%define section         free

Name:           jakarta-%{short_name}
Version:        1.7
Release:        10.6%{?dist}
Epoch:          0
Summary:        Jakarta Commons Digester Package
License:        ASL 2.0
Group:          Development/Libraries/Java
Source0:        http://archive.apache.org/dist/commons/digester/source/commons-digester-1.7-src.tar.gz
Source1:        commons-digester-1.7-component-info.xml
URL:            http://jakarta.apache.org/commons/digester/
BuildRequires:  ant
BuildRequires:  jakarta-commons-beanutils >= 0:1.7
BuildRequires:  jakarta-commons-logging >= 0:1.0
BuildRequires:  jpackage-utils > 0:1.5
Requires:       jakarta-commons-beanutils >= 0:1.7
Requires:       jakarta-commons-logging >= 0:1.0
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:       %{short_name} = %{epoch}:%{version}-%{release}
Obsoletes:      %{short_name} < %{epoch}:%{version}-%{release}

%description
The goal of Digester project is to create and maintain a XML -> Java
object mapping package written in the Java language to be distributed
under the ASF license.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
# for /bin/rm and /bin/ln
Requires(post): coreutils
Requires(postun): coreutils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src


tag=`echo %{name}-%{version}-%{release} | sed 's|\.|_|g'`
sed -i "s/@TAG@/$tag/g" %{SOURCE1}

%build
cp LICENSE.txt ../LICENSE

export CLASSPATH=%(build-classpath commons-logging commons-beanutils junit)
ant dist

# Build rss -- needed by struts
export CLASSPATH=$CLASSPATH:`pwd`/dist/%{short_name}.jar
(cd src/examples/rss; ant dist)

rm ../LICENSE

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p src/examples/rss/dist/%{short_name}-rss.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}-rss.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%changelog
* Mon Feb 22 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-10.6
- Fix Soure0.

* Thu Jan 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.7-10.5
- Remove gcj_support.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.7-10.4
- Rebuilt for RHEL 6

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 0:1.7-10.3
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-9.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.7-7.3
- fix license tag
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.7-7jpp.2
- Autorebuild for GCC 4.3

* Fri Sep 07 2007 Matt Wringe <mwringe@redhat.com> - 0:1.7-6jpp.2
- Fix unowned dir (/usr/lib/gcj/jakarta-commons-digester)

* Mon Jan 22 2007 Vivek Lakshmanan <vivekl at redhat.com> - 0:1.7-6jpp.1
- Resynch with JPP release

* Tue Jan 16 2007 Vivek Lakshmanan <vivekl at redhat.com> - 0:1.7-5jpp.3
- Update component-info.xml to add scm and tag attribute instead of a comment
- Remove the export of a versioned jar

* Tue Jan 9 2007 Vivek Lakshmanan <vivekl at redhat.com> - 0:1.7-5jpp.2
- Upgrade to latest from JPP and FC6
- Remove old RHUG specific trigger
- Add support for conditional build of repolib package
- Build repolib package by default

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:1.7-5jpp.1
- Merge with upstream version:
 - Add missing requires for javadoc

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 1.7-4jpp_3fc
- Requires(post/postun): coreutils

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.7-4jpp_2fc
- Rebuilt

* Wed Jul 19 2006 Matt Wringe <mwringe at redhat.com> - 0:1.7-4jpp_1fc
- Merged with upstream version

* Wed Jul 19 2006 Matt Wringe <mwringe at redhat.com> - 0:1.7-4jpp
- Removed separate definition of name, version and release.

* Mon Jul 17 2006 Matt Wringe <mwringe at redhat.com> - 0:1.7-3jpp
- Added conditional native compiling

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.7-2jpp
- First JPP 1.7 build

* Tue Jul 26 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.7-1jpp
- Upgrade to 1.7

* Thu Nov 26 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.6-2jpp
- Rebuild so that rss package is included

* Thu Oct 21 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.6-1jpp
- Upgrade to 1.6

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.5-4jpp
- Rebuild with ant-1.6.2

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:1.5-3jpp
- update for JPackage 1.5

* Thu May 08 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.5-2jpp
- used correct JPP 1.5 spec file

* Thu May 08 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.5-2jpp
- 1.5

* Tue Mar 25 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> - 1.4.1-2jpp
- for jpackage-utils 1.5

* Mon Mar  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.4.1-1jpp
- Update to 1.4.1.
- No macros in URL and SourceX tags.
- Run unit tests during build.
- Remove spurious api/ from installed javadoc path.
- Some spec file cleanup.

* Thu Feb 27 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.4-2jpp
- fix ASF license and add packager tag

* Fri Feb 14 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.4-1jpp
- 1.4

* Tue Aug 20 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.3-1jpp
- 1.3

* Fri Jul 12 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.2-3jpp
- update to meet new jaxp_parser_impl and xml-commons-apis

* Mon Jun 10 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.2-2jpp
- use sed instead of bash 2.x extension in link area to make spec compatible
  with distro using bash 1.1x

* Fri Jun 07 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.2-1jpp
- 1.2
- added short names in _javadir, as does jakarta developpers
- first jPackage release
