#!/usr/bin/env python3
# Точка входа в игру 'Лабиринт сокровищ'.

from labyrinth_game import player_actions, utils


def process_command(game_state: dict, command: str) -> None:
    # Обрабатывает команду игрока.
    parts = command.split()
    if not parts:
        return

    cmd = parts[0]
    arg = " ".join(parts[1:]) if len(parts) > 1 else ""

    # Проверяем односложные команды для перемещения
    direction_commands = [
        "north",
        "south",
        "east",
        "west",
        "север",
        "юг",
        "восток",
        "запад",
    ]

    if cmd in direction_commands:
        # Маппинг русских названий
        direction_map = {
            "север": "north",
            "юг": "south",
            "восток": "east",
            "запад": "west",
        }

        direction = direction_map.get(cmd, cmd)
        player_actions.move_player(game_state, direction)

    elif cmd in ["go", "идти"]:
        if arg:
            player_actions.move_player(game_state, arg)
        else:
            print("Укажите направление: go north/south/east/west")

    elif cmd in ["take", "взять", "подобрать"]:
        if arg:
            if arg == "treasure_chest":
                print("Вы не можете поднять сундук, он слишком тяжелый.")
            else:
                player_actions.take_item(game_state, arg)
        else:
            print("Укажите предмет: take <предмет>")

    elif cmd in ["use", "использовать"]:
        if arg:
            player_actions.use_item(game_state, arg)
        else:
            print("Укажите предмет: use <предмет>")

    elif cmd in ["inventory", "инвентарь", "inv"]:
        player_actions.show_inventory(game_state)

    elif cmd in ["solve", "решить"]:
        # В комнате с сокровищами открываем сундук
        if game_state["current_room"] == "treasure_room":
            utils.attempt_open_treasure(game_state)
        else:
            utils.solve_puzzle(game_state)

    elif cmd in ["open", "открыть"]:
        if arg == "treasure_chest":
            utils.attempt_open_treasure(game_state)
        else:
            print(f"Нельзя открыть '{arg}'.")

    elif cmd in ["help", "помощь"]:
        utils.show_help()

    elif cmd in ["look", "осмотреться", "осмотреть", "ls"]:
        utils.describe_current_room(game_state)

    else:
        print(f"Неизвестная команда: {cmd}")
        print("Введите 'help' для списка команд.")


def move_player(game_state: dict, direction: str) -> None:
    player_actions.move_player(game_state, direction)


def take_item(game_state: dict, item_name: str) -> None:
    player_actions.take_item(game_state, item_name)


def main() -> None:
    # Основная функция игры.
    print("\nДобро пожаловать в Лабиринт сокровищ!")
    print("=" * 50)

    # Состояние игры
    game_state = {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Флаг окончания игры
        "steps_taken": 0,  # Количество шагов
    }

    # Показываем стартовую комнату
    utils.describe_current_room(game_state)
    print("\nВведите 'help' для списка команд.")

    # Основной игровой цикл
    while not game_state["game_over"]:
        try:
            # Получаем команду
            command = player_actions.get_input("\nВведите команду: ")

            if not command:
                continue

            # Выход из игры
            if command in ["quit", "exit", "выход"]:
                print("Спасибо за игру!")
                break

            # Обработка команд
            process_command(game_state, command)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            continue


if __name__ == "__main__":
    main()
