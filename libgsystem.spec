#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	LibGSystem - GIO-based library for use by operating system components
Summary(pl.UTF-8):	LibGSystem - biblioteka oparta na GIO przeznaczona dla komponentów systemu operacyjnego
Name:		libgsystem
Version:	2014.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgsystem/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	5d4d4cd4ae0cf7f774d87ebccf5615f2
URL:		https://wiki.gnome.org/Projects/LibGSystem
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gobject-introspection-devel >= 1.34.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libtool >= 2:2.2.4
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	systemd-devel >= 1:200
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.34.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibGSystem is a GIO-based library, targeted primarily for use by
operating system components. It has a few goals:
- Provide macros for the GCC attribute(cleanup) that work with GLib
  data types. Using these can dramatically simplify local memory
  management inside functions.
- Prototype and test APIs that will eventually be in GLib. Currently
  these include "GSSubprocess" for launching child processes, and
  some GFile helpers.
- Provide Linux-specific APIs in a nicer GLib fashion, such as
  O_NOATIME.

%description -l pl.UTF-8
LibGSystem to oparta na GIO biblioteka przeznaczona głównie do
wykorzystania w komponentach systemu operacyjnego. Ma kilka zadań:
- dostarczenie makr dla attribute(cleanup) w GCC, działających z
  typami danych GLiba; przy ich użyciu można znacząco uprościć
  lokalne zarządzanie pamięcią wewnątrz funkcji
- prototypowe i testowe API, które ewentualnie znajdą się w GLibie;
  obecnie obejmują "GSSubprocess" do uruchamiania procesów potomnych
  oraz kilka funkcji pomocniczych GFile
- dostarczenie API specyficznych dla Linuksa w stylu GLiba, takich jak
  O_NOATIME.

%package devel
Summary:	Header files for libgsystem library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgsystem
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.34.0

%description devel
Header files for libgsystem library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgsystem.

%package static
Summary:	Static libgsystem library
Summary(pl.UTF-8):	Statyczna biblioteka libgsystem
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libgsystem library.

%description static -l pl.UTF-8
Statyczna biblioteka libgsystem.

%package apidocs
Summary:	GSystem API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GSystem
Group:		Documentation

%description apidocs
GSystem API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GSystem.

%package -n dracut-libgsystem
Summary:	GSystem support for Dracut
Summary(pl.UTF-8):	Obsługa GSystem dla Dracuta
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	dracut

%description -n dracut-libgsystem
GSystem support for Dracut.

%description -n dracut-libgsystem -l pl.UTF-8
Obsługa GSystem dla Dracuta.

%prep
%setup -q

%build
# rebuild ac/am to get as-needed working
%{__libtoolize}
%{__gtkdocize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgsystem.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libgsystem.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgsystem.so.0
%{_libdir}/girepository-1.0/GSystem-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsystem.so
%{_includedir}/libgsystem
%{_datadir}/gir-1.0/GSystem-1.0.gir
%{_pkgconfigdir}/libgsystem.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgsystem.a
%endif
