# labyrinth_game/utils.py
# Вспомогательные функции для игры.

import math

from labyrinth_game import constants, player_actions


def describe_current_room(game_state: dict) -> None:
    # Выводит описание текущей комнаты.
    current_room = game_state["current_room"]
    room_data = constants.ROOMS[current_room]

    print(f"\n{'='*20} {current_room.upper()} {'='*20}")
    print(room_data["description"])

    # Выводим предметы в комнате
    if room_data["items"]:
        print("\nЗаметные предметы:", ", ".join(room_data["items"]))
    else:
        print("\nВ комнате нет заметных предметов.")

    # Выводим выходы
    if room_data["exits"]:
        exits_str = ", ".join(
            [f"{direction}->{room}" for direction, room in room_data["exits"].items()]
        )
        print(f"\nВыходы: {exits_str}")
    else:
        print("\nВыходов нет!")

    # Упоминание о загадке
    if room_data["puzzle"]:
        print("\nКажется, здесь есть загадка (используйте команду solve).")

    print(f"\nШагов сделано: {game_state['steps_taken']}")


def solve_puzzle(game_state: dict) -> None:
    # Решает загадку в текущей комнате.
    current_room = game_state["current_room"]
    room_data = constants.ROOMS[current_room]

    if not room_data["puzzle"]:
        print("\nВ этой комнате нет загадок.")
        return

    question, correct_answer = room_data["puzzle"]

    print(f"\nЗагадка: {question}")

    # Получаем ответ от игрока
    answer = player_actions.get_input("Ваш ответ: ")
    alternative_answers = []

    if current_room == "hall":
        alternative_answers = ["десять", "10", "десяти", "ten"]
    elif current_room == "trap_room":
        alternative_answers = ["шаг шаг шаг", "шаг шаг шаг.", "шагшагшаг"]
    elif current_room == "library":
        alternative_answers = ["резонанс", "резонанса"]
    elif current_room == "secret_room":
        alternative_answers = ["5", "пять", "five"]

    # Проверяем ответ
    if answer in alternative_answers:
        print("\nПравильно! Загадка решена!")

        # Награда за решение загадки
        if current_room == "hall":
            print(
                "Сундук на пьедестале открылся! Вы нашли 'key_from_secret_room'"
                " и 'key_from_treasure_room'!"
            )
            game_state["player_inventory"].append("key_from_secret_room")
            game_state["player_inventory"].append("key_from_treasure_room")
            player_actions.show_inventory(game_state)
        elif current_room == "trap_room":
            print(
                "Плиты перестали двигаться. Вы можете безопасно перемещаться. "
                "В комнате появилась 'bronze_box'."
            )
            room_data["items"].append("bronze_box")
        elif current_room == "library":
            print("На полке появилась 'ancient_book', содержащая в важную информацию!")
            room_data["items"].append("ancient_book")
        elif current_room == "secret_room":
            print("На полке появилась 'old_map'!")
            room_data["items"].append("old_map")

        # Убираем загадку
        room_data["puzzle"] = None

    else:
        print("\nНеверно. Попробуйте снова.")

    if current_room == "trap_room":
        print("Неверный ответ активирует ловушку!")
        trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    # Пытается открыть сундук с сокровищами.
    current_room = game_state["current_room"]
    room_data = constants.ROOMS[current_room]

    if "treasure_chest" not in room_data["items"]:
        print("\nℹЗдесь нет сундука с сокровищами.")
        return

    print("\n" + "=" * 50)
    print("ПЕРЕД ВАМИ ВЕЛИКИЙ СУНДУК С СОКРОВИЩАМИ!")
    print("=" * 50)

    # Проверяем наличие ключа
    if "treasure_key" in game_state["player_inventory"]:
        print("\nВы вставляете ключ, и древний замок с грохотом открывается!")

        # Удаляем ключ из инвентаря
        game_state["player_inventory"].remove("treasure_key")

        # Удаляем сундук из комнаты
        room_data["items"].remove("treasure_chest")

        print("\n" + "=" * 50)
        print("ПОЗДРАВЛЯЕМ! ВЫ НАШЛИ СОКРОВИЩА ЛАБИРИНТА!")
        print("=" * 50)
        print("\nВаши достижения:")
        print(f"   Шагов сделано: {game_state['steps_taken']}")
        print(f"   Собрано предметов: {len(game_state['player_inventory'])}")
        print("   Найдено сокровищ: БЕСЦЕННО")
        print("\nИгра завершена. Спасибо за прохождение!")
        print("=" * 50)

        game_state["game_over"] = True
        return

    # Если ключа нет, предлагаем ввести код
    print("\nСундук заперт на магический замок.")
    print("У вас нет ключа, но можно попробовать угадать код.")

    response = player_actions.get_input("Попробовать ввести код? (да/нет): ")

    if response in ["да", "yes", "y", "д"]:
        # Используем загадку из комнаты как код
        if room_data["puzzle"]:
            _, correct_code = room_data["puzzle"]
            code_attempt = player_actions.get_input("Введите магический код: ")

            # Проверяем различные форматы ответа
            if code_attempt in ["10", "десять", "ten"]:
                print("\nКОД ПРИНЯТ! Замок растворяется в воздухе!")
                room_data["items"].remove("treasure_chest")

                print("\n" + "=" * 50)
                print("ВЫ ВЗЛОМАЛИ ЗАМОК И ДОБЫЛИ СОКРОВИЩА!")
                print("=" * 50)
                print("\nВаша хитрость позволила обойти защиту!")
                print(f"   Шагов сделано: {game_state['steps_taken']}")
                print("   Решено загадок: Подсчет...")
                print("\nАльтернативная победа за смекалку!")
                print("=" * 50)

                game_state["game_over"] = True
            else:
                print("\nНеверный код. Замок вспыхивает синим пламенем!")
                # Небольшой негативный эффект
                if game_state["player_inventory"]:
                    lost = game_state["player_inventory"].pop()
                    print(f"Из-за магической вспышки вы теряете: {lost}")
        else:
            print("\nЗамок уже был вскрыт или защита снята.")
    else:
        print("\nℹВы решаете не рисковать и отходите от сундука.")


def pseudo_random(seed: int, modulo: int) -> int:
    # Генерирует псевдослучайное число на основе seed.
    # Используем формулу на основе синуса для генерации
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    result = math.floor(fractional * modulo)

    return result


def trigger_trap(game_state: dict) -> None:
    # Активирует ловушку с негативными последствиями для игрока.
    print("\nЛовушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        # Выбираем случайный предмет для потери
        if len(inventory) > 0:
            item_index = pseudo_random(game_state["steps_taken"], len(inventory))
            lost_item = inventory.pop(item_index)
            print(f"Вы потеряли предмет: {lost_item}!")

            # Показываем обновленный инвентарь
            if inventory:
                print(f"Осталось предметов: {len(inventory)}")
            else:
                print("Теперь ваш инвентарь пуст.")
    else:
        print("Ваш инвентарь пуст - ловушка наносит урон!")

        # Генерируем случайное число для проверки поражения
        damage_check = pseudo_random(game_state["steps_taken"], 10)

        if damage_check < 3:  # 30% шанс поражения
            print("\nЛовушка оказалась смертельной! Вы погибли...")
            game_state["game_over"] = True
        else:
            print("Вы чудом уцелели, но получили ушиб.")


def random_event(game_state: dict) -> None:
    # Случайное событие, которое может произойти при перемещении.
    # Проверяем, произойдет ли событие (10% шанс)
    event_chance = pseudo_random(game_state["steps_taken"], 10)

    if event_chance == 0:  # Событие происходит
        # Выбираем тип события
        event_type = pseudo_random(game_state["steps_taken"] + 1, 3)

        match event_type:
            case 0:  # Находка
                current_room = game_state["current_room"]
                constants.ROOMS[current_room]["items"].append("coin")
                print("\nВы нашли монетку на полу!")

            case 1:  # Испуг
                print("\nВы слышите странный шорох из темноты...")

                if "sword" in game_state["player_inventory"]:
                    print("Вы грозно взмахиваете мечом, и шорох прекращается.")
                else:
                    print("Вам становится не по себе...")

            case 2:  # Ловушка
                current_room = game_state["current_room"]
                has_torch = "torch" in game_state["player_inventory"]

                if current_room == "trap_room" and not has_torch:
                    print("\nВы не заметили ловушку в темноте!")
                    trigger_trap(game_state)
                else:
                    print("\nВы слышите щелчок механизма, но успеваете отскочить.")


def show_help() -> None:
    # Показывает список доступных команд.
    print("\nДоступные команды:")
    print("=" * 40)

    for cmd, description in constants.COMMANDS.items():
        cmd_display = cmd.ljust(20)
        print(f"  {cmd_display} - {description}")

    print("=" * 40)
    print("\nСовет: Вы можете использовать сокращения для направлений")
    print("Например: 'north' вместо 'go north'")
