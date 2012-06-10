%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_channel pear.symfony.com
%global pear_name %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')

Name:             php-symfony2-Console
Version:          2.0.14
Release:          3%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/doc/current/components/console.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildArch:        noarch
BuildRequires:    php-pear >= 1:1.4.9-1.2
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php-common >= 5.3.2
Requires:         php-mbstring
Requires:         php-pcre
Requires:         php-posix
Requires:         php-readline
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
The Console component eases the creation of beautiful and testable command line
interfaces.

The Console component allows you to create command-line commands. Your console
commands can be used for any recurring task, such as cron jobs, imports, or
other batch jobs.


%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Move documentation to correct location
# NOTE: Remove this when upstream updates their package.xml with role="doc"
#       for these files
mkdir -p $RPM_BUILD_ROOT%{pear_docdir}/Symfony/Component/%{pear_name}
mv -f \
    $RPM_BUILD_ROOT%{pear_phpdir}/Symfony/Component/%{pear_name}/composer.json \
    $RPM_BUILD_ROOT%{pear_phpdir}/Symfony/Component/%{pear_name}/LICENSE \
    $RPM_BUILD_ROOT%{pear_phpdir}/Symfony/Component/%{pear_name}/README.md \
    $RPM_BUILD_ROOT%{pear_docdir}/Symfony/Component/%{pear_name}

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%doc %{pear_docdir}/Symfony/Component/%{pear_name}
%dir %{pear_docdir}/Symfony/Component
%dir %{pear_docdir}/Symfony
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Symfony/Component/%{pear_name}
%dir %{pear_phpdir}/Symfony/Component
%dir %{pear_phpdir}/Symfony


%changelog
* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-3
- Moved documentation to correct location

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-2
- Removed BuildRoot
- Changed php require to php-common
- Added the following requires based on phpci results:
  php-mbstring, php-pcre, php-posix, php-readline
- %%description update
- Removed %%defattr from %%files section

* Fri May 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-1
- Updated to upstream version 2.0.14
- %%global instead of %%define
- Removed unnecessary cd from %%build section

* Wed May 2 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.13-1
- Updated to upstream version 2.0.13

* Sat Apr 21 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.12-1
- Initial package
