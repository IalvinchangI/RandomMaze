# 新增結構、物件導向
import random
import copy
import turtle
import time


class maze():
    def __init__(self, ground = [[0]], start = []):
        # 只是存ground用的
        self.xd = len(ground[0])
        self.yd = len(ground)
        self.ground = ground
        self.start = start  # 第1個是入口，其他都是出口
        self.auto_setting()
    
    def auto_setting(self):
        # 增加外框 (為get_cross_pos準備)
        for A in self.ground:
            A.append(0)
        self.ground.append([0] * (self.xd + 1))
        # 設定好隨機路徑相關變數
        self.position = {self.ground[i[1]][i[0]]:[i] for i in self.start}
        self.Number = sorted(list(self.position))
        self.max_number = self.Number[-1] if self.Number else 0

    '''
    def add_struct(self, x, y, number, struct):
        """
        可加，就加struct
        不可加，就加(x, y)
        """
        # struct === obj
        ok = self.__check_struct(x, y, number, struct)
        if ok[0]:
            print(True)
            for number_s_n, become_list in enumerate(ok[3]):
                number_s = struct.Number[number_s_n]
                if len(become_list) > 1:  # 有碰到很多東西
                    if 1 in become_list:
                        number = 1
                    else:
                        number = become_list[0]  # become的第1個是"要變成的"
                    for i in range(1, len(become_list)):
                        self.__exchange(become_list[i], number)
                elif len(become_list) == 1:  # 有碰到1個東西
                    number = become_list[0]
                else:  # 沒有碰到東西
                    self.max_number += 1
                    number = self.max_number
                    self.Number.append(number)
                    self.position[number] = []
                for (sx, sy), (gx, gy) in zip(ok[1][number_s], ok[2][number_s_n]):  # 把struct印到ground上
                    if struct.ground[sy][sx] == number_s:
                        self.ground[gy][gx] = number
                        self.position[number].append((gx, gy))
        else:
            print(False)
            self.ground[y][x] = number
            self.position[number].append((x, y))
    
    def __check_struct(self, x, y, number, struct):
        # struct === obj
        S = copy.deepcopy(struct.ground)
        save_s = copy.deepcopy(struct.position)
        save_g = [[(x + struct.start[i][0] - struct.start[0][0], y + struct.start[i][1] - struct.start[0][1])] for i in range(len(struct.Number))]  # <<< enumerate(self.Number)
        # save_self_pos = [[(x + pos[0] - struct.start[0][0], y + pos[1] - struct.start[0][1]) for pos in struct.position[i]] for i in struct.Number]
        # follow_numbers = []
        become = []  # become的第1個是"要變成的"
        for i in range(len(struct.Number)):
            become.append([])
        try:
            for number_s_n, number_s in enumerate(struct.Number):  # change
                i = 0
                while len(save_s[number_s]) > i:
                    print(i)
                    sx, sy = save_s[number_s][i]
                    gx, gy = save_g[number_s_n][i]
                    for x_, y_ in self.get_cross_pos(0, 0):
                        # struct內
                        if (sx + x_ < struct.xd and sx + x_ >= 0) and (sy + y_ < struct.yd and sy + y_ >= 0):
                            if S[sy + y_][sx + x_] == 0 or S[sy + y_][sx + x_] != number_s:  #為0或不為nomber_s就不用檢查ground合不合了
                                continue
                        elif (sx + x_ > struct.xd and sx + x_ < -1) and (sy + y_ > struct.yd and sy + y_ < -1):
                            continue
                        # ground內
                        gx_, gy_ = gx + x_, gy + y_
                        if (gx_ >= self.xd and gx_ < 0) and (gy_ >= self.yd and gy_ < 0):
                            raise Exception("can't add struct")
                        if self.ground[gy_][gx_] in become[number_s_n - 1]:
                            raise Exception("can't add struct")
                        if (self.ground[gy_][gx_] not in become[number_s_n - 1]) and (self.ground[gy_][gx_] != 0):
                            # if follow_numbers:  # 碰過東西了  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                            become[number_s - 1].append(self.ground[gy_][gx_])
                            # follow_numbers.append(self.ground[gy_][gx_])
                        save_s[number_s].append((sx + x_, sy + y_))
                        save_g[number_s_n].append((gx_, gy_))
                        S[sy + y_][sx + x_] = 0
                    i += 1
                # follow_numbers = []
        except:
            return (False, None, None, None)
        else:
            del save_s[struct.Number[0]][0]
            del save_g[0][0]
            return (True, save_s, save_g, become)
    '''

    def add_struct(self, x, y, struct, make_x_y_TF = False):
        """ (x, y) 不能有 number """
        ok = self.__check_struct(x, y, struct)
        # ok[1] = become_s_to_g,  ok[2] = S_range,  ok[3] = save_struct_pos
        if ok[0]:  # 放置結構
            # self exchange
            for become_key in ok[1]:
                become_list = ok[1][become_key]
                if not become_list:  # new_number
                    self.max_number += 1
                    self.position[self.max_number] = []
                    self.Number.append(self.max_number)
                    become_list.append(self.max_number)
                elif 1 in become_list:
                    become_list.remove(1)
                    for become in become_list:
                        self.__exchange(become, 1)
                    become_list.insert(0, 1)
                else:
                    for delete in become_list[1:]:
                        self.__exchange(delete, become_list[0])
            # struct 印到 self 上
            for sy in range(struct.yd):
                gy = y + sy - struct.start[0][1]
                for sx in range(struct.xd):
                    gx = x + sx - struct.start[0][0]
                    if ok[2][sy][sx] == 2:
                        if struct.ground[sy][sx] > 0:
                            self.ground[gy][gx] = ok[1][struct.ground[sy][sx]][0]
                        else:
                            self.ground[gy][gx] = 0
                    if struct.ground[sy][sx] == -1:
                        self.ground[gy][gx] = -1
            # 新增 position
            for frame_key in ok[3]:
                position = []
                for sx, sy in ok[3][frame_key]:
                    position.append((x + sx - struct.start[0][0], y + sy - struct.start[0][1]))
                self.position[ok[1][frame_key][0]] += position
        else:  # 放置點
            if make_x_y_TF:
                become = 0
                for cross_pos_x, cross_pos_y in self.get_cross_pos(x, y):
                    if self.ground[cross_pos_y][cross_pos_x] > 0:
                        if not become:
                            become = self.ground[cross_pos_y][cross_pos_x]
                        else:
                            break
                else:
                    if become:
                        self.ground[y][x] = become
                        self.position[become].append((x, y))
                    else:
                        self.max_number += 1
                        self.Number.append(self.max_number)
                        self.ground[y][x] = self.max_number
                        self.position[self.max_number] = [(x, y)]

    def __check_struct(self, x, y, struct):
        def save_pos(pos):  # save struct 的 number 和 pos
            if pos:
                if S[pos[1]][pos[0]] in save_struct_pos:
                    save_struct_pos[S[pos[1]][pos[0]]].append(pos)
                else:
                    save_struct_pos[S[pos[1]][pos[0]]] = [pos]
        # 檢查是否超出self的範圍
        if (x - struct.start[0][0] < 0 or x + (struct.xd - 1) - struct.start[0][0] >= self.xd) or \
           (y - struct.start[0][1] < 0 or y + (struct.yd - 1) - struct.start[0][1] >= self.yd):
            return (False,)
        S = struct.ground
        G = self.ground
        # 找出邊框、檢查struct是否和self重和
        save_struct_pos = dict()  # key存struct的number，value存struct的pos
        first_x = [None] * struct.yd  # 最左
        last_x = [None] * struct.yd  # 最右
        first_y = [None] * struct.xd  # 最上
        last_y = [None] * struct.xd  # 最下
        for sy in range(struct.yd):
            for sx in range(struct.xd):
                # 找出邊框
                if S[sy][sx] > 0:
                    if not first_x[sy]: first_x[sy] = (sx, sy)
                    if not first_y[sx]: first_y[sx] = (sx, sy)
                    last_x[sy] = (sx, sy)
                    last_y[sx] = (sx, sy)
            save_pos(first_x[sy])
            save_pos(last_x[sy])
        tuple(map(save_pos, first_y))
        tuple(map(save_pos, last_y))
        # 標明struct範圍 (first_x, last_x, first_y, last_y)
        S_range = []
        for sy in range(struct.yd):
            gy = y + sy - struct.start[0][1]
            S_range.append([0] * struct.xd)
            for sx in range(struct.xd):
                gx = x + sx - struct.start[0][0]
                if first_x[sy]:
                    if first_x[sy][0] <= sx and last_x[sy][0] >= sx:
                        S_range[sy][sx] += 1
                if first_y[sx]:
                    if first_y[sx][1] <= sy and last_y[sx][1] >= sy:
                        S_range[sy][sx] += 1
                # struct是否和self重和
                if S_range[sy][sx] == 2 and G[gy][gx] != 0:
                    return (False,)
            S_range[sy].append(0)
        S_range.append([0] * struct.xd)
        # 確認外部沒有多連
        become_s_to_g = dict()  # 用key、value來處理struct對self的number變化
        for number_Pos in save_struct_pos.items():
            become = []
            for sx, sy in number_Pos[1]:
                for cross_pos_x, cross_pos_y in self.get_cross_pos(sx, sy):
                    if S_range[cross_pos_y][cross_pos_x] == 2:
                        continue
                    gn = G[y + cross_pos_y - struct.start[0][1]][x + cross_pos_x - struct.start[0][0]]
                    if gn not in become:
                        if gn != 0:
                            become.append(gn)
                    else:
                        return (False,)
            become_s_to_g[number_Pos[0]] = become  # become的第1個是"要變成的"
        return (True, become_s_to_g, S_range, save_struct_pos)

    def get_cross_pos(self, x, y, center_TF = False):
        # 上右下左(中)的資料
        #'''
        if center_TF:
            return ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y), (x, y))
        else:
            return ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y))
        '''
        yield (x, y + 1)
        yield (x + 1, y)
        yield (x, y - 1)
        yield (x - 1, y)
        if check_exchage_TF == False:
            yield (x, y)
        #'''

    def __check(self, x, y, number):
        count = 0
        become = -1
        if (x < self.xd and x >= 0) and (y < self.yd and y >= 0) and self.ground[y][x] >= 0:
            #檢查是否為-1
            #檢查是否碰到同number
            for x_, y_ in self.get_cross_pos(x, y, True):
                if self.ground[y_][x_] == number:
                    count += 1
            #檢查是否需要exchange
            for x_, y_ in self.get_cross_pos(x, y):
                if self.ground[y_][x_] != number and self.ground[y_][x_] > 0:
                    count += 10
                    become = self.ground[y_][x_]
                    break
        return (count, become)

    def __road(self, x, y, number):
        # 走路
        position = self.position[number]
        turn = [0, 1, 2, 3]  #[up, right, down, left]
        ok = (0, -1)
        while ok[0] != 11 and turn != []:
            r = random.choice(turn)   #r=random
            if r == 0:  #y + 1
                ok = self.__check(x, y + 1, number)
                if ok[0] == 1 or ok[0] == 11:
                    y += 1
                    self.ground[y][x] = number
                    position.append((x, y))
                    turn = [0, 1, 2, 3]
                else:
                    turn.remove(r)
            elif r == 1:  #x + 1
                ok = self.__check(x + 1, y, number)
                if ok[0] == 1 or ok[0] == 11:
                    x += 1
                    self.ground[y][x] = number
                    position.append((x, y))
                    turn = [0, 1, 2, 3]
                else:
                    turn.remove(r)
            elif r == 2:  #y - 1
                ok = self.__check(x, y - 1, number)
                if ok[0] == 1 or ok[0] == 11:
                    y -= 1
                    self.ground[y][x] = number
                    position.append((x, y))
                    turn = [0, 1, 2, 3]
                else:
                    turn.remove(r)
            elif r == 3:  #x - 1
                ok = self.__check(x - 1, y, number)
                if ok[0] == 1 or ok[0] == 11:
                    x -= 1
                    self.ground[y][x] = number
                    position.append((x, y))
                    turn = [0, 1, 2, 3]
                else:
                    turn.remove(r)
            
        if ok[0] == 11:  #碰到的數字不同時
            return (1, ok[1])
        else:
            return (0, ok[1])

    def __find(self, number):
        position = self.position[number]
        x = -1
        y = -1
        while position != []:
            r_position = random.choice(position)   #r=random
            change_ok = self.__check(r_position[0], r_position[1], number)
            if change_ok[0] == 3 or change_ok[0] == 4:
                x, y = r_position
                position.remove(r_position)
                break
            position.remove(r_position)
        return (x, y)

    def __exchange(self, delete, become):
        """當不同數字連在一起時，改成相同數字，並整合position"""
        for l in range(self.yd):
            while delete in self.ground[l]:
                place = self.ground[l].index(delete)
                self.ground[l].remove(delete)
                self.ground[l].insert(place, become)
        self.position[become] += self.position[delete]
        # 有可能position先空，但還沒碰到別人，所以只能這裡刪
        del self.position[delete]
        self.Number.remove(delete)
    
    def create_random_maze(self):
        """製作隨機迷宮"""
        start = [self.position[i][0] for i in self.Number]
        while True:
            if self.position[1] == []:
                break
            else:
                for list_n, number in enumerate(self.Number):
                    x, y = start[list_n]
                    change = self.__road(x, y, number)
                    if change[0] == 1:
                        if number == 1:
                            self.__exchange(change[1], 1)
                        else:
                            self.__exchange(number, change[1])

                for list_n, number in enumerate(self.Number):
                    start[list_n] = self.__find(number)

def create_list2(xd, yd):
    A = [0] * (xd)
    G = []
    for i in range(yd):
        G.append(A[:])
    return G

def create_in_out(maze_obj, ending, random_TF = True, construct_structs = None):
    # 製作出入口
    for number in range(1, ending + 2):
        while True:
            if random_TF:  #隨機選
                x = random.randint(0, maze_obj.xd - 1)
                y = random.randint(0, maze_obj.yd - 1)
                pos = (x, y)
                if pos in maze_obj.start:
                    continue
                if construct_structs:  #隨機放置結構
                    struct_number = random.randint(0, len(construct_structs) - 1)
            else:  #手動選
                i = 1
                try:
                    if i == 1:
                        x, y = eval(input("%d 號出入口，座標 x, y :" % number))
                        pos = (int(x), int(y))
                        i += 1
                    if i == 2 and construct_structs:  # 放置結構
                        struct_number = eval(input("%d 號出入口，放置結構的編號 :" % number))
                except ValueError:
                    print("資料型態錯誤，請重新輸入")
                    continue
                if (pos[0] < 0) or (pos[1] < 0) or (pos[0] >= maze_obj.xd) or (pos[1] >= maze_obj.yd):
                    print("座標超出範圍，請重新輸入")
                    continue
                if pos in maze_obj.start:
                    print("座標重複，請重新輸入")
                    continue
            maze_obj.start.append(pos)
            if construct_structs:
                maze_obj.add_struct(x, y, construct_structs[struct_number], True)
            else:
                maze_obj.ground[y][x] = number
            break
    if not construct_structs:
        maze_obj.auto_setting()
        

#畫迷宮
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

def draw(maze_obj, distance):
    x_side = maze_obj.xd * distance
    y_side = maze_obj.yd * distance
    #畫出入口
    turtle.penup()
    for i in range(len(maze_obj.start)):
        turtle.setposition(-1 * x_side / 2 + maze_obj.start[i][0] * distance + 1, -1 * y_side / 2 + maze_obj.start[i][1] * distance + 1)
        if i == 0:
            turtle.color(0, 1, 0)
        else:
            turtle.color(1, 0, 0)
        block(distance - 2)
    
    #畫路
    turtle.color(0, 0, 0)
    turtle.setposition(-1 * x_side / 2, -1 * y_side / 2)
    for y in range(maze_obj.yd):
        for x in range(maze_obj.xd):
            if maze_obj.ground[y][x] <= 0:
                block(distance)
                # maze_obj.ground[y][x] = 0
            else:
                turtle.forward(distance)
        changeline(maze_obj.xd, distance)
    
    #畫框
    turtle.pendown()
    for i in range(2):
        turtle.forward(x_side)
        turtle.right(90)
        turtle.forward(y_side)
        turtle.right(90)
    turtle.penup()

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

turtle.tracer(0, 0)

A_55 = [[-1, -1, -1, -1, -1], 
        [-1, 1, 1, 1, -1], 
        [-1, 1, -1, 1, 0], 
        [-1, 1, 1, 1, -1], 
        [-1, -1, -1, -1, -1]]

B_55 = [[1, 1, 1, 1, 1], 
        [-1, -1, -1, -1, -1], 
        [2, 2, 2, -1, 3], 
        [2, -1, -1, -1, 3], 
        [2, 2, 2, 3, 3]]

A_77 = [[-1, -1, -1, 0, -1, -1, -1], 
        [-1, 1, 1, 1, 1, 1, -1], 
        [-1, 1, -1, -1, -1, 1, -1], 
        [-1, 1, -1, -1, -1, 1, 0], 
        [-1, 1, -1, -1, -1, 1, -1], 
        [-1, 1, 1, 1, 1, 1, -1], 
        [-1, -1, -1, -1, -1, -1, -1]]


construct_structs = [maze(copy.deepcopy(A_55), [(1, 1)]), maze(copy.deepcopy(B_55)[::-1], [(0, 0)]), maze(copy.deepcopy(A_77), [(1, 1)])]

ground = maze(create_list2(xd, yd))
create_in_out(ground, ending, random_TF, construct_structs)
# create_in_out(ground, ending, random_TF)

ground.create_random_maze()

print("製作迷宮時間：", time.process_time())

draw(ground, distance)

print("繪製迷宮時間：", time.process_time())
turtle.done()

