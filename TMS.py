import math
import datetime
import getpass


decimal = ""
wire_dict = {}
tms_sce = {"1.90": {"0.81": "TMS-SCE-1K-3/32-2.0-9         2.36     0.79     0000154314"},
           "2.66": {"1.11": "TMS-SCE-1K-1/8-2.0-9          3.18     1.07     0000112634"},
           "4.06": {"1.75": "TMS-SCE-1K-3/16-2.0-9         4.75     1.57     0000130298"},
           "5.46": {"2.31": "TMS-SCE-1K-1/4-2.0-9          6.35     2.11     0000075442"},
           "8.12": {"3.47": "TMS-SCE-1K-3/8-2.0-9          9.53     3.18     0000152806"},
           "10.79": {"4.64": "TMS-SCE-1K-1/2-2.0-9          12.70    4.22     0000075440"},
           "16.25": {"6.99": "TMS-SCE-1K-3/4-2.0-9          19.05    6.35     0000138206"},
           "21.59": {"9.29": "TMS-SCE-1K-1-2.0-9            25.40    8.46     0000122084"},
           "33.02": {"20.95": "TMS-SCE-1K-1 1/2-2.0-9        38.10    19.05    0000486275"},
           "44.95": {"27.94": "TMS-SCE-1K-2-2.0-9            50.80    25.40    0000498999"},
           "50.80": {"22.32": "TMS-SCE-1K-2 1/4-2.0-9        57.15    19.05    0000153740"}}
num_parts = 0
num_type_wire = 0
count_type_wire = 0
name_parts = ""
diam_type_wire = 0
count_num_type_wire = 1
choice = ""


def main_tms():
    global decimal
    action = True
    while action:
        foolproof_choice()
        if choice == "Да":
            decimal = input("Введите децимальный номер кабеля (ИВУА.444444.444): ")
            num_of_parts()
        else:
            action = False
            print("See you later")


def foolproof_choice():
    global choice
    bool_choice = True
    choice = input("Хотите посчитать диаметр жгута в кабеле по ГОСТ 23586-96? (Да/Нет) ").lower().title()
    while bool_choice:
        if choice == "Да" or choice == "Нет":
            bool_choice = False
        else:
            print('Нужно выбрать "Да" или "Нет"!')
            choice = input("Хотите посчитать диаметр жгута в кабеле по ГОСТ 23586-96? (Да/Нет) ").lower().title()
    return choice


def num_of_parts():
    foolproof_num_parts()
    count_num_parts = 1
    with open(f"C:\\Users\\{getpass.getuser()}\\Desktop\\{decimal}.txt", "wt") as f:
        f.write(f"Расчет произведен согласно ГОСТ 23586-96.\n"
                f"\n")
    while count_num_parts <= num_parts:
        name_of_part(count_num_parts)
        count_num_parts += 1
    diameter_cable()
    print()
    tms_choice()
    foolproof_file()
    save_file()


def foolproof_num_parts():
    global num_parts
    bool_num_parts = True
    num_parts = input("Введите количество участков кабеля (целое число): ")
    while bool_num_parts:
        try:
            num_parts = int(num_parts)
            bool_num_parts = False
        except ValueError:
            print("Количество участков кабеля может быть ТОЛЬКО ЦЕЛОЕ ЧИСЛО")
            num_parts = input("Введите количество участков кабеля (целое число): ")
    return num_parts


def name_of_part(parts):
    global num_type_wire, count_type_wire, name_parts, diam_type_wire, count_num_type_wire
    tmp_list = []
    name_parts = input(f"Введите наименование участка {parts} "
                       f"(Например: Х1 - МР1, где МР1 - место разветвления 1): ")
    foolproof_num_type_wire()
    while count_num_type_wire <= num_type_wire:
        foolproof_diam_type_wire()
        foolproof_count_type_wire()
        for i in range(count_type_wire):
            tmp_list.append(diam_type_wire)
        count_num_type_wire += 1
    count_num_type_wire = 1
    wire_dict[name_parts] = {"Dср": round(sum(tmp_list) / len(tmp_list), 2), "n": len(tmp_list)}


def foolproof_num_type_wire():
    global num_type_wire
    bool_num_type_wire = True
    num_type_wire = input(f"Введите сколько различных типов проводов на участке {name_parts} (целое число): ")
    while bool_num_type_wire:
        try:
            num_type_wire = int(num_type_wire)
            bool_num_type_wire = False
        except ValueError:
            print("Количество типов проводов может быть ТОЛЬКО ЦЕЛОЕ ЧИСЛО")
            num_type_wire = input(f"Введите сколько различных типов проводов на участке {name_parts} (целое число): ")
    return num_type_wire


def foolproof_diam_type_wire():
    global diam_type_wire
    bool_diam_type_wire = True
    diam_type_wire = input(f"Введите диаметр {count_num_type_wire} провода: ").replace(",", ".")
    while bool_diam_type_wire:
        try:
            diam_type_wire = float(diam_type_wire)
            bool_diam_type_wire = False
        except ValueError:
            print("Диаметр провода может быть ТОЛЬКО ЧИСЛОМ")
            diam_type_wire = input(f"Введите диаметр {count_num_type_wire} провода: ")
    return diam_type_wire


def foolproof_count_type_wire():
    global count_type_wire
    bool_count_type_wire = True
    count_type_wire = input(f"Введите количество {count_num_type_wire} провода (целое число): ")
    while bool_count_type_wire:
        try:
            count_type_wire = int(count_type_wire)
            bool_count_type_wire = False
        except ValueError:
            print("Количество провода может быть ТОЛЬКО ЦЕЛОЕ ЧИСЛОМ")
            count_type_wire = input(f"Введите количество {count_num_type_wire} провода (целое число): ")
    return count_type_wire


def diameter_cable():
    for i in wire_dict:
        d = round(1.3 * math.sqrt(wire_dict[i]["n"]) * wire_dict[i]["Dср"])
        wire_dict[i]["D"] = d


def tms_choice():
    for i in wire_dict:
        print(f"Подходящие трубки для участка {i}: "
              f"Dср = {wire_dict[i]['Dср']}мм, "
              f"n = {wire_dict[i]['n']}, "
              f"D = {wire_dict[i]['D']}мм "
              f"\n")
        print("Тип трубки                    MAX      MIN       Код PDM \n")
        for j in tms_sce:
            for k in tms_sce[j]:
                if float(k) < wire_dict[i]["D"] < float(j):
                    print(tms_sce[j][k])


def foolproof_file():
    try:
        with open(f"C:\\Users\\{getpass.getuser()}\\Desktop\\{decimal}.txt", "r") as f:
            f.read()
            print(f"\nФайл {decimal}.txt записан на рабочем столе текущего пользователя\n")
    except FileNotFoundError:
        print("\nФайл будет записан в полной версии программы. Самое время задонатить автору\n")
    except UnicodeEncodeError:
        print("\nФайл будет записан в полной версии программы. Самое время задонатить автору\n")


def save_file():
    with open(f"C:\\Users\\{getpass.getuser()}\\Desktop\\{decimal}.txt", "at") as f:
        for i in wire_dict:
            f.write(f"Для участка жгута {i}:"
                    f"Dср = {wire_dict[i]['Dср']}, "
                    f"n = {wire_dict[i]['n']}, "
                    f"D = {wire_dict[i]['D']}.\n"
                    f"где Dср - среднее арифметическое значение диаметра провода, мм;\n"
                    f"n - число проводов, шт.;\n"
                    f"D - диаметр жгута, мм.\n\n"
                    f"Подходящие трубки:\n\n")
            f.write("Тип трубки                    MAX      MIN       Код PDM \n")
            for j in tms_sce:
                for k in tms_sce[j]:
                    if float(k) < wire_dict[i]["D"] < float(j):
                        f.write(f"{tms_sce[j][k]}\n")
            f.write("\n\n")
        f.write("Файл был записан ")
        f.write(datetime.datetime.now().strftime("%d.%m.%Y в %H:%M"))


main_tms()
