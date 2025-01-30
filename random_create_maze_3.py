# 造迷宮
# tree
from itertools import count as itertools__count
import random




class __point():
    """
        組成支鏈(branch)的基本結構
        會直接放在迷宮的ground上

        Data:
        有3個種類(type) [start(1), middle(0), end(-1)]
    ----有指向性 [up(0), right(1), down(2), left(3)]，指向start----
        紀錄上一個point(previous_point)，有點像link_list。沒有就是None
        紀錄下一個point(next_point)，有點像link_list。沒有就是None
        所在支鏈編號(branch_number)
    """

    branch2io = dict()  # {branch_number : io_number}

    def __init__(self, type_, previous_point, branch_number):
        self.__type = type_  # 種類
        self.__previous_point = previous_point  # 上一個point
        self.__next_point = None  # 下一個point
        self.__branch_number = branch_number  # 所在支鏈編號
    
    def set_next_point(self, next_point):
        """ 紀錄下一個point """
        self.__next_point = next_point

    # previous_point = property(lambda self: self.__previous_point)  # 上一個point
    # next_point = property(lambda self: self.__next_point)  # 下一個point
    branch_number = property(lambda self: self.__branch_number)  # 所在支鏈編號
    io_number = property(lambda self: branch2io[self.__branch_number])  # point連接到的出入口編號

    def branch_start(self):
        """ 取得支鏈開頭的point """
        if self.__previous_point != None:
            return self.__previous_point.branch_start()
        else:
            return self
    
    def branch_end(self):
        """ 取得支鏈結尾的point """
        if self.__next_point != None:
            return self.__next_point.branch_end()
        else:
            return self
    

class __branches():
    """
        製造branch用
    """
    def __init__(self, xd, yd, ground):
        # """ 方便存取資料用，一個maze只需一個，不用每條branch都一個 """
        self.__xd = xd
        self.__yd = yd
        self.__ground = ground  # address

    def __check(self, x, y, number, check_center_TF = True):
        """
            檢查周圍point的number，如果io_number同就"+1"，不同就"+10"
            回傳：
                (-1, ): 不能走
                (count, ): 附近有幾個相同io_number的point
                (count, io_number): 附近有幾個相同io_number的point + 10, 碰到的不同的io_number
        """
        if (x < self.__xd and x >= 0) and (y < self.__yd and y >= 0) and self.__ground[y][x].io_number >= 0:
           # 在範圍內                                                    # 檢查是否為-1
            if check_center_TF and self.__ground[y][x].io_number == number:  # 檢查數字是否相同
                return (-1, )
            count = 0
            for x_, y_ in self.get_cross_pos(x, y):
                if self.__ground[y_][x_].io_number == number:  #檢查是否碰到同number
                    count += 1
            for x_, y_ in self.get_cross_pos(x, y, True):
                if self.__ground[y_][x_].io_number > 0 and self.__ground[y_][x_].io_number != number:  #檢查是否需要exchange
                    count += 10
                    return (count, self.__ground[y_][x_].io_number)
            return (count, )
        return (-1, )

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

    def exchange():
        pass

    @staticmethod
    def get_cross_pos(x, y, center_TF = False):  # (中)上右下左的資料
        if center_TF == False:
            return iter(((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)))
        else:
            return iter(((x, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)))


class maze():
    """
        造出迷宮主體用

        Data:
        迷宮的二維串列(ground)
        出入口(io)
        branch計數器(branch_counter)
    """
    def __init__(self, xd, yd, ground_generate = lambda x, y: 0):
        self.__xd = xd
        self.__yd = yd
        self.__ground = list()
        self.__branch_generator = __branches(self.__xd, self.__yd, self.__ground)

    ground = property(lambda self: [[i.io_number for i in j[:-1]] for j in self.__ground[:-1]])
    
    def __find():
        pass

    def create_random_maze():
        pass

