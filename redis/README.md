Policy of Redis-server
===========================

Installing ``redis`` :
--------------------

```
yum install -y redis

```

Download policy module of ``Redis-server``
-------------------------------------

```
# Clone selinux_module
git clone http://gitrep.stackexpress.com/sandip.singh/selinux_module.git

# Change Directory
cd selinux_module/redis/

```

Install Policy Module ``Redis_module 1.0.1``
------------------------------------------

```
# Install policy module by running install script
./redis-server.sh

```

Start ``Redis``:
------------

```
systemctl start redis

```

Check ``Context`` for ``process``/``files``/``port``
---------------------------------------------------

```
# Check context of redis process
ps -eZ |grep redis

# Check context of files
ls -Z /usr/sbin/redis-server

# Check context for port
netstat -tulpnZ |grep redis

# Check install policy
semodule -l |grep redis

```



``Redis-server`` policy module ``1.0.1`` (what goes where)
--------------------------------------------------
- ``redis-server.fc`` - This file defines the default file context for the system, it takes the file types created in the te file and associates file paths to the types.  Tools like restorecon and RPM will use these paths to put down labels.

- ``redis-server.te`` - This file can be used to define all the types rules for a particular domain.

- ``redis-server_selinux.spec`` - This file is an RPM SPEC file that can be used to install the SELinux policy on to machines and setup the labeling. The spec file also  installs  the  interface  file  and  a  man  page describing the policy.

- ``redis-server.sh`` -  This is a helper shell script to compile, install and fix the labeling on your system.  It will also generate a man page based on the installed policy, and compile and build an RPM suitable to be installed on other machines.



