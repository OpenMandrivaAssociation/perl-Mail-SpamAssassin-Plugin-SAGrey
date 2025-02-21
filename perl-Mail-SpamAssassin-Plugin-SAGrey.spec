Summary:	The SAGrey plugin for SpamAssassin
Name:		perl-Mail-SpamAssassin-Plugin-SAGrey
Version:	0.02
Release:	6
License:	Apache License
Group:		Development/Perl
URL:		https://www.ntrg.com/misc/sagrey/
Source0:	http://www.ntrg.com/misc/sagrey/sagrey.cf
Source1:	http://www.ntrg.com/misc/sagrey/sagrey.pm
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  spamassassin-spamd >= 3.1.1
Requires:	spamassassin-spamd >= 3.1.1
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mail::SpamAssassin::Plugin::SAGrey is a SpamAssassin plugin that provides a
limited amount of greylisting functionality using SpamAssassin's existing
services.

SAGrey is two-phased, in that it first looks to see if the current score of
the current message exceeds the user-defined threshold value (as set in one
of the cf files), and then looks to see if the message sender's email and IP
address tuple are already known to the auto-whitelist (AWL) repository. If the
message is spam and the sender is unknown, SAGrey assumes that this is one-time
spam from a throwaway or zombie account, the SAGREY rule fires, adds 1.0 to the
current message score, and optionally creates a header field in the message
itself. The rulename or header field can then be used to perform additional
greylisting functions (EG, having your delivery or transfer agent defer
delivery), or the score by itself can be used to penalize the message.
This model has two benefits over MTA-specific greylisting mechanisms: first, it
only subjects probable-spam to greylisting (instead of making everybody be
deferred, which has known problems), and it repurposes the existing
spamassassin history database (meaning no additional databases need to be
maintained).  Another benefit is that it can still work at the MTA level if
your MTA can call spamassassin while the transfer is active and then defer
delivery based on the presence of header-field data (postfix 2.x will not do
this unfortunately, since the header checks don't provide a DEFER verb), but
can also be used in other models (such as delivery routines).

%prep

%setup -q -T -c -n %{name}-%{version}

cp %{SOURCE0} SAGrey.cf
cp %{SOURCE1} SAGrey.pm

# fix path
perl -pi -e "s|sagrey\.pm|%{perl_vendorlib}/Mail/SpamAssassin/Plugin/SAGrey\.pm|g" SAGrey.cf

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -d %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin

install -m0644 SAGrey.cf %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 SAGrey.pm %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin/

%post
if [ -f %{_var}/lock/subsys/spamd ]; then
    %{_initrddir}/spamd restart 1>&2;
fi
    
%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/spamd ]; then
        %{_initrddir}/spamd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/spamassassin/SAGrey.cf
%{perl_vendorlib}/Mail/SpamAssassin/Plugin/SAGrey.pm


%changelog
* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.02-4mdv2010.0
+ Revision: 430494
- rebuild

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.02-3mdv2009.0
+ Revision: 239110
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix description-line-too-long
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Jul 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.02-2mdv2008.0
+ Revision: 46364
- misc fixes


* Sat Nov 25 2006 Emmanuel Andry <eandry@mandriva.org> 0.02-1mdv2007.0
+ Revision: 87311
- New version 0.2

* Sat Nov 25 2006 Emmanuel Andry <eandry@mandriva.org> 0.01-3mdv2007.1
+ Revision: 87281
- bump release
- patch to fix perl module path
- Import perl-Mail-SpamAssassin-Plugin-SAGrey

