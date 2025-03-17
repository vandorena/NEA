from boats import Boat

print("Test 1.1")
boat = Boat("Imoca60")
boat.add_polar_v2("Imoca60.pol")
for i in range(0,len(dir(boat))):
    print((f"{dir(boat)[i]} : "+ f"{eval(f'boat.{dir(boat)[i]}')}"))
print("Test 2.1")
list = [0,1,2,3,4,5,6,7,8]
print(boat._binary_list_class_search(list,3))
print("Test 2.2")
print(boat._binary_list_class_search(list,0.5))
print("Test 2.3")
print(boat._binary_list_class_search(list,10))
print("Test 2.4")
list.remove(0)
print(list)
print(boat._binary_list_class_search(list,1))
print("Test 3.1")
print(boat.find_polar_speed(18,120))
print("Test 3.3")
print(boat.find_polar_speed(19,1000))
print("Test 3.2")
print(boat.find_polar_speed("18",120))