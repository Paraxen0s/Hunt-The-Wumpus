from audioop import add
from re import I
import re
from cave import *
from settings import *
from entities import *


cave = None
player = None
wumpus = None
bats_list = []
pits_list = []
running = True


def quit_game():
    global running
    running = False


def win_game():
    print('You\'ve killed the Wumpus! Good job :]')
    quit_game()


def lose_game():
    print('You\'ve lost! Sorry')
    quit_game()


def setup_game():
    #print('setting up game...')

    global cave
    cave = Cave('dodecahedron')

    global player
    player = Player(cave)

    global wumpus
    wumpus = Wumpus(cave)

    global bats_list
    for _ in range(0, BAT_COUNT):
        bats_list.append(Bat(cave))

    global pits_list
    for _ in range(0, PIT_COUNT):
        pits_list.append(Pit(cave))

    print_status()

def general_commands(command: str):
    match command:
        case 'q' | 'quit':
            quit_game()
        case 'h' | 'help':
            print_help()
        case 'status':
            print_status()
        # case 'debug':
        #     print_debug()
        case _:
            print("Invalid command, try typing 'help'")


def print_help():
    print("----------------------------------------------------------------")
    print("'quit' quits the game, without confirmation")
    print("'help' brings up the list of commands (this thing)")
    print("'move [x]' to move the player to room [x], if [x] is adjacent")
    print("'shoot [x] [y] [...]' to shoot an arrow into room [x] if its adjacent, then [y] if its adjacent to [x], etc")
    print("'status' to show your current location, and info about it")
    print("----------------------------------------------------------------")


def print_debug():
    print("----------------------DEBUG-------------------------------------")
    print('player position:', player.room.room_num, "- adjacent to rooms", player.get_adjacent_room_nums())
    print('wumpus position:', wumpus.room.room_num, "- adjacent to rooms", wumpus.get_adjacent_room_nums())
    bat_pos = []
    for bat in bats_list:
        bat_pos.append(bat.room.room_num)
    print('bat positions:', bat_pos)
    pit_pos = []
    for pit in pits_list:
        pit_pos.append(pit.room.room_num)
    print('pit positions:', pit_pos)
    print("----------------------------------------------------------------")


def print_status():
    print('You are in room', player.room.room_num)
    print('You are adjacent to rooms', player.get_adjacent_room_nums())
    player.check_surroundings()


def game_tick(took_shot: bool):
    if wumpus.alive is False:
        win_game()
        return
    
    if player.room.room_num == wumpus.room.room_num:
        wumpus.eat(player)

    if took_shot:
        wumpus.try_wake()

    if wumpus.awake:
        wumpus.move()
    
    for bat in bats_list:
        if player.room.room_num == bat.room.room_num:
            bat.fly_to_random_room(player)

    for pit in pits_list:
        if player.room.room_num == pit.room.room_num:
            print('You fall to your death in the bottomless pit')
            player.die()

    if player.alive is False:
        lose_game()
        return
    
    print_status()


if __name__ == '__main__':
    setup_game()

    while running:
        input_string = input('> ')
        command = None
        values = []
        if ' ' in input_string:
            input_string = input_string.split()
            for x in range(0, len(input_string)):
                if x == 0:
                    command = input_string[x]
                if x > 0:
                    values.append(int(input_string[x]) - 1)

        match command:
            case 'm' | 'move':
                player.move(values[0])
                game_tick(False)
            case 's' | 'shoot':
                player.shoot(values)
                game_tick(True)
            case _:
                general_commands(input_string)
