def get_platform_content_by_name(platform_dict, platform_name):
    ret_list = []
    for x in platform_dict:
        if x["name"] == platform_name:
            ret_list.append(x)
    return ret_list


def get_platform_by_name_serial(platform_dict, platform_name, serial_number):
    platform_list = get_platform_content_by_name(platform_dict, platform_name)
    new_list = []
    for p in platform_list:
        serial = p.pop("serial_number", None)
        if serial == serial_number:
            new_list.append(p)
    return new_list


def get_platform_by_serial(platform_dict, serial_number):
    ret_list = []
    for x in platform_dict:
        if x["serial_number"] == serial_number:
            ret_list.append(x)
    return ret_list


def get_by_name(model_dict_list, name):
    ret_list = []
    for x in model_dict_list:
        if x["name"].lower() == name.lower():
            ret_list.append(x)
    return ret_list


def get_by_given_id(model_dict_list, id_list):
    ret_list = []
    for x in model_dict_list:
        if x["id"] in id_list:
            ret_list.append(x)
    return ret_list


def get_by(model_dict_list, match_dict):
    ret_list = []
    for x in model_dict_list:
        for key, item in match_dict.items():
            if x[key] != item:
                break
        else:
            ret_list.append(x)
    return ret_list

