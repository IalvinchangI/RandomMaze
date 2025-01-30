# 造迷宮
# tree
from itertools import count as itertools__count  # generate new branch_number
from itertools import deque  # store positions which have not been checked
import random



class __branch():
    """
        支鏈(branch)，或者說路
        會直接放在迷宮的ground上

        Data:
        紀錄上一個branch(previous_branch)，有點像link_list。沒有就是None
        紀錄下一個branch(next_branch)，有點像link_list。沒有就是None
        所在支鏈編號(branch_number)
    """
    def __init__(self, belong, previous_branch, branch_number):
        self.__belong = belong  # 存在哪個maze物件
        self.__previous_branch = previous_branch  # 上一個branch
        self.__next_branch = None  # 下一個branch
        self.branch_number = branch_number  # 所在支鏈編號
    
    def set_next_branch(self, next_branch):
        """ 紀錄下一個branch """
        self.__next_branch = next_branch

    previous_branch = property(lambda self: self.__previous_branch if self.__previous_branch.branch_number == self.branch_number else None)  # 上一個branch
    # next_branch = property(lambda self: self.__next_branch)  # 下一個branch
    io_number = property(lambda self: self.__belong.branch2io[self.__branch_number])  # branch連接到的出入口編號
    

class __node(__branch):
    """
        節點(node)，可能是岔路口or死路
        branch的進階版
        會在支鏈的尾
        會直接放在迷宮的ground上

        Data:
        紀錄上一個node(previous_node)，有點像link_list。沒有就是None
        紀錄上一個branch(previous_branch)，有點像link_list。沒有就是None
        紀錄下一個node(next_node)，有點像link_list。沒有就是None。會有3個
        紀錄下一個branch(next_branch)，有點像link_list。沒有就是None。會有3個
        所在支鏈編號(branch_number)
    """
    def __init__(self, belong, previous_node, previous_branch, branch_number):
        self.__belong = belong  # 存在哪個maze物件
        self.__previous_node = previous_node  # 上一個node
        self.__previous_branch = previous_branch  # 上一個branch
        self.__next_node = list()  # 下一個node
        self.__next_branch = list()  # 下一個branch
        self.branch_number = branch_number  # 所在支鏈編號

    def set_next_branch(self, next_branch):
        """ 紀錄下一個branch """
        self.__next_branch.append(next_branch)

    def set_next_node(self, next_node):
        """ 紀錄下一個node """
        self.__next_node.append(next_node)
    
    
    previous_node = property(lambda self: self.__previous_node)  # 上一個node
    # next_node = property(lambda self: self.__next_node[:])  # 下一個node
    # next_branch = property(lambda self: self.__next_branch[:])  # 下一個branch

    # def branch_start(self):
    #     """ 取得支鏈開頭的point """
    #     if self.__previous_point != None:
    #         return self.__previous_point.branch_start()
    #     else:
    #         return self
    
    # def branch_end(self):
    #     """ 取得支鏈結尾的point """
    #     if self.__next_point != None:
    #         return self.__next_point.branch_end()
    #     else:
    #         return self
    

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

            Return:
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
    branch2io = dict()  # {branch_number : io_number}
    
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

