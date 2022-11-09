from dht11 import DHT11
import read_config

path_to_db = ''
config = read_config.open_json()

if read_config.valid_data(config, read_config.schema_dht11) == True:
    test = DHT11(config['name'], config['room'], config['type'], config['mac'], config["temp_uuid_in_cels"], config["humidity_in_proc"])

    try:
        test.connect_to()
        #print(test.get_value(test.humidity_in_proc))
        test.add_to_db(path_to_db)
    finally:
        test.disconnect_to()


    print(test.see_from_db(path_to_db))