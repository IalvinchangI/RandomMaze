#造迷宮
from collections import defaultdict
from itertools import count as itertools__count
from random import randint, choice
from copy import deepcopy

import logging
logging.basicConfig(level=logging.DEBUG, format=">>> %(levelname)s\t%(message)s")
logging.disable(logging.CRITICAL)

def debug_log(func):
    def function(*tup, **dic):
        logging.debug(f"{func.__name__}\tinput: {tup[1:]}, {dic}")
        out = func(*tup, **dic)
        logging.debug(f"{func.__name__}\toutput: {out}")
        return out
    return function

class maze():
    # 製作時 ground上 數字的定義: road >0; nothing =0; wall =-1(無法改成road)
    # 輸出時 ground上 數字的定義: road >0; wall <=0

    __name2struct = dict()  # install 的結構

    @classmethod
    def install_struct(cls, struct_name, struct_obj):
        cls.__name2struct[struct_name] = struct_obj
    
    @classmethod
    def uninstall_struct(cls, struct_name):
        del cls.__name2struct[struct_name]
    
    @staticmethod
    def create_list2(xd, yd, value=0):
        """ 製作2維陣列 """
        A = [value] * xd
        G = []
        for i in range(yd):
            G.append(A[:])
        return G

    def __init__(self, ground, *entrances):
        # 只是存ground用的
        self.__xd = len(ground[0])
        self.__yd = len(ground)
        self.__ground = deepcopy(ground)
        # 先宣告各變數
        self.__entrance = list()  # 第1個是入口，其他都是出口
        self.__first_start = list()  # 所有非create_random_maze生成的點
        self.__position = defaultdict(list)
        self.__Number = list()
        self.__max_number_counter = itertools__count(1)  # 計數器，要使用next()取值
        self.__struct_pos2name = dict()
        # 增加外框 (為get_cross_pos準備)
        for A in self.__ground:
            A.append(0)
        self.__ground.append([0] * (self.__xd + 1))
        # 設定出入口
        for pos in entrances:
            self.add_entrance(pos)
    
    # entrance
    entrance = property(lambda self: self.__entrance[:])
    
    def __set_first_start(self, *positions, entrance_append_TF = True, change_ground_number_TF = True):
        """ 增加出入口數，並新增其number和position變數，(且將ground上的那格標上number)。允許傳入多個座標 """
        max_number = self.__max_number
        self.__Number.append(max_number)
        for pos in positions:
            if entrance_append_TF:
                self.__entrance.append(pos)
            self.__first_start.append(pos)
            self.__position[max_number].append(pos)
            if change_ground_number_TF:  # 將ground上的那格標上number  # 若該格本身就不是0，更改number可達到多條路徑的目的
                self.__ground[pos[1]][pos[0]] = max_number
    
    def add_entrance(self, pos):
        """ 增加出入口數，並新增其number和position變數，且將ground上的那格標上number。會檢查是否合理 """
        # 檢查增加的出入口是否合理
        if (pos[0] < 0) or (pos[1] < 0) or (pos[0] >= self.__xd) or (pos[1] >= self.__yd):
            raise Exception("座標超出範圍")
        if pos in self.__entrance:
            raise Exception("座標重複")
        if self.__ground[pos[1]][pos[0]]:  # 先檢測該格是否是路
            logging.warning(f"{pos}")
            raise Exception("已有路徑通過，無法設置出入口")
        if self.__check(*pos, (self.__Number[-1] + 1) if self.__Number else 1)[0] != 0:  # 再檢測周圍是否是路
            raise Exception("已有路徑從旁通過，無法設置出入口")
        # 增加出入口數，並新增其number和position變數，且將ground上的那格標上number
        self.__set_first_start(pos)

    @property
    def __max_number(self):
        """ 專門為了回傳新的max_number的值。只能class內呼叫 """
        return next(self.__max_number_counter)
    
    # ground, xd, yd getter
    ground = property(lambda self: [self.__ground[i][:-1] for i in range(self.__yd)])  # 回傳值會把多餘的外框裁掉
    xd = property(lambda self: self.__xd)
    yd = property(lambda self: self.__yd)

    def delete(self):
        for i in range(len(self.__ground)):
            del self.__ground[0]

    # random maze
    def get_cross_pos(self, x, y, center_TF = False):  # (中)上右下左的資料
        if center_TF:
            return iter(((x, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)))
        else:
            return iter(((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)))

    @debug_log
    def __check(self, x, y, number, check_center_TF = True):
        if (x < self.__xd and x >= 0) and (y < self.__yd and y >= 0) and self.__ground[y][x] >= 0:
           # 在範圍內                                                    # 檢查是否為-1
            if check_center_TF and self.__ground[y][x] == number:  # 檢查數字是否相同
                return (-1, )
            count = 0
            for x_, y_ in self.get_cross_pos(x, y):
                if self.__ground[y_][x_] == number:  #檢查是否碰到同number
                    count += 1
            for x_, y_ in self.get_cross_pos(x, y, True):
                if self.__ground[y_][x_] > 0 and self.__ground[y_][x_] != number:  #檢查是否需要exchange
                    count += 10
                    return (count, self.__ground[y_][x_])
            return (count, )
        return (-1, )

    @debug_log
    def __road(self, x, y, number):
        """ 走出一整條同number的路。回傳(是否要exchange, excnange的數字) """
        position = self.__position[number]
        pos = None
        x_, y_ = x, y
        turn = [0, 1, 2, 3]  #[up, right, down, left]
        ok = (0, )
        while True:
            r = choice(turn)   #r=random
            if r == 0:  #y + 1
                x_, y_ = x, y + 1
            elif r == 1:  #x + 1
                x_, y_ = x + 1, y
            elif r == 2:  #y - 1
                x_, y_ = x, y - 1
            elif r == 3:  #x - 1
                x_, y_ = x - 1, y
            
            ok = self.__check(x_, y_, number)
            if ok[0] == 1 or ok[0] == 11:
                if pos:  # 使末端格的座標無法儲存，因為一定不能走
                    position.append(pos)
                x, y = pos = (x_, y_)
                self.__ground[y][x] = number
                if ok[0] == 11:  # 碰到的數字不同時，結束
                    position.append(pos)
                    return (1, ok[1])
                else:
                    turn = [0, 1, 2, 3]
            else:
                turn.remove(r)
                if turn == []:  # 結束
                    return (0, )
    
    def __find(self, number):
        position = self.__position[number]
        while position != []:
            r_position = choice(position)   #r=random
            change_ok = self.__check(r_position[0], r_position[1], number, check_center_TF=False)
            if change_ok[0] == 2 or change_ok[0] == 3 or r_position in self.__first_start:
                position.remove(r_position)
                return r_position
            position.remove(r_position)
        return (-1, -1)

    def __exchange(self, delete, become):
        """當不同數字連在一起時，改成相同數字，並整合position"""
        for l in range(self.__yd):
            while delete in self.__ground[l]:
                place = self.__ground[l].index(delete)
                self.__ground[l].remove(delete)
                self.__ground[l].insert(place, become)
        self.__position[become] += self.__position[delete]
        # 有可能position先空，但還沒碰到別人，所以只能這裡刪
        del self.__position[delete]
        self.__Number.remove(delete)
    
    # struct
    def __check_struct(self, sPos, gPos, struct_obj):
        """ 檢查是否能把結構安插進迷宮中。檢查項目：scale、entrance。回傳(檢查結果, struct2maze_x, struct2maze_y) """
        struct2maze_x = {i:(gPos[0] - sPos[0] + i) for i in range(struct_obj.xd)}
        struct2maze_y = {i:(gPos[1] - sPos[1] + i) for i in range(struct_obj.yd)}
        if (struct2maze_x[0] < 0) or (struct2maze_x[struct_obj.xd - 1] >= self.__xd) or \
           (struct2maze_y[0] < 0) or (struct2maze_y[struct_obj.yd - 1] >= self.__yd):  # 確認有無超界
            return (False, )
        struct_ground = struct_obj.ground
        
        # 確認範圍可否安插進去
        struct_scale = struct_obj.scale
        for sy in range(struct_obj.yd):
            gy = struct2maze_y[sy]
            for sx in range(struct_obj.xd):
                gx = struct2maze_y[sx]
                if struct_scale[sy][sx] == 1 and self.__ground[gy][gx] != 0:
                    return (False, )
        
        # 確認出入口可否安插進去
        for sx, sy in struct_obj.entrance:
            gx = struct2maze_x[sx]
            gy = struct2maze_y[sy]
            if self.__ground[gy][gx] != 0 and (gx, gy) != gPos:
                return (False, )
        
        del struct_ground
        return (True, struct2maze_x, struct2maze_y)
    
    def place_struct_scale(self, x, y, struct_name, same_entrance_number_TF = False, manual_entrance_end_index = 0):
        """ 在迷宮中安插結構所占的格子。回傳成功與否。manual_entrance_end_index 為串列切片的尾 """
        try:
            struct_obj = self.__name2struct[struct_name]
        except:
            raise Exception("結構尚未載入")
        if struct_obj.xd > self.__xd or struct_obj.yd > self.__yd:  # 結構比迷宮大
            return False
        
        if manual_entrance_end_index == 0:  # 自動選
            entrance_choice = struct_obj.entrance
            for i in range(len(entrance_choice)):
                struct_pos = choice(entrance_choice)
                ok = self.__check_struct(struct_pos, (x, y), struct_obj)
                if ok[0]:  # 能把結構安插進迷宮
                    break
                entrance_choice.remove(struct_pos)
            else:
                return False
        else:  # 手動選
            entrance_choice = struct_obj.entrance[:manual_entrance_end_index]
            for struct_pos in entrance_choice:
                ok = self.__check_struct(struct_pos, (x, y), struct_obj)
                if ok[0]:  # 能把結構安插進迷宮
                    break
            else:
                return False
        
        # 成功
        del entrance_choice
        # 放置出入口
        if same_entrance_number_TF:
            self.__set_first_start(*(set(map(lambda pos: (ok[1][pos[0]], ok[2][pos[1]]), struct_obj.entrance)) - set(self.__entrance)), entrance_append_TF=False)
        else:
            for sx, sy in struct_obj.entrance:
                pos = (ok[1][sx], ok[2][sy])
                if pos not in self.__entrance:
                    self.__set_first_start(pos, entrance_append_TF=False)  # 不在self.__entrance那新增出入口
        # 安插結構所占的格子
        struct_scale = struct_obj.scale
        for sy in range(struct_obj.yd):
            gy = ok[2][sy]
            for sx in range(struct_obj.xd):
                gx = ok[1][sx]
                if struct_scale[sy][sx] == 1:
                    self.__ground[gy][gx] = -1
        self.__struct_pos2name[(ok[1][0], ok[2][0])] = struct_name
        return True
    
    def place_struct(self):
        """ 把結構安插進迷宮中 """
        for struct_pos in self.__struct_pos2name:
            struct_obj = self.__name2struct[self.__struct_pos2name[struct_pos]]
            struct_ground = struct_obj.ground
            for sy in range(struct_obj.yd):
                for sx in range(struct_obj.xd):
                    if struct_ground[sy][sx] != 0:
                        self.__ground[struct_pos[1] + sy][struct_pos[0] + sx] = struct_ground[sy][sx]
    
    # create
    def create_random_maze(self):
        """製作隨機迷宮"""
        start = list(map(lambda pos: (self.__ground[pos[1]][pos[0]], pos), self.__first_start[:]))  # 各非create_random_maze生成的點
        while True:
            if self.__position[1] == []:  # 結束
                break
            else:
                for number, (x, y) in start:  # 各編號(or 非create_random_maze生成的點)畫路
                    if number not in self.__Number:
                        continue
                    change = self.__road(x, y, number)
                    if change[0] == 1:
                        if number == 1:
                            self.__exchange(change[1], 1)
                        else:
                            self.__exchange(number, change[1])
                    # print_maze(self)
                
                for list_n, number in enumerate(self.__Number):  # 挑選各編號的下一個起始點
                    start[list_n] = (number, self.__find(number))
                for i in range(list_n + 1, len(start)):  # 刪掉多餘的點
                    del start[-1]


class maze_struct(maze):
    def __init__(self, ground, *entrance):
        super().__init__(ground, *entrance)
        self.__struct_setting()
    
    def __scale_entrance_check(self, x, y):
        """ 檢測struct的邊界和對外出口。回傳(是否有東西, 是否是entrance) """
        if self.__ground[y][x] != 0:  # 是否有東西
            if self.__ground[y][x] > 0:  # 是否是路
                for x_, y_ in self.get_cross_pos(x, y):
                    if self.__ground[y_][x_] == 0:  # 旁邊是否為nothing
                        return (True, True)  # << 有東西, 是entrance >>
            return (True, False)  # << 有東西, 不是entrance >>
        return (False, )  # << 沒東西 >>

    def __struct_setting(self):
        """ 將物件改成struct的形式，使其可以加入maze中。找出邊框和所有與外連接的部分 """
        self.__ground = self._maze__ground
        self.__scale = self.create_list2(self.xd, self.yd)  # 被struct邊界包圍的範圍
        self.__roads_number = self.create_list2(self.xd + 1, self.yd + 1)  # 被struct邊界包圍的範圍
        for y in range(self.yd):
            for x in range(self.xd):
                ok = self.__scale_entrance_check(x, y)
                if ok[0]:  # 該格有東西
                    if ok[1]:  # 該格是entrance
                        if (x, y) not in self._maze__entrance:  # 座標是否重複
                            self._maze__set_first_start((x, y), change_ground_number_TF=False)  # 不改變ground上的數字
                    else:
                        self.__scale[y][x] = 1  # 被struct邊界包圍的點
        
    scale = property(lambda self: [self.__scale[y][:] for y in range(self.yd)])
    roads = property(lambda self: [self.__roads_number[y][:-1] for y in range(self.yd)])  # 回傳值會把多餘的外框裁掉
    
    def create_random_maze(self):
        super().create_random_maze()
        self.__struct_setting()
    
    '''
    def __become_struct(self):  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<?
        """ 將物件改成struct的形式，使其可以加入maze中。找出邊框和所有與外連接的部分 """
        def set_range(now_x, now_y, first_x, first_y, last_x, last_y):
            """ 專門操作邊框串列(first...、last...)。只會更改(now_x, now_y)的那項。傳入 list的指標，直接進行變更 """
            if first_x[now_y] == None:
                first_x[now_y] = now_x
            if first_y[now_x] == None:
                first_y[now_x] = now_y
            last_x[now_y] = now_x
            last_y[now_x] = now_y
        def range_check(now, first, last):
            """ 專門操作範圍(...range)。若在範圍內，回傳1，反之，回傳0 """
            if first != None:
                if first <= now and last >= now:
                    return 1
            return 0
        # 找出邊框
        first_road_x = [None] * self.__yd  # 該橫列最左的邊框
        last_road_x = [None] * self.__yd  # 該橫列最右的邊框
        first_road_y = [None] * self.__xd  # 該直行最上的邊框
        last_road_y = [None] * self.__xd  # 該直行最下的邊框
        first_wall_x = [None] * self.__xd  # 該橫列-1的最左位置
        last_wall_x = [None] * self.__xd  # 該橫列-1的最右位置
        first_wall_y = [None] * self.__yd  # 該直行-1的最上位置
        last_wall_y = [None] * self.__yd  # 該直行-1的最下位置
        for y in range(self.__yd):
            for x in range(self.__xd):
                if self.__ground[y][x] > 0:  # 找出邊框(>0)
                    set_range(x, y, first_road_x, first_road_y, last_road_x, last_road_y)
                elif self.__ground[y][x] == -1:  # 找出-1
                    set_range(x, y, first_wall_x, first_wall_y, last_wall_x, last_wall_y)
                if x == self.__yd - 1 and last_wall_y[x] == None:  # 幫直行的範圍封尾
                    last_wall_y[x] = last_road_y[x]
            if last_wall_x[y] == None:  # 幫橫列的範圍封尾
                last_wall_x[y] = last_road_x[y]
        
        # # 儲存邊框上所有與外連接的座標  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<?
        # self.__struct_entrance_onFrame = defaultdict(list)  # key存struct的number，value存struct的pos
        # def store_pos(pos):
        #     """ store struct 的 number 和 pos """
        #     self.__struct_entrance_onFrame[self.__ground[pos[1]][pos[0]]].append(pos)
        
        # 標明struct範圍 (first_x, last_x, first_y, last_y)
        self.__road_range = list()  # 邊框(>0)包圍區塊
        self.__wall_range = list()  # -1包圍區塊
        self.__struct_range = self.create_list2(self.__xd + 1, self.__yd + 1)  # struct範圍。1: road_range; -1: wall_range
        for y in range(self.__yd):
            self.__road_range.append([0] * self.__xd)
            self.__wall_range.append([0] * self.__xd)
            for x in range(self.__xd):
                self.__road_range[y][x] += range_check(x, first_road_x[y], last_road_x[y])  # 橫列邊框
                self.__road_range[y][x] += range_check(y, first_road_y[x], last_road_y[x])  # 直行邊框
                self.__wall_range[y][x] += range_check(x, first_wall_x[y], last_wall_x[y])  # 橫列-1
                self.__wall_range[y][x] += range_check(y, first_wall_y[x], last_wall_y[x])  # 直行-1
                # struct範圍
                if self.__road_range[y][x] == 2:
                    self.__struct_range[y][x] = 1
                elif self.__wall_range[y][x] == 2:
                    self.__struct_range[y][x] = -1
    
    # ...range getter
    road_range = property(lambda self: [self.__road_range[y][:] for y in range(self.__yd)])  # 原則上，外部用不到
    wall_range = property(lambda self: [self.__wall_range[y][:] for y in range(self.__yd)])  # 原則上，外部用不到

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
                    self.__position[self.max_number] = []
                    self.__Number.append(self.max_number)
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
                gy = y + sy - struct.entrance[0][1]
                for sx in range(struct.xd):
                    gx = x + sx - struct.entrance[0][0]
                    if ok[2][sy][sx] == 2:
                        if struct.ground[sy][sx] > 0:
                            self.__ground[gy][gx] = ok[1][struct.ground[sy][sx]][0]
                        else:
                            self.__ground[gy][gx] = 0
                    if struct.ground[sy][sx] == -1:
                        self.__ground[gy][gx] = -1
            # 新增 position
            for frame_key in ok[3]:
                position = []
                for sx, sy in ok[3][frame_key]:
                    position.append((x + sx - struct.entrance[0][0], y + sy - struct.entrance[0][1]))
                self.__position[ok[1][frame_key][0]] += position
        else:  # 放置點
            if make_x_y_TF:
                become = 0
                for cross_pos_x, cross_pos_y in self.get_cross_pos(x, y):
                    if self.__ground[cross_pos_y][cross_pos_x] > 0:
                        if not become:
                            become = self.__ground[cross_pos_y][cross_pos_x]
                        else:
                            break
                else:
                    if become:
                        self.__ground[y][x] = become
                        self.__position[become].append((x, y))
                    else:
                        self.max_number += 1
                        self.__Number.append(self.max_number)
                        self.__ground[y][x] = self.max_number
                        self.__position[self.max_number] = [(x, y)]

    def __check_struct(self, gx, gy, struct, sx, sy):
        """ 輸入self座標(gx, gy)下的建構起點、struct物件和struct座標(sx, sy)下的建構起點。
        回傳是否可在self上建造、struct和self.ground的number對照表(number_s2g) """
        def save_pos(pos):  # save struct 的 number 和 pos
            if pos:
                if S[pos[1]][pos[0]] in save_struct_pos:
                    save_struct_pos[S[pos[1]][pos[0]]].append(pos)
                else:
                    save_struct_pos[S[pos[1]][pos[0]]] = [pos]
        # 檢查是否超出self的範圍
        if (gx - sx < 0 or gx - sx + (struct.xd - 1) >= self.__xd) or (gy - sy < 0 or gy - sy + (struct.yd - 1) >= self.__yd):
            return (False,)
        
        
        # 標明struct範圍 (first_x, last_x, first_y, last_y)
        S_range = []
        for sy in range(struct.yd):
            gy = y + sy - struct.entrance[0][1]
            S_range.append([0] * struct.xd)
            for sx in range(struct.xd):
                gx = x + sx - struct.entrance[0][0]
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
                    gn = G[y + cross_pos_y - struct.entrance[0][1]][x + cross_pos_x - struct.entrance[0][0]]
                    if gn not in become:
                        if gn != 0:
                            become.append(gn)
                    else:
                        return (False,)
            become_s_to_g[number_Pos[0]] = become  # become的第1個是"要變成的"
        return (True, become_s_to_g, S_range, save_struct_pos)
    '''

def create_in_out(maze_obj, ending, random_TF = True,):
    # 製作出入口
    for number in range(1, ending + 2):
        while True:
            if random_TF:  #隨機選
                x = randint(0, maze_obj.xd - 1)
                y = randint(0, maze_obj.yd - 1)
                pos = (x, y)
            else:  #手動選
                try:
                    x, y = eval(input("%d 號出入口，座標 x, y :" % number))
                    pos = (int(x), int(y))
                except ValueError:
                    print("資料型態錯誤，請重新輸入")
                    continue
            try:
                maze_obj.add_entrance(pos)
            except Exception as e:
                print(e if random_TF else (e + "，請重新輸入"))
                continue
            break


def debug_print_maze(func):
    def function(maze_obj):
        translate = {1:"　", 0:"██", -1:"▓▓"}
        ground = maze_obj.ground
        print("　　" + "".join([("%2d" % x) for x in range(maze_obj.xd)]))
        print("　　" + "▁" * maze_obj.xd * 2)
        for y in range(maze_obj.yd):
            print("%2d ▕" % y, end="")
            for x in range(maze_obj.xd):
                try:
                    print(translate[ground[y][x]], end="")
                except:
                    print("%2d" % ground[y][x], end="")
            print("▏")
        print("　　" + "▔" * maze_obj.xd * 2)
    return function

@debug_print_maze
def print_maze(maze_obj):
    ground = maze_obj.ground
    for y in range(maze_obj.yd):
        for x in range(maze_obj.xd):
            print("%2d" % ground[y][x], end=" ")
        print()


if __name__ == "__main__":
    from pprint import pprint
    logging.disable(logging.WARNING)
    a = True
    B_55 = [[ 1,  1,  1,  1,  1], 
            [-1, -1, -1, -1, -1], 
            [ 0,  0,  0, -1,  1], 
            [ 0, -1, -1, -1,  1], 
            [ 0,  0,  0,  1,  1]]

    A_77 = [[-1, -1, -1,  1, -1, -1, -1], 
            [-1,  1,  1,  1,  1,  1, -1], 
            [-1,  1, -1,  1, -1,  1, -1], 
            [ 1,  1,  1,  1,  1,  1,  1], 
            [-1,  1, -1,  1, -1,  1, -1], 
            [-1, -1,  0,  0,  0, -1, -1], 
            [-1, -1,  0, -1,  0, -1, -1]]
    test_A = maze_struct(A_77)
    test_B = maze_struct(B_55)
    # pprint(test_A.scale)
    # print(test_A.entrance)
    # pprint(test_B.scale)
    # print(test_B.entrance)
    maze.install_struct("A_77", test_A)
    maze.install_struct("B_55", test_B)
    while a:
        test = maze(maze.create_list2(20, 20))
        test.place_struct_scale(5, 5, "A_77", same_entrance_number_TF=True)
        test.place_struct_scale(14, 14, "B_55")
        create_in_out(test, 1)
        print_maze(test)
        print(test.entrance)
        print("-" * 50)
        test.create_random_maze()
        test.place_struct()
        print(test.xd, test.yd)
        print_maze(test)
        print(test.entrance)
        print("-" * 50)
        # print_maze(test_A)
        # pprint(A_77)
        # print_maze(test_B)
        # pprint(B_55)

        
        a = bool(int(input("continue? ")))
    

