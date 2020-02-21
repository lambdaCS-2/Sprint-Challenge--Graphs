from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


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

# instead of destination_vertex we are looking for '?'
def bfs(starting_vertex):
    q = Queue()
    q.enqueue([starting_vertex])
    visited = set()
    while q.size() > 0:
        # get rooms in queue
        path = q.dequeue()
        # grab last room
        v = path[-1]
        if v not in visited:
            # check the exits in current room
            for exit in graph[v]:
                # if unexplored
                if graph[v][exit] == '?':
                    return path
            visited.add(v)
            for vertex in graph[v]:
                # copy
                new_path = list(path) 
                # add room to path copy
                new_path.append(graph[v][vertex])
                # put back in queue and continue search
                q.enqueue(new_path)
    return None

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
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
graph = {}
switch_directions = {"n": "s", "s": "n", "w": "e", "e": "w"}
starting_room = player.current_room.id

# Find starting room and store it in graph
if starting_room not in graph:
    # create graph with first starting room
    graph[starting_room] = {}
    # all exits start as unexplored
    for direction in player.current_room.get_exits():
        graph[starting_room][direction] = '?'
        # print(f"Start: {graph}")
# Loop through room_graph
while len(graph) < len(room_graph):


# initialize list to hold unexplored exits for later
    unexplored_exits = []
    current_room = graph[player.current_room.id]
    # Get current room's unexplored exits and save to list
    # save the unexplored exits for later
    for exit in current_room:
        if current_room[exit] == '?':
            unexplored_exits.append(exit)
            # print(f"Unexplored exits: {unexplored_exits}")

    # If current room has unexplored rooms pick a random unexplored direction from the player's current room
    if len(unexplored_exits) > 0:
        # shuffle the exits
        random.shuffle(unexplored_exits)
        # pick the first random one
        new_path = unexplored_exits[0]
        # add to the count
        traversal_path.append(new_path)
        prev_room = player.current_room.id
        # travel 
        # Move player to room

        player.travel(new_path)

        # Add new room to graph
        if player.current_room.id not in graph:
            graph[player.current_room.id] = {}
            for rooms in player.current_room.get_exits():
                graph[player.current_room.id][rooms] = '?'

        # Update the graph for the room you just left and entered
        graph[prev_room][new_path] = player.current_room.id
        graph[player.current_room.id][switch_directions[new_path]] = prev_room
    else:
        # if deadend back up and look for ?
        back_up = bfs(player.current_room.id)
        direction = ''
        for room in back_up:
            for exit in graph[player.current_room.id]:
                if room == graph[player.current_room.id][exit]:
                    direction = exit

        player.travel(direction)
        traversal_path.append(direction)
        # print(f"travel path {traversal_path}")


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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
