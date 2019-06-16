Name:           tzdata
Version:        2019a
Release:        25
License:        Public-Domain BSD-4-Clause-UC
Summary:        Timezone database
Url:            https://www.iana.org/time-zones
Group:          base
Source0:        https://data.iana.org/time-zones/releases/tzdata2019a.tar.gz
Source1:        https://data.iana.org/time-zones/releases/tzcode2019a.tar.gz
Requires:       tzdata-minimal

%define debug_package %{nil}

%description
Timezone database.

%package minimal
Summary: tzdata minimal components - UTC and zone.tab files only

%description minimal
Timezone database, minimal components.

%prep
%setup -q -c tzdata-%{version}
cd ../
tar xzf %{SOURCE1} -C tzdata-%{version}

%build
make %{?_smp_mflags} TZDIR=/usr/share/zoneinfo CFLAGS="%{optflags} -DHAVE_GETTEXT=1 -DTZDEFAULT='\"%{_sysconfdir}/localtime\"'"
make %{?_smp_mflags} TZDIR=zoneinfo zones

%install
mkdir -p %{buildroot}/usr/share/zoneinfo
cp -a zoneinfo %{buildroot}/usr/share/zoneinfo/posix
cp -al %{buildroot}/usr/share/zoneinfo/posix/. %{buildroot}/usr/share/zoneinfo
cp -a zoneinfo-leaps %{buildroot}/usr/share/zoneinfo/right
install -m 644 zone1970.tab %{buildroot}/usr/share/zoneinfo/zone1970.tab
install -m 644 iso3166.tab %{buildroot}/usr/share/zoneinfo/iso3166.tab
install -m 644 zone.tab    %{buildroot}/usr/share/zoneinfo/zone.tab

%files
%exclude /usr/share/zoneinfo/zone.tab
%exclude /usr/share/zoneinfo/iso3166.tab
%exclude /usr/share/zoneinfo/UTC
/usr/share/zoneinfo

%files minimal
/usr/share/zoneinfo/zone.tab
/usr/share/zoneinfo/iso3166.tab
/usr/share/zoneinfo/zone1970.tab
/usr/share/zoneinfo/UTC
