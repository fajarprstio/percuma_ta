# Copyright (C) 2019 Fajar prasetio <fajarprstyo05@gmail.com>
#



#!/usr/bin/env python


from conf.fake_responses import *
from core import percuma_download_files
import re

class ProcessCmd:
    """
    Class for processing any and all supported fake commands.
    """

    def __init__(self, cmd, params, transport, attacker_username, ip, fake_workingdir):
        """
        Set up internal variables then run a generic factory eval to execute command.
        """
        self.cmd = cmd
        self.params = params
        self.transport = transport
        self.attacker_username = attacker_username
        self.ip = ip
        self.fake_workingdir = fake_workingdir
        _process_cmd = 'self.process_' + self.cmd + '()'
        message = cmd + ' ' + ' '.join(params)
        _methodname = 'process_' + cmd
        if hasattr(ProcessCmd, _methodname):
            eval(_process_cmd)
        else:
	    print self.process_undef()

    def get_values(self):
        return (self.fake_workingdir,self.attacker_username)

    def process_apachectl(self):
        if len(self.params)>0 and self.params[0]=='status':
            self.transport.write(FAKE_APACHECTL)
        else:
            self.process_undef()

    def process_awk(self):
        self.transport.write(FAKE_AWK)

    def process_cd(self):
    	#print self.params[0]
    	global parent
        if self.params == '':
            if self.attacker_username in FAKE_HOMEDIRS:
                self.fake_workingdir = FAKE_HOMEDIRS[self.attacker_username]
            else:
                self.fake_workingdir = "/"
	elif self.params[0] == '..':
        	if self.fake_workingdir == "/":
        		pass
        	pattern = re.compile(".*\/.*\/")
        	if pattern.match(self.fake_workingdir):
        		regex = re.search(r"(.*)\/",self.fake_workingdir)
        		self.fake_workingdir = regex.group(1)
        	else:
        		self.fake_workingdir = "/"

	else:
            pat = re.compile("\/home\/(.*)\/")
            pat2 = re.compile("\/home\/(.*)")
            old_dir = self.fake_workingdir
            if self.params[0][0:1] == '/':
                self.fake_workingdir = self.params[0]
            else:
                self.fake_workingdir = self.fake_workingdir.rstrip('/')
                self.fake_workingdir += '/' + self.params[0]
            if self.fake_workingdir == "/root":
                if self.attacker_username != "root":
                    self.transport.write('-bash: cd: /root: Permission denied\r\n')
                    self.fake_workingdir = old_dir

	    elif self.fake_workingdir not in FAKE_DIR_STRUCT:
                self.transport.write('-bash: cd: ' + self.params[0] + ': No such file or directory\r\n')
                self.fake_workingdir = old_dir

            elif pat.match(self.fake_workingdir):
            	regex = re.search(r"\/home\/(.*)\/",self.fake_workingdir)
            	if regex.group(1)!= self.attacker_username and self.attacker_username!="root":
                	self.transport.write('-bash: cd: '+self.fake_workingdir+' : Permission denied\r\n')
                	self.fake_workingdir = old_dir

            elif pat2.match(self.fake_workingdir):
            	regex = re.search(r"\/home\/(.*)",self.fake_workingdir)
            	if regex.group(1)!= self.attacker_username and self.attacker_username!="root":
                	self.transport.write('-bash: cd: '+self.fake_workingdir+' : Permission denied\r\n')
                	self.fake_workingdir = old_dir


    def process_cat(self):
        if len(self.params)>0:
            #cat /etc/passwd
            if self.params[0]=="/etc/passwd":
                for line in FAKE_CAT_PASSWD:
                    self.transport.write(line + '\r\n')
            #cat /etc/issue
            elif self.params[0] == "/etc/issue":
                for line in FAKE_ETC_ISSUE:
                    self.transport.write(line + '\r\n')
            #cat /proc/cpuinfo
            elif self.params[0] == "/proc/cpuinfo":
                for line in FAKE_CPUINFO:
                    self.transport.write(line + '\r\n')
            elif self.params[0] == "/etc/hosts":
                self.transport.write(FAKE_CAT_ETC_HOSTS)
            #cat /etc/resolv.conf
            elif self.params[0] == "/etc/resolv.conf":
                self.transport.write(FAKE_ETC_RESOLV_CONF + '\r\n')
            else:
                self.transport.write('-bash: cat: ' + self.params[0] + ': No such file or directory\r\n')

    def process_curl(self):
        result_data =xsweet_download_files.curl(self.params, self.ip)
        if result_data != "":
            self.transport.write(result_data+'\r\n')

    def process_date(self):
        self.transport.write(datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y") + '\r\n')

    def process_exit(self):
        self.transport.loseConnection()

    def process_export(self):
        pass

    def process_free(self):
        if len(self.params)>0 and self.params[0]=='-m':
            self.transport.write('             total       used       free     shared    buffers     cached\r\n')
            self.transport.write('Mem:          7858       5622       2235          0        277       3113\r\n')
            self.transport.write('-/+ buffers/cache:       2231       5626\r\n')
            self.transport.write('Swap:         7871        191       7680\r\n')
        else:
            self.transport.write('             total       used       free     shared    buffers     cached\r\n')
            self.transport.write('Mem:       8046892    5757244    2289648          0     284060    3188352\r\n')
            self.transport.write('-/+ buffers/cache:    2284832    5762060\r\n')
            self.transport.write('Swap:      8060924     196176    7864748\r\n')

    def process_gawk(self):
        self.transport.write(FAKE_AWK)

    def process_gcc(self):
        self.transport.write('gcc: no input files\r\n')

    def process_grep(self):
        self.transport.write(FAKE_GREP)

    def process_halt(self):
        if(self.attacker_username =="root"):
            now=time.strftime("%H:%M",time.localtime())
            self.transport.write('\r\nBroadcast message from root@' +FQDN+'\r\n')
            self.transport.write('\t(/dev/pts/0) at ' +now+ ' ...\r\n\r\n')
            self.transport.write('The system is going down for halt NOW!\r\n')
            self.transport.loseConnection()
        else:
            self.transport.write("Failed to start halt.target: Interactive authentication required.\r\n"
            +"See system logs and 'systemctl status halt.target' for details.\r\n"
            +"Failed to open /dev/initctl: Permission denied\r\n"
            +"Failed to talk to init daemon.\r\n")

    def process_history(self):
        self.transport.write("ksh: cd: 0403-011 The specified substitution is not valid for this command.\r\n")

    def process_hostname(self):
        self.transport.write(FQDN+'\r\n')

    def process_id(self):
        if self.attacker_username == "root":
            self.transport.write('uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)\r\n')
        else:
            self.transport.write('uid=501('+self.attacker_username+') gid=502('+self.attacker_username+') groups=100(users)\r\n')
    def process_ifconfig(self):
        for line in FAKE_IFCONFIG:
            self.transport.write(line + '\r\n')

    def process_logout(self):
        self.transport.loseConnection()

    def process_ls(self):
        if len(self.params) > 0:
            dir_to_ls = self.params[0]
            if(dir_to_ls[0] == '-'):
                if(len(self.params) > 1):
                    dir_to_ls = self.params[1]
                else:
                    dir_to_ls = self.fake_workingdir
            if (dir_to_ls in FAKE_DIR_STRUCT):
                for line in FAKE_DIR_STRUCT[dir_to_ls]:
                    if (line == FAKE_DIR_STRUCT[dir_to_ls][-1]):
                        self.transport.write(line)
                    else:
                        self.transport.write(line + '\r\n')
                self.transport.write('\r\n')
            else:
                 self.transport.write('ls: cannot access ' + dir_to_ls + ': No such file or directory\r\n')
        elif (self.fake_workingdir in FAKE_DIR_STRUCT):
            for line in FAKE_DIR_STRUCT[self.fake_workingdir]:
                if (line == FAKE_DIR_STRUCT[self.fake_workingdir][-1]):
                    self.transport.write(line)
                else:
                    self.transport.write(line + '\r\n')
            self.transport.write('\r\n')
        else:
            self.transport.write('ls: Error.\r\n')

    def process_make(self):
        self.transport.write('make: *** No targets specified and no makefile found.  Stop.\r\n')

    def process_mail(self):
        self.transport.write('No mail for ' + self.attacker_username + '\r\n')

    def process_mkdir(self):
        if len(self.params) == 0:
            self.transport.write("mkdir: missing operand\r\nTry `mkdir --help' for more information.\r\n")
        else:
            #format the new entry
            newdirectory = 'drwx--x--x 70 ' + self.attacker_username + '     users 4.0K ' + datetime.now().strftime("%Y-%m-%d %H:%M ") + self.params[0] + '/'
            FAKE_DIR_STRUCT[self.fake_workingdir].append(newdirectory)
            FAKE_DIR_STRUCT[self.fake_workingdir + '/' + self.params[0]] = ""


    def process_netstat(self):
        for line in FAKE_NETSTAT:
            self.transport.write(line + '\r\n')

    def process_passwd(self):
        self.transport.write('Changing password for user.\r\n')
        self.transport.write('New password: \r\n')

    def process_perl(self):
        self.transport.write('This is perl 5, version 12, subversion 4 (v5.12.4) ')
        self.transport.write('built for i386-linux-thread-multi\r\n\r\n')
        self.transport.write('Copyright 1987-2010, Larry Wall\r\n\r\n')
        self.transport.write('Perl may be copied only under the terms of either the')
        self.transport.write('Artistic License or the\r\nGNU General Public License, ')
        self.transport.write('which may be found in the Perl 5 source kit.\r\n\r\n')
        self.transport.write('Complete documentation for Perl, including FAQ lists, ')
        self.transport.write('should be found on\r\nthis system using "man perl" or ')
        self.transport.write('"perldoc perl".  If you have access to the\r\nInternet, ')
        self.transport.write( 'point your browser at http://www.perl.org/, the Perl Home Page.\r\n')

    def process_php(self):
        self.transport.write(FAKE_PHP)

    def process_ping(self):
        self.transport.write('PING ' + self.params[0] + ' 56(84) bytes of data.\r\n')
        self.transport.write('64 bytes from ' + self.params[0] + ': icmp_seq=1 ttl=63 time=81.1 ms\r\n')
        self.transport.write('64 bytes from ' + self.params[0] + ': icmp_seq=2 ttl=63 time=83.9 ms\r\n')
        self.transport.write('64 bytes from ' + self.params[0] + ': icmp_seq=3 ttl=63 time=81.0 ms\r\n')
        self.transport.write('64 bytes from ' + self.params[0] + ': icmp_seq=4 ttl=63 time=83.8 ms\r\n\r\n')
        self.transport.write('--- ' + self.params[0] + ' ping statistics ---\r\n')
        self.transport.write('4 packets transmitted, 4 received, 0% packet loss, time 3088ms\r\n')
        self.transport.write('rtt min/avg/max/mdev = 81.072/82.506/83.960/1.411 ms\r\n')

    def process_ps(self):
        for line in FAKE_PS:
            self.transport.write(line + '\r\n')

    def process_pwd(self):
        self.transport.write(self.fake_workingdir + '\r\n')

    def process_reboot(self):
        if(self.attacker_username=="root"):
            now=time.strftime("%H:%M",time.localtime())
            self.transport.write('\r\nBroadcast message from root@' +FQDN+'\r\n')
            self.transport.write('\t(/dev/pts/0) at ' +now+ ' ...\r\n\r\n')
            self.transport.write('The system is going down for reboot NOW!\r\n')
            self.transport.loseConnection()
        else:
            self.transport.write("Failed to set wall message, ignoring: Interactive authentication required.\r\n"
            "Failed to reboot system via logind: Interactive authentication required.\r\n"
            "Failed to start reboot.target: Interactive authentication required.\r\n"
            "See system logs and 'systemctl status reboot.target' for details.\r\n"
            "Failed to open /dev/initctl: Permission denied\r\n"
            "Failed to talk to init daemon.\r\n")

    def process_rpm(self):
        self.transport.write('RPM version 4.8.0\r\n')
        self.transport.write('Copyright (C) 1998-2002 - Red Hat, Inc.\r\n')
        self.transport.write('This program may be freely redistributed under the terms of the GNU GPL\r\n')

    def process_rm(self):
        self.transport.write('\r\n' + FAKE_RM + '\r\n')

    def process_service(self):
        if (len(self.params)) == 2:
            if self.params[0] in FAKE_SERVICES:
                if self.params[1] == "start":
                    self.transport.write('Starting ' + self.params[0] + ":\r\n")
                elif self.params[1] == "stop":
                    self.transport.write('Stopping ' + self.params[0] + ":\r\n")
                elif self.params[1] == "restart":
                    self.transport.write('Restarting ' + self.params[0] + ":\r\n")
                elif self.params[1] == "status":
                    self.transport.write(self.params[0] + " dead but subsys locked\r\n")
                else:
                    self.transport.write(FAKE_SERVICE_USAGE.format(self.params[0]))
            else:
                self.transport.write(self.params[0] + ': unrecognized service\r\n')
        elif (len(self.params)) == 1:
            if self.params[0] == "--status-all":
                for line in FAKE_SERVICE_ALL:
                    self.transport.write(line + '\r\n')
            elif self.params[0] in FAKE_SERVICES:
                self.transport.write('Usage: ' + self.params[0] + ': {start|stop|restart}\r\n')
            else:
                self.transport.write(self.params[0] + ': unrecognized service\r\n')
        else:
            self.transport.write('Usage: service < option > | --status-all | [ service_name [ command | --full-restart ] ]\r\n')

    def process_strings(self):
        if len(self.params)>1 and self.params== ['-a','/usr/sbin/sshd','|','grep','%s:%s','-A2','-B2']:
            self.transport.write('port %d\r\n')
            self.transport.write('listenaddress [%s]:%s\r\n')
            self.transport.write('listenaddress %s:%s\r\n')
            self.transport.write('subsystem %s %s\r\n')
            self.transport.write('maxstartups %d:%d:%d\r\n')
        else:
            self.process_undef()

    def process_time(self):
        self.transport.write(FAKE_TIME)

    def process_tar(self):
        if len(self.params)>0 and self.params[0] == '--help':
            self.transport.write(FAKE_TAR_HELP)
        else:
            self.transport.write(FAKE_TAR)

    def process_uname(self):
        self.transport.write(FAKE_OS+'\r\n')

    def process_undef(self):
        if self.cmd == "":
            pass
        else:
            self.transport.write(self.cmd + ": command not found\r\n")

    def process_unset(self):
        pass

    def process_uptime(self):
        self.transport.write(" " + datetime.now().strftime("%H:%M:%S") + " up 15 days, 7 min,  1 users,  load average: 0.07, 0.06, 0.04\r\n")

    def process_w(self):
        self.transport.write('USER\tTTY\tFROM\tLOGIN@\t\tIDLE\tJCPU\tPCPU\tWHAT\r\n')
        self.transport.write(self.attacker_username + '\tpts/1\t'+self.ip+'\t09:05\t0.00s\t0.04s\t0.00s\tw\r\n')

    def process_wget(self):
	result_data = xsweet_download_files.wget(self.params, self.ip)
        if result_data != "":
            self.transport.write(result_data+'\r\n')
        return True

    def process_who(self):
        self.transport.write(self.attacker_username + '\tpts/1\t'+datetime.now().strftime("%Y:%M:%S %H:%M")+'('+self.ip+')\r\n')

    def process_whoami(self):
        self.transport.write(self.attacker_username+'\r\n')

    def process_yum(self):
        if len(self.params)>0 and (self.params[0] == 'install' or self.params[0] == 'update'):
            self.transport.write('Another app is currently holding the yum lock; waiting for it to exit...\r\n')
        else:
            self.transport.write('Loaded plugins: fastestmirror\r\n')
            self.transport.write('You need to give some command\r\n')
            self.transport.write('Usage: yum [options] COMMAND\r\n')
