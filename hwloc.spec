# TODO: scotch (for netlockscotch), CUDA >= 30.20, NVML/nvidia-ml on bcond?
# NOTES (as of 1.9-1.11):
# - kerrighed library (>= 2.0) is only checked for; kerrighed support in hwloc uses /proc filesystem
# - myriexpress (open-mx) library is only checked for, but not used by hwloc code
#   (just in one test); in binary packages only interface header is included
# - same with libibverbs
#
# Conditional build:
%bcond_with	mpi	# MPI support in netloc
%bcond_with	scotch	# SCOTCH support in netloc
%bcond_without	netloc	# netloc library

Summary:	Portable Hardware Locality
Summary(pl.UTF-8):	Przenośna lokalizacja sprzętu
Name:		hwloc
Version:	2.2.0
Release:	1
License:	BSD
Group:		Applications/System
#Source0Download: https://www.open-mpi.org/software/hwloc/v2.2/
Source0:	https://download.open-mpi.org/release/hwloc/v2.2/%{name}-%{version}.tar.bz2
# Source0-md5:	5247ba4c1c63623c9285425552df5d92
URL:		https://www.open-mpi.org/projects/hwloc/
BuildRequires:	OpenCL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	cairo-devel
BuildRequires:	libXNVCtrl-devel
BuildRequires:	libltdl-devel >= 2:2.2.6
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_mpi:BuildRequires:	mpi-devel}
BuildRequires:	ncurses-devel
BuildRequires:	numactl-devel
BuildRequires:	pkgconfig >= 1:0.9.0
%{?with_scotch:BuildRequires:	scotch-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libpciaccess-devel
BuildRequires:	xorg-proto-xproto-devel
%if %{with tests}
BuildRequires:	libibverbs-devel
BuildRequires:	open-mx-devel
%endif
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
Requires:	libltdl-devel >= 2:2.2.6
Requires:	numactl-devel
Requires:	udev-devel

%description devel
Header files for hwloc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hwloc.

%package -n bash-completion-hwloc
Summary:	Bash completion for hwloc commands
Summary(pl.UTF-8):	Bashowe dopełnianie poleceń hwloc
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-hwloc
Bash completion for hwloc commands.

%description -n bash-completion-hwloc -l pl.UTF-8
Bashowe dopełnianie poleceń hwloc.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env perl,%{__perl},' utils/netloc/infiniband/netloc_ib_gather_raw.in

%build
%configure \
	%{!?with_mpi:ac_cv_header_mpi_h=no} \
	%{!?with_scotch:ac_cv_lib_scotch_SCOTCH_archSub=no} \
	%{?with_netloc:--enable-netloc} \
	--enable-plugins \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la \
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
%if %{with netloc}
%attr(755,root,root) %{_bindir}/netloc_*
%endif
%attr(755,root,root) %{_sbindir}/hwloc-dump-hwdata
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/hwloc_opencl.so
%attr(755,root,root) %{_libdir}/%{name}/hwloc_pci.so
%attr(755,root,root) %{_libdir}/%{name}/hwloc_xml_libxml.so
%{_datadir}/%{name}
%{_desktopdir}/lstopo.desktop
%{_mandir}/man1/hwloc-*.1*
%{_mandir}/man1/lstopo.1*
%{_mandir}/man1/lstopo-no-graphics.1*
%{_mandir}/man7/hwloc.7*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/libhwloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwloc.so.15
%if %{with netloc}
%attr(755,root,root) %{_libdir}/libnetloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetloc.so.0
%endif

%files devel
%defattr(644,root,root,755)
%doc doc/doxygen-doc/html doc/doxygen-doc/hwloc-a4.pdf
%attr(755,root,root) %{_libdir}/libhwloc.so
%if %{with netloc}
%attr(755,root,root) %{_libdir}/libnetloc.so
%endif
%{_pkgconfigdir}/hwloc.pc
%{_includedir}/hwloc
%{_includedir}/hwloc.h
%{_mandir}/man3/HWLOC_*.3*
%{_mandir}/man3/hwloc_*.3*
%{_mandir}/man3/hwlocality_*.3*

%files -n bash-completion-hwloc
%defattr(644,root,root,755)
/etc/bash_completion.d/hwloc-completion.bash
