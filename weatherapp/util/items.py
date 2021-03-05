def change_item(change: dict, items: list, value):
    if len(items) == 1:
        change[items[0]] = value
    elif len(items) == 2:
        change[items[0]][items[1]] = value
    elif len(items) == 3:
        change[items[0]][items[1]][items[2]] = value
    elif len(items) == 4:
        change[items[0]][items[1]][items[2]][items[3]] = value
    elif len(items) == 5:
        change[items[0]][items[1]][items[2]][items[3]][items[4]] = value
    elif len(items) == 6:
        change[items[0]][items[1]][items[2]][items[3]][items[4]][items[5]] = value
    return change
