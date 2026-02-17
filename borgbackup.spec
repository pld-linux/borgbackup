Summary:	Deduplicating backup program with compression and authenticated encryption
Name:		borgbackup
Version:	1.4.3
Release:	2
License:	BSD 3 clause
Group:		Networking/Utilities
Source0:	https://github.com/borgbackup/borg/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	87a1f4e760c22a0a8bd9b1ea699fd337
URL:		https://github.com/borgbackup/borg
BuildRequires:	acl-devel >= 2.2.47
BuildRequires:	lz4-devel >= 1.7.0
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-guzzle_sphinx_theme
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinxcontrib-jquery
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.720
BuildRequires:	sphinx-pdg
BuildRequires:	xxHash-devel >= 0.7.3
BuildRequires:	zstd-devel >= 1.3.0
Requires:	python3-modules >= 1:3.9
Requires:	python3-setuptools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
borgbackup is a deduplicating backup program which stores deltas. it
supports compression and authenticated encryption as well,
facilitating frequent backups and storing to not fully trusted
targets.

%package -n bash-completion-borgbackup
Summary:	bash completion for %{name}
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-borgbackup
borgbackup is a deduplicating backup program which stores deltas. it
supports compression and authenticated encryption as well,
facilitating frequent backups and storing to not fully trusted
targets.

this package contains the bash completion script for borgbackup.

%package -n zsh-completion-borgbackup
Summary:	zsh completion for %{name}
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-borgbackup
borgbackup is a deduplicating backup program which stores deltas. it
supports compression and authenticated encryption as well,
facilitating frequent backups and storing to not fully trusted
targets.

this package contains the zsh completion script for borgbackup.

%package -n fish-completion-borgbackup
Summary:	fish completion for %{name}
Group:		Applications/Shells
Requires:	%{name} = %{version}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-borgbackup
borgbackup is a deduplicating backup program which stores deltas. it
supports compression and authenticated encryption as well,
facilitating frequent backups and storing to not fully trusted
targets.

this package contains the fish completion script for borgbackup.

%prep
%setup -q

# remove bundled libraries, that we don't want to be included
rm -rf src/borg/algorithms/{lz4,zstd,blake2}

# remove precompiled Cython code
find src/ -name '*.pyx' | sed -e 's/.pyx/.c/g' | xargs rm -f

%build
export BORG_OPENSSL_PREFIX=%{_libdir}
export BORG_LIBLZ4_PREFIX=%{_libdir}
export BORG_LIBZSTD_PREFIX=%{_libdir}
export BORG_LIBXXHASH_PREFIX=%{_libdir}
export BORG_LIBACL_PREFIX=%{_libdir}
%py3_build

%{__make} -C docs man text

%install
rm -rf $RPM_BUILD_ROOT

export BORG_OPENSSL_PREFIX=%{_libdir}
export BORG_LIBLZ4_PREFIX=%{_libdir}
export BORG_LIBZSTD_PREFIX=%{_libdir}
export BORG_LIBXXHASH_PREFIX=%{_libdir}
export BORG_LIBACL_PREFIX=%{_libdir}
%py3_install

install -D docs/_build/man/borg.1 $RPM_BUILD_ROOT%{_mandir}/man1/borg.1
install -D scripts/shell_completions/bash/* $RPM_BUILD_ROOT%{bash_compdir}/borg
install -D scripts/shell_completions/zsh/* $RPM_BUILD_ROOT%{zsh_compdir}/borg
install -D scripts/shell_completions/fish/* $RPM_BUILD_ROOT%{fish_compdir}/borg.fish

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.rst LICENSE MANIFEST.in README.rst README_WINDOWS.rst SECURITY.md
%doc docs/_build/text/*
%attr(755,root,root) %{_bindir}/borg
%attr(755,root,root) %{_bindir}/borgfs
%{_mandir}/man1/borg.1*
%{py3_sitedir}/borg
%{py3_sitedir}/borgbackup-*-py*.egg-info

%files -n bash-completion-borgbackup
%defattr(644,root,root,755)
%{bash_compdir}/borg

%files -n fish-completion-borgbackup
%defattr(644,root,root,755)
%{fish_compdir}/borg.fish

%files -n zsh-completion-borgbackup
%defattr(644,root,root,755)
%{zsh_compdir}/borg
