#!/usr/bin/python3
import pygatt
from binascii import hexlify
import datetime
import sqlite3

class Device():
    def __init__(self, name, room, type, mac):
        self.name = name
        self.room = room
        self.type = type
        self.mac = mac

    def get_date(self):
        self.date = {'cur_date' : datetime.datetime.today().strftime("%d/%m/%Y"),
                     'cur_time' : datetime.datetime.today().strftime("%H:%M:%S")
                    }

    def connect_to_ble(self):
        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.device = self.adapter.connect(self.mac)

    def disconnect_from_ble(self):
        self.device.disconnect()
        self.adapter.stop()

    def get_value_from_ble(self, char_uuid):
        self.get_date()
        self.value = self.device.char_read(char_uuid)
        self.value = int(hexlify(self.value), 16)
        return str(self.value)

