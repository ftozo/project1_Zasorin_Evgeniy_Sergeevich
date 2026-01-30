# labyrinth_game/player_actions.py
# Действия игрока.

from labyrinth_game import constants, utils

def show_inventory(game_state: dict) -> None:
    # Показывает инвентарь игрока.
    inventory = game_state['player_inventory']
    
    if inventory:
        print("\nВаш инвентарь:")
        for idx, item in enumerate(inventory, 1):
            print(f"  {idx}. {item}")
    else:
        print("\nВаш инвентарь пуст.")

def get_input(prompt: str = "> ") -> str:
    # Получает ввод от пользователя.
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state: dict, direction: str) -> None:
    # Перемещает игрока в указанном направлении.
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]
    
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        if new_room == 'treasure_room':
            if 'key_from_treasure_room' in game_state['player_inventory']:
                print("\nВы используете ключ, чтобы открыть дверь в сокровищницу.")
                game_state['player_inventory'].remove('key_from_treasure_room')
                print("Ключ сломался в замке, но дверь открылась.")
            else:
                print("\nДверь в сокровищницу заперта. Нужен ключ, чтобы пройти дальше.")
                return
            
        elif new_room == 'secret_room':
            if 'key_from_secret_room' in game_state['player_inventory']:
                print("\nВы применяете ключ, и замок щёлкает. Дверь открыта!")
            else:
                print("\nДверь заперта, нужен ключ, чтобы ее открыть.")
                return
            
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        print(f"\nВы переместились {direction} в {new_room}.")
        utils.random_event(game_state)
        utils.describe_current_room(game_state)
    else:
        print(f"\nНельзя пойти в направлении '{direction}'.")


def take_item(game_state: dict, item_name: str) -> None:
    # Берет предмет из комнаты.
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]
    
    if item_name in room_data['items']:
        # Добавляем в инвентарь
        game_state['player_inventory'].append(item_name)
        # Удаляем из комнаты
        room_data['items'].remove(item_name)
        print(f"\nВы подобрали: {item_name}")
        show_inventory(game_state)
    else:
        print(f"\nПредмет '{item_name}' не найден в этой комнате.")


def use_item(game_state: dict, item_name: str) -> None:
    #Использует предмет из инвентаря.
    inventory = game_state['player_inventory']
    
    if item_name not in inventory:
        print(f"\nУ вас нет предмета '{item_name}'.")
        return
    
    # Уникальные действия для предметов
    if item_name == 'torch':
        print("\nВы зажгли факел. Стало светлее!")
        
    elif item_name == 'sword':
        print("\nВы почувствовали уверенность с мечом в руках!")
        
    elif item_name == 'bronze_box':
        print("\nВы открыли бронзовую шкатулку!")
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Внутри вы нашли старый 'rusty_key'!")
        else:
            print("Шкатулка оказалась пуста.")
        
    elif item_name == 'ancient_book':
        print("\nВы прочитали древнюю книгу. Вы узнали секрет: "
              "ключ от сундука с сокровищем называется 'rusty_key'!")
        
    elif item_name == 'old_map':
        print("\nНа карте отмечены все комнаты лабиринта. "
              "Теперь вы лучше ориентируетесь!")
        
    elif item_name == 'rusty_key':
        print("\nРжавый ключ холодный на ощупь. "
              "Возможно, он откроет что-то важное.")
        
    elif item_name == 'key_from_secret_room':
        print("\nБольшой железный ключ."
              "Скорее всего он открывает какую-то дверь.")
    else:
        print(f"\nВы не знаете, как использовать {item_name}.")