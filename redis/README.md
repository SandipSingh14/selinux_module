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



Contents of ``redis-server.fc``
-------------------------------
```
# Add path of the files & related 'context' as you wanted to be 'labeled' your files.
# Find redis-server path of the files by 'rpm -ql redis'
# File Context
    - First field   'User'
    - Second field  'Role'
    - Third field   'Type'
    - Fourth field  'MLS'
    - Fivth field   'MCS'

# Mapping between path of the file and the file context, 

/usr/lib/systemd/system/redis.service   --  gen_context(system_u:object_r:redis_server_unit_file_t,s0)
/usr/sbin/redis-server                  --  gen_context(system_u:object_r:redis_server_exec_t,s0)

# Regural expression which is mapping everything in '/var/lib/redis' with file context mention below.

/var/lib/redis(/.*)?                        gen_context(system_u:object_r:redis_server_var_lib_t,s0)
/var/log/redis(/.*)?                        gen_context(system_u:object_r:redis_server_log_t,s0)
/var/run/redis(/.*)?                        gen_context(system_u:object_r:redis_server_var_run_t,s0)


```

Contents of ``redis-server.te``
-------------------------------

```
# Add policy module 
policy_module(redis_server, 1.0.1)

### Declaritions part of module 

# Types
type redis_server_t;
type redis_server_exec_t;

# Confined daemon domains use the interface init_daemon_domain which defines a transition from the initscript domain (initrc_t) to the confined domain as here 'redis_server_t' & 'redis_server_exec_t' when running an executable labeled 'redis_server_exec_t'.

init_daemon_domain(redis_server_t, redis_server_exec_t)

# Module should be treated as permissive, once you complete your tests, collect denied access, rewrite policy & comment-out below line. 

permissive redis_server_t;

# Types
type redis_server_log_t;

# 'Logfiles' are marked through the 'logging_jog_file' interface and usually end with the 'log_t' suffix, such as 'redis_server_log_t'. By marking it as a logfile, domains that are assigned an operation concerning all logfiles automatically have these privileges on the newly defined type. Often, a file transition is set so that files created In /vam/ log/ automatically get the right type. This is done through the logging_log_filetrans interface: 

logging_log_file(redis_server_log_t)

type redis_server_var_lib_t;

# The macro 'files_type' simply adds the attribute to identify the new redis_server_var_lib_t type as a file type 
files_type(redis_server_var_lib_t)

type redis_server_var_run_t;
files_pid_file(redis_server_var_run_t)

type redis_server_unit_file_t;

# 'systemd' unit file are marked through 'systemd_unit_file', set type with the systemd_unit_file interface, if you want to treat the files as systemd unit content.

systemd_unit_file(redis_server_unit_file_t)




########################################
#
# redis_server local policy
#

# The 'allow rule' checks whether the 'operations' between the 'source_type' and 'target_type' are allowed. It is the most common statement that many of the Reference Policy helper macros and interface definitions expand into multiple allow rules

# Allow 'redis_server_t' or 'redis_server_exec_t' type to 'process' with permission to do as 'fork' 'setrlimit' 'signal_perms'
allow redis_server_t self:process { fork setrlimit signal_perms };

# Internal communication is often done using 'fifo' and 'unix sockets'.
allow redis_server_t self:fifo_file rw_fifo_file_perms;
allow redis_server_t self:unix_stream_socket create_stream_socket_perms;

# Manage types transition & create context for 'dir', 'files' and 'links'
# This Macro says that if a process is runing as 'redis_server_t' and creates a file in a directory labeles 'redis_server_log_t', the kernel will create the file labeles 'redis_server_log_t'.

manage_dirs_pattern(redis_server_t, redis_server_log_t, redis_server_log_t)
manage_files_pattern(redis_server_t, redis_server_log_t, redis_server_log_t)
manage_lnk_files_pattern(redis_server_t, redis_server_log_t, redis_server_log_t)

# Make the specified type usable for log files in a filesystem
logging_log_filetrans(redis_server_t, redis_server_log_t, { dir file lnk_file })

# Manage types transition & create context for 'dir', 'files' and 'links'
# This Macro says that if a process is runing as 'redis_server_t' and creates a file in a directory labeles 'redis_server_var_lib_t', the kernel will create the file labeles 'redis_server_var_lib_t'.

manage_dirs_pattern(redis_server_t, redis_server_var_lib_t, redis_server_var_lib_t)
manage_files_pattern(redis_server_t, redis_server_var_lib_t, redis_server_var_lib_t)
manage_lnk_files_pattern(redis_server_t, redis_server_var_lib_t, redis_server_var_lib_t)

# Make the specified type usable for /var/lib files in a filesystem
files_var_lib_filetrans(redis_server_t, redis_server_var_lib_t, { dir file lnk_file })

# Manage types transition & create context for 'dir', 'files' and 'links'
# This Macro says that if a process is runing as 'redis_server_t' and creates a file in a directory labeles 'redis_server_var_run_t', the kernel will create the file labeles 'redis_server_var_run_t'.

manage_dirs_pattern(redis_server_t, redis_server_var_run_t, redis_server_var_run_t)
manage_files_pattern(redis_server_t, redis_server_var_run_t, redis_server_var_run_t)
manage_lnk_files_pattern(redis_server_t, redis_server_var_run_t, redis_server_var_run_t)

# Make the specified type usable for /var/run files in a filesystem
files_pid_filetrans(redis_server_t, redis_server_var_run_t, { dir file lnk_file })

# This domain allows the tool so interact with the terminal file descriptors created at login
domain_use_interactive_fds(redis_server_t)

# Allow 'redis_server_t' domain to read 'etc_t' files
files_read_etc_files(redis_server_t)

# Sending 'syslog' messages
logging_send_syslog_msg(redis_server_t)

# This macro allows 'redis_server_t' to read files/directories labeled 'public_content_t'
miscfiles_read_localization(redis_server_t)

# This macro allows 'redis_server_t' to connect to the dns port via 'tcp_socket'.  
sysnet_dns_name_resolve(redis_server_t)








```










