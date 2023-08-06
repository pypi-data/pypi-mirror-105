gotoarrays = []


def place(id, execution):
    if id in gotoarrays:
        return False
    gotoarrays.append({"id": id, "command": execution})


def remove(id):
    count = 0
    for arr in gotoarrays:
        if id == arr["id"]:
            gotoarrays.pop(count)
        count += 1


def execute(id):
    count = 0
    for arr in gotoarrays:
        if id == arr["id"]:
            try:
                exec(arr["command"])
            except:
                return False
        count += 1

