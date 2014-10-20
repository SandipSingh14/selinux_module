# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/sbin/redis-server; \
restorecon -R /usr/lib/systemd/system/redis.service; \
restorecon -R /var/lib/redis; \
restorecon -R /var/log/redis; \
restorecon -R /var/run/redis; \

%define selinux_policyver 3.12.1-189

Name:   redis_server_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for redis_server

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	redis_server.pp
Source1:	redis_server.if
Source2:	redis_server_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
Requires(post): redis
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for redis_server.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/redis_server_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/redis_server.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r redis_server
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/redis_server.pp
%{_datadir}/selinux/devel/include/contrib/redis_server.if
%{_mandir}/man8/redis_server_selinux.8.*


%changelog
* Thu Oct 16 2014 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version

