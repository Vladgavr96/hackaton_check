import os
import sys
import csv
import json

def check_cargo_position(cargo, cargoSpace):
    min_x = 0
    min_y = 0
    min_z = 0

    pos_x = cargo['position']['x']
    pos_y = cargo['position']['y']
    pos_z = cargo['position']['z']


    max_x = cargoSpace['loading_size']['length'] + 0.01
    max_y = cargoSpace['loading_size']['height'] + 0.01
    max_z = cargoSpace['loading_size']['width'] + 0.01

    size_x = cargo['size']['length'] /2
    size_y = cargo['size']['height']/2
    size_z = cargo['size']['width']/2
    if(min_x + size_x <= pos_x <= max_x - size_x ) and (min_y + size_y <= pos_y <= max_y - size_y )and (min_z + size_z <= pos_z <= max_z - size_z ):
        return True
    return False


def culc_q(data):
    cargo_max_y = 0
    volume = 0
    res_v = True
    mess = " - "
    try:
        cargoSpace = data['cargoSpace']
        max_x = cargoSpace['loading_size']['length'] + 0.01
        max_y = cargoSpace['loading_size']['height'] + 0.01
        max_z = cargoSpace['loading_size']['width'] + 0.01
        for cargo in data['cargos']:
            if check_cargo_position(cargo, cargoSpace):
                volume += cargo['size']['length'] * cargo['size']['height'] * cargo['size']['width']
                cargo_max = cargo['size']['height']/2 + cargo['position']['y']
                if (cargo_max > cargo_max_y):
                    cargo_max_y = cargo_max
            else:
                res_v = False
                mess = "Грузы вне грузового пространства. "
        density = volume / (max_x * max_z * cargo_max_y)
        if (density > 1):
            return [False,mess+"Грузы пересекаются", density, volume, cargo_max_y]
        return [res_v,mess, density, volume, cargo_max_y]
    except:
        return [False, "некорректный формат данных", 0, 0, 0]


path = sys.argv[1]
team = os.listdir(path)

for folder in team:
    with open(f'{path}/{folder}.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',')
        files_path = os.path.join(path, folder)
        files = os.listdir(files_path)
        for file in files:
            file_path = os.path.join(files_path, file)
            data = json.load(open(f"{file_path}"))
            #is_valid, mess, density, volume, cargo_max_y = culc_q(data)
            writer.writerow(culc_q(data))
