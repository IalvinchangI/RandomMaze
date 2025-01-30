import random
import turtle


def check(x, y, number):
    count = 0
    if (x <= size - 1 and x >= 0) and (y <= size - 1 and y >= 0):
        if ground[y + 1][x] == number:
            count += 1
        if ground[y][x + 1] == number:
            count += 1
        if ground[y - 1][x] == number:
            count += 1
        if ground[y][x - 1] == number:
            count += 1
        if ground[y][x] == number:
            count += 1

        if ground[y + 1][x] != number and ground[y + 1][x] != 0:
            count += 10
        elif ground[y][x + 1] != number and ground[y][x + 1] != 0:
            count += 10
        elif ground[y - 1][x] != number and ground[y - 1][x] != 0:
            count += 10
        elif ground[y][x - 1] != number and ground[y][x - 1] != 0:
            count += 10
    return count

#turn = [go_up + 1, go_right + 1, go_up - 1, go_right - 1]  ###
def road(x, y, number, ground, position):
    #print("--------------", number)
    turn = [0, 1, 2, 3]
    ok = 0
    while ok != 11 and turn != []:
        r = random.choice(turn)   #r=random
        #print(">", r)
        if r == 0:  #y + 1
            ok = check(x, y + 1, number)
            if ok == 1 or ok == 11:
                y += 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        elif r == 1:  #x + 1
            ok = check(x + 1, y, number)
            if ok == 1 or ok == 11:
                x += 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        elif r == 2:  #y - 1
            ok = check(x, y - 1, number)
            if ok == 1 or ok == 11:
                y -= 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        elif r == 3:  #x - 1
            ok = check(x - 1, y, number)
            if ok == 1 or ok == 11:
                x -= 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        """
        print(ok)
        if ok == 11:
            for i in range(size, -1, -1):
                print(ground[i])
        print(position)
        """
    if ok == 11:
        #print("break_exchange")
        return 1
    else:
        #print("break")
        return 0

def find(number, position):
    change_ok = 0
    x = -1
    y = -1
    while change_ok != 3 and position != []:
        r_position = random.choice(position)   #r=random
        change_ok = check(r_position[0], r_position[1], number)
        if change_ok == 3:
            x = r_position[0]
            y = r_position[1]
            #print((x, y))
        position.remove(r_position)
    return [x, y]

def exchange(delete, become, ground):
    #當不同數字連在一起時，改成相同數字
    for l in range(size):
        while delete in ground[l]:
            place = ground[l].index(delete)
            ground[l].remove(delete)
            ground[l].insert(place, become)


#畫路
def block(distance):
    turtle.pendown()
    turtle.begin_fill()
    for h in range(4):
        turtle.forward(distance)
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    turtle.forward(distance)

def changeline(size, distance):
    turtle.penup()
    turtle.right(180)
    turtle.forward(size * distance)
    turtle.right(90)
    turtle.forward(distance)
    turtle.right(90)
    turtle.pendown()


###################
size = 10  #迷宮大小
distance = 10  #路的大小
run = True
###################
side = size * distance


A = [0] * (size + 1)
ground = []
for i in range(size + 1):
    ground.append(A[:])

x_first = random.randint(0, size - 1)
y_first = random.randint(0, size - 1)
position_first = [(x_first, y_first)]
ground[y_first][x_first] = 1

x_final = random.randint(0, size - 1)
y_final = random.randint(0, size - 1)
position_final = [(x_final, y_final)]
ground[y_final][x_final] = 2


#畫路
turtle.speed(0)
turtle.hideturtle()

#first
turtle.penup()
turtle.setposition(-1 * side / 2 + x_first * 10 + 1, -1 * side / 2 + y_first * 10 + 1)
turtle.color(0, 1, 0)
block(distance - 2)

#final
turtle.penup()
turtle.setposition(-1 * side / 2 + x_final * 10 + 1, -1 * side / 2 + y_final * 10 + 1)
turtle.color(1, 0, 0)
block(distance - 2)

turtle.penup()
turtle.color(0, 0, 0)
turtle.setposition(-1 * side / 2, -1 * side / 2)


while run == True:
    if position_first == []:
        print("all_break")
        break
    else:
        if position_final == []:
            road(x_first, y_first, 1, ground, position_first)
            x_first, y_first = find(1, position_first)

        else:
            change = 0
            change += road(x_first, y_first, 1, ground, position_first)
            if change == 1:
                exchange(2, 1, ground)
                position_first += position_final
                position_final = []
                continue
                
            change += road(x_final, y_final, 2, ground, position_final)
            if change == 1:
                exchange(2, 1, ground)
                position_first += position_final
                position_final = []
                continue
            
            x_first, y_first = find(1, position_first)
            x_final, y_final = find(2, position_final)

'''
for i in range(random.randint(1, size)):
    x = random.randint(0, size - 1)
    y = random.randint(0, size - 1)
    ground[y][x] = 1
'''
"""
for i in range(size, -1, -1):
    print(ground[i])
print(position_first)
"""#"""


#畫路
#樣式：方的
for j in range(size):
    for i in range(size):
        if ground[j][i] != 1:
            block(distance)
            ground[j][i] = 0
        else:
            turtle.forward(distance)
    changeline(size, distance)
    turtle.penup()
    #print(ground[j])

#畫框
turtle.pendown()
for i in range(4):
    turtle.forward(side)
    turtle.right(90)

turtle.done()



