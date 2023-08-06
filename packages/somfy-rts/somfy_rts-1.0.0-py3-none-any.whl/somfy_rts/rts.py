"""
This module provides support for the Somfy RS485 RTS Transmitter functions
"""
# Copyright (c) 2020 Brad Keifer
#
# This file is part of the Somfy RS485 RTS package.
# 
# The Somfy RS485 RTS package is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The Somfy RS485 RTS package  is distributed in the hope that it will be useful,
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
import logging
import logging.handlers
import argparse
import errno
import platform
import socket
import select
import sys
import time

if platform.system() == 'Windows':
    EAGAIN = errno.WSAEWOULDBLOCK
else:
    EAGAIN = errno.EAGAIN


# Somfy RTS Protocol Constants
GET_NODE_ADDR = 0x40           # Read NodeID / AppID
GET_GROUP_ADDR = 0x41          # Read NodeID of designated group (1 on 16)
GET_NODE_LABEL = 0x45          # Read Label of the node
GET_NODE_SERIAL_NUMBER = 0x4c  # Read Serial Number of the node
GET_NETWORK_ERROR_STAT = 0x4d  # Read error counter of the stack
GET_NETWORK_STAT = 0x4e        # Read network communication diagnosis
GET_NODE_STACK_VERSION = 0x70  # Read version of the stack
GET_NODE_APP_VERSION = 0x74    # Read version of the software

SET_GROUP_ADDR = 0x51          # Write NodeID of designated group (1 on 16)
SET_NODE_LABEL = 0x55          # Write Label of the node
SET_NETWORK_STAT = 0x5e        # Configure and reset diagnosis counters


POST_NODE_ADDR = 0x60           # Send NodeID / AppID ion network
POST_GROUP_ADDR = 0x61          # Send NodeID of designated group (1 on 16)
POST_NODE_LABEL = 0x65          # Send Label of the node
POST_NODE_SERIAL_NUMBER = 0x6c  # Send Serial Number of the node
POST_NETWORK_ERROR_STAT = 0x6d  # Send error counter of the stack
POST_NETWORK_STAT = 0x6e        # Send network communication diagnosis
POST_NODE_STACK_VERSION = 0x71  # Send version of the stack
POST_NODE_APP_VERSION = 0x75    # Send version of the software

NACK_FRAME = 0x6f               # Send acknowledgment with error code
ACK_FRAME = 0x7f                # Send acknowledgment

# RS485 RTS Transmitter Application-specific Messages
CTRL_POSITION = 0x80
CTRL_TILT = 0x81
CTRL_DIM = 0x82

SET_CHANNEL_MODE = 0x90
SET_TILT_FRAMECOUNT = 0x91
SET_DIM_FRAMECOUNT = 0x92
SET_SUN_AUTO = 0x93
SET_DCT_LOCK = 0x94
SET_CHANNEL = 0x97
SET_OPEN_PROG = 0x98
SET_IP = 0x9a

GET_CHANNEL_MODE = 0xa0
GET_TILT_FRAMECOUNT = 0xa1
GET_DIM_FRAMECOUNT = 0xa2
GET_DCT_LOCK = 0xa4

POST_CHANNEL_MODE = 0xb0
POST_TILT_FRAMECOUNT = 0xb1
POST_DIM_FRAMECOUNT = 0xb2
POST_DCT_LOCK = 0xb4

RTS_MSG = {
    GET_NODE_ADDR: 'GET_NODE_ADDR',
    GET_GROUP_ADDR: 'GET_GROUP_ADDR',
    GET_NODE_LABEL: 'GET_NODE_LABEL',
    GET_NODE_SERIAL_NUMBER: 'GET_NODE_SERIAL_NUMBER',
    GET_NETWORK_ERROR_STAT: 'GET_NETWORK_ERROR_STAT',
    GET_NETWORK_STAT: 'GET_NETWORK_STAT',
    GET_NODE_STACK_VERSION: 'GET_NODE_STACK_VERSION',
    GET_NODE_APP_VERSION: 'GET_NODE_APP_VERSION',
    SET_GROUP_ADDR: 'SET_GROUP_ADDR',
    SET_NODE_LABEL: 'SET_NODE_LABEL',
    SET_NETWORK_STAT: 'SET_NETWORK_STAT',
    POST_NODE_ADDR: 'POST_NODE_ADDR',
    POST_GROUP_ADDR: 'POST_GROUP_ADDR',
    POST_NODE_LABEL: 'POST_NODE_LABEL',
    POST_NODE_SERIAL_NUMBER: 'POST_NODE_SERIAL_NUMBER',
    POST_NETWORK_ERROR_STAT: 'POST_NETWORK_ERROR_STAT',
    POST_NETWORK_STAT: 'POST_NETWORK_STAT',
    POST_NODE_STACK_VERSION: 'POST_NODE_STACK_VERSION',
    POST_NODE_APP_VERSION: 'POST_NODE_APP_VERSION',
    NACK_FRAME: 'NACK_FRAME',
    ACK_FRAME: 'ACK_FRAME',
    # RS485 RTS Transmitter Application-specific Messages
    CTRL_POSITION: 'CTRL_POSITION',
    CTRL_TILT: 'CTRL_TILT',
    CTRL_DIM: 'CTRL_DIM',
    SET_CHANNEL_MODE: 'SET_CHANNEL_MODE',
    SET_TILT_FRAMECOUNT: 'SET_TILT_FRAMECOUNT',
    SET_DIM_FRAMECOUNT: 'SET_DIM_FRAMECOUNT', 
    SET_SUN_AUTO: 'SET_SUN_AUTO',
    SET_DCT_LOCK: 'SET_DCT_LOCK',
    SET_CHANNEL: 'SET_CHANNEL',
    SET_OPEN_PROG: 'SET_OPEN_PROG',
    SET_IP: 'SET_IP',
    GET_CHANNEL_MODE: 'GET_CHANNEL_MODE',
    GET_TILT_FRAMECOUNT: 'GET_TILT_FRAMECOUNT',
    GET_DIM_FRAMECOUNT: 'GET_DIM_FRAMECOUNT',
    GET_DCT_LOCK: 'GET_DCT_LOCK',
    POST_CHANNEL_MODE: 'POST_CHANNEL_MODE',
    POST_TILT_FRAMECOUNT: 'POST_TILT_FRAMECOUNT',
    POST_DIM_FRAMECOUNT: 'POST_DIM_FRAMECOUNT',
    POST_DCT_LOCK: 'POST_DCT_LOCK',
}

RTS_NODE_TYPE = 0x05    # Node type of the RS485 RTS Transmitter is always 0x05
MY_NODE_ID = 0xffff00   # Node ID of the 3rd party master (i.e. Me)
NACK_REQ = 0x00         # NACK = do not acknowledge request
ACK_REQ = 0x80          # ACK = acknowledge request

# Constants/defaults for this package
BROADCAST_ADDR = 0xffffff
RTS_ERR_NO_CONN = 1
RTS_MSG_INTERVAL = 1  # Seconds to wait between RF transmissions
MAX_MSG_ERRORS = 10   # Maximum errors tolerated before exiting
MAX_RECONNECTS = 5    # Maximum number of reconnect attempts after broken pipe
PING_PERIOD = 60      # Seconds between pings of the RS485 network

# Log levels
RTS_LOG_INFO = 'info'
RTS_LOG_WARNING = 'warning'
RTS_LOG_ERROR = 'error'
RTS_LOG_DEBUG = 'debug'
RTS_LOG_CRITICAL = 'critical'
LOGGING_LEVEL = {
    RTS_LOG_DEBUG: logging.DEBUG,
    RTS_LOG_INFO: logging.INFO,
    RTS_LOG_WARNING: logging.WARNING,
    RTS_LOG_ERROR: logging.ERROR,
    RTS_LOG_CRITICAL: logging.CRITICAL,
}


class RTSProtocol(object):
    """Somfy RS485 RTS Transmitter protocol class

    This is the main class for communication with a multi-drop network of Somfy
    RS485 RTS Transmitters.

    General usage flow:

    * Use connect() to connect to a RS485 network
    * Use enable_logger() to enable logging
    * Use disable_logger() to disable logging
    * Use get_nodes() to obtain a dictionary of all RTS Transmitter nodes
      on the RS485 network
    * Use control_position() to control the end device
    * Use disconnect() to disconnect from the RS485 network
    """
    
    UP = 0x01
    DOWN = 0x02
    STOP = 0x03
    MY = 0x04
        
    def __init__(self, connection="socket"):
        """connection defines the form of connection to the RTS Transmitter.
        Set connection to "serial" to use a serial connection.
        Set connection to "socket" to use a socket, which is the default.
        """
        
        if connection.lower() not in ('serial', 'socket'):
            raise ValueError(
                'connection must be "serial" or "socket", not %s' % connection)
        self._connection = connection.lower()
        if self._connection == "socket":
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._sock = None
        
        self._msg_errors = 0
        self._nodes_discovered = False
        self._nodes = {}
        self._node_addresses = []
        self._node_labels = []
        self._host = ""
        self._port = 4660
        self._logger = None
        self._last_tx_t = time.time()
        
    def _sock_recv(self, bufsize):
        for i in range(MAX_RECONNECTS):
            try:
                r, w, e = select.select([self._sock], [], [self._sock], 2.0)
                if self._sock in e:
                    self._easy_log(RTS_LOG_ERROR,
                                   f'_sock_recv(): Unexpected socket select error'
                                   f' with RTS Transmitter socket {self._sock}.')
                    self._sock.close()
                    sys.exit(1)
                
                if self._sock in r:
                    return self._sock.recv(bufsize)
                else:
                    # Timed out - node must be dead. Time to exit
                    self._easy_log(RTS_LOG_ERROR,
                                   f'_sock_recv(): Timed out waiting on read from '
                                   f'RTS Transmitter socket {self._sock}.')
                    self._sock.close()
                    sys.exit(1)
            except ConnectionError as err:
                self._easy_log(RTS_LOG_ERROR,
                               f'Connection Error ({err.errno}) on recv. '
                               f'Reconnect attempt {i+1}.')
                self._reconnect()
            except:
                self._easy_log(RTS_LOG_ERROR,f'Unexpected Error on recv.')
                raise
            
        self._easy_log(RTS_LOG_ERROR,
                       f'_sock_recv exceeded MAX_RECONNECTS ({MAX_RECONNECTS})')
        self._sock.close()
        sys.exit(1)

    def _sock_send(self, buf):
        for i in range(MAX_RECONNECTS):
            now = time.time()
            inter_tx_time = now - self._last_tx_t
            self._easy_log(RTS_LOG_DEBUG,
                           f'_sock_send(): _last_tx_t = {self._last_tx_t}, '
                           f'now = {now}, inter_tx_time = {inter_tx_time}.')
            if inter_tx_time < RTS_MSG_INTERVAL:
                self._easy_log(RTS_LOG_DEBUG,
                               f'Short inter-transmission time ({inter_tx_time} s).')
                self._easy_log(RTS_LOG_DEBUG,
                               f'Sleeping for {RTS_MSG_INTERVAL - inter_tx_time} s.')
                time.sleep(RTS_MSG_INTERVAL - inter_tx_time)
                
            self._easy_log(RTS_LOG_DEBUG,
                           f'_sock_send(): Sending {buf}')
            self._last_tx_t = time.time()
            try:
                return self._sock.sendall(buf)
            except ConnectionError as err:
                self._easy_log(RTS_LOG_ERROR,
                               f'Connection Error ({err.errno}) on send. '
                               f'Reconnect attempt {i+1}.')
                self._reconnect()
            except:
                self._easy_log(RTS_LOG_ERROR,f'Unexpected Error on send.')
                raise
                
        self._easy_log(RTS_LOG_ERROR,
                       f'_sock_send exceeded MAX_RECONNECTS ({MAX_RECONNECTS})')
        self._sock.close()
        sys.exit(1)


    def _reconnect(self):
        if self._sock is None or self._connection != "socket":
            return RTS_ERR_NO_CONN
        
        self.disconnect()
        
        if self._connection == "socket":
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._sock = None
        
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE,
                              self._keepalive)
        c = self._sock.connect((self._host, self._port))
        self._flush_input_buffer()
        return c
        
        

    def _flush_input_buffer(self):
        input_flushed = False
        while not input_flushed:
            ready_to_read, ready_to_write, in_error = \
                           select.select([self._sock], [], [self._sock], 2.0)
            if len(in_error) != 0:
                self._easy_log(RTS_LOG_ERROR,
                               'Unexpected socket select error with RTS Transmitter socket.')
                self._sock.close()
                sys.exit(1)
            
            if len(ready_to_read) > 0:
                reply_msg = self._sock_recv(1024)    
                self._easy_log(RTS_LOG_DEBUG,
                               'Flush initial data: ' + str(reply_msg))
                self._easy_log(RTS_LOG_DEBUG,
                               'Initial data length = %d bytes ', len(reply_msg))
                if not reply_msg:
                    self._easy_log(RTS_LOG_ERROR, 'Error reading data after socket connect.')
                    self._sock.close()
                    sys.exit(1)
            else:
                # No more input data to be flushed
                input_flushed = True
                
    def _get_node_addresses(self):
        """Discover all RTS Transmitters on the RS485 network.
        
        
        Returns a list of node addresses
        """
        
        # Return existing list of already known.
        if len(self._node_addresses) > 0:
            return self._node_addresses
        else:
            self._node_addresses = []
            
        frame = self._frame_encode(BROADCAST_ADDR, GET_NODE_ADDR, NACK_REQ)
        self._sock_send(frame)
        
        # Since we have issued a broadcast, we should receive a POST_NODE_ADDR from
        # each active node on the RS485 network
        reply_buf = b''
        input_flushed = False
        while not input_flushed:
            ready_to_read, ready_to_write, in_error = \
                           select.select([self._sock], [], [self._sock], 2.0)
            if len(in_error) != 0:
                self._easy_log(RTS_LOG_ERROR,
                               'Unexpected socket select error with RTS Transmitter'
                               ' socket.')
                self._sock.close()
                sys.exit(1)
            
            if len(ready_to_read) > 0:
                reply_buf += self._sock_recv(1024)    
                self._easy_log(RTS_LOG_DEBUG,
                               'GET_NODE_ADDR  reply: ' + str(reply_buf))
                self._easy_log(RTS_LOG_DEBUG,
                               'GET_NODE_ADDR  reply length = %d bytes ',
                               len(reply_buf))
                if not reply_buf:
                    self._easy_log(RTS_LOG_ERROR,
                                   'GET_NODE_ADDR : Error reading data.')
                    self._sock.close()
                    sys.exit(1)
            else:
                # No more input data to be flushed
                input_flushed = True
                if reply_buf == b'':
                    # No nodes available on this socket. Time to exit.
                    self._easy_log(RTS_LOG_ERROR,
                                   'GET_NODE_ADDR : No RTS Transmitters online.')
                    self._sock.close()
                    sys.exit(1)
                    
            
        if (len(reply_buf) % 11):
            self._easy_log(RTS_LOG_ERROR,
                           'Invalid frame data received: ' + str(reply_buf))
            self._sock.close()
            sys.exit(1)
        
        frame_count = len(reply_buf) // 11
        reply_list = []
        node_addresses = []
        for i in range(frame_count):
            reply_list.append(reply_buf[i*11:(i+1)*11])
            self._easy_log(RTS_LOG_DEBUG,
                           f'GET_NODE_ADDR  actual reply[{i}]: {reply_list[i]}')

            # Now decode the reply_list[i] from "actual" format to "raw"
            reply_frame = reply_list[i]
            checksum = 0
            raw_frame = b''
            for j in range(9):
                checksum += reply_frame[j]
                raw_frame += (0xff ^ reply_frame[j]).to_bytes(1, byteorder='big')
                
            expected_checksum = (0xffff & checksum).to_bytes(2, byteorder='big')
            received_checksum = reply_frame[-2:]
            self._easy_log(RTS_LOG_DEBUG,
                           'Checksum received is %s and the expected checksum is %s',
                           str(received_checksum), str(expected_checksum))
            
            if expected_checksum != received_checksum:
                self._easy_log(RTS_LOG_ERROR,
                               'Checksum received is %s and the expected checksum is %s',
                               str(received_checksum), str(expected_checksum))
                self._msg_error_handler()
                return None

            self._easy_log(RTS_LOG_DEBUG,
                           f'GET_NODE_ADDR     raw reply[{i}]: {raw_frame}')

            if raw_frame[0] != POST_NODE_ADDR:
                self._easy_log(RTS_LOG_ERROR,
                               f'GET_NODE_ADDR reply format invalid. '
                               f'MSG byte should be POST_NODE_ADDR '
                               f'but is {RTS_MSG[raw_frame[0]]}.')
                self._msg_error_handler()
                return None

            # Extract the node address
            node_address = int.from_bytes(raw_frame[3:6], byteorder='little')
            self._easy_log(RTS_LOG_DEBUG,
                           f'GET_NODE_ADDR address is 0x{node_address:06x}.')
            node_addresses.append(node_address)
            self._node_addresses.append(node_address)
            
        return node_addresses

    def _discover_nodes(self):
        """Discover details of devices on RS485 Network"""
        
        self._easy_log(RTS_LOG_DEBUG,
                       f'_discover_nodes(): Function called.')
        if self._nodes_discovered:
            self._easy_log(RTS_LOG_WARNING,
                           '_discover_nodes() called more than once. Rediscovering..')
            self._nodes_discovered = False
            self._node_labels = []
            self._node_addresses = []
            self._nodes = {}
        
        self._get_node_addresses()
        self._easy_log(RTS_LOG_DEBUG,
                       f'_discover_nodes(): Node addresses are {self._node_addresses}')
        for i in range(len(self._node_addresses)):
            self._node_labels.append(self.get_node_label(self._node_addresses[i]))
            self._nodes[self._node_addresses[i]] = self._node_labels[i]
        
        self._nodes_discovered = True
        return self._nodes_discovered
            

    def _get_node_labels(self):
        """Return a list of node labels

        If they aren't already known, then they will be discovered.
        """
        if not self._nodes_discovered:
            self._easy_log(RTS_LOG_DEBUG,
                           '_get_node_labels(): Nodes not yet discovered')
            self._discover_nodes()
        else:
            self._easy_log(RTS_LOG_DEBUG,
                           '_get_node_labels(): Nodes are discovered')
            
        self._easy_log(RTS_LOG_DEBUG,
                       f'_get_node_labels(): Nodes are {self._node_labels}')
        return self._node_labels
        
    def get_node_label(self, node_addr):
        """Return the node label"""
        
        self._easy_log(RTS_LOG_DEBUG,
                       f'get_node_label(): Function called with '
                       f'node_addr 0x{node_addr:06x}')
        
        frame = self._frame_encode(node_addr, GET_NODE_LABEL, NACK_REQ)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_NODE_LABEL:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_NODE_LABEL reply format invalid. '
                           f'MSG byte should be POST_NODE_LABEL '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the node label
        node_label = raw_frame[9:25].rstrip().decode(errors='ignore')
        self._easy_log(RTS_LOG_DEBUG, f'GET_NODE_LABEL is {node_label}.')
        return node_label

    def _easy_log(self, level, fmt, *args):
        if self._logger is not None:
            level_std = LOGGING_LEVEL[level]
            self._logger.log(level_std, fmt, *args)

    def _frame_encode(self, node_addr, command, acknack, data=b''):
        """Raw frame encoder. Returns a frame ready for transmission"""
        
        frame_len = 11 + len(data)
        if data.isascii():
            self._easy_log(RTS_LOG_DEBUG,
                           f'_frame_encode(): Encoding data ({str(data)}) '
                           f'with command ({RTS_MSG[command]})')
        else:
            self._easy_log(RTS_LOG_DEBUG,
                           f'_frame_encode(): Encoding data ({data}) '
                           f'with command ({RTS_MSG[command]})')
                
        #Build the formatted frame
        # Byte 1: MSG
        frame = (0xff ^ command).to_bytes(1, byteorder='little')

        # Byte 2: ACK/LEN
        frame += (0xff ^ (acknack | frame_len)).to_bytes(1, byteorder='little')

        # Byte 3: Node Type
        frame += (0xff ^ RTS_NODE_TYPE).to_bytes(1, byteorder='little')

        # Byte 4-6: Source NodeID. Least significant byte first
        frame += (0xffffff ^ MY_NODE_ID).to_bytes(3, byteorder='little')

        # Byte 7-9: Destination NodeID, Least significant byte first.
        # We will do a broadcast (ff:ff:ff), as we don't yet know
        # the NodeID of the receiver
        frame += (0xffffff ^ node_addr).to_bytes(3, byteorder='little')
        
        # Byte 10+: Data
        for i in range(len(data)):
            frame += (0xff ^ data[i]).to_bytes(1, byteorder='little')
        
        # Byte (n-1)-n: Checksum.
        # Calculated as the lower two bytes of the sum of the raw message bytes
        # But, just make things interesting, the checksum is transmitted
        # Most Significant Byte First (MSBF)
        checksum = 0
        for i in range(len(frame)):
            checksum += frame[i]

        self._easy_log(RTS_LOG_DEBUG, 'Checksum is 0x{:04x}'.format(checksum))
        frame += (0xffff & checksum).to_bytes(2, byteorder='big')
        self._easy_log(RTS_LOG_DEBUG, f'_frame_encode() result: {frame}')
        
        return frame
    
    def _msg_error_handler(self):
        """Generic handler when messages received from RTS Transmitter are in error."""
        self._msg_errors += 1
        if self._msg_errors >= MAX_MSG_ERRORS:
            self._sock.close()
            sys.exit(1)
            
        return None
    
    def _frame_read(self):
        """Read a frame from the RS485 network and return the complete message frame."""
        reply_frame = b''
        while len(reply_frame) < 2:        
            reply_frame += self._sock_recv(1024)    
            self._easy_log(RTS_LOG_DEBUG,
                           f'_frame_read() reply: {reply_frame}')
            self._easy_log(RTS_LOG_DEBUG,
                           f'_frame_read() reply length = {len(reply_frame)} bytes.')
            if not reply_frame:
                self._easy_log(RTS_LOG_ERROR, f'_frame_read() error reading data. '
                               f'reply_frame = {reply_frame}')
                self._msg_error_handler()
        
        # Byte 1 contains the MSG identifier
        msg_id = (0xff ^ reply_frame[0])
        if msg_id in RTS_MSG:
            msg_name = RTS_MSG[msg_id]
        else:
            self._easy_log(RTS_LOG_ERROR,
                           f'_frame_read(): MSG id (0x{msg_id:02x}) not known.')
            self._sock.close()
            sys.exit(1)            
        
        # Byte 2 contains the ACK/LEN information. LEN is in bits b4-b0    
        frame_len = (0xff ^ reply_frame[1]) & 0x1f

        while len(reply_frame) < frame_len:
            self._easy_log(RTS_LOG_DEBUG, f'Did not get full {msg_name} reply '
                           f'on first read attempt, so keep reading till we do')
            reply_frame += self._sock_recv(1024)

        self._easy_log(RTS_LOG_DEBUG,
                       f'{msg_name} actual reply: {reply_frame}')

        # Now decode the reply_frame from "actual" format to "raw"
        checksum = 0
        raw_frame = b''
        for i in range(frame_len-2):
            checksum += reply_frame[i]
            raw_frame += (0xff ^ reply_frame[i]).to_bytes(1, byteorder='big')
            
        expected_checksum = (0xffff & checksum).to_bytes(2, byteorder='big')
        received_checksum = reply_frame[-2:]
        self._easy_log(RTS_LOG_DEBUG,
                       'Checksum received is %s and the expected checksum is %s',
                       str(received_checksum), str(expected_checksum))
        
        if expected_checksum != received_checksum:
            self._easy_log(RTS_LOG_ERROR,
                           'Checksum received is %s and the expected checksum is %s',
                           str(received_checksum), str(expected_checksum))
            self._msg_error_handler()
            return None

        self._easy_log(RTS_LOG_DEBUG,
                       f'{msg_name}    raw reply: {raw_frame}')

        return raw_frame


    def control_position(self, node_addr, command, channel=int):
        """Issue a control position command"""
                
        # Byte 10: Data byte 1: Channel Number. min=0, max=15
        if channel < 0 or channel > 15:
                self._easy_log(RTS_LOG_ERROR,
                               f'control_position(): Channel ({channel}) not in range [0-15].')
                self._msg_error_handler()
                return False
            
        data = channel.to_bytes(1, byteorder='little')
        
        # Byte 11: Data byte 2: Command (UP/DOWN/STOP/MY)
        if command not in (self.UP, self.DOWN, self.STOP, self.MY):
                self._easy_log(RTS_LOG_ERROR,
                               f'control_position(): Command (0x{command:02x}) not in '
                               f'UP (0x{self.UP:02x}), '
                               f'DOWN (0x{self.DOWN:02x}), '
                               f'STOP (0x{self.STOP:02x}), '
                               f'MY (0x{self.MY:02x}).')
                self._msg_error_handler()
                return False
            
        data += command.to_bytes(1, byteorder='little')

        frame = self._frame_encode(node_addr, CTRL_POSITION, ACK_REQ, data)
        self._sock_send(frame)
        raw_frame = self._frame_read()
                
        if raw_frame[0] == ACK_FRAME:
            self._easy_log(RTS_LOG_DEBUG, f'CTRL_POSITION ACK_FRAME success.')
            success = True
        elif raw_frame[0] == NACK_FRAME:
            if raw_frame[9] == 0x00:
                self._easy_log(RTS_LOG_DEBUG,
                               f'CTRL_POSITION NACK_FRAME success.')
                success = True
            elif raw_frame[9] == 0x01:
                self._easy_log(RTS_LOG_ERROR,
                               f'CTRL_POSITION NACK_FRAME failure: Data ({data}) out of range.')
                self._msg_error_handler()
                success = False
            elif raw_frame[9] == 0x10:
                self._easy_log(RTS_LOG_ERROR,
                               f'CTRL_POSITION NACK_FRAME failure: Unknown message.')
                self._msg_error_handler()
                success = False
            elif raw_frame[9] == 0x11:
                self._easy_log(RTS_LOG_ERROR,
                               f'CTRL_POSITION NACK_FRAME failure: Message Length Error.')
                self._msg_error_handler()
                success = False
            elif raw_frame[9] == 0xff:
                self._easy_log(RTS_LOG_ERROR,
                               f'CTRL_POSITION NACK_FRAME failure: Busy - '
                               f'Cannot process message.')
                self._msg_error_handler()
                success = False
            else:
                self._easy_log(RTS_LOG_ERROR,
                               f'CTRL_POSITION NACK_FRAME failure: Status data '
                               f'0x{raw_frame[9]:02x} invalid.')
                self._msg_error_handler()
                success = False

        else:
            self._easy_log(RTS_LOG_ERROR,
                           f'CTRL_POSITION reply format invalid. '
                           f'MSG byte should be ACK or NACK '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            success = False

        return success

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

    def connect(self, host, port=4660, keepalive=PING_PERIOD):
        """Connect to a RTS Transmitter network

        host is the hostname or IP address of the ethernet to serial converter
        port is the network port of the ethernet to serial converter to connect to.
        Defaults to 4660.
        keepalive: Maximum period in seconds between communications with the
        RTS Transmitter. If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the RTS Transmitter.
        """

        if host is None or len(host) == 0:
            raise ValueError('Invalid host.')
        if port <= 0:
            raise ValueError('Invalid port number.')
        if keepalive < 0:
            raise ValueError('Keepalive must be >=0.')
        
        self._msg_errors = 0
        self._host = host
        self._port = port
        self._keepalive = keepalive
        self._easy_log(RTS_LOG_DEBUG,
                       f'Attempting socket connection to host {host}, '
                       f'port {port} with keepalive {keepalive}s.')
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE,
                              keepalive)
        c = self._sock.connect((host, port))
        self._flush_input_buffer()
        self._discover_nodes()
        return c

    def disconnect(self):
        if self._sock is None:
            return RTS_ERR_NO_CONN

        return self._sock.close()
        
    def socket(self):
        """Return the socket for this client."""
        return self._sock

    def ping(self):
        """Ping each node on the RS485 network."""
        self._easy_log(RTS_LOG_DEBUG,
                       f'ping(): Pinging node addresses {self._node_addresses}')
        for node_addr in self._node_addresses:
            self._easy_log(RTS_LOG_INFO,
                           f'ping(): Pinging node address 0x{node_addr:06x}')            
            self.get_network_stat(node_addr)
        
        return True

    def loop_misc(self):
        """Handles general ongoing housekeeping duties for the RTS connections.

        At this stage, the only housekeeping task is to ping() the nodes of the
        socket on a regular basis
        """
        if time.time() - self._last_tx_t >= self._keepalive:
            self._easy_log(RTS_LOG_DEBUG,
                           f'loop_misc(): Time for a ping!')
            self.ping()
    
        return None

    def get_nodes(self):
        """Returns a dictionary of all RTS nodes on the RS485 Network
        
        They will be discovered if not already known. The dictionary will contain
        node_address as the key, and node_label as the value.
        """
        
        if not self._nodes_discovered:
            self._discover_nodes()
        return self._nodes
            
    def get_node_stack_version(self, node_addr):
        """Returns a tuple containing the protocol software information.
        
        The tuple structure is:
        Stack Reference: 24-bit number
        Stack Index Letter: 8-bit ASCII character
        Stack Index Number: 8-bit number
        Stack Standard: 8-bit number
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_node_stack_version(): Function called with '
                       f'node_address 0x{node_addr:06x}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            raise ValueError(f'Invalid node 0x{node_addr:06x}.')
            
        frame = self._frame_encode(node_addr, GET_NODE_STACK_VERSION, NACK_REQ)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_NODE_STACK_VERSION:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_NODE_STACK_VERSION reply format invalid. '
                           f'MSG byte should be POST_NODE_STACK_VERSION '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the stack version info and pack into a tuple
        stack_reference = int.from_bytes(raw_frame[9:12], byteorder='little')
        stack_index_letter = raw_frame[12:13].decode()
        stack_index_number = int.from_bytes(raw_frame[13:14], byteorder='little')
        stack_standard = int.from_bytes(raw_frame[14:15], byteorder='little')
        stack_version = stack_reference, \
                        stack_index_letter, \
                        stack_index_number, \
                        stack_standard
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_STACK_VERSION stack reference is '
                       f'{stack_reference}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_STACK_VERSION stack index letter is '
                       f'{stack_index_letter}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_STACK_VERSION stack index number is '
                       f'{stack_index_number}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_STACK_VERSION stack standard is '
                       f'{stack_standard}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_STACK_VERSION is {stack_version}.')
        return stack_version

    def get_node_serial_number(self, node_addr):
        """Returns the serial number as a 12-byte ASCII string.
        
        The serial number structure is:
        Product NodeID: Six characters in hexadecimal representation
        Manufacturer ID: Two letters
        Year: Two digits
        Week: Julian Week
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_node_serial_number(): Function called with '
                       f'node_address 0x{node_addr:06x}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            raise ValueError(f'Invalid node 0x{node_addr:06x}.')
            
        frame = self._frame_encode(node_addr, GET_NODE_SERIAL_NUMBER, NACK_REQ)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_NODE_SERIAL_NUMBER:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_NODE_SERIAL_NUMBER reply format invalid. '
                           f'MSG byte should be POST_NODE_SERIAL_NUMBER '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the serial number
        serial_number = raw_frame[9:21].decode()
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_SERIAL_NUMBER serial number is '
                       f'{serial_number}.')
        return serial_number

    def get_node_app_version(self, node_addr):
        """Returns a tuple containing the application software information.
        
        The tuple structure is:
        App Reference: 24-bit number
        App Index Letter: 8-bit ASCII character
        App Index Number: 8-bit number
        App Profile: 8-bit number
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_node_app_version(): Function called with '
                       f'node_address 0x{node_addr:06x}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            raise ValueError(f'Invalid node 0x{node_addr:06x}.')
            
        frame = self._frame_encode(node_addr, GET_NODE_APP_VERSION, NACK_REQ)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_NODE_APP_VERSION:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_NODE_APP_VERSION reply format invalid. '
                           f'MSG byte should be POST_NODE_APP_VERSION '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the app version info and pack into a tuple
        app_reference = int.from_bytes(raw_frame[9:12], byteorder='little')
        app_index_letter = raw_frame[12:13].decode()
        app_index_number = int.from_bytes(raw_frame[13:14], byteorder='little')
        app_standard = int.from_bytes(raw_frame[14:15], byteorder='little')
        app_version = app_reference, \
                        app_index_letter, \
                        app_index_number, \
                        app_standard
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_APP_VERSION app reference is '
                       f'{app_reference}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_APP_VERSION app index letter is '
                       f'{app_index_letter}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_APP_VERSION app index number is '
                       f'{app_index_number}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_APP_VERSION app standard is '
                       f'{app_standard}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NODE_APP_VERSION is {app_version}.')
        return app_version
        
    def set_node_label(self, node_addr, label):
        """Set the user-defined text label for the node.
        
        The node address and new label must be supplied as arguments.
        The function will return True for success and False for failure.
        """
        
        self._easy_log(RTS_LOG_DEBUG,
                       f'set_node_label(): Function called with '
                       f'node_addr 0x{node_addr:x}, label "{label}"')
        
        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            self._easy_log(RTS_LOG_ERROR,
                           f'Invalid node 0x{node_addr:06x}.')
            return False
        
        label_buf = str(label).encode()
        if not label_buf.isascii():
            self._easy_log(RTS_LOG_ERROR,
                           f'Invalid label "{label}". Must be ASCII.')
            return False
        
        if len(label_buf) > 16:
            self._easy_log(RTS_LOG_ERROR,
                           f'Label "{label}" too long. Maximum of 16 characters.')
            return False
        
        if not str(label).isalnum():
            self._easy_log(RTS_LOG_WARNING,
                           f'set_node_label(): Label "{label}" is not alphanumeric.')


        # Pad label with spaces (0x20) values up to full label data length of 16 bytes
        pad_len = 16 - len(label_buf)
        for i in range(pad_len):
            label_buf += (0x20).to_bytes(1, byteorder='little')


        frame = self._frame_encode(node_addr, SET_NODE_LABEL, ACK_REQ, label_buf)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame == None:
            self._easy_log(RTS_LOG_ERROR, 'SET_NODE_LABEL fatal error')
            self._sock.close()
            sys.exit(1)


        if raw_frame[0] == ACK_FRAME:
            self._easy_log(RTS_LOG_DEBUG, 'SET_NODE_LABEL ACK_FRAME success.')
            success = True
        elif raw_frame[0] == NACK_FRAME:
            if raw_frame[9] == 0x00:
                self._easy_log(RTS_LOG_DEBUG, 'SET_NODE_LABEL NACK_FRAME success.')
                success = True
            elif raw_frame[9] == 0x01:
                self._easy_log(RTS_LOG_ERROR, 'SET_NODE_LABEL NACK_FRAME failure: Data out of range.')
                self._msg_error_handler()
                success = False
            elif raw_frame[9] == 0x10:
                self._easy_log(RTS_LOG_ERROR, 'SET_NODE_LABEL NACK_FRAME failure: Unknown message.')
                self._msg_error_handler()
                success = False
            elif raw_frame[9] == 0x11:
                self._easy_log(RTS_LOG_ERROR, 'SET_NODE_LABEL NACK_FRAME failure: Message Length Error.')
                self._msg_error_handler()
                success = False
            elif raw_frame[9] == 0xff:
                self._easy_log(RTS_LOG_ERROR, 'SET_NODE_LABEL NACK_FRAME failure: Busy - Cannot process message.')
                self._msg_error_handler()
                success = False
            else:
                self._easy_log(RTS_LOG_ERROR, 'SET_NODE_LABEL NACK_FRAME failure: Status data (0x%x) invalid.',
                             raw_frame[9])
                self._msg_error_handler()
                success = False

        else:
            self._easy_log(RTS_LOG_ERROR,
                           f'SET_NODE_LABEL reply format invalid. '
                           f'MSG byte should be ACK_FRAME or NACK_FRAME '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            success = False

        return success

    def get_network_stat(self, node_addr):
        """Returns the network communication diagnostics.
        
        Encoding structure of the data frame is unknown due to inability to find
        documentation.
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_network_stat(): Function called with '
                       f'node_address 0x{node_addr:06x}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            raise ValueError(f'Invalid node 0x{node_addr:06x}.')
            
        frame = self._frame_encode(node_addr, GET_NETWORK_STAT, NACK_REQ)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_NETWORK_STAT:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_NETWORK_STAT reply format invalid. '
                           f'MSG byte should be POST_NETWORK_STAT '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the diagnostics data
        # Waiting feedback from somfy technical support as to data format
        data = raw_frame[9:len(raw_frame)-2]
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NETWORK_STAT diagnostics data is '
                       f'{data}.')
        return data

    def get_network_error_stat(self, node_addr):
        """Returns the error counter of the stack.
        
        Encoding structure of the data frame is unknown due to inability to find
        documentation.
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_network_error_stat(): Function called with '
                       f'node_address 0x{node_addr:06x}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            raise ValueError(f'Invalid node 0x{node_addr:06x}.')

        frame = self._frame_encode(node_addr, GET_NETWORK_ERROR_STAT, NACK_REQ)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_NETWORK_ERROR_STAT:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_NETWORK_ERROR_STAT reply format invalid. '
                           f'MSG byte should be POST_NETWORK_ERROR_STAT '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the error counter data - format is unknown.
        # Waiting feedback from somfy technical support as to data format
        data = raw_frame[9:len(raw_frame)-2]
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_NETWORK_ERROR_STAT data frame is '
                       f'{data}.')
        return data

    def get_channel_mode(self, node_addr, channel=int):
        """Returns the mode used for the selected channel as a tuple.
        
        The mode information is:
        US/CE mode: 0x00 = CE Mode, 0x01 = US Mode (default)
        Rolling/Tilting mode: 0x00 = Rolling mode (default), 0x01 = Tilting mode
        Modulis mode: 0x00 = Normal mode, 0x01 = Modulis mode (default)
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_channel_mode(): Function called for '
                       f'node_address 0x{node_addr:06x}, '
                       f'channel {channel}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            self._easy_log(RTS_LOG_ERROR, f'Invalid node 0x{node_addr:06x}.')
            return None
        
        if channel < 0 or channel > 15:
            self._easy_log(RTS_LOG_ERROR,
                           f'Invalid channel ({channel}). Must be between 0 and 15.')
            return None
        
        data_frame = channel.to_bytes(1, byteorder='little')
        frame = self._frame_encode(node_addr, GET_CHANNEL_MODE, NACK_REQ, data_frame)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_CHANNEL_MODE:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_CHANNEL_MODE reply format invalid. '
                           f'MSG byte should be POST_CHANNEL_MODE '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the channel mode information and pack into a tuple
        channel_number = raw_frame[9]
        us_ce_mode = raw_frame[10]
        rolling_tilting_mode = raw_frame[11]
        modulis_mode = raw_frame[12]
        
        if channel_number != channel:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_CHANNEL_MODE received info for channel {channel_number}'
                           f', but was seeking it for channel {channel}')
            return None
            
        channel_mode = us_ce_mode, rolling_tilting_mode, modulis_mode
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_CHANNEL_MODE US/CE Mode is '
                       f'{us_ce_mode}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_CHANNEL_MODE Rolling/Tilting Mode is '
                       f'{rolling_tilting_mode}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_CHANNEL_MODE Modulis Mode is '
                       f'{modulis_mode}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_CHANNEL_MODE for channel {channel} is '
                       f'{channel_mode}.')
        return channel_mode

    def get_tilt_framecount(self, node_addr, channel=int):
        """Returns the number of RTS frames the product should send on a CTRL_TILT order.
        
        The information is returned as a tuple consisting of two values:
        US mode: The number of frames to send for US mode. Range is 4-255. Default is 5.
        CE mode: The number of frames to send for CE mode. Range is 2-13. Default is 2.
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_tilt_framecount(): Function called for '
                       f'node_address 0x{node_addr:06x}, '
                       f'channel {channel}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            self._easy_log(RTS_LOG_ERROR, f'Invalid node 0x{node_addr:06x}.')
            return None
        
        if channel < 0 or channel > 15:
            self._easy_log(RTS_LOG_ERROR,
                           f'Invalid channel ({channel}). Must be between 0 and 15.')
            return None
               
        data_frame = channel.to_bytes(1, byteorder='little')
        frame = self._frame_encode(node_addr, GET_TILT_FRAMECOUNT, NACK_REQ, data_frame)
        self._sock_send(frame)
        raw_frame = self._frame_read()

        if raw_frame[0] != POST_TILT_FRAMECOUNT:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_TILT_FRAMECOUNT reply format invalid. '
                           f'MSG byte should be POST_TILT_FRAMECOUNT '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the channel mode information and pack into a tuple
        channel_number = raw_frame[9]
        us_frames = raw_frame[10]
        ce_frames = raw_frame[11]
        
        if channel_number != channel:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_TILT_FRAMECOUNT received info for channel {channel_number}'
                           f', but was seeking it for channel {channel}')
            return None
            
        tilt_framecount = us_frames, ce_frames
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_TILT_FRAMECOUNT number of frames to send for US mode is '
                       f'{us_frames}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_TILT_FRAMECOUNT number of frames to send for CE mode is '
                       f'{ce_frames}.')
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_TILT_FRAMECOUNT for channel {channel} is '
                       f'{tilt_framecount}.')
        return tilt_framecount

    def get_dim_framecount(self, node_addr, channel=int):
        """Returns the number of RTS frames the product should send on a CTRL_DIM order.
        
        The information is returned as an integer.
        Minimum value is 4, maximum is 255, default is 5.
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_dim_framecount(): Function called for '
                       f'node_address 0x{node_addr:06x}, '
                       f'channel {channel}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            self._easy_log(RTS_LOG_ERROR, f'Invalid node 0x{node_addr:06x}.')
            return None
        
        if channel < 0 or channel > 15:
            self._easy_log(RTS_LOG_ERROR,
                           f'Invalid channel ({channel}). Must be between 0 and 15.')
            return None
        
        data_frame = channel.to_bytes(1, byteorder='little')
        frame = self._frame_encode(node_addr, GET_DIM_FRAMECOUNT, NACK_REQ, data_frame)
        self._sock_send(frame)
        raw_frame = self._frame_read()

        if raw_frame[0] != POST_DIM_FRAMECOUNT:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_DIM_FRAMECOUNT reply format invalid. '
                           f'MSG byte should be POST_DIM_FRAMECOUNT '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the channel mode information and pack into a tuple
        channel_number = raw_frame[9]
        dim_framecount = raw_frame[10]
        
        if channel_number != channel:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_DIM_FRAMECOUNT received info for channel {channel_number}'
                           f', but was seeking it for channel {channel}')
            return None
            
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_DIM_FRAMECOUNT for channel {channel_number} is '
                       f'{dim_framecount}.')
        return dim_framecount

    def get_dct_lock(self, node_addr):
        """Get the lock status of the Dry Contacts (DCT) for the node as tuple.
        
        A value of 0 indicates Unlocked.
        A value of 1 indicates Locked.
        Format of tuple is (DCT1, DCT2, DCT3, DCT4, DCT5)
        """

        self._easy_log(RTS_LOG_DEBUG,
                       f'get_dct_lock(): Function called with '
                       f'node_address 0x{node_addr:06x}')

        if not self._nodes_discovered:
            self._discover_nodes()
            
        if not node_addr in self._node_addresses:
            raise ValueError(f'Invalid node 0x{node_addr:06x}.')
            
        frame = self._frame_encode(node_addr, GET_DCT_LOCK, NACK_REQ)
        self._sock_send(frame)
        raw_frame = self._frame_read()
        
        if raw_frame[0] != POST_DCT_LOCK:
            self._easy_log(RTS_LOG_ERROR,
                           f'GET_DCT_LOCK reply format invalid. '
                           f'MSG byte should be POST_DCT_LOCK '
                           f'but is {RTS_MSG[raw_frame[0]]}.')
            self._msg_error_handler()
            return None

        # Extract the DCT lock status
        # Data is a single byte with the following strucutre:
        # b0: Reserved
        # b1: DCT1 Lock Status
        # b2: DCT2 Lock Status
        # b3: DCT3 Lock Status
        # b4: DCT4 Lock Status
        # b5: DCT5 Lock Status
        # b6: Reserved
        # b7: Reserved
        if 0x02 & raw_frame[9]:
            dct1 = 1
        else:
            dct1 = 0
        if 0x04 & raw_frame[9]:
            dct2 = 1
        else:
            dct2 = 0
        if 0x08 & raw_frame[9]:
            dct3 = 1
        else:
            dct3 = 0
        if 0x10 & raw_frame[9]:
            dct4 = 1
        else:
            dct4 = 0
        if 0x20 & raw_frame[9]:
            dct5 = 1
        else:
            dct5 = 0
        dct_lock = dct1, dct2, dct3, dct4, dct5
        self._easy_log(RTS_LOG_DEBUG,
                       f'GET_DCT_LOCK status is '
                       f'{dct_lock}.')
        return dct_lock


# Testing stub
if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description =
                                     'Expose Somfy RS485 RTS Transmitter')
    parser.add_argument('--log_level',
                        help='Set logging level. Defaults to error.',
                        choices=[RTS_LOG_DEBUG, RTS_LOG_INFO, RTS_LOG_WARNING, \
                                 RTS_LOG_ERROR, RTS_LOG_CRITICAL],
                        default=RTS_LOG_DEBUG)
    parser.add_argument('--rts_host', help =
                        'The hostname or IP address of the Somfy RTS Transmitter. '
                        'Defaults to localhost.', default='localhost')
    parser.add_argument('--rts_port', help =
                        'The Somfy RTS Transmitter port. Defaults to 4660.',
                        type = int, default = 4660)
    parser.add_argument('--channels', help =
                        'The number of RTS channels to manage. Defaults to 16.',
                        type = int, default=16)
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
    
    logger.info('Obtaining Somfy client')
    som = RTSProtocol()
    logger.info('Enabling Somfy logger')
    som.enable_logger(logger)
    s = som.socket()
    logger.info(f'Somfy socket is {s}.')
    logger.info(f'Establishing RTS Transmitter connection to host {args.rts_host}, port {args.rts_port}')
    som.connect(args.rts_host, args.rts_port)
    
    logger.info('Obtaining nodes')
    nodes = som.get_nodes()
    logger.info(f'Nodes are {nodes}.')
    
    for node_addr, node_label in nodes.items():
        stack_version = som.get_node_stack_version(node_addr)
        logger.info(f'Stack version for node {node_label}/0x{node_addr:06x} '
                     f'is {stack_version}')
        serial_number = som.get_node_serial_number(node_addr)
        logger.info(f'Serial number for node {node_label}/0x{node_addr:06x} '
                     f'is {serial_number}')
        app_version = som.get_node_app_version(node_addr)
        logger.info(f'App version for node {node_label}/0x{node_addr:06x} '
                     f'is {app_version}')
        for channel in range(args.channels):
            channel_mode = som.get_channel_mode(node_addr, channel)
            logger.info(f'Channel mode for node {node_label}/0x{node_addr:06x}'
                        f', channel {channel} is {channel_mode}')
            tilt_framecount = som.get_tilt_framecount(node_addr, channel)
            logger.info(f'Tilt framecount for node {node_label}/0x{node_addr:06x}'
                        f', channel {channel} is {tilt_framecount}')
            dim_framecount = som.get_dim_framecount(node_addr, channel)
            logger.info(f'Dim framecount for node {node_label}/0x{node_addr:06x}'
                        f', channel {channel} is {dim_framecount}')
        dct_lock = som.get_dct_lock(node_addr)
        logger.info(f'DCT lock status for node {node_label}/0x{node_addr:06x} '
                    f'is {dct_lock}')
        diag_data = som.get_network_stat(node_addr)
        logger.info(f'Network communication diagnostics for node '
                    f'{node_label}/0x{node_addr:06x} '
                    f'is {diag_data}')
        error_data = som.get_network_error_stat(node_addr)
        logger.info(f'Error counter of the stack for node '
                    f'{node_label}/0x{node_addr:06x} '
                    f'is {error_data}')
    
    set_label = 'n'
    set_label = input('Would you like to test set_node_label [Y/n]: ')
    if set_label == 'Y':
        logger.info('OK. Setting Node Labels')
        for node_addr, node_label in nodes.items():
            label = ''
            print(f'Existing label for node_address 0x{node_addr:06x} is {node_label}')
            label = input(f'Enter new label for node address 0x{node_addr:06x}: ')
            success = som.set_node_label(node_addr, label)
            logger.info(f'Set label to {label}. Success was {success}.')

    som.ping()
    
    som.disconnect()
    
