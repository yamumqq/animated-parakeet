import random

deistv = [
    "Исследовать",
    "Налево",
    "Направо",
    "Назад",
    "Собрать",
    "Инвентарь",
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


def main():
    print("Добро пожаловать в игру-новеллу!")
    while nachalo["progress"] < len(komnata) - 1:
        story()
        print("\nДоступные действия:")
        for i, action in enumerate(deistv, start=1):
            print(f"{i}. {action}")
        choice = int(input("Выберите действие (1-6): "))
        if 1 <= choice <= 6:
            perform_action(deistv[choice - 1])
            if check_win():
                break
        else:
            print("Неверный выбор. Попробуйте снова.")

    story()
    print("Вы прошли игру!")


if __name__ == "__main__":
    main()