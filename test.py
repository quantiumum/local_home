from dht11 import DHT11

path_to_db = ''
test = DHT11(name = '', room = '', type = '', mac = '', temp_uuid_in_cels = "beb5483e-36e1-4688-b7f5-ea07361b26a8", humidity_in_proc = "3e1b86b6-5b88-11ed-9b6a-0242ac120002")
try:
    test.connect_to_ble()
    #print(test.get_value(test.humidity_in_proc))
    test.add_to_db(path_to_db)
finally:
    test.disconnect_from_ble()