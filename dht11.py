from device import Device
import sqlite3

class DHT11(Device):
    def __init__(self, name, room, type, mac, temp_uuid_in_cels, humidity_in_proc):
        super().__init__(name, room, type, mac)
        self.temp_uuid_in_cels = temp_uuid_in_cels
        self.humidity_in_proc = humidity_in_proc

    def add_to_db(self, file_db):
        try:
            self.sqlite_connection = sqlite3.connect(file_db)
            self.cursor = self.sqlite_connection.cursor()
            self.sql1 = """INSERT INTO temp_sens(temperature, humidity, currentdate, currentime, device)
                 values(?, ?, ?, ?, ?);"""
            self.sql2 = (self.get_value(self.temp_uuid_in_cels), self.get_value(self.humidity_in_proc), self.date['cur_date'], self.date['cur_time'], self.room)
            self.cursor.execute(self.sql1, self.sql2)
            self.sqlite_connection.commit()
            self.cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (self.sqlite_connection):
                self.sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def see_from_db(self, file_db):
        try:
            self.sqlite_connection = sqlite3.connect(file_db)
            self.cursor = self.sqlite_connection.cursor()
            self.sql1 = """SELECT * FROM temp_sens ORDER BY id DESC LIMIT 1;"""
            #self.sql1 = """SELECT * FROM sqlite_master;"""
            self.cursor.execute(self.sql1)
            self.records = self.cursor.fetchall()
            self.sqlite_connection.commit()
            self.cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (self.sqlite_connection):
                self.sqlite_connection.close()
                print("Соединение с SQLite закрыто")
                return self.records