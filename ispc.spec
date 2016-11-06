Name:		ispc
Version:	1.9.1
Release:	9%{?dist}
Summary:	C-based SPMD programming language compiler

License:	BSD
URL:		https://ispc.github.io/
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz 

BuildRequires:	llvm-devel
BuildRequires:	clang-devel
BuildRequires:	gcc-c++
BuildRequires:	make
BuildRequires:	bison
BuildRequires:	flex 
BuildRequires:	ncurses-devel
ExclusiveArch:	%{arm} %{ix86} x86_64
# Hardcoded path from 32-bit glibc-devel needed to build
# See https://github.com/ispc/ispc/wiki/Building-ispc:-Linux-and-Mac-OS-X
%ifarch x86_64
BuildRequires:	/usr/lib/crt1.o
%endif
BuildRequires:	zlib-devel
# Conditional build for f24 and less
%if 0%{?fedora} <= 24 || 0%{?rhel} <= 7
BuildRequires:	python
%endif
# Set verbose compilation and remove -Werror on Makefile
Patch0:		Makefile.patch

%description
A compiler for a variant of the C programming language, with extensions for
"single program, multiple data" (SPMD) programming.

%prep
%autosetup


%build
%make_build gcc OPT="%{optflags}" LDFLAGS="%{__global_ldflags}" 


%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE.txt
%{_bindir}/%{name}

%changelog
* Sun Nov 06 2016 Luya Tshimbalanga <luya@fedoraproject.org> - 1.9.1-9
- Rebuilt agaisnt llvm

* Fri Aug 26 2016 Dan Horák <dan[at]danny.cz> 1.9.1-8
- set ExclusiveArch

* Tue Aug 23 2016 Luya Tshimbalanga <luya@fedoraproject.org> 1.9.1-7
- Added conditional build for Fedora 24- and rhel7-

* Tue Aug 23 2016 Luya Tshimbalanga <luya@fedoraproject.org> 1.9.1-6
- Included OPT and LDFLAGS on build line

* Tue Aug 23 2016 Luya Tshimbalanga <luya@fedoraproject.org> 1.9.1-5
- Improved patch to remove -Werror line
- Removed unecesary CXXFLAGS and LDFLAGS on make_build line
- Removed useless llvm-config

* Sat Aug 20 2016 Luya Tshimbalanga <luya_tfz@thefinalzone.net> 1.9.1-4
- Added gcc into make_build line
- Added patch against Makefile for verbose dialog
- Use llvm-config

* Sun Aug 14 2016 Luya Tshimbalanga <luya_tfz@thefinalzone.net> 1.9.1-3
- Fixed spec
- Added missing cflags for build
- Added zlib-devel for dependency

* Sun Aug 14 2016 Luya Tshimbalanga <luya_tfz@thefinalzone.net> 1.9.1-2
- Remove misplaced url on BuildRequires
- Include gcc-c++ and make for BuildRequires
- Used proper installation method
- Optimize build

* Sun Aug 14 2016 Luya Tshimbalanga <luya_tfz@thefinalzone.net> 1.9.1-1
- Initial build
