from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# key will be the room the player is in value will be a dictionary with directions
# the strings for cardinal directions will be the keys and
#  values will be what I know lies in that direction
# {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}
player_map = {}
# opposite directions for cardinal directions
opposite_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e', "?": "?"}
# direction to the right of the player
right_dir = {'n': 'e', 'e': 's', 's': 'w', 'w': 'n'}
# direction I am facing
facing = 'n'
previous_room = None
# I need to check to see if the room I am in is in my map


def updateMap():
    if player.current_room not in player_map:
        room_exits = player.current_room.get_exits()
        room_init_dict = {}
        for room_exit in room_exits:
            # if the previous room is in the opposite direcition I am facing
            if room_exit == opposite_dir[facing]:
                if previous_room == None:
                    room_init_dict[room_exit] = "?"
                else:
                    room_init_dict[room_exit] = previous_room.id
                    player_map[previous_room.id][facing] = player.current_room.id
            else:
                room_init_dict[room_exit] = "?"
        player_map[player.current_room.id] = room_init_dict.copy()


def travel(direction):
    global previous_room
    global facing
    previous_room = player.current_room
    player.travel(direction)
    facing = direction
    updateMap()


def turnRight():
    # if the room only contains one exit, point to way I came in- opposite of facing
    global facing
    right = right_dir[facing]
    left = right_dir[opposite_dir[facing]]
    if right in player_map[player.current_room.id]:
        facing = right
    elif facing in player_map[player.current_room.id]:
        facing = facing
    elif left in player_map[player.current_room.id]:
        facing = left
    else:
        facing = opposite_dir[facing]

# if not I need to check the exits in the room I am in and add them to my map
# if their is nothing in that direction I add None
#
# if there is  a question mark in the room I turn right until I am facing it
# I go that way
# if there isn't a question mark in the room I search my map for the closest one
# I can use my shortest path algorithm for that
# I then go to a room with one
# I repeat until i have traversed the whole board

# I need a function to update facing
# if the player walked facing points the direction he walked


# I need a function to return an array with the shortest path to a ?
# look at the directions in that room
#  and for every node that is not None
# traverse look up the nodes in that room
# if any node contains
# Actually social graph might be better
class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def find_unknown_path(room_number):
    """
    Takes a user's user_id as an argument

    Returns a dictionary containing every user in that user's
    extended network with the shortest friendship path between them.

    The key is the friend's ID and the value is the path.
    """
    visited = {}  # Note that this is a dictionary, not a set
    # !!!! IMPLEMENT ME
    paths_walked = Queue()
    paths_walked.enqueue([(None, room_number)])
    # if the node hasn't been added to the visited add it(don't worry otherwise it isn't the )
    while paths_walked.size() > 0:
        path = paths_walked.dequeue()
        # first index direction to travel, second is destination
        current_room_tuple = path[-1]
        current_room_id = current_room_tuple[1]

        if current_room_id in visited:
            # stops this iteration. The loop will continue with next path
            continue
        # add it to my list of visited nodes
        visited[current_room_id] = path
        # lets look at all the friends that friend has and if we haven't visited them
        # player_map example {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}
        global player_map
        # print("I hate my life")
        # print(player_map)
        # for key in player_map:
        #     print(key)

        for room_door_dict in player_map[current_room_id]:
            print(f"room_door_dict:{room_door_dict}")
            for direction in room_door_dict:
                print(f"direction:{direction}")
                new_room_id = room_door_dict[direction]
                path_copy = path.copy()
                if new_room_id == '?':
                    directions = []
                    for n in path_copy:
                        directions.append(n[0])
                    return directions
                if new_room_id != None:
                    path_copy.append((direction, new_room_id))
                    paths_walked.enqueue(path_copy)
    return False


updateMap()
print(player_map)
travel('n')
print(player_map)
travel(facing)
print(player_map)
print(facing)
turnRight()
print(facing)
find_unknown_path(player.current_room.id)

# I need a function that takes an array with the shortest path
#  and walks the player to the room
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)


if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
