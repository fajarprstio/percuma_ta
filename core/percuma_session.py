# Copyright (C) 2019 Fajar prasetio <fajarprstyo05@gmail.com>
#


#!/usr/bin/env python

from twisted.conch.ssh import session

from core.percuma_protocol import *

class PercumaSession:

    def __init__(self, avatar):
	"test"

    def openShell(self, protocol):
        serverProtocol = PercumaProtocol()
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def getPty(self, terminal, windowSize, attrs):
        return None

    def execCommand(self, protocol, cmd):
        raise NotImplementedError

    def closed(self):
        pass
