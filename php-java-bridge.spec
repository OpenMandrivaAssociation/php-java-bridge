%define modname         java-bridge
%define webappdir       %{_var}/lib/tomcat5/webapps
%define build_free      1
%define gcj_support     1

%define _requires_exceptions pear(lucene/All.php)\\|pear(rt/java_io_File.php)\\|pear(javabridge/Java.php)\\|pear(itext/All.php)\\|pear(rt/java_awt_Color.php)\\|pear(rt/java_io_ByteArrayOutputStream.php)\\|pear(rt/java_lang_System.php)\\|pear(java/Java.php)

Summary:        PHP Hypertext Preprocessor to Java Bridge
Name:           php-%{modname}
Version:        4.0.1
Release:        %mkrel 3
Epoch:          0
Group:          Development/PHP
License:        PHP License
URL:            http://php-java-bridge.sourceforge.net/
Source0:        http://internap.dl.sourceforge.net/sourceforge/php-java-bridge/php-java-bridge_%{version}.tar.gz
Requires:       %{name}-backend
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
Requires:       myfaces
Requires:       servletapi5
BuildRequires:  ejb
BuildRequires:  gcc-c++
BuildRequires:  java-devel >= 0:1.4.2
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
BuildRequires:  myfaces
BuildRequires:  servletapi5
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
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
Requires:       php-java-bridge = %{epoch}:%{version}
Requires:       tomcat5
Requires(post): rpm-helper
Requires(postun): rpm-helper
Obsoletes:      php-java-bridge-standalone
Provides:       %{name}-backend

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
pushd examples/php+jsp
%{jar} xf numberGuess.jar
popd
%if %{build_free}
%{_bindir}/find . -name "*.class" | %{_bindir}/xargs -t %{__rm} -f
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm} -f
%{_bindir}/find . -name "*.war" | %{_bindir}/xargs -t %{__rm} -f
%{_bindir}/find . -name "*.dll" | %{_bindir}/xargs -t %{__rm} -f
%{_bindir}/find . -name "*.exe" | %{_bindir}/xargs -t %{__rm} -f
%endif
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
%{java_home}/bin/rmic -classpath .:$(build-classpath ejb) DocumentHome   
%{java_home}/bin/rmic -classpath .:$(build-classpath ejb) DocumentRemote   
%{__rm} -f *_Skel*.class
%{jar} cf ../documentBean.jar *
popd
pushd unsupported
%{__ln_s} %{_javadir}/myfaces/myfaces-jsf-api.jar jsf-api.jar
%{__ln_s} %{_javadir}/myfaces/myfaces-impl.jar jsf-impl.jar
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
%{__perl} -pi -e 's|\$CC|\$CC -fPIC|g' tests.m4/java_check_jni.m4      

%build
export CLASSPATH=
%{_bindir}/phpize
%{__aclocal} -I tests.m4
%{__autoconf}
(cd server && %{__autoconf})
%{configure2_5x} --with-java=%{java_home} \
                 --enable-servlet=%{_javadir}/servletapi5.jar \
                 --enable-faces=%{_javadir}/myfaces/myfaces-jsf-api.jar
%{__make}

%install
%{__rm} -rf %{buildroot}

pushd server
%{jar} uf JavaBridge.war TestInstallation.class
popd

%{makeinstall} INSTALL_ROOT=%{buildroot}

%{__rm} -f %{buildroot}%{_libdir}/php/extensions/libnatcJavaBridge.a

%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__install} -m 644 java-servlet.ini %{buildroot}%{_sysconfdir}/php.d/java-servlet.ini
%{__install} -m 644 java.ini %{buildroot}%{_sysconfdir}/php.d/java.ini
%{__install} -m 644 mono.ini %{buildroot}%{_sysconfdir}/php.d/mono.ini

for i in examples/php+jsp/index.php examples/php+jsp/index.html \
  examples/java-server-faces/helloWorld.jsp \
  examples/java-server-faces/page2.jsp tests.php5/NumberTest.java \
  tests.php4/NumberTest.java; do
  %{__perl} -pi -e 's/\r$//g' ${i}
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm --exclude %{_libdir}/php/extensions/JavaBridge.war
%endif

%{__mkdir_p} %{buildroot}%{webappdir}/JavaBridge
pushd %{buildroot}%{webappdir}/JavaBridge
%{jar} xf %{buildroot}%{_libdir}/php/extensions/JavaBridge.war
%{__rm} -f %{buildroot}%{_libdir}/php/extensions/JavaBridge.war
popd

%{__cp} -a examples/J2EE/RMI-IIOP/documentBean.jar %{buildroot}%{webappdir}/JavaBridge/WEB-INF/lib

%{__rm} %{buildroot}%{_libdir}/php/extensions/stamp

%{__chmod} 755 %{buildroot}%{webappdir}/JavaBridge/WEB-INF/cgi/*.sh
%{__chmod} 755 %{buildroot}%{webappdir}/JavaBridge/test.php

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post tomcat
%{_post_webapp}

%postun tomcat
%{_postun_webapp}

%files
%defattr(0644,root,root,0755)
%doc README CREDITS NEWS test.php INSTALL.LINUX security COPYING INSTALL RPM-GPG-KEY VERSION
#%doc LICENSE
%{_libdir}/php/extensions/JavaBridge.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif
%attr(0755,root,root) %{_libdir}/php/extensions/java.so
%attr(0755,root,root) %{_libdir}/php/extensions/libnatcJavaBridge.so
%attr(0755,root,root) %{_libdir}/php/extensions/RunJavaBridge
%attr(0755,root,root) %{_libdir}/php/extensions/java
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
%doc README.GNU_JAVA README.MONO+NET ChangeLog PROTOCOL.TXT documentation examples tests.php5 tests.php4 php_java_lib INSTALL
%{_libdir}/php/extensions/php-script.jar
%{_libdir}/php/extensions/script-api.jar


