import random
import turtle

#路的草稿
def exchange(delete, become):
    #當不同數字連在一起時，改成相同數字
    for l in range(j + 1):
        while delete in ground[l]:
            place = ground[l].index(delete)
            ground[l][place] = become

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
size = 60  #迷宮大小
distance = 10  #路的大小
###################
side = size * distance

max_number = 1

A = [-1] * size
ground = []
for i in range(size):
    ground.append(A[:])

turtle.speed(0)
turtle.penup()
turtle.setposition(-1 * side / 2, -1 * side / 2)

#i=x軸, j=y軸
#路的草稿
for j in range(size):
    i = random.randint(-1 * size, 0)  #每一行的起始點
    for k in range(size):
        if k == 0 and j == 0:
            ground[0][0] = 1
            i = 0
            """
            up = ground[j - 1][i]  #上項
            before = ground[j][i - 1]  #前項
            up_end = 1 in ground[j - 1][i + 1:]  #上項之後的項是否有1
            """
        else:
            r = random.randint(-2, 5)   #r=random, 0=wall, 1=road
            if r >= 1:            #road
                if i != 0 and j == 0:  #首行(非排首)
                    before = ground[j][i - 1]
                    if before == 0:   #前項是否為零
                        max_number += 1
                        ground[0][i] = max_number
                    else:
                        ground[0][i] = before
                        
                elif (i == 0 or i == -1 * size) and j != 0:  #排首
                    up = ground[j - 1][i]
                    if up == 0:   #上項是否為零
                        max_number += 1
                        ground[j][i] = max_number
                    else:
                        ground[j][i] = up
                
                elif (i != 0 or i != -1 * size) and j != 0:  #非排首(非首行)
                    if k == 0:  #是否為該排第一個填入的數字
                        up = ground[j - 1][i]
                        if up == 0:   #上項是否為零
                            max_number += 1
                            ground[j][i] = max_number
                        else:
                            ground[j][i] = up
                    else:
                        before = ground[j][i - 1]
                        up = ground[j - 1][i]
                        if before == 0 and up == 0:
                            max_number += 1
                            ground[j][i] = max_number
                        elif before != 0:  #前項
                            #當不同數字連在一起時，改成相同數字
                            if up == 1 and before > 1:
                                ground[j][i] = 1
                                exchange(before, 1)
                            elif up > 1 and before > 1 and before != up:
                                ground[j][i] = up
                                exchange(before, up)
                            elif up > 1 and before == 1:
                                ground[j][i] = 1
                                exchange(up, 1)
                            else:
                                ground[j][i] = before
                            
                        elif up != 0:   #上項
                            ground[j][i] = up
                
            else:              #wall
                if (i == 0 or i == -1 * size) and j != 0:  #排首(非首行)
                    up = ground[j - 1][i]
                    up_end = 1 in ground[j - 1][i + 1:]
                    if up == 1 and up_end == False:  #上項、上項之後的項
                        ground[j][i] = 1
                    else:
                        ground[j][i] = 0
                        
                elif ((i > 0 and i < size - 1) or (i > -1 * size and i < -1)) and j != 0:  #(非首行)
                    up = ground[j - 1][i]
                    up_end = 1 in ground[j - 1][i + 1:]
                    if up == 1 and up_end == False and (1 not in ground[j]):  #上項、上項之後的項，之前的項
                        ground[j][i] = 1
                    else:
                        ground[j][i] = 0
                    
                elif (i == size - 1 or i == -1) and j != 0:  #排尾(非首行)
                    up = ground[j - 1][i]
                    if up == 1 and (1 not in ground[j]):  #上項、後項
                        ground[j][i] = 1
                    else:
                        ground[j][i] = 0
                        
                else:  #j=0
                    ground[0][i] = 0
                """#"""
        i += 1            
    #print(ground)


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





