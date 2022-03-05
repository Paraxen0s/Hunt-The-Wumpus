from re import L
from settings import *
from cave import *

class Entity:
    def __init__(self, cave: Cave, room: Room):
        self.cave = cave
        self.room = room
        self.room.entities.append(self)
        self.adjacent_rooms = self.cave.get_adjacent_rooms(self.room)

    def teleport(self, new_room: Room):
        self.room.entities.remove(self)
        self.room = self.cave.rooms_list[new_room.room_num - 1]
        self.room.entities.append(self)
        self.adjacent_rooms = self.cave.get_adjacent_rooms(self.room)

    def get_adjacent_room_nums(self) -> list[int]:
        room_num_list = []
        for room in self.adjacent_rooms:
            room_num_list.append(room.room_num)
        return room_num_list
            

class Player(Entity):
    def __init__(self, cave: Cave):
        super().__init__(cave, cave.get_random_empty_room())
        self.arrows = 1
        self.alive = True

    def is_adjacent_to_room(self, target_room: Room) -> bool:
        if target_room in self.cave.get_adjacent_rooms(self.room):
            return True
        else:
            if target_room.room_num == self.room.room_num:
                print('You are already in room', target_room.room_num)
            elif target_room.room_num <= len(self.cave.rooms_list) & target_room.room_num > 0:
                print('You are not adjacent to room', target_room.room_num)
            else:
                print('Room', target_room.room_num, 'does not exist')

    def move(self, target_room_num: int):
        target_room = self.cave.rooms_list[target_room_num]
        if self.is_adjacent_to_room(target_room):
            super().teleport(target_room)

    def shoot(self, target_room_nums):
        target_rooms = []
        for x in target_room_nums:
            target_rooms.append(self.cave.rooms_list[x])
        
        arrow_rooms_to_go = ARROW_TRAVEL_DISTANCE
        if len(target_rooms) < arrow_rooms_to_go:
            arrow_rooms_to_go == len(target_rooms)
            
        old_room = self.room
        for room in target_rooms:
            if room not in self.cave.get_adjacent_rooms(old_room):
                random_room_choice = self.cave.get_adjacent_rooms(room)
                random_room_choice.remove(old_room)
                room = random_room_choice
            for entity in room.entities:
                if type(entity) is Wumpus:
                    entity.get_hit()
                    return
            old_room = room
            arrow_rooms_to_go - 1
        self.arrows -= 1
        
    def die(self):
        self.alive = False;

    def check_surroundings(self):
        any_wumpi = False
        any_pits = False
        any_bats = False
        for room in self.adjacent_rooms:
            for entity in room.entities:
                if type(entity) is Wumpus:
                    any_wumpi = True
                if type(entity) is Pit:
                    any_pits = True
                if type(entity) is Bat:
                    any_bats = True

        if any_wumpi:
            print('You smell something awful')
        
        if any_pits:
            print('You can feel a cold breeze')

        if any_bats:
            print('You hear rustling sounds nearby')


class Wumpus(Entity):
    def __init__(self, cave):
        super().__init__(cave, cave.get_random_empty_room())
        self.awake = False
        self.alive = True

    def try_wake(self):
        if randrange(0, 100) > WUMPUS_WAKE_CHANCE:
            self.awake = True

    def move(self):
        target_room = self.adjacent_rooms[randrange(
            0, len(self.adjacent_rooms))]
        super().teleport(target_room)
        for entity in target_room.entities:
            if type(entity) is Player:
                self.eat(entity)

    def eat(self, player: Player):
        print('The Wumpus devours you!')
        player.die()

    def get_hit(self):
        self.alive = False


class Bat(Entity):
    def __init__(self, cave):
        super().__init__(cave, cave.get_random_empty_room())

    def fly_to_random_room(self, player: Player):
        random_room_for_player = self.cave.get_random_room()
        random_room_for_self = self.cave.get_random_empty_room()

        player.teleport(random_room_for_player)
        print('You have been taken by a bat! You have been moved to room', random_room_for_player.room_num)

        super().teleport(random_room_for_self)


class Pit(Entity):
    def __init__(self, cave):
        super().__init__(cave, cave.get_random_empty_room())
