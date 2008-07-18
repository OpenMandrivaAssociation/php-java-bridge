%define _fortify_cflags %nil

%bcond_without          faces

%define modname         java-bridge
%define webappdir       %{_var}/lib/tomcat5/webapps
%define build_free      1
%define gcj_support     1

%define _requires_exceptions pear(lucene/All.php)\\|pear(rt/java_io_File.php)\\|pear(javabridge/Java.php)\\|pear(itext/All.php)\\|pear(rt/java_awt_Color.php)\\|pear(rt/java_io_ByteArrayOutputStream.php)\\|pear(rt/java_lang_System.php)\\|pear(java/Java.php)\\|pear(rt/java_util_LinkedList.php)

Name:           php-%{modname}
Version:        5.2.2
Release:        %mkrel 0.0.3
Epoch:          0
Summary:        PHP Hypertext Preprocessor to Java Bridge
Group:          Development/PHP
License:        PHP License
URL:            http://php-java-bridge.sourceforge.net/
# XXX: upstream is terrible about providing pure source releases
# XXX: and CVS doesn't help because it contains binaries also
# cvs -d:pserver:anonymous@php-java-bridge.cvs.sourceforge.net:/cvsroot/php-java-bridge login   
# cvs -z3 -d:pserver:anonymous@php-java-bridge.cvs.sourceforge.net:/cvsroot/php-java-bridge co -r upstream_version_5_0_0 php-java-bridge
# mv php-java-bridge php-java-bridge-5.0.0
# tar cvjf php-java-bridge-5.0.0.tar.bz2 php-java-bridge-5.0.0
#Source0:        %{name}-%{version}.tar.bz2
Source0:        http://internap.dl.sourceforge.net/sourceforge/php-java-bridge/php-java-bridge_%{version}.tar.gz
Source1:        %{name}-cvs.sh
Requires:       %{name}-backend = %{epoch}:%{version}-%{release}
Requires:       ejb
Requires:       java >= 0:1.4.2
Requires:       mod_php
Requires:       jakarta-commons-beanutils
Requires:       jakarta-commons-collections
Requires:       jakarta-commons-digester
Requires:       jakarta-commons-logging
Requires:       jakarta-poi
Requires:       jakarta-taglibs-standard
Requires:       kawa
Requires:       log4j
Requires:       lucene
%if %with faces
Requires:       myfaces
%endif
Requires:       servletapi5
BuildRequires:  java-rpmbuild
BuildRequires:  ejb
BuildRequires:  php-devel >= 3:5.2.0
BuildRequires:  jakarta-commons-beanutils
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-digester
BuildRequires:  jakarta-commons-logging
BuildRequires:  jakarta-poi
BuildRequires:  jakarta-taglibs-standard
BuildRequires:  kawa
BuildRequires:  log4j
BuildRequires:  lucene
%if %with faces
BuildRequires:  myfaces
%endif
BuildRequires:  servletapi5
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description 
PHP Hypertext Preprocessor to Java Bridge is a Java module/extension
for the PHP script language. It contains a java extension for
PHP/Apache HTTP server and a simple backend which automatically
starts and stops when the HTTP server starts/stops. The bridge log
appears in the http server error log.

%package tomcat
Summary:        Tomcat/J2EE backend for the PHP/Java Bridge
Group:          Development/PHP
Requires(post): apache-base
Requires(postun): apache-base
Requires:       apache-base
Requires:       php-java-bridge = %{epoch}:%{version}
Requires:       tomcat5
Requires(post): rpm-helper
Requires(postun): rpm-helper
Requires(post): tomcat5
Requires(postun): tomcat5
Obsoletes:      php-java-bridge-standalone < %{epoch}:%{version}-%{release}
Provides:       %{name}-backend = %{epoch}:%{version}-%{release}

%description tomcat
The Tomcat/J2EE backend for the PHP/Java Bridge deploys the J2EE
backend into the Tomcat servlet engine. The Tomcat backend is more
than two times faster than the standalone backend but less secure
since it uses named pipes instead of abstract local unix domain
sockets.

%package devel
Summary:        PHP/Java Bridge development files and documentation
Group:          Development/PHP
Requires:       php-java-bridge = %{epoch}:%{version}

%description devel
The PHP/Java Bridge development files and documentation contain the
development documentation and the development files needed to create
Java applications with embedded PHP scripts.

%prep
%setup -q
%{_bindir}/find . -type d -name CVS | %{_bindir}/xargs %{__rm} -rf
%{_bindir}/find documentation/API -name '*.html' -o -name '*.css' | %{_bindir}/xargs %{__perl} -pi -e 's/\r$//g'
for i in examples/php+jsp/index.php \
         tests.php5/NumberTest.java; do
  test -w $i && %{__perl} -pi -e 's/\r$//g' ${i} || exit 1
done

%{__rm} server/WEB-INF/cgi/php-cgi-i386-linux
%{__rm} server/WEB-INF/cgi/php-cgi-x86-sunos
%{__rm} server/WEB-INF/cgi/php-cgi-i386-freebsd

%{__ln_s} tests.php5/ tests
pushd examples/php+jsp
%{jar} xf numberGuess.jar
popd

%if %{build_free}
%{_bindir}/find . -name "*.class" | %{_bindir}/xargs -t %{__rm}
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm}
%{_bindir}/find . -name "*.war" | %{_bindir}/xargs -t %{__rm}
%{_bindir}/find . -name "*.dll" | %{_bindir}/xargs -t %{__rm}
%{_bindir}/find . -name "*.exe" | %{_bindir}/xargs -t %{__rm}
%{__perl} -pi -e 's| WEB-INF/cgi/\*\.exe||' server/Makefile.am
%endif

pushd unsupported
%if %with faces
%{__ln_s} %{_javadir}/myfaces/myfaces-jsf-api.jar jsf-api.jar
%{__ln_s} %{_javadir}/myfaces/myfaces-impl.jar jsf-impl.jar
%endif
%{__ln_s} %{_javadir}/jakarta-taglibs-core.jar jstl.jar
%{__ln_s} %{_javadir}/kawa.jar kawa.jar
%{__ln_s} %{_javadir}/log4j.jar log4j.jar
%{__ln_s} %{_javadir}/poi.jar poi.jar
%{__ln_s} %{_javadir}/servletapi5.jar servlet-api.jar
%{__ln_s} %{_javadir}/jakarta-taglibs-standard.jar standard.jar
%{__ln_s} %{_javadir}/commons-beanutils.jar commons-beanutils.jar
%{__ln_s} %{_javadir}/commons-collections.jar commons-collections.jar
%{__ln_s} %{_javadir}/commons-digester.jar commons-digester.jar
%{__ln_s} %{_javadir}/commons-logging.jar commons-logging.jar
%{__ln_s} %{_javadir}/ejb.jar ejb.jar
%{__ln_s} %{_javadir}/lucene.jar lucene.jar
popd

export CLASSPATH=
pushd server
%{javac} TestInstallation.java
popd
pushd examples/php+jsp
%{javac} num/NumberGuessBean.java
%{jar} cf numberGuess.jar num
%{__rm} -rf num
popd
pushd examples/J2EE/RMI-IIOP/src
%{javac} -classpath $(build-classpath ejb) *.java
%{jar} cf ../../../../unsupported/documentBeanClient.jar *
#%%{java_home}/bin/rmic -classpath .:$(build-classpath ejb) DocumentHome   
#%%{java_home}/bin/rmic -classpath .:$(build-classpath ejb) DocumentRemote   
#%%{__rm} -f *_Skel*.class
%{jar} cf ../documentBean.jar *
popd

%{__perl} -pi -e 's|\$CC|\$CC -fPIC|g' tests.m4/java_check_jni.m4      

%{_bindir}/phpize
%{__aclocal} -I . -I ./tests.m4/
%{__autoconf}
pushd server
%{__aclocal} -I . -I ../tests.m4/
%{__autoconf}
popd

%{__perl} -pi -e 's/^Class-Path:.*//' server/META-INF/MANIFEST.MF

%build
%serverbuild

export CLASSPATH=
%{configure2_5x} --with-java=%{java_home} \
                 --enable-servlet=%{_javadir}/servletapi5.jar \
%if %with faces
                 --enable-faces=%{_javadir}/myfaces/myfaces-jsf-api.jar
%else
                 --disable-faces
%endif
%{__make}

%install
%{__rm} -rf %{buildroot}

pushd server
%{jar} uf JavaBridge.war TestInstallation.class
popd

%{__make} INSTALL_ROOT=%{buildroot} install

%{__rm} -f %{buildroot}%{_libdir}/php/extensions/libnatcJavaBridge.a

%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__install} -m 644 java-servlet.ini %{buildroot}%{_sysconfdir}/php.d/java-servlet.ini
%{__install} -m 644 java.ini %{buildroot}%{_sysconfdir}/php.d/java.ini
%{__install} -m 644 mono.ini %{buildroot}%{_sysconfdir}/php.d/mono.ini

%{__mkdir_p} %{buildroot}%{webappdir}/JavaBridge
pushd %{buildroot}%{webappdir}/JavaBridge
%{jar} xf %{buildroot}%{_libdir}/php/extensions/JavaBridge.war
%{__rm} -f %{buildroot}%{_libdir}/php/extensions/JavaBridge.war
popd

%{__cp} -a examples/J2EE/RMI-IIOP/documentBean.jar %{buildroot}%{webappdir}/JavaBridge/WEB-INF/lib

%{__rm} %{buildroot}%{_libdir}/php/extensions/stamp

%{__chmod} 755 %{buildroot}%{webappdir}/JavaBridge/WEB-INF/cgi/*.sh
%{__chmod} 755 %{buildroot}%{webappdir}/JavaBridge/test.php

pushd %{buildroot}%{webappdir}/JavaBridge/WEB-INF/lib
%{__rm} commons-beanutils.jar && %{__ln_s} %{_javadir}/commons-beanutils.jar commons-beanutils.jar
%{__rm} commons-collections.jar && %{__ln_s} %{_javadir}/commons-collections.jar commons-collections.jar
%{__rm} commons-digester.jar && %{__ln_s} %{_javadir}/commons-digester.jar commons-digester.jar
%{__rm} commons-logging.jar && %{__ln_s} %{_javadir}/commons-logging.jar commons-logging.jar
%{__rm} ejb.jar && %{__ln_s} %{_javadir}/ejb.jar ejb.jar
%{__rm} jstl.jar && %{__ln_s} %{_javadir}/jakarta-taglibs-core.jar jstl.jar
%{__rm} kawa.jar && %{__ln_s} %{_javadir}/kawa.jar kawa.jar
%{__rm} lucene.jar && %{__ln_s} %{_javadir}/lucene.jar lucene.jar
%{__rm} poi.jar && %{__ln_s} %{_javadir}/poi.jar poi.jar
%{__rm} standard.jar && %{__ln_s} %{_javadir}/jakarta-taglibs-standard.jar standard.jar
popd

%{gcj_compile}

%check
%{__make} test

%post
%if %{gcj_support}
%{update_gcjdb}
%endif

if [ -f %{_var}/lock/subsys/tomcat5 ]; then
    /sbin/service tomcat5 restart >/dev/null || :
fi

%{_post_webapp}

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif

if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/tomcat5 ]; then
        /sbin/service tomcat5 restart >/dev/null || :
    fi
fi

%{_postun_webapp}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README CREDITS NEWS test.php INSTALL.LINUX security COPYING INSTALL RPM-GPG-KEY VERSION
#%doc LICENSE
%{_libdir}/php/extensions/JavaBridge.jar
%{gcj_files}
%attr(0755,root,root) %{_libdir}/php/extensions/java.so
%attr(0755,root,root) %{_libdir}/php/extensions/libnatcJavaBridge.so
%attr(0755,root,root) %{_libdir}/php/extensions/RunJavaBridge
%if 0
%attr(0755,root,root) %{_libdir}/php/extensions/java
%endif
%exclude %{_libdir}/php/extensions/javabridge.policy
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/java.ini
%exclude %config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/mono.ini

%files tomcat
%defattr(0644,root,root,0755)
%doc INSTALL.J2EE
%defattr(-,root,tomcat,775)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/java-servlet.ini
%{webappdir}/*

%files devel
%defattr(0644,root,root,0755)
%doc README.GNU_JAVA README.MONO+NET ChangeLog PROTOCOL.TXT documentation examples tests.php5 php_java_lib INSTALL
%{_libdir}/php/extensions/*
