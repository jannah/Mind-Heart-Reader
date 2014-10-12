# based off code copyright (c) 2009, Kai Groner 

#
# TODO: 
#
# capture Blink events
# calculate entropy
#

import sys, serial, struct, logging, logging.handlers
from cStringIO import StringIO
from collections import namedtuple
import numpy as np

_log = logging.getLogger(__name__)

_bytelog = logging.getLogger(__name__+'.bytes')
_bytelog.propagate = False

# Uncomment this to save log messages about the data stream in memory
# _bytes = logging.handlers.MemoryHandler(sys.maxint, 100)
# _bytes.addFilter(logging.Filter(name=__name__+'.bytes'))
# _bytelog.addHandler(_bytes)


class ThinkGearProtocol(object):
    '''Process the ThinkGear protocol.

    >>> tg = ThinkGearProtocol(device)
    >>> for pkt in tg.get_packets():
    ...     for d in pkt:
    ...         if isinstance(d, ThinkGearAttentionData) and d.value == 100:
    ...             print "You win!"
    ...             break

    '''

    # The _read/_deread scheme is untested

    def __init__(self, port):
        # TODO: Handle bluetooth rfcomm setup
        # TODO: ???

        self.serial = serial.Serial(port, 57600)
        self.preread = StringIO()
        self.io = self.serial

    @staticmethod
    def _chksum(packet):
        return ~sum( ord(c) for c in packet ) & 0xff

    def _read(self, n):
        buf = self.io.read(n)
        if len(buf) < n:
            _log.debug('incomplete read, short %s bytes', n - len(buf))
            if self.io == self.preread:
                _log.debug('end of preread buffer')
                self.preread.reset()
                self.preread.truncate()
                self.io = self.serial
                buf += self.io.read(n-len(buf))
                if len(buf) < n:
                    _log.debug('incomplete read, short %s bytes', n - len(buf))

        for o in xrange(0, len(buf), 16):
            _bytelog.debug('%04X  '+' '.join(('%02X',)*len(buf[o:o+16])), o, *( ord(c) for c in buf[o:o+16] ))

        return buf

    def _deread(self, buf):
        _log.debug('putting back %s bytes', len(buf))
        pos = self.preread.tell()
        self.preread.seek(0, 2)
        self.preread.write(buf)
        self.preread.seek(pos)
        self.io = self.preread

    def get_packets(self):
        last_two = ()
        while True:
            last_two = last_two[-1:]+(self._read(1),)
            #_log.debug('last_two: %r', last_two)
            if last_two == ('\xAA','\xAA'):
                plen = self._read(1)
                if plen >= '\xAA':
                    # Bogosity
                    _log.debug('discarding %r while syncing', last_two[0])
                    last_two = last_two[-1:]+(plen,)

                else:
                    last_two = ()
                    packet = self._read(ord(plen))
                    checksum = self._read(1)

                    if ord(checksum) == self._chksum(packet):
                        yield self._decode(packet)

                    else:
                        _log.debug('bad checksum')
                        self._deread(packet+checksum)

            elif len(last_two) == 2:
                _log.debug('discarding %r while syncing', last_two[0])

    def _decode(self, packet):
        decoded = []

        while packet:
            extended_code_level = 0
            while len(packet) and packet[0] == '\x55':
                extended_code_level += 1
                packet = packet[1:]
            if len(packet) < 2:
                _log.debug('ran out of packet: %r', '\x55'*extended_code_level+packet)
                break
            code = ord(packet[0])
            if code < 0x80:
                value = packet[1]
                packet = packet[2:]
            else:
                vlen = ord(packet[1])
                if len(packet) < 2+vlen:
                    _log.debug('ran out of packet: %r', '\x55'*extended_code_level+chr(code)+chr(vlen)+packet)
                    break
                value = packet[2:2+vlen]
                packet = packet[2+vlen:]

            if not extended_code_level and code in data_types:
                data = data_types[code](extended_code_level, code, value)

            elif (extended_code_level,code) in data_types:
                data = data_types[(extended_code_level,code)](extended_code_level, code, value)

            else:
                data = ThinkGearUnknownData(extended_code_level, code, value)

            decoded.append(data)

        return decoded


data_types = {}

class ThinkGearMetaClass(type):
    def __new__(mcls, name, bases, data):
        cls = super(ThinkGearMetaClass, mcls).__new__(mcls, name, bases, data)
        code = getattr(cls, 'code', None)
        if code:
            data_types[code] = cls
            extended_code_level = getattr(cls, 'extended_code_level', None)
            if extended_code_level:
                data_types[(extended_code_level,code)] = cls
        return cls


class ThinkGearData(object):
    def __init__(self, extended_code_level, code, value):
        self.extended_code_level = extended_code_level
        self.code = code
        self.value = self._decode(value)
        if self._log:
            _log.log(self._log, '%s', self)

    @staticmethod
    def _decode(v):
        return v

    def __str__(self):
        return self._strfmt % vars(self)

    __metaclass__ = ThinkGearMetaClass

    _log = logging.DEBUG


class ThinkGearUnknownData(ThinkGearData):
    '''???'''
    _strfmt = 'Unknown: code=%(code)02X extended_code_level=%(extended_code_level)s %(value)r'


class ThinkGearPoorSignalData(ThinkGearData):
    '''POOR_SIGNAL Quality (0-255)'''
    code = 0x02
    _strfmt = '%(value)s'
    _decode = staticmethod(ord)


class ThinkGearBlinkData(ThinkGearData):
    '''BLINK (0-255)'''
    code = 0x16
    _strfmt = 'BLINK: %(value)s'
    _decode = staticmethod(ord)


class ThinkGearAttentionData(ThinkGearData):
    '''ATTENTION eSense (0 to 100)'''
    code = 0x04
    _strfmt = 'ATTENTION eSense: %(value)s'
    _decode = staticmethod(ord)


class ThinkGearMeditationData(ThinkGearData):
    '''MEDITATION eSense (0 to 100)'''
    code = 0x05
    _strfmt = 'MEDITATION eSense: %(value)s'
    _decode = staticmethod(ord)


class ThinkGearRawWaveData(ThinkGearData):
    '''RAW Wave Value (-32768 to 32767)'''
    code = 0x80
    _strfmt = '%(value)s'
    _decode = staticmethod(lambda v: struct.unpack('>h', v)[0])
    # There are lots of these, don't log them by default
    _log = False


#EEGPowerData = namedtuple('EEGPowerData', 'delta theta lowalpha highalpha lowbeta highbeta lowgamma midgamma')
class ThinkGearEEGPowerData(ThinkGearData):
    '''Eight EEG band power values (0 to 16777215).
    
    delta, theta, low-alpha high-alpha, low-beta, high-beta, low-gamma, and
    mid-gamma EEG band power values.
    '''

    code = 0x83
    _strfmt = '%(value)r'
    _decode = staticmethod(lambda v: struct.unpack('>8L', ''.join( '\x00'+v[o:o+3] for o in xrange(0, 24, 3))))

