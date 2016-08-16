#! -*- coding=utf-8 -*-

def quit(param):
    return "shutdown", {}


def press_keycode(param):
    print(param)
    return "action", {"action": "pressKeyCode", "params": param}


def find_element(params):
    data = {
        "strategy": params["using"],
        "selector": params["value"],
        "context": "",
        "multiple": False
    }
    print(("find %s" % str(data["selector"])))
    return "action", {"action": "find", "params": data}


def find_elements(params):
    data = {
        "strategy": params["using"],
        "selector": params["value"],
        "context": "",
        "multiple": True
    }
    print(("find %s" % str(data["selector"])))
    return "action", {"action": "find", "params": data}


def find_child_element(params):
    data = {
        "strategy": params["using"],
        "selector": params["value"],
        "context": params["id"],
        "multiple": False
    }
    print(("find %s" % str(data["selector"])))
    return "action", {"action": "find", "params": data}


def find_child_elements(params):
    data = {
        "strategy": params["using"],
        "selector": params["value"],
        "context": params["id"],
        "multiple": True
    }
    print(("find %s" % str(data["selector"])))
    return "action", {"action": "find", "params": data}


def click_element(params):
    print(params)

    return "action", {"action": "element:click", "params": {"elementId": params["id"]}}


def tap(params):
    print(params)
    return "action", {"action": "click", "params": {"x": params["x"], "y": params["y"]}}


def swipe(params):
    print(params)
    return "action", {"action": "swipe", "params": params}


def flick(params):
    print(params)
    return "action", {"action": "flick", "params": params}


def flick_element(params):
    print(params)
    elid = params.pop("id")
    params["elementId"] = elid
    return "action", {"action": "element:flick", "params": params}


def element_send_keys(params):
    print(params)
    data = {
        "elementId": params["id"],
        "text": params["value"],
        "unicodeKeyboard": True,
        "replace": False
    }
    return "action", {"action": "element:setText", "params": data}


def element_text(params):
    return "action", {"action": "element:getText", "params": {"elementId": params["id"]}}


def element_attr(params):
    return "action", {"action": "element:getAttribute",
                      "params": {"elementId": params["id"], "attribute": params["name"]}}


def element_location(params):
    return "action", {"action": "element:getLocation", "params": {"elementId": params["id"]}}


def element_size(params):
    return "action", {"action": "element:getSize", "params": {"elementId": params["id"]}}


def element_tag_name(params):
    return "action", {"action": "element:getSize", "params": {"elementId": params["id"]}}

def get_screenshot_as_file(params):
    return "action", {"action": "element:setText", "params": data}
