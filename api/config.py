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
        else:
            cookies_str = data["cookies"]
            data["cookies"] = dict()
            for itr in cookies_str.split("; "):
                aux = itr.split('=')
                data["cookies"][aux[0]] = aux[1]

        if ok:
            return data
        else:
            return None
