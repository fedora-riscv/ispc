%global with_snapshot 0
%global commit 34da2d23bbf32abf44da11d2cdca595dc7318cec
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		ispc
Version:	1.11.0	
%if %{with_snapshot}
Release:	20190305.%{shortcommit}%{?dist}
%else
Release:	2%{?dist}
%endif
Summary:	C-based SPMD programming language compiler

License:	BSD
URL:		https://ispc.github.io/
%if %{with_snapshot}
Source0:	https://github.com/%{name}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	clang-devel
BuildRequires:	doxygen
BuildRequires:	flex 
BuildRequires:	gcc-c++
BuildRequires:	llvm-devel
BuildRequires:	ncurses-devel
BuildRequires:	python2-devel
BuildRequires:	/usr/bin/pathfix.py
ExclusiveArch:	%{arm} %{ix86} x86_64
# Hardcoded path from 32-bit glibc-devel needed to build
# See https://github.com/ispc/ispc/wiki/Building-ispc:-Linux-and-Mac-OS-X
%ifarch x86_64
BuildRequires:	/usr/lib/crt1.o
%endif
BuildRequires:	zlib-devel


# Set verbose compilation remove -Werror on Makefile
# Also remove uses of llvm dump
Patch1:		0002-Remove-uses-of-LLVM-dump-functions-and-verbose-makefile.patch

%description
A compiler for a variant of the C programming language, with extensions for
"single program, multiple data" (SPMD) programming.

%prep
%if %{with_snapshot}
%autosetup -p1 -n %{name}-%{commit}
%else
%autosetup -p1 -n %{name}-%{version}
%endif

# Use gcc rather clang by default
sed -i 's|set(CMAKE_C_COMPILER "clang")|set(CMAKE_C_COMPILER "gcc")|g' CMakeLists.txt
sed -i 's|set(CMAKE_CXX_COMPILER "clang++")|set(CMAKE_CXX_COMPILER "g++")|g' CMakeLists.txt

# Fix all Python shebangs recursively in .
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" .

%build
# Disable examples otherwise build fails
%cmake  -DISPC_INCLUDE_EXAMPLES=OFF \
	-DCMAKE_BUILD_TYPE=release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_EXE_LINKER_FLAGS="%{optflags} -fPIE" \
	.
%make_build OPT="%{optflags}" LDFLAGS="%{__global_ldflags}"

%install
%make_install

%files
%license LICENSE.txt
%{_bindir}/%{name}
%{_bindir}/check_isa

%changelog
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Apr 20 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 1.11.0-1
- Update to 1.11.0
- Patch to remove obsolete wno and werror

* Thu Mar 07 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 1.10.0-4
- Add exe_linker_flag for cmake compilation
- Disable examples

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 19 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 1.10.0-2
- Patch for Makefile and remove llvm dump

* Sat Jan 19 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 1.10.0-1
- Update to 1.10.0

* Wed Dec 26 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.9.3-0.5.git.20190102.e338aaa
- Git snasphot 20190102

* Wed Dec 26 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.9.3-0.4.git.20181220.1e4bfb7
- Git snasphot 20181220

* Tue Nov 06 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.9.3-0.3.git.20181106.3d846b
- Git snasphot 1.9.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-0.3.git.20180222.07fe054
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.9.3-0.2.git.20180222.07fe054
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wikiComponents/FinalizingFedoraSwitchtoPython3)

* Sat Mar 03 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.9.3-0.1.git.20180222.07fe054 
- Update to 1.9.3 git snapshot
- Use new guideline versioning semantique for snapshot

* Fri Mar 02 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-18.git.20171023.6dc0ccc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 24 2017 Tom Stellard <tComponentsComponentsstellar@redhat.com> - 1.9.1-17.git.20171023.6dc0ccc
- Rebase to more current snapshot for LLVM 5.0 support.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-16.git.20170324.a618ad4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-15.git.20170324.a618ad4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 25 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.1-14.git.20170324.a618ad4
- Rebuild clang/llvm-4

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-13.git.20170324.a618ad4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Mar 24 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.9.1-12.git.20170324.a618ad4
- Update to git snapshot which support LLVM4

* Thu Mar 16 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.9.1-11
- Rebuild for llvm 3.9

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

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
