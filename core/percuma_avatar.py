# Copyright (C) 2019 Fajar prasetio <fajarprstyo05@gmail.com>
#



#!/usr/bin/env python

from twisted.conch.ssh import session
from twisted.conch import avatar

class SSHAvatar(avatar.ConchUser):

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
	self.channelLookup.update({'session':session.SSHSession})
