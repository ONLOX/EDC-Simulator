goal_grid_str = ''
goal_pos_str = ''
now_grid_str = ''
now_pos_str = ''


def str_to_pos(str):
    try:
        return [float(str[str.find('(')+1:str.find(',')]),
                float(str[str.find(',')+1:str.find(')')])]
    except:
        return [0.0, 0.0]