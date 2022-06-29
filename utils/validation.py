def validation_excel(file_name: str):
    if file_name.find('.xlsx') == -1:
        return True
    elif file_name[0] == '1' and file_name[1] != '.':
        if int(file_name[1]) > 6:
            return True
    elif len(file_name) == 6 and not file_name[0].isdigit() \
            or len(file_name) == 7 and not file_name[0:2].isdigit():
        return True
    elif file_name[0] == '-' or file_name[0] == '1':
        return True
    elif len(file_name) > 7:
        return True
    return False


def validation_room(room_number: str):
    if len(room_number) > 6 or len(room_number) < 5:
        return True
    if len(room_number) == 5:
        if not room_number[0:3].isdigit():
            return True
        if int(room_number[1:3]) > 17:
            return True
        if not room_number[-1].isdigit():
            return True
    if len(room_number) == 6:
        if not room_number[0:4].isdigit():
            return True
        if int(room_number[2:4]) > 17:
            return True
        if not room_number[-1].isdigit():
            return True
        if int(room_number[0:2]) > 16:
            return True
    if int(room_number[-1]) > 3 or int(room_number[-1]) < 2:
        return True
    return False
