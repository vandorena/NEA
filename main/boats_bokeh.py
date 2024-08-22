from boats import Boat


CURRENT_BOATS = {"boat_list":[]}

def find_boats():
    with open("..\Boats\Boat_saves.txt","r") as file:
        boats = file.readlines()
    for i in range(0,len(boats)):
        line_content = boats[i].split()
        boat = Boat(line_content[0])
        CURRENT_BOATS["boat_list"].append(line_content[0])
        boat.add_polar(line_content[1])
        CURRENT_BOATS[line_content[0]] = boat
        boat = None
        

def boats(doc):
    find_boats()