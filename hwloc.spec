Summary:	Portable Hardware Locality
Name:		hwloc
Version:	1.3
Release:	1
License:	BSD
Group:		Applications/System
Source0:	http://www.open-mpi.org/software/hwloc/v1.3/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	e3ba4029ff4956727431495b642d1afb
URL:		http://www.open-mpi.org/projects/hwloc/
BuildRequires:	cairo-devel
BuildRequires:	libxml2-devel
BuildRequires:	numactl-devel
BuildRequires:	pciutils-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-proto-xproto-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Portable Hardware Locality (hwloc) software package provides a
portable abstraction (across OS, versions, architectures, ...) of the
hierarchical topology of modern architectures, including NUMA memory
nodes, sockets, shared caches, cores and simultaneous multithreading.
It also gathers various system attributes such as cache and memory
information. It primarily aims at helping applications with gathering
information about modern computing hardware so as to exploit it
accordingly and efficiently.

%package libs
Summary:	%{name} library
Group:		Libraries

%description libs
%{name} library.

%package devel
Summary:	Header files for %{name} library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name} library.

%prep
%setup -q

%build
%configure
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} %{_libdir}/lib%{name}.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-*
%attr(755,root,root) %{_bindir}/lstopo
%{_datadir}/%{name}
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man1/lstopo.1*
%{_mandir}/man7/%{name}.7*

%files libs
%defattr(644,root,root,755)
%{_pkgconfigdir}/%{name}.pc
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.4

%files devel
%defattr(644,root,root,755)
%doc doc/doxygen-doc/html doc/doxygen-doc/%{name}-*.pdf
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}
%{_includedir}/%{name}.h
%{_mandir}/man3/HWLOC_*.3*
%{_mandir}/man3/hwloc_*.3*
%{_mandir}/man3/hwlocality_*.3*
