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
#map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
maze_finished = False


def updateMap():
    """
    Checks to see if the map exists for a room. If it doesn't it makes a blank map.
    It then updates both the room it came from and the new room to connect to one another
    """
    global player_map
    cur_room_id = player.current_room.id
    room_exits = player.current_room.get_exits()

    if cur_room_id not in player_map:
        player_map[cur_room_id] = {}

    for room_exit in room_exits:
        if room_exit not in player_map[cur_room_id]:
            player_map[cur_room_id][room_exit] = "?"
        if room_exit == opposite_dir[facing] and previous_room != None:
            player_map[cur_room_id][opposite_dir[facing]
                                    ] = previous_room.id
            player_map[previous_room.id][opposite_dir[room_exit]
                                         ] = cur_room_id


def travel(direction):
    """
    Moves the player in the direction of given, updates previous room,
    and turns them with their back to the door. Then updates the map.
    """
    global previous_room, facing, player_map
    global facing
    global player_map
    previous_room = player.current_room
    traversal_path.append(direction)
    player.travel(direction)
    facing = direction
    updateMap()


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
   Takes the room id as a variable. Returns a list directions to get to the nearest unsearched room
   if there isn't one it tells global state it is finished running the program
    """
    visited = {}  # Note that this is a dictionary, not a set

    paths_walked = Queue()
    paths_walked.enqueue([(None, room_number)])
    global player_map
    global maze_finished
    # if the node hasn't been added to the visited add it(don't worry otherwise it isn't the )
    # if the queue is empty the entire maze has been walked it lets the program know it is done walking
    while paths_walked.size() > 0:
        path = paths_walked.dequeue()

        # current_room_tuple first index is direction to travel, second is destination
        current_room_tuple = path[-1]
        current_room_id = current_room_tuple[1]

        if current_room_id in visited:
            # stops this iteration. The loop will continue with next path
            continue
        # updates the visited list with the current room
        visited[current_room_id] = path
        # For each direction in the map it checks to see if it is unexplored. It is it returns the path
        # If it is it processess the tuples and returns directions to it
        # if it isn't it appends all the paths to adjacent rooms
        for direction in player_map[current_room_id]:
            new_room_id = player_map[current_room_id][direction]
            path_copy = path.copy()
            if new_room_id == '?':
                directions = []
                for n in path_copy:
                    if n[0] != None:
                        directions.append(n[0])
                return directions
            if new_room_id != None:
                path_copy.append((direction, new_room_id))
                paths_walked.enqueue(path_copy)
    maze_finished = True
    return []


# Here I traverse the graph
#
updateMap()
# Maze finished fires when my search algorithm can't find an unexplored room
while not maze_finished:
    # Moves in a direction if it hasn't gone there before
    if 'w' in player_map[player.current_room.id] and player_map[player.current_room.id]['w'] == '?':
        travel('w')
    elif 's' in player_map[player.current_room.id] and player_map[player.current_room.id]['s'] == '?':
        travel('s')
    elif 'n' in player_map[player.current_room.id] and player_map[player.current_room.id]['n'] == '?':
        travel('n')
    elif 'e' in player_map[player.current_room.id] and player_map[player.current_room.id]['e'] == '?':
        travel('e')
    else:
        # If it has been to all the surrounding rooms it gets a path to the nearest room that has an unexplored door
        for direction in find_unknown_path(player.current_room.id):
            travel(direction)


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
