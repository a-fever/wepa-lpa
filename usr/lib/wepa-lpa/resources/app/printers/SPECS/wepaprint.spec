Name:		wepaprint
Version:	1.0.17
Release:	1%{?dist}
Summary:	A CUPS print driver to send user print jobs to the WEPA backend

Group:		Applications/Publishing
License:	GPL
URL:		http://www.wepanow.com
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	cups >= 1.8.0
Requires:	incron >= 0.5.0

%description
This installs a printer into CUPS that uploads print jobs to the WEPA backend.

%install

# install the print driver PPD files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cups/model
cp %{_sourcedir}/wepa_*.ppd $RPM_BUILD_ROOT%{_datadir}/cups/model/


# copy filters
# mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/cups/filter
# cp %{_sourcedir}/okiraster $RPM_BUILD_ROOT%{_prefix}/lib/cups/filter/

# create app folder
mkdir -p $RPM_BUILD_ROOT%{_datadir}/wepa


# copy wrapper to bin
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp %{_sourcedir}/wepaprint $RPM_BUILD_ROOT%{_bindir}/


%post

# create the CUPS backend script
echo "#!/bin/sh" > %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "FILE=\$6" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "if [ -z "\$FILE" ]" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "then" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "  FILE=-" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "fi" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "echo JOB=\$1 > %{_localstatedir}/wepa/metadata/\$1.prn.metadata" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "echo USER=\$2 >> %{_localstatedir}/wepa/metadata/\$1.prn.metadata" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "echo TITLE=\$3 >> %{_localstatedir}/wepa/metadata/\$1.prn.metadata" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "echo NUMCOPIES=\$4 >> %{_localstatedir}/wepa/metadata/\$1.prn.metadata" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "echo OPTIONS=\$5 >> %{_localstatedir}/wepa/metadata/\$1.prn.metadata" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "env >> %{_localstatedir}/wepa/metadata/\$1.prn.metadata" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "cat \$FILE > %{_localstatedir}/wepa/prn/\$1.prn" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "chmod 644 %{_localstatedir}/wepa/prn/\$1.prn" >> %{_prefix}/lib/cups/backend/WepaPDFQueue
echo "exit 0" >> %{_prefix}/lib/cups/backend/WepaPDFQueue


#chmod 555 %{_prefix}/lib/cups/backend/WepaQueue
chmod 555 %{_prefix}/lib/cups/backend/WepaPDFQueue

# create the WEPA print queue directory
mkdir %{_localstatedir}/wepa
mkdir %{_localstatedir}/wepa/log
mkdir %{_localstatedir}/wepa/metadata
mkdir %{_localstatedir}/wepa/prn
mkdir %{_localstatedir}/wepa/wepaout
chown -R lp:lp %{_localstatedir}/wepa
chmod 700 %{_localstatedir}/wepa

# install the CUPS printers
echo "Installing WEPA printers in CUPS..."
# lpadmin -p wepaColor -D "wepa Color" -P %{_datadir}/cups/model/WEPACOLOR.ppd -v WepaQueue:/ -E -o printer-is-shared=false
# lpadmin -p wepaBW -D "wepa BW" -P %{_datadir}/cups/model/WEPAMONO.ppd -v WepaQueue:/ -E -o printer-is-shared=false
lpadmin -p wepa_Color -D "wepa Color" -P %{_datadir}/cups/model/wepa_color_simplex.ppd -v WepaPDFQueue:/ -E -o printer-is-shared=false
lpadmin -p wepa_Color_Two_Sided -D "wepa Color Two-Sided" -P %{_datadir}/cups/model/wepa_color_duplex.ppd -v WepaPDFQueue:/ -E -o printer-is-shared=false
lpadmin -p wepa_BW -D "wepa BW" -P %{_datadir}/cups/model/wepa_bw_simplex.ppd -v WepaPDFQueue:/ -E -o printer-is-shared=false
lpadmin -p wepa_BW_Two_Sided -D "wepa BW Two-Sided" -P %{_datadir}/cups/model/wepa_bw_duplex.ppd -v WepaPDFQueue:/ -E -o printer-is-shared=false




# set default printer
lpoptions -d wepa_BW

# configure incrond
echo "/var/wepa/prn IN_CREATE /usr/bin/wepaprint" > /var/spool/incron/root
if [ -f /lib/systemd/system/incron.service ];
then
  echo root > /etc/incron.allow
  systemctl enable incron.service;
  systemctl restart incron.service;
elif [ -f /usr/lib/systemd/system/incrond.service ];
then
  echo root > /etc/incron.allow
  systemctl enable incrond.service;
  systemctl restart incrond.service;
fi



%postun

# remove the printer from CUPS
echo "Removing WEPA printers from CUPS..."
lpadmin -x wepaColor
lpadmin -x wepaBW
lpadmin -x wepa_Color
lpadmin -x wepa_BW
lpadmin -x wepa_Color_Two_Sided
lpadmin -x wepa_BW_Two_Sided

# remove the CUPS backend script
rm %{_prefix}/lib/cups/backend/WepaPDFQueue

# remove the WEPA queue directory
rm -rf %{_localstatedir}/wepa


# rm incron rule
rm -f /var/spool/incron/root


%files
%defattr(-,root,root,-)
%attr(644,root,root) %{_datadir}/cups/model/wepa*.ppd
%attr(755,root,root) %{_bindir}/wepaprint
#%attr(755,root,root) %{_prefix}/lib/cups/filter/okiraster

%changelog
* Fri Mar 8 2019 - Sergiy Markin <serge.markin@wepanow.com> 1.0.1
* Fri May 31 2013 - Richard Eppes <richard@eppesconsulting.com> 0.0.1
- Initial version
