# Copyright (C) 2019 Fajar prasetio <fajarprstyo05@gmail.com>
#


#!/usr/bin/env python

from datetime import datetime
import tzlocal

from twisted.cred import checkers, credentials
from twisted.internet import defer
from zope.interface import implements
from twisted.conch import error

from core.percuma_logging import *

class HoneypotPasswordChecker:
    implements(checkers.ICredentialsChecker)

    credentialInterfaces = {credentials.IUsernamePassword}

    def requestAvatarId(self, credentials):
	now = datetime.now(tzlocal.get_localzone())
        attempts =str(now)+ " " +credentials.username+":"+credentials.password+"\n"
        normalwrite(LOGFILE,attempts)
        if self.checkUserPass(credentials.username, credentials.password):
            return defer.succeed(credentials.username)
        else:
            return defer.fail(error.UnauthorizedLogin())
        return defer.fail(error.UnhandledCredentials())

    def checkUserPass(self, username, password):
        filepath = 'list.txt'
        with open(filepath) as fp:
            line = fp.readline().strip("\n")
            while line:
                user, passw = line.split(":")
                if user==username and passw == password:

                    return True


                line = fp.readline().strip("\n")
        return False
