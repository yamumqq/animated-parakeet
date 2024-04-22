import random
import json
import csv
import os

deistv = [
    "Исследовать",
    "Налево",
    "Направо",
    "Назад",
    "Собрать",
    "Инвентарьb",
]

nachalo = {
    "progress": 0,
    "inventory": set(),
}

history = []


def key():
    return "ключ" not in nachalo["inventory"]


def trap():
    return "зелье" not in nachalo["inventory"]


def sword():
    return "меч" not in nachalo["inventory"]


komnata = {
    0: {
        "Описание": "Вы в стартовой комнате.",
    },
    1: {
        "Описание": "Вы нашли ключ на полу.",
        "условие": key,
    },
    2: {
        "Описание": "Вы попали в ловушку и потеряли здоровье.",
        "условие": trap,
    },
    3: {
        "Описание": "Вы нашли меч. Он пригодится для защиты.",
        "условие": sword,
    },
    4: {
        "Описание": "Вы нашли выход из подземелья!",
    },
}


def story():
    for a in history:
        print(a)


def perform_action(deistv):
    cur_komnt = komnata[nachalo["progress"]]

    if deistv == "Исследовать":
        history.append(cur_komnt["Описание"])
    elif deistv == "Налево" or deistv == "Направо":
        if cur_komnt.get("условие") and cur_komnt["условие"]():
            nachalo["progress"] -= 1
            history.append("Вы вернулись назад из-за недостаточных ресурсов.")
        else:
            nachalo["progress"] += 1
            history.append(f"Вы продвинулись дальше.")
    elif deistv == "Назад":
        nachalo["progress"] -= 1
        history.append(f"Вы вернулись назад.")
    elif deistv == "Собрать":
        if cur_komnt.get("условие") and cur_komnt["условие"]():
            history.append("Здесь нечего собирать.")
        else:
            item = random.choice(["ключ", "меч", "зелье"])
            nachalo["inventory"].add(item)
            history.append(f"Вы собрали {item}.")
    elif deistv == "Инвентарь":
        print_inventory()


def check_win():
    if nachalo["progress"] == len(komnata) - 1:
        history.append("Поздравляем! Вы успешно выбрались из подземелья!")
        return True
    return False


def print_inventory():
    inventory = ", ".join(nachalo["inventory"])
    history.append(f"Инвентарь: {inventory}")


SAVE_FILE = "save_data.json"
CSV_FILE = "game_data.csv"

def save_game_data():
    data_to_save = {
        "nachalo": {
            "progress": nachalo["progress"],
            "inventory": list(nachalo["inventory"])
        },
        "history": history
    }
    with open(SAVE_FILE, "w") as save_file:
        json.dump(data_to_save, save_file)
    print("Данные игры сохранены.")

def load_game_data():
    try:
        with open(SAVE_FILE, "r") as save_file:
            data = json.load(save_file)
            nachalo.update(data.get("nachalo", {}))
            history.extend(data.get("history", []))
        print("Данные игры загружены.")
    except FileNotFoundError:
        print("Не найдены сохраненные данные игры.")
def delete_game_data():
    try:
        os.remove(SAVE_FILE)
        print("Данные игры удалены.")
    except FileNotFoundError:
        print("Не найдены сохраненные данные игры.")

def save_to_csv():
    with open(CSV_FILE, mode='w', newline='') as csv_file:
        fieldnames = ['Игрок', 'Прогресс', 'Инвентарь']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not os.path.exists(CSV_FILE):
            writer.writeheader()

        writer.writerow({'Игрок': 'Игрок 1', 'Прогресс': nachalo['progress'], 'Инвентарь': ', '.join(nachalo['inventory'])})
        print("Данные сохранены в CSV.")

def main():
    print("Добро пожаловать в игру-новеллу!")

    while nachalo["progress"] < len(komnata) - 1:
        story()
        print("\nДоступные действия:")
        print("1. Сохранить игру")
        print("2. Загрузить игру")
        print("3. Удалить сохранение")
        for i, action in enumerate(deistv, start=4):
            print(f"{i}. {action}")

        choice = int(input("Выберите действие (1-9): "))
        if choice == 1:
            save_game_data()
        elif choice == 2:
            load_game_data()
        elif choice == 3:
            delete_game_data()
        elif 4 <= choice <= 9:
            perform_action(deistv[choice - 4])
            if check_win():
                break
        else:
            print("Неверный выбор. Попробуйте снова.")

    save_to_csv()
    story()
    print("Вы прошли игру!")

if __name__ == "__main__":
    main()
