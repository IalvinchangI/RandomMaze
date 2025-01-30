# 一路到底，多個終點的最終版
import random
import turtle
import time


def check(x, y, number):
    count = 0
    become = -1
    if (x <= xd - 1 and x >= 0) and (y <= yd - 1 and y >= 0):
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
            become = ground[y + 1][x]
        elif ground[y][x + 1] != number and ground[y][x + 1] != 0:
            count += 10
            become = ground[y][x + 1]
        elif ground[y - 1][x] != number and ground[y - 1][x] != 0:
            count += 10
            become = ground[y - 1][x]
        elif ground[y][x - 1] != number and ground[y][x - 1] != 0:
            count += 10
            become = ground[y][x - 1]
    return (count, become)

def road(x, y, number, ground, position):
    turn = [0, 1, 2, 3]  #[up, right, down, left]
    ok = (0, -1)
    while ok[0] != 11 and turn != []:
        r = random.choice(turn)   #r=random
        if r == 0:  #y + 1
            ok = check(x, y + 1, number)
            if ok[0] == 1 or ok[0] == 11:
                y += 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        elif r == 1:  #x + 1
            ok = check(x + 1, y, number)
            if ok[0] == 1 or ok[0] == 11:
                x += 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        elif r == 2:  #y - 1
            ok = check(x, y - 1, number)
            if ok[0] == 1 or ok[0] == 11:
                y -= 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        elif r == 3:  #x - 1
            ok = check(x - 1, y, number)
            if ok[0] == 1 or ok[0] == 11:
                x -= 1
                ground[y][x] = number
                position.append((x, y))
                turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
        
    if ok[0] == 11:  #碰到的數字不同時
        return (1, ok[1])
    else:
        return (0, ok[1])

def find(number, position):
    x = -1
    y = -1
    while position != []:  #####################################
        r_position = random.choice(position)   #r=random
        change_ok = check(r_position[0], r_position[1], number)
        if change_ok[0] == 3:
            x = r_position[0]
            y = r_position[1]
            position.remove(r_position)
            break
        position.remove(r_position)
    return (x, y, )

def exchange(delete, become, ground):
    """當不同數字連在一起時，改成相同數字"""
    for l in range(len(ground)):
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

def changeline(xd, distance):
    turtle.penup()
    turtle.right(180)
    turtle.forward(xd * distance)
    turtle.right(90)
    turtle.forward(distance)
    turtle.right(90)
    turtle.pendown()

#########################################################
i = 1
while True:
    try:
        if i == 1:
            xd = int(input("迷宮長度(x軸)："))   #迷宮大小(x軸)   185
            if xd <= 0:
                print("資料值錯誤，請重新輸入")
                continue
            i += 1
        if i == 2:
            yd = int(input("迷宮寬度(y軸)："))   #迷宮大小(y軸)   95
            if yd <= 0:
                print("資料值錯誤，請重新輸入")
                continue
            Max_ending = xd * yd - 1
            i += 1
        if i == 3:
            distance = int(input("路的大小："))  #路的大小   8
            if distance <= 0:
                print("資料值錯誤，請重新輸入")
                continue
            i += 1
        if i == 4:
            ending = int(input("幾個出口："))    #出口數   20
            if ending > Max_ending:
                print("資料值大於%d，請重新輸入" % Max_ending)
                continue
            i += 1
        if i == 5:
            random_TF = bool(eval(input("是否隨機選擇起終點座標 (True、False)：")))  #隨機選擇起終點座標  True
            del i
    except ValueError:
        print("資料型態錯誤，請重新輸入")
    except Exception:
        print("輸入錯誤，請重新輸入")
    else:
        break
#########################################################
x_side = xd * distance
y_side = yd * distance


Number = []
for i in range(1, ending + 2):
    Number.append(i)

A = [0] * (xd + 1)
ground = []
for i in range(yd + 1):
    ground.append(A[:])

start = []
position = []

for number in Number:
    while True:
        if random_TF:  #隨機選
            x = random.randint(0, xd - 1)
            y = random.randint(0, yd - 1)
            pos = (x, y)
            if pos in start:
                continue
        else:  #手動選
            try:
                x, y = eval(input("%d 號出入口，座標 x, y :" % number))
                pos = (int(x), int(y))
            except ValueError:
                print("資料型態錯誤，請重新輸入")
                continue
            if (pos[0] < 0) or (pos[1] < 0) or (pos[0] >= xd) or (pos[1] >= yd):
                print("座標超出範圍，請重新輸入")
                continue
            if pos in start:
                print("座標重複，請重新輸入")
                continue
        
        position.append([pos])
        start.append(pos)
        ground[y][x] = number
        break


turtle.tracer(0, 0)

#畫出入口
for i in range(len(start)):
    turtle.penup()
    turtle.setposition(-1 * x_side / 2 + start[i][0] * distance + 1, -1 * y_side / 2 + start[i][1] * distance + 1)
    if i == 0:
        turtle.color(0, 1, 0)
    else:
        turtle.color(1, 0, 0)
    block(distance - 2)

turtle.penup()
turtle.color(0, 0, 0)
turtle.setposition(-1 * x_side / 2, -1 * y_side / 2)

print("繪製出口時間：", time.process_time())
while True:
    if position[0] == []:
        print("製作迷宮時間：", time.process_time())
        break
    else:
        for number in Number:
            x = start[number - 1][0]
            y = start[number - 1][1]
            change = road(x, y, number, ground, position[number - 1])
            if change[0] == 1:
                if number == 1:
                    exchange(change[1], 1, ground)
                    position[0] += position[change[1] - 1]
                    position[change[1] - 1] = []
                    Number.remove(change[1])
                else:
                    exchange(number, change[1], ground)
                    position[change[1] - 1] += position[number - 1]
                    position[number - 1] = []
                    Number.remove(number)

        for number in Number:
            start[number - 1] = find(number, position[number - 1])


#畫路
#樣式：方的
for y in range(yd):
    for x in range(xd):
        if ground[y][x] == 0:
            block(distance)
            ground[y][x] = 0
        else:
            turtle.forward(distance)
    changeline(xd, distance)
    turtle.penup()

#畫框
turtle.pendown()
for i in range(2):
    turtle.forward(x_side)
    turtle.right(90)
    turtle.forward(y_side)
    turtle.right(90)
turtle.penup()

print("繪製迷宮時間：", time.process_time())
turtle.done()
