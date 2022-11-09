from jsonschema import validate
import json

schema_dht11 = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "room": {
      "type": "string"
    },
    "type": {
      "type": "string"
    },
    "mac": {
      "type": "string"
    },
    "temp_uuid_in_cels": {
      "type": "string"
    },
    "humidity_in_proc": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "room",
    "type",
    "mac",
    "temp_uuid_in_cels",
    "humidity_in_proc"
  ]
}

def valid_data(data: dict, json_schema: dict):
    try:
        validate(data, json_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def open_json():
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
        return data