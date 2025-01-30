import random
import turtle


def check(x, y):
    count = 0
    if (x <= size - 1 and x >= 0) and (y <= size - 1 and y >= 0):
        if ground[y + 1][x] == 1:
            count += 1
        if ground[y][x + 1] == 1:
            count += 1
        if ground[y - 1][x] == 1:
            count += 1
        if ground[y][x - 1] == 1:
            count += 1
        if ground[y][x] == 1:
            count += 1
    return count



#畫路
def wall(distance):
    turtle.forward(distance)
    turtle.pendown()

def road(distance):
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
###################
side = size * distance


A = [0] * (size + 1)
ground = []
for i in range(size + 1):
    ground.append(A[:])


y = 0
x = 0
ground[y][x] = 1

position = [(x, y)]


turtle.speed(0)
turtle.hideturtle()
turtle.penup()
turtle.setposition(-1 * side / 2, -1 * side / 2)


#turn = [go_up + 1, go_right + 1, go_up - 1, go_right - 1]  ###
while position != []:
    turn = [0, 1, 2, 3]
    ok = 0
    #print("---", i)
    while ok != 1:
        r = random.choice(turn)   #r=random
        #print(">", r)
        if r == 0:  #y + 1
            ok = check(x, y + 1)
            if ok == 1:
                y += 1
                ground[y][x] = 1
                position.append((x, y))
            else:
                turn.remove(r)
        elif r == 1:  #x + 1
            ok = check(x + 1, y)
            if ok == 1:
                x += 1
                ground[y][x] = 1
                position.append((x, y))
            else:
                turn.remove(r)
        elif r == 2:  #y - 1
            ok = check(x, y - 1)
            if ok == 1:
                y -= 1
                ground[y][x] = 1
                position.append((x, y))
            else:
                turn.remove(r)
        elif r == 3:  #x - 1
            ok = check(x - 1, y)
            if ok == 1:
                x -= 1
                ground[y][x] = 1
                position.append((x, y))
            else:
                turn.remove(r)
                
        #print(ok)
        if turn == []:
            change_ok = 0
            while change_ok != 3 and position != []:
                r_position = random.choice(position)   #r=random
                change_ok = check(r_position[0], r_position[1])
                if change_ok == 3:
                    x = r_position[0]
                    y = r_position[1]
                    #print(r_position)
                position.remove(r_position)
            #print("break")
            break
        
    if position == []:
        print("all_break")
        break

"""
for i in range(size, -1, -1):
    print(ground[i])
print(position)
"""


#畫路
"""

#樣式1：圓的
turtle.pensize(distance)
turtle.pendown()
for j in range(size):
    for i in range(size):
        if ground[j][i] != 1:
            wall(distance)
            ground[j][i] = 0
        else:
            road(distance)
    changeline(size, distance)
    #print(ground[j])
"""
#樣式2：方的
def block(distance):
    turtle.pendown()
    turtle.fillcolor(0, 0, 0)
    turtle.begin_fill()
    for h in range(4):
        turtle.forward(distance)
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    turtle.forward(distance)

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
"""#"""

turtle.pendown()
for i in range(4):
    turtle.forward(side)
    turtle.right(90)

turtle.done()


