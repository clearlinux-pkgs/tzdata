Name:           tzdata
Version:        2017c
Release:        20
License:        Public-Domain BSD-4-Clause-UC
Summary:        Timezone database
Url:            ftp://elsie.nci.nih.gov/pub/
Group:          base
Source0:        ftp://ftp.iana.org/tz/releases/tzdata2017c.tar.gz
Source1:        ftp://ftp.iana.org/tz/releases/tzcode2017c.tar.gz
Requires:       tzdata-minimal

%define debug_package %{nil}

%description
Timezone database.

%package minimal
Summary: tzdata minimal components - UTC and zone.tab files only

%description minimal
Timezone database, minimal components.

%prep
%setup -q -c %{name}-%{version}
cd ../
tar xzf %{SOURCE1} -C %{name}-%{version}

%build
make %{?_smp_mflags} TZDIR=%{_datadir}/zoneinfo CFLAGS="%{optflags} -DHAVE_GETTEXT=1 -DTZDEFAULT='\"%{_sysconfdir}/localtime\"'"
make %{?_smp_mflags} TZDIR=zoneinfo zones

%install
mkdir -p %{buildroot}%{_datadir}/zoneinfo
cp -a zoneinfo %{buildroot}%{_datadir}/zoneinfo/posix
cp -al %{buildroot}%{_datadir}/zoneinfo/posix/. %{buildroot}%{_datadir}/zoneinfo
cp -a zoneinfo-leaps %{buildroot}%{_datadir}/zoneinfo/right
install -m 644 iso3166.tab %{buildroot}%{_datadir}/zoneinfo/iso3166.tab
install -m 644 zone.tab    %{buildroot}%{_datadir}/zoneinfo/zone.tab

%files
%exclude %{_datadir}/zoneinfo/zone.tab
%exclude %{_datadir}/zoneinfo/iso3166.tab
%exclude %{_datadir}/zoneinfo/UTC
%{_datadir}/zoneinfo

%files minimal
%{_datadir}/zoneinfo/zone.tab
%{_datadir}/zoneinfo/iso3166.tab
%{_datadir}/zoneinfo/UTC
