# labyrinth_game/utils.py
# Вспомогательные функции для игры.

from labyrinth_game import constants, player_actions


def describe_current_room(game_state: dict) -> None:
    # Выводит описание текущей комнаты.
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]
    
    print(f"\n{'='*20} {current_room.upper()} {'='*20}")
    print(room_data['description'])
    
    # Выводим предметы в комнате
    if room_data['items']:
        print("\nЗаметные предметы:", ", ".join(room_data['items']))
    else:
        print("\nВ комнате нет заметных предметов.")
    
    # Выводим выходы
    if room_data['exits']:
        exits_str = ", ".join([f"{direction}->{room}" 
                              for direction, room in room_data['exits'].items()])
        print(f"\nВыходы: {exits_str}")
    else:
        print("\nВыходов нет!")
    
    # Упоминание о загадке
    if room_data['puzzle']:
        print("\nКажется, здесь есть загадка (используйте команду solve).")
    
    print(f"\nШагов сделано: {game_state['steps_taken']}")

def solve_puzzle(game_state: dict) -> None:
    # Решает загадку в текущей комнате.
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]
    
    if not room_data['puzzle']:
        print("\nВ этой комнате нет загадок.")
        return
    
    question, correct_answer = room_data['puzzle']
    
    print(f"\nЗагадка: {question}")
    
    # Получаем ответ от игрока
    answer = player_actions.get_input("Ваш ответ: ")
    
    # Проверяем ответ
    if answer == correct_answer:
        print("\nПравильно! Загадка решена!")
        
        # Награда за решение загадки
        if current_room == 'hall':
            print("Сундук на пьедестале открылся! Вы нашли 'key_from_secret_room'!")
            game_state['player_inventory'].append('key_from_secret_room')
            player_actions.show_inventory(game_state)
        elif current_room == 'trap_room':
            print("Плиты перестали двигаться. Вы можете безопасно перемещаться. В комнате появилась 'bronze_box'.")
            room_data['items'].append('bronze_box')
        elif current_room == 'library':
            print("На полке появилась 'ancient_book', содержащая в себе важную информацию!")
            room_data['items'].append('ancient_book')
        elif current_room == 'secret_room':
            print("На полке появилась 'old_map'!")
            room_data['items'].append('old_map')
        
        # Убираем загадку
        room_data['puzzle'] = None
        
    else:
        print("\nНеверно. Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    # Попытка открыть сундук с сокровищами.
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]
    
    if 'treasure_chest' not in room_data['items']:
        print("\nЗдесь нет сундука с сокровищами.")
        return
    
    print("\nПеред вами большой сундук с сокровищами.")
    
    # Проверяем наличие ключа
    if 'rusty_key' in game_state['player_inventory']:
        print("\nВы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        # Удаляем сундук из комнаты
        room_data['items'].remove('treasure_chest')
        
        print("\nВ сундуке сокровище! Вы победили!")
        print("=" * 50)
        print("ПОЗДРАВЛЯЕМ! Вы нашли сокровища лабиринта!")
        print(f"Всего шагов: {game_state['steps_taken']}")
        print(f"Собрано предметов: {len(game_state['player_inventory'])}")
        print("=" * 50)
        
        game_state['game_over'] = True
        return
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. У вас нет ключа, но можно попробовать ввести код.")
    
    response = player_actions.get_input("Попробовать ввести код? (да/нет): ")
    
    if response in ['да', 'yes', 'y']:
        # Используем загадку из комнаты как код
        if room_data['puzzle']:
            _, correct_code = room_data['puzzle']
            code_attempt = player_actions.get_input("Введите код: ")
            
            if code_attempt == correct_code:
                print("\nКод верный! Сундук открывается!")
                room_data['items'].remove('treasure_chest')
                
                print("\nВы нашли сокровища! Победа!")
                print("=" * 50)
                print("Вы взломали замок и добыли сокровища!")
                print(f"Всего шагов: {game_state['steps_taken']}")
                print("=" * 50)
                
                game_state['game_over'] = True
            else:
                print("\nНеверный код. Сундук не открылся.")
        else:
            print("\nКод уже был использован или отсутствует.")
    else:
        print("\nВы отходите от сундука.")

def attempt_open_secret_room(game_state: dict) -> bool:
    # Попытка открыть секретную комнату
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]
    
    # Проверяем наличие ключа
    if 'key_from_secret_room' in game_state['player_inventory']:
        print("\nВы применяете ключ, и замок щёлкает. Дверь открыта!")
        return True
    else:
        print("\nДверь заперта, нужен ключ, чтобы ее открыть.")
        return False


def show_help() -> None:
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")