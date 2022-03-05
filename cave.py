from random import random, randrange

dodecahedron = {
    # [up, down, left, right]
    1: [0, 8, 2, 5],
    2: [0, 10, 3, 1],
    3: [0, 12, 4, 2],
    4: [0, 14, 5, 3],
    5: [0, 6, 1, 4],
    6: [5, 0, 7, 15],
    7: [0, 17,  8, 6],
    8: [1, 0, 9, 7],
    9: [0, 18, 10, 8],
    10: [2, 0, 11, 9],
    11: [0, 19, 12, 10],
    12: [3, 0, 13, 11],
    13: [0, 20, 14, 12],
    14: [4, 0, 15, 13],
    15: [0, 16, 6, 14],
    16: [15, 0, 17, 20],
    17: [7, 0, 18, 16],
    18: [9, 0, 19, 17],
    19: [11, 0, 20, 18],
    20: [13, 0, 16, 19]
}

class Room():
	def __init__(self, room_num: int, up: int, down: int, left: int, right: int):
		self.room_num = room_num
		self.up = up
		self.down = down
		self.left = left
		self.right = right
		self.entities = []
	
	def get_entity_of_type(self, entity_type: type):
		for entity in self.entities:
			if type(entity) == entity_type:
				print(entity)
				return entity


class Cave():
	def __init__(self, layout: str):
		self.rooms_list = []
		self.generate_cave(layout)
		self.empty_rooms = []


	def get_adjacent_rooms(self, room: Room) -> list[Room]:
		room_num_list = dodecahedron[room.room_num]
		new_room_nums_list = []
		for x in range(0, len(room_num_list)):
			if room_num_list[x] > 0:
				new_room_nums_list.append(self.rooms_list[room_num_list[x] - 1])
		return new_room_nums_list

	def get_random_room(self) -> Room:
		return self.rooms_list[randrange(0, len(self.rooms_list)) - 1]

	def get_random_empty_room(self) -> Room:
		self.empty_rooms.clear()
		for room in self.rooms_list:
			if len(room.entities) == 0:
				self.empty_rooms.append(room)
		if len(self.empty_rooms) == 0:
			return None
		random_number = randrange(0, len(self.empty_rooms))
		random_empty_room = self.empty_rooms[random_number]
		return self.rooms_list[random_empty_room.room_num - 1]


	def make_dodeca_cave(self):
		for x in dodecahedron:
			self.rooms_list.append(Room(
				x,
				dodecahedron[x][0],
				dodecahedron[x][1],
				dodecahedron[x][2],
				dodecahedron[x][3]
			))
	

	def generate_cave(self, layout:str):
		match layout:
			case 'dodecahedron':
				self.make_dodeca_cave()
			case _:
				pass



# dodecahedron = {
#     # [up, down, left, right]
#     1: [0, 8, 2, 5],
#     2: [0, 10, 3, 1],
#     3: [0, 12, 4, 2],
#     4: [0, 14, 5, 3],
#     5: [0, 6, 1, 4],
#     6: [5, 0, 7, 15],
#     7: [0, 17,  8, 6],
#     8: [1, 0, 9, 7],
#     9: [0, 18, 10, 8],
#     10: [2, 0, 11, 9],
#     11: [0, 19, 12, 10],
#     12: [3, 0, 13, 11],
#     13: [0, 20, 14, 12],
#     14: [4, 0, 15, 13],
#     15: [0, 16, 6, 14],
#     16: [15, 0, 17, 20],
#     17: [7, 0, 18, 16],
#     18: [9, 0, 19, 17],
#     19: [11, 0, 20, 18],
#     20: [13, 0, 16, 19]
# }