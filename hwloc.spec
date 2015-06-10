# TODO: CUDA >= 30.20, NVML/nvidia-ml on bcond?
# NOTES (as of 1.10):
# - kerrighed library is only checked for; kerrighed support in hwloc uses /proc filesystem
# - myriexpress (open-mx) library is only checked for, but not used by hwloc code
#   (just in one test); in binary packages only interface header is included
Summary:	Portable Hardware Locality
Summary(pl.UTF-8):	Przenośna lokalizacja sprzętu
Name:		hwloc
Version:	1.10.0
Release:	2
License:	BSD
Group:		Applications/System
Source0:	http://www.open-mpi.org/software/hwloc/v1.10/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	c0502d93b1b8800cde28f84010bccfe0
URL:		http://www.open-mpi.org/projects/hwloc/
BuildRequires:	OpenCL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	cairo-devel
BuildRequires:	libXNVCtrl-devel
BuildRequires:	libibverbs-devel
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	ncurses-devel
BuildRequires:	numactl-devel
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libpciaccess-devel
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

%description -l pl.UTF-8
Pakiet HWLOC (Portable Hardware Locality) zapewnia przenośną (między
systemami operacyjnymi, werjami, architekturami...) abstrakcję
hierarchicznej topologii współczesnych architektur, w tym węzłów z
pamięcią NUMA, gniazd, współdzielonych pamięci podręcznych, rdzeni i
wielowątkowości. Gromadzi też różne właściwości systemów, takie jak
informacje o pamięci głównej i podręcznej. Głównym celem jest pomoc
aplikacjom w gromadzeniu informacji o współczesnym sprzęcie
obliczeniowym w celu jego właściwego i wydajnego wykorzystania.

%package libs
Summary:	Portable Hardware Locality (hwloc) library
Summary(pl.UTF-8):	Biblioteka przenośnej lokalizacji sprzętu (hwloc)
Group:		Libraries

%description libs
Portable Hardware Locality (hwloc) library.

%description libs -l pl.UTF-8
Biblioteka przenośnej lokalizacji sprzętu (hwloc).

%package devel
Summary:	Header files for hwloc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki hwloc
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libltdl-devel
Requires:	numactl-devel

%description devel
Header files for hwloc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hwloc.

%prep
%setup -q

%build
%configure \
	--enable-plugins \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhwloc.la \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/hwloc/hwloc*.pdf

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hwloc-*
%attr(755,root,root) %{_bindir}/lstopo
%attr(755,root,root) %{_bindir}/lstopo-no-graphics
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/hwloc_opencl.so
%attr(755,root,root) %{_libdir}/%{name}/hwloc_pci.so
%attr(755,root,root) %{_libdir}/%{name}/hwloc_xml_libxml.so
%{_datadir}/%{name}
%{_desktopdir}/hwloc-ls.desktop
%{_mandir}/man1/hwloc-*.1*
%{_mandir}/man1/lstopo.1*
%{_mandir}/man1/lstopo-no-graphics.1*
%{_mandir}/man7/hwloc.7*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/libhwloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwloc.so.5

%files devel
%defattr(644,root,root,755)
%doc doc/doxygen-doc/html doc/doxygen-doc/hwloc-a4.pdf
%attr(755,root,root) %{_libdir}/libhwloc.so
%{_pkgconfigdir}/hwloc.pc
%{_includedir}/hwloc
%{_includedir}/hwloc.h
%{_mandir}/man3/HWLOC_*.3*
%{_mandir}/man3/hwloc_*.3*
%{_mandir}/man3/hwlocality_*.3*
