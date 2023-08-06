"""
This module provides support for the HAL CA1006 prtocol
"""
# Copyright (c) 2020 Brad Keifer
#
# This file is part of the HAL CA1006 package.
# 
# The HAL CA1006 package is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The HAL CA1006 package  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# For a copy of the GNU General Public License, see <https://www.gnu.org/licenses/>.
# 
#
# Contributors:
#    Brad Keifer - initial release
#

# Protocol details:
# E0: TURN ECHO OFF
# E1: TURN ECHO ON
# HE: HELP
# ? : HELP
# ID: INTERCOM DISABLE
# IE: INTERCOM ENABLE
# IM: XMIT IR MACRO  :- IM <MACRO>
# IR: XMIT IR        :- IR <SRC> <KEY>
# MU: SET NODE MUTE  :- MU <ADDR> <MUTE>
# NO: GET NODE STATUS:- NO <ADDR>
# PM: SET NODE PARTY MODE :- PM <PARTY ZONE> <STATE> <SOURCE> <VOLUME> <MUTE>
# PW: SET NODE POWER :- PW <ADDR> <STATE>
# SA: SET NODE SOURCE REL:-  SA <ADDR> <SRC>
# SC: SCAN 485 NODES
# SE: SET NODE STATUS:- SE <ADDR> <STATE> <SRC> <VOL> <MUTE>
# SS: SET NODE SOURCE:- SS <ADDR> <SRC>
# SR: RETURNS RA STATUS  :- SR <ADDR>
# SL: SET SLAVE STATUS:- SL <STATE>
# ST: AM6 STATUS
# TO: SYSTEM PWR SAVE
# VA: NODE VOL ABS   :- VA <ADDR> <VOL>
# VE: VERSION
# VR: NODE VOL REL   :- VR <ADDR> <INC/DEC>
# VX: RETURNS RA FIRMWARE VERSION  :- VX <ADDR>
# ZI: Transmit IR Code of the Nodes' selected source :- ZI <ADDR> <KEY>


import logging
import logging.handlers
import argparse
import errno
import platform
import socket
import select
import sys
import time
from threading import Lock

if platform.system() == 'Windows':
    EAGAIN = errno.WSAEWOULDBLOCK
else:
    EAGAIN = errno.EAGAIN


# HAL CA1006 Protocol Commands
ECHO_OFF = b'E0'
ECHO_ON = b'E1'
HELP = b'HE'
INTERCOM_DISABLE = b'ID'
INTERCOM_ENABLE = b'IE'
SET_NODE_MUTE = b'MU ' #<ADDR> <MUTE>
GET_NODE_STATUS = b'NO ' #<ADDR>
SET_NODE_PARTY_MODE = b'PM ' #<PARTY ZONE> <STATE> <SOURCE> <VOLUME> <MUTE>
SET_NODE_POWER = b'PW ' #<ADDR> <STATE>
SET_NODE_SOURCE_REL = b'SA ' #<ADDR> <SRC>
SCAN_485_NODES = b'SC'
SET_NODE_STATUS = b'SE ' #<ADDR> <STATE> <SRC> <VOL> <MUTE>
SET_NODE_SOURCE = b'SS ' #<ADDR> <SRC>
GET_RA_STATUS = b'SR ' #<ADDR>
SET_SLAVE_STATUS = b'SL ' #<STATE>
GET_AM6_STATUS = b'ST'
SET_SYSTEM_PWR_SAVE = b'TO'
SET_NODE_VOL_ABS = b'VA ' #<ADDR> <VOL>
GET_VERSION = b'VE'
SET_NODE_VOL_REL = b'VR ' #<ADDR> <INC/DEC>
GET_RA_VERSION = b'VX ' #<ADDR>

HAL_MSG = {
    ECHO_OFF: 'ECHO OFF',
    ECHO_ON: 'ECHO ON',
    HELP: 'HELP',
    INTERCOM_DISABLE: 'INTERCOM DISABLE',
    INTERCOM_ENABLE: 'INTERCOM ENABLE',
    SET_NODE_MUTE: 'SET NODE MUTE',
    GET_NODE_STATUS: 'GET NODE STATUS',
    SET_NODE_PARTY_MODE: 'SET PARTY MODE',
    SET_NODE_POWER: 'SET NODE POWER',
    SET_NODE_SOURCE_REL: 'SET NODE SOURCE REL',
    SCAN_485_NODES: 'SCAN 485 NODES',
    SET_NODE_STATUS: 'SET NODE STATUS',
    SET_NODE_SOURCE: 'SET NODE SOURCE',
    GET_RA_STATUS: 'GET RA STATUS',
    SET_SLAVE_STATUS: 'SET SLAVE STATUS',
    GET_AM6_STATUS: 'GET AM6 STATUS',
    SET_SYSTEM_PWR_SAVE: 'SET SYSTEM POWER SAVE',
    SET_NODE_VOL_ABS: 'SET NODE VOL ABS',
    GET_VERSION: 'GET VERSION',
    SET_NODE_VOL_REL: 'SET NODE VOL REL',
    GET_RA_VERSION: 'GET RA FIRMWARE VERSION',
}

HAL_SUCCESS_MSG = {
    ECHO_OFF: 'ECHO OFF',
    ECHO_ON: 'ECHO ON',
    HELP: 'HELP',
    INTERCOM_DISABLE: 'INTERCOM DISABLE',
    INTERCOM_ENABLE: 'INTERCOM ENABLE',
    SET_NODE_MUTE: b'MUTE SENDING - PLEASE WAIT\n\rMUTE SEND COMPLETE',
    GET_NODE_STATUS: b'SCAN COMPLETE',
    SET_NODE_PARTY_MODE: 'SET PARTY MODE',
    SET_NODE_POWER: b'PWR STATE SEND-PLEASE WAIT\n\rPOWER STATE SEND COMPLETE',
    SET_NODE_SOURCE_REL: 'SET NODE SOURCE REL',
    SCAN_485_NODES: 'SCAN 485 NODES',
    SET_NODE_STATUS: b'SE ',
    SET_NODE_SOURCE: b'SOURCE SEND - PLEASE WAIT\n\rSOURCE SEND COMPLETE',
    GET_RA_STATUS: b'Status Source Volume Video Mute  !!!!!RA Status!!!!!   \n\r',
    SET_SLAVE_STATUS: 'SET SLAVE STATUS',
    GET_AM6_STATUS: 'GET AM6 STATUS',
    SET_SYSTEM_PWR_SAVE: b'SYSTEM POWERSAVE EXECUTING\n\rSYSTEM POWERSAVE EXECUTED',
    SET_NODE_VOL_ABS: b'VOLUME SEND - PLEASE WAIT\n\rVOLUME SEND COMPLETE',
    GET_VERSION: b'AM6 VERSION ',
    SET_NODE_VOL_REL: 'SET NODE VOL REL',
    GET_RA_VERSION: 'GET RA FIRMWARE VERSION',
}

# Constants/defaults for this package
HAL_ERR_NO_CONN = 1
HAL_MSG_INTERVAL = 0.1  # Seconds to wait between commands to the HAL
HAL_SELECT_INTERVAL = 1 # Max Seconds to wait for response to command
HAL_SELECT_MIN_INTERVAL = 0.3 # Min seconds that _select_interval can be set to
HAL_MAX_VOL = 32
HAL_EOL = b'\r'
HAL_ZONES = 6
HAL_SOURCES = 8
HAL_NODES = 64
HAL_UNKNOWN = 'UNKNOWN'
MAX_MSG_ERRORS = 10   # Maximum errors tolerated before exiting
MAX_RECONNECTS = 5    # Maximum number of reconnect attempts after broken pipe
PING_PERIOD = 60      # Seconds between pings of the HAL

# Log levels
HAL_LOG_INFO = 'info'
HAL_LOG_WARNING = 'warning'
HAL_LOG_ERROR = 'error'
HAL_LOG_DEBUG = 'debug'
HAL_LOG_CRITICAL = 'critical'
LOGGING_LEVEL = {
    HAL_LOG_DEBUG: logging.DEBUG,
    HAL_LOG_INFO: logging.INFO,
    HAL_LOG_WARNING: logging.WARNING,
    HAL_LOG_ERROR: logging.ERROR,
    HAL_LOG_CRITICAL: logging.CRITICAL,
}


class HALProtocol(object):
    """HAL CA1006 protocol class

    This is the main class for communication with a HAL CA1006
    multi-zone amplifier.

    General usage flow:

    * Use connect() to connect to a HAL CA1006 unit
    * Use enable_logger() to enable logging
    * Use disable_logger() to disable logging
    * ADD STUFF IN HERE
    * Use disconnect() to disconnect from the HAL CA1006 unit
    """
           
    def __init__(self, host, port, name='', keepalive=PING_PERIOD):
        """ Initialise HAL CA1006 class """

        self._host = host
        self._port = int(port)
        self._name = name
        self._keepalive = keepalive
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._msg_errors = 0
        self._logger = None
        self._last_tx_t = time.time()
        self._power = {}
        self._source = {}
        self._volume = {}
        self._mute = {}
        self._node_status = {}
        self._lock = Lock()
        self._select_interval = HAL_SELECT_INTERVAL
        self._version = HAL_UNKNOWN
        for i in range(1, HAL_ZONES+1):
            self._power[i] = HAL_UNKNOWN
            self._source[i] = HAL_UNKNOWN
            self._volume[i] = HAL_UNKNOWN
            self._mute[i] = HAL_UNKNOWN
        for i in range(HAL_NODES):
            self._node_status[i] = HAL_UNKNOWN
        
    def _txrx(self, send_msg):
        self._easy_log(HAL_LOG_DEBUG,
                       f'_txrx: Obtaining lock for {self._lock}')
        with self._lock:
            self._easy_log(HAL_LOG_DEBUG,
                           f'_txrx: Lock obtained for {self._lock}')
            self._sock_send(send_msg)
            rcv_msg = self._read_input_buffer()
        
        self._easy_log(HAL_LOG_DEBUG,
                       f'_txrx: Lock released for {self._lock}')
        return rcv_msg
        
    def _sock_recv(self, bufsize):
        for i in range(MAX_RECONNECTS):
            try:
                r, w, e = select.select([self._sock], [], [self._sock], self._select_interval)
                if self._sock in e:
                    self._easy_log(HAL_LOG_ERROR,
                                   f'_sock_recv():{self._name}:Unexpected socket select error'
                                   f' with HAL CA1006 socket {self._sock}.')
                    self._sock.close()
                    self._reconnect()
                    return b''
                
                if self._sock in r:
                    return self._sock.recv(bufsize)
                else:
                    # Timed out - node must be dead. Time to exit
                    self._easy_log(HAL_LOG_ERROR,
                                   f'_sock_recv():{self._name}:Timed out waiting on read from '
                                   f'HAL CA1006 socket {self._sock}.')
                    self._sock.close()
                    self._reconnect()
                    return b''
            except ConnectionError as err:
                self._easy_log(HAL_LOG_ERROR,
                               f'Connection Error ({err}) on recv. '
                               f'Reconnect attempt {i+1}.')
                self._reconnect()
                return b''
            except:
                self._easy_log(HAL_LOG_ERROR,f'Unexpected Error on recv.')
                raise
            
        self._easy_log(HAL_LOG_ERROR,
                       f'_sock_recv():{self._name} exceeded MAX_RECONNECTS ({MAX_RECONNECTS})')
        self._sock.close()
        self._reconnect()
        return b''

    def _sock_send(self, buf):
        if not buf.endswith(HAL_EOL):
            self._easy_log(HAL_LOG_WARNING,
                           f'_sock_send():{self._name}: buffer ({buf}) does not '
                           f'end with EOL byte ({HAL_EOL}). '
                           f'It will be added.')
            buf += HAL_EOL
        for i in range(MAX_RECONNECTS):
            now = time.time()
            inter_tx_time = now - self._last_tx_t
            self._easy_log(HAL_LOG_DEBUG,
                           f'_sock_send():{self._name}: _last_tx_t = {self._last_tx_t}, '
                           f'now = {now}, inter_tx_time = {inter_tx_time}.')
            if inter_tx_time < HAL_MSG_INTERVAL:
                self._easy_log(HAL_LOG_DEBUG,
                               f'Short inter-transmission time ({inter_tx_time} s).')
                self._easy_log(HAL_LOG_DEBUG,
                               f'Sleeping for {HAL_MSG_INTERVAL - inter_tx_time} s.')
                time.sleep(HAL_MSG_INTERVAL - inter_tx_time)
                
            self._easy_log(HAL_LOG_DEBUG,
                           f'_sock_send():{self._name}: Sending {buf}')
            self._last_tx_t = time.time()
            try:
                return self._sock.sendall(buf)
            except ConnectionError as err:
                self._easy_log(HAL_LOG_ERROR,
                               f'Connection Error ({err}) on send. '
                               f'Reconnect attempt {i+1}.')
                self._reconnect()
                return 0
            except:
                self._easy_log(HAL_LOG_ERROR,f'Unexpected Error on send.')
                raise
                
        self._easy_log(HAL_LOG_ERROR,
                       f'_sock_send():{self._name} exceeded MAX_RECONNECTS ({MAX_RECONNECTS})')
        self._sock.close()
        self._reconnect()
        return 0


    def _reconnect(self):
        if self._sock is None:
            return RTS_ERR_NO_CONN
        
        self.disconnect()        
        c = self._sock.connect((self._host, self._port))
        self._flush_input_buffer()
#         self._get_all_info()
        return c
        
    def _set_echo(self, echo):
        """ Set echo property of HAL device
        :param echo: 0 = off, 1 = on
        """

        self._easy_log(HAL_LOG_DEBUG,
                       f'set_echo():{self._name}: change echo to {echo}.')
        if echo == '0':
            send_msg = ECHO_OFF
        else:
            send_msg = ECHO_ON
        send_msg += HAL_EOL

        self._sock_send(send_msg)
        
        rcv_msg = self._read_input_buffer()
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_echo():{self._name}: Bytes read: {rcv_msg}')
        return True

    def _get_all_info(self):
        """Obtain all info about HAL CA1006 system"""
        if not self.is_connected():
            self.connect()
        self._get_version()
        for i in range(1, HAL_ZONES+1):
            self.get_zone_info(str(i))
        for i in range(HAL_NODES):
            self._get_node_status(str(i))

    def _flush_input_buffer(self):
        """Flush any and all data in the input buffer"""
        self._read_input_buffer()
        return None
                
    def _read_input_buffer(self):
        """Read and return the input buffer"""
        
        all_input_read = False
        reply_msg = b''
        while not all_input_read:
            ready_to_read, ready_to_write, in_error = \
                           select.select([self._sock], [], [self._sock], self._select_interval)
            if len(in_error) != 0:
                self._easy_log(HAL_LOG_ERROR,
                               '_read_input_buffer():{self._name}: Unexpected socket select error.')
                self._sock.close()
                self._reconnect()
            
            elif len(ready_to_read) > 0:
                reply_msg += self._sock_recv(1024)    
                self._easy_log(HAL_LOG_DEBUG,
                               f'Read data:{self._name}: {reply_msg}')
                self._easy_log(HAL_LOG_DEBUG,
                               'Data length = %d bytes ', len(reply_msg))
                if not reply_msg:
                    self._easy_log(HAL_LOG_ERROR,
                                   '_read_input_buffer(): Error reading data after socket connect.')
                    self._sock.close()
                    self._reconnect()
            else:
                # No more input data to be flushed
                all_input_read = True
        
        return reply_msg
                

    def _easy_log(self, level, fmt, *args):
        if self._logger is not None:
            level_std = LOGGING_LEVEL[level]
            self._logger.log(level_std, fmt, *args)

    def _msg_error_handler(self):
        """Generic handler when messages received from HAL are in error."""
        self._msg_errors += 1
        if self._msg_errors >= MAX_MSG_ERRORS:
            self._sock.close()
            self._reconnect()
            
        return None
    
    def _find_signature(self, data_stream, msg_signature):
        """ Takes the stream of bytes received and looks for a
        message that matches the signature of the expected response """
        
        index = data_stream.find(msg_signature)
        if index == -1:
            self._easy_log(HAL_LOG_DEBUG,
                           f'find_signature():{self._name}: {msg_signature} '
                           f'not found in {data_stream}.')
        else:
            self._easy_log(HAL_LOG_DEBUG,
                           f'find_signature():{self._name}: {msg_signature} '
                           f' found in {data_stream} at index {index}.')
        return index



    def enable_logger(self, logger=None):
        """ Enables a logger to send log messages to """
        if logger is None:
            if self._logger is not None:
                # Do not replace existing logger
                return
            logger = logging.getLogger(__name__)
        self._logger = logger

    def disable_logger(self):
        self._logger = None

    def connect(self):
        """Connect to a HAL CA1006 multi-zone amplifier"""

        self._msg_errors = 0
        self._easy_log(HAL_LOG_DEBUG,
                       f'connect():{self._name}:Attempting socket connection to host {self._host}, '
                       f'port {self._port} with keepalive {self._keepalive}s.')
        try:
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE,
                                  self._keepalive)
            c = self._sock.connect((self._host, self._port))
            self._easy_log(HAL_LOG_DEBUG,
                           f'connect():{self._name}: Socket connect call returned {c}.')
            if c == -1:
                self._easy_log(HAL_LOG_ERROR,
                               f'connect():{self._name}: Cannot connect to host '
                               f'{self._host}, port {self._port}.'
                               f' Errno {errno}')
                return False
                
            self._flush_input_buffer()
            self._set_echo('0') #Turn off echo to be safe
            self._get_version()
            return True
        except socket.error as msg:
            self._easy_log(HAL_LOG_DEBUG,
                           f'connect():{self._name}: Socket connect call threw exception. '
                           f'{msg}')
            if self.is_connected():
                self._easy_log(HAL_LOG_WARNING,
                               f'connect():{self._name}: Already connected.')
                return True
            
            self._easy_log(HAL_LOG_ERROR,
                           f'connect():{self._name}: Error connecting to host '
                           f'{self._host}, port {self._port}')
            return False


    def disconnect(self):
        if not self.is_connected():
            return HAL_ERR_NO_CONN

        self._easy_log(HAL_LOG_DEBUG,
                       f'disconnect(): Disconnecting.')
        return self._sock.close()
        
    def is_connected(self):
        """ Check we are connected """

        try:  # Will throw an exception if sock is not connected hence the try catch.
            return self._sock.getpeername() != ''
        except:
            return False
        return False

    def socket(self):
        """Return the socket for this client."""
        return self._sock

    def ping(self):
        """Ping the amp."""
        pass

    def loop_misc(self):
        """Handles general ongoing housekeeping duties for the HAL connections.

        At this stage, the only housekeeping task is to ping() the nodes of the
        socket on a regular basis
        """
        if time.time() - self._last_tx_t > PING_PERIOD:
            self._easy_log(HAL_LOG_DEBUG,
                           f'loop_misc():{self._name}: Time for a ping!')
            self.ping()
    
        return None
    
    def get_select_interval(self):
        """Return the select interval used to wait for all data to be returned by the HAL."""
        return self._select_interval
    
    def set_select_interval(self, interval):
        """Change the wait time used in select calls when reading data from the HAL."""
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_select_interval():Changing _select_interval from '
                       f'{self._select_interval} to {interval}.')
        new_interval = float(interval)
        if new_interval <= HAL_SELECT_MIN_INTERVAL:
            self._easy_log(HAL_LOG_WARNING,
                           f'set_select_interval():New interval {interval} is invalid. '
                           f'Must be greater than {HAL_SELECT_MIN_INTERVAL}.')
        else:
            self._select_interval = new_interval

    def turn_off(self):
        """Turn off all zones."""
        self._easy_log(HAL_LOG_DEBUG, f'turn_off() called.')
        send_msg = SET_SYSTEM_PWR_SAVE
        send_msg += HAL_EOL
        rcv_msg = self._txrx(send_msg)
        i = self._find_signature(rcv_msg, HAL_SUCCESS_MSG[SET_SYSTEM_PWR_SAVE])
        if i != -1:
            self._easy_log(HAL_LOG_DEBUG, f'turn_off() Success.')
            return True
        self._easy_log(HAL_LOG_ERROR, f'turn_off() Failure.')
        return False
        
    def set_node_status(self, zone, power, source, volume, mute):
        """ Generic node status change """
        
        z = int(zone)
        vol = str(int(volume) * HAL_MAX_VOL // 100)
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_node_status():{self._name}: zone {zone}, '
                       f'change power from {self._power[z]} to {power}, '
                       f'change source from {self._source[z]} to {source}, '
                       f'change volume from {self._volume[z]} to {vol}, '
                       f'change mute from {self._mute[z]} to {mute}')
        send_msg = SET_NODE_STATUS
        send_msg += zone.encode()
        send_msg += b' '
        send_msg += power.encode()
        send_msg += b' '
        send_msg += source.encode()
        send_msg += b' '
        send_msg += vol.encode()
        send_msg += b' '
        send_msg += mute.encode()
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_node_status():{self._name}: Bytes read: {rcv_msg}')
        i = self._find_signature(rcv_msg, HAL_SUCCESS_MSG[SET_NODE_STATUS])
        if i != -1:
            j = i + 15 #self._find_signature(rcv_msg[i:], b'\n')
            attrs = rcv_msg[i:j].decode().split()
            self._easy_log(HAL_LOG_DEBUG,
                           f'set_node_status():{self._name}: i {i}, j {j}, attrs {attrs}.')
            if z != int(attrs[1]):
                self._easy_log(HAL_LOG_ERROR,
                               f'set_node_status():Error: Expected zone {zone}, '
                               f'but read zone {attrs[1]} in the response from HAL')
                return False
            self._power[z] = attrs[2]
            self._source[z] = attrs[3]
            self._volume[z] = attrs[4]
            self._mute[z] = attrs[5]
            self._easy_log(HAL_LOG_DEBUG,
                           f'set_node_status():{self._name}: Success!.')
            return True
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'set_node_status():{self._name}: Failure :-(.')
            return False        

    def set_power(self, zone, power):
        """ Switch power on/off to a zone
        :param zone: The zone to be controlled [1-6]
        :param power: 0 = off, 1 = on
        """

        self._easy_log(HAL_LOG_DEBUG,
                       f'set_power():{self._name}: zone {zone}, change power to {power}.')
        send_msg = SET_NODE_POWER
        send_msg += zone.encode()
        send_msg += b' '
        send_msg += power.encode()
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
                    
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_power():{self._name}: Bytes read: {rcv_msg}')
        if self._find_signature(rcv_msg, HAL_SUCCESS_MSG[SET_NODE_POWER]) != -1:
            self._power[int(zone)] = power
            self._easy_log(HAL_LOG_DEBUG,
                           f'set_power():{self._name}: Success!.')
            return True
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'set_power():{self._name}: Failure :-(.')
            return False

    def set_volume(self, zone, volume):
        """ Set volume for zone to specific value.
        Scale the volume to translate to a range (0..HAL_MAX_VOL) as expected by HAL
        (Even though the keypads show 0..100).
        """
        
        volume = str((int(volume) * HAL_MAX_VOL) // 100)
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_volume():{self._name}: zone {zone}, change volume to {volume}.')
        send_msg = SET_NODE_VOL_ABS
        send_msg += zone.encode()
        send_msg += b' '
        send_msg += volume.encode()
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_volume():{self._name}: Bytes read: {rcv_msg}')
        if self._find_signature(rcv_msg, HAL_SUCCESS_MSG[SET_NODE_VOL_ABS]) != -1:
            self._volume[int(zone)] = volume
            self._easy_log(HAL_LOG_DEBUG,
                           f'set_volume():{self._name}: Success!.')
            return True
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'set_volume():{self._name}: Failure :-(.')
            return False

    def set_source(self, zone, source):
        """ Set source for a zone """

        # Source must be a two char field
        source = f'{int(source):02d}'
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_source():{self._name}: zone {zone}, change source to {source}.')
        send_msg = SET_NODE_SOURCE
        send_msg += zone.encode()
        send_msg += b' '
        send_msg += source.encode()
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_source():{self._name}: Bytes read: {rcv_msg}')
        if self._find_signature(rcv_msg, HAL_SUCCESS_MSG[SET_NODE_SOURCE]) != -1:
            self._source[int(zone)] = source
            self._easy_log(HAL_LOG_DEBUG,
                           f'set_source():{self._name}: Success!.')
            return True
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'set_source():{self._name}: Failure :-(.')
            return False

    def all_on_off(self, power):
        """ Turn all zones on or off
        Note that the all on function is not supported by the HAL CA1006, although it does support the all off.
        """

        self._easy_log(HAL_LOG_DEBUG,
                       f'all_on_off():{self._name}: Power {power}.')
        
        if power != '0':
            self._easy_log(HAL_LOG_WARNING,
                           f'all_on_off():{self._name}: Only supports all off.')
            return False
        
        send_msg = SET_SYSTEM_PWR_SAVE
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'all_on_off():{self._name}: Bytes read: {rcv_msg}')
        if self._find_signature(rcv_msg, HAL_SUCCESS_MSG[SET_SYSTEM_PWR_SAVE]) != -1:
            for i in range(1, HAL_ZONES+1):
                self._power[i] = power
            self._easy_log(HAL_LOG_DEBUG,
                           f'all_on_off():{self._name}: Success!.')
            return True
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'all_on_off():{self._name}: Failure :-(.')
            return False

    def set_mute(self, zone, mute):
        """ Switch mute on/off to a zone
        :param zone: The zone to be controlled [1-6]
        :param mute: 0 = off, 1 = on
        """
        mute_str = str(mute)
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_mute():{self._name}: Setting zone {zone} mute to {mute_str}')
        
        send_msg = SET_NODE_MUTE
        send_msg += zone.encode()
        send_msg += b' '
        send_msg += mute_str.encode()
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'set_mute():{self._name}: Bytes read: {rcv_msg}')
        if self._find_signature(rcv_msg, HAL_SUCCESS_MSG[SET_NODE_MUTE]) != -1:
            self._mute[int(zone)] = mute_str
            self._easy_log(HAL_LOG_DEBUG,
                           f'set_mute():{self._name}: Success!.')
            return True
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'set_mute():{self._name}: Failure :-(.')
            return False

    def _get_version(self):
        """ Get HAL CA1006 firmware version """

        self._easy_log(HAL_LOG_DEBUG,
                       f'_get_version():{self._name}.')
        send_msg = GET_VERSION
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'_get_version():{self._name}: Bytes read: {rcv_msg}')
        index = self._find_signature(rcv_msg, HAL_SUCCESS_MSG[GET_VERSION]) 
        if index != -1:
            self._easy_log(HAL_LOG_DEBUG,
                           f'_get_version():{self._name}: Success! Index {index}.')
            index +=len(HAL_SUCCESS_MSG[GET_VERSION])
            data = rcv_msg[index:].split(b'\n\r')
            if len(data) >= 1:
                ver_dt = data[0].split()
                self._version = ver_dt[0].decode()
            else:
                self._version = HAL_UNKNOWN
        else:
            self._version = HAL_UNKNOWN
            
    def get_version(self):
        """ Get HAL CA1006 firmware version """

        return self._version

    def _get_node_status(self, zone):
        """ Get node status for the zone """

        self._easy_log(HAL_LOG_DEBUG,
                       f'_get_node_status():{self._name}: zone {zone}.')
        send_msg = GET_NODE_STATUS
        send_msg += zone.encode()
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'_get_node_status():{self._name}: Bytes read: {rcv_msg}')
        index = self._find_signature(rcv_msg, HAL_SUCCESS_MSG[GET_NODE_STATUS]) 
        if index != -1:
            self._easy_log(HAL_LOG_DEBUG,
                           f'_get_node_status():{self._name}: Success! Index {index}.')
            status_msg = rcv_msg[index+len(HAL_SUCCESS_MSG[GET_NODE_STATUS]):]
            i = self._find_signature(status_msg, b'- ')
            j = self._find_signature(status_msg[i:], b'\n')
            status = status_msg[i+2:i+j].decode()
            self._easy_log(HAL_LOG_DEBUG,
                           f'_get_node_status():{self._name}: Status is {status}.')
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'_get_node_status():{self._name}: Failure :-(.')
            status = HAL_UNKNOWN
        
        self._node_status[int(zone)] = status
        return status

    def get_node_status(self, zone):
        """ Get node status for the zone """

        self._easy_log(HAL_LOG_DEBUG,
                       f'get_node_status():{self._name}: zone {zone}.')
        return self._node_status[int(zone)]

    def get_zone_info(self, zone):
        """ Get all relevant info for the zone """

        self._easy_log(HAL_LOG_DEBUG,
                       f'get_zone_info():{self._name}: zone {zone}.')
        send_msg = GET_RA_STATUS
        send_msg += zone.encode()
        send_msg += HAL_EOL

        rcv_msg = self._txrx(send_msg)
            
        self._easy_log(HAL_LOG_DEBUG,
                       f'get_zone_info():{self._name}: Bytes read: {rcv_msg}')
        index = self._find_signature(rcv_msg, HAL_SUCCESS_MSG[GET_RA_STATUS]) 
        if index != -1:
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Success! Index {index}.')
            index +=len(HAL_SUCCESS_MSG[GET_RA_STATUS])
            data = rcv_msg[index:index+14]
            split_data = data.split(b' ')
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Data ({data}).')
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Split data ({split_data}).')
            status = data[0:2]
            self._power[int(zone)] = status.decode()
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Status ({status}).')
            source = data[3:5]
            self._source[int(zone)] = source.decode()
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Source ({source}).')
            volume = data[6:8]
            self._volume[int(zone)] = volume.decode()
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Volume ({volume}).')
            video = data[9:11]
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Video ({video}).')
            mute = data[12:14]
            self._mute[int(zone)] = mute.decode()
            self._easy_log(HAL_LOG_DEBUG,
                           f'get_zone_info():{self._name}: Mute ({mute}).')
            return True
        else:
            self._easy_log(HAL_LOG_ERROR,
                           f'get_zone_info():{self._name}: Failure :-(.')
            return False

    def get_power(self, zone):
        """ Get power info for the zone """

        self._easy_log(HAL_LOG_DEBUG,
                       f'get_power():{self._name}: Power for zone {zone} '
                       f'is {self._power[int(zone)]}.')
        
        return self._power[int(zone)]

    def get_source(self, zone):
        """ Get source info for the zone """

        self._easy_log(HAL_LOG_DEBUG,
                       f'get_source():{self._name}: Source for zone {zone} '
                       f'is {self._source[int(zone)]}.')
        
        return self._source[int(zone)]

    def get_volume(self, zone):
        """ Get volume info [0..100] for the zone """

        self._easy_log(HAL_LOG_DEBUG,
                       f'get_volume():{self._name}: Volume for zone {zone} '
                       f'is {self._volume[int(zone)]}.')
        
        vol_pc = (int(self._volume[int(zone)]) * 100) // HAL_MAX_VOL
        return f'{vol_pc}'

    def get_mute(self, zone):
        """ Get mute info for the zone """

        self._easy_log(HAL_LOG_DEBUG,
                       f'get_mute():{self._name}: Mute for zone {zone} '
                       f'is {self._mute[int(zone)]}.')
        
        return self._mute[int(zone)]


# Testing stub
if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description =
                                     'Expose HAL CA1006 multi-zone amplifier')
    parser.add_argument('--log_level',
                        help='Set logging level. Defaults to error.',
                        choices=[HAL_LOG_DEBUG, HAL_LOG_INFO, HAL_LOG_WARNING, \
                                 HAL_LOG_ERROR, HAL_LOG_CRITICAL],
                        default=HAL_LOG_DEBUG)
    parser.add_argument('--hal_host', help =
                        'The hostname or IP address of the HAL CA1006. '
                        'Defaults to localhost.', default='localhost')
    parser.add_argument('--hal_port', help =
                        'The HAL CA1006 IP port. Defaults to 7000.',
                        type = int, default = 7000)
    args = parser.parse_args()

    # Establish logging
    logger = logging.getLogger(sys.argv[0])
    logger.setLevel(LOGGING_LEVEL[args.log_level])

    # create handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(LOGGING_LEVEL[args.log_level])

    # create formatter
    formatter = logging.Formatter('%(levelname)s: %(message)s')

    # add formatter to handler
    ch.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(ch)
    
    logger.info('Obtaining HAL client')
    hal = HALProtocol(args.hal_host, args.hal_port)
    logger.info('Enabling logger')
    hal.enable_logger(logger)
    s = hal.socket()
    logger.info(f'HAL socket is {s}.')
    
    while True:
        cmd = '0'
        print(f'Test commands:\n'
              f'0: Exit\t'
              f'1: Connect\t'
              f'2: Is connected?\n'
              f'3: Set Power\t'
              f'4: Set Volume\t'
              f'5: Set Source\t'
              f'6: All on/off\n'
              f'7: Toggle Mute\t'
              f'8: Get Zone Info\t'
              f'9: Get Power\n'
              f'10: Get Source\t'
              f'11: Get Volume\t'
              f'12: Get Mute\n'
              f'13: Set Echo\t'
              f'14: Get Version\t'
              f'15: Set Node Status\n'
              f'16: Get Node Status\t'
              f'17: Set Select Interval\t'
              f'18: Get Select Interval\n'
              f'20: Show all\t'
              f'21: Get all\n')
        cmd = input('Enter command you would like to test: ')
        if cmd == '1':
            logger.info('OK. Connecting..')
            hal.connect()
        elif cmd == '2':
            logger.info('OK. Checking if connected')
            if hal.is_connected():
                print(f'Yes, we are connected via socket {s}.\n')
            else:
                print(f'No, we are not connected.\n')
        elif cmd == '3':
            logger.info('Set Power Test')
            zone = input('Enter zone [1-6]: ')
            power = input('Enter Power mode 0=Off, 1=On: ')
            hal.set_power(zone, power)
        elif cmd == '4':
            logger.info('Set Volume Test')
            zone = input('Enter zone [1-6]: ')
            volume = input('Enter Volume [0-100]: ')
            hal.set_volume(zone, volume)
        elif cmd == '5':
            logger.info('Set Source Test')
            zone = input('Enter zone [1-6]: ')
            source = input('Enter Source [1-8]: ')
            hal.set_source(zone, source)
        elif cmd == '6':
            logger.info('All on/off test')
            power = input('Enter Power mode 0=Off, 1=On: ')
            hal.all_on_off(power)
        elif cmd == '7':
            logger.info('Toggle Mute test')
            zone = input('Enter zone [1-6]: ')
            hal.set_mute(zone)
        elif cmd == '8':
            logger.info('Get Zone Info Test')
            zone = input('Enter zone [1-6]: ')
            hal.get_zone_info(zone)
        elif cmd == '9':
            logger.info('Get Power Test')
            zone = input('Enter zone [1-6]: ')
            print(f'Zone {zone} power is {hal.get_power(zone)}.')
        elif cmd == '10':
            logger.info('Get Source Test')
            zone = input('Enter zone [1-6]: ')
            print(f'Zone {zone} source is {hal.get_source(zone)}.')
        elif cmd == '11':
            logger.info('Get Volume Test')
            zone = input('Enter zone [1-6]: ')
            print(f'Zone {zone} volume is {hal.get_volume(zone)}.')
        elif cmd == '12':
            logger.info('Get Mute Test')
            zone = input('Enter zone [1-6]: ')
            print(f'Zone {zone} mute is {hal.get_mute(zone)}.')
        elif cmd == '13':
            logger.info('Set Echo')
            echo = input('Enter echo [0,1]: ')
            hal._set_echo(echo)
        elif cmd == '14':
            logger.info('Get Version')
            version = hal.get_version()
            print(f'{version}')
        elif cmd == '15':
            logger.info('Set Node Status Test')
            zone = input('Enter zone [1-6]: ')
            power = input('Enter Power mode 0=Off, 1=On: ')
            source = input('Enter Source [1-8]: ')
            volume = input('Enter Volume [0-100]: ')
            mute = input('Enter Mute 0=Off, 1=On: ')
            hal.set_node_status(zone, power, source, volume, mute)
        elif cmd == '16':
            logger.info('Get Node Status Test')
            zone = input('Enter zone [1-6]: ')
            print(f'Zone {zone} status is {hal.get_node_status(zone)}')
        elif cmd == '17':
            logger.info('Set Select Interval')
            interval = input(f'Enter new interval > {HAL_SELECT_MIN_INTERVAL}:')
            hal.set_select_interval(interval)
        elif cmd == '18':
            logger.info('Get Select Interval')
            print(f'Select interval is {hal.get_select_interval()}s.')
        elif cmd == '20':
            logger.info('Show all')
            for i in range(1, HAL_ZONES+1):
                print(f'Zone {i} power is {hal._power[i]}, '
                      f'source is {hal._source[i]}, '
                      f'volume is {hal._volume[i]}, '
                      f'mute is {hal._mute[i]}.')
        elif cmd == '21':
            logger.info('Get all')
            hal._get_all_info()
        else:
            break
    
    hal.disconnect()
    
