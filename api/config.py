import json


def init_config(config_file_path):
    with open(config_file_path) as json_file:
        data = json.load(json_file)

        ok = True
        if "url" not in data:
            print("URL not specified in config")
            ok = False

        if "cookies" not in data:
            print("Cookies not specified in config")
            ok = False

        if ok:
            return data
        else:
            return None
