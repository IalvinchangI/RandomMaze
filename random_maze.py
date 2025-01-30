# 新增GUI顯示、照片儲存
import random
import copy
import tkinter as tk
import time
from random_create_maze import maze, create_in_out



#畫迷宮
class show_maze():
    distance = 20
    pointer_size = 12
    pointer_padding = (distance - pointer_size) / 2
    flag_style = (
        (pointer_padding + 1, pointer_padding + 1 + pointer_size), (pointer_padding + 1 + pointer_size, pointer_padding + 1 + pointer_size), 
        (pointer_padding + 1 + pointer_size, pointer_padding + 1 + pointer_size - 2), (pointer_padding + 1 + pointer_size / 2 + 1, pointer_padding + 1 + pointer_size - 2), 
        (pointer_padding + 1 + pointer_size / 2 + 1, pointer_padding + 1 + pointer_size - 4), (pointer_padding + 1 + pointer_size, pointer_padding + 1 + pointer_size - 8), 
        (pointer_padding + 1 + pointer_size / 2 + 1, pointer_padding + 1), (pointer_padding + 1 + pointer_size / 2 - 1, pointer_padding + 1), 
        (pointer_padding + 1 + pointer_size / 2 - 1, pointer_padding + 1 + pointer_size - 2), (pointer_padding + 1, pointer_padding + 1 + pointer_size - 2)
    )
    entrance_color = "lightgreen"
    exit_color = "red"
    wall_color = "black"
    road_color = "white"
    background_color = "whitesmoke"
    frame_width = 4
    pos_O = (frame_width / 2, frame_width / 2)

    max_tag_number = 0
    @classmethod
    def __return_new_tag(cls):
        cls.max_tag_number += 1
        return f"{cls.max_tag_number} canva"
    
    def __init__(self, canva, maze_obj):
        self.tag = self.__return_new_tag()
        self.start = maze_obj.entrance
        self.ground_data = maze_obj.ground
        self.ground_xd = maze_obj.xd
        self.ground_yd = maze_obj.yd
        self.ground_x = self.ground_y = 0
        self.canva = canva
        self.canva_x, self.canva_y = self.pos_O
        self.x_side = self.ground_xd * self.distance
        self.y_side = self.ground_yd * self.distance
        self.trace_tags = set()
        self.frame_store = None
        self.blocks_store = []
        for i in range(self.ground_yd):
            self.blocks_store.append([None] * self.ground_xd)
    
    def delete(self):
        self.canva.delete(self.tag)
        self.canva.update()
        self.trace_tags.clear()
        self.blocks_store.clear()

    # 繪製
    def draw(self):
        #畫出入口
        self.ground_x, self.ground_y = self.start[0]
        self.canva_x, self.canva_y = self.pos_O[0] + self.ground_x * self.distance, self.pos_O[1] + self.ground_y * self.distance
        self.__block(self.entrance_color)
        for self.ground_x, self.ground_y in self.start[1:]:
            self.canva_x, self.canva_y = self.pos_O[0] + self.ground_x * self.distance, self.pos_O[1] + self.ground_y * self.distance
            self.__block(self.exit_color)
        
        #畫路
        self.canva_y = self.pos_O[1]
        for self.ground_y in range(self.ground_yd):
            self.canva_x = self.pos_O[0]
            for self.ground_x in range(self.ground_xd):
                if self.ground_data[self.ground_y][self.ground_x] <= 0:
                    self.__block(self.wall_color)
                    self.canva_x += self.distance
                else:
                    self.canva_x += self.distance
            self.canva_y += self.distance
        
        #畫框
        self.canva.config(scrollregion=(0, 0, self.x_side + self.pos_O[0] * 2, self.y_side + self.pos_O[1] * 2), bg=self.background_color)
        self.frame_store = self.canva.create_rectangle(self.pos_O[0], self.pos_O[1], self.x_side + self.pos_O[0], self.y_side + self.pos_O[1], width=self.frame_width, tag=(self.tag, ))

        # pointer
        self.pointer_gx, self.pointer_gy = self.start[0]
        self.canva_x, self.canva_y = self.pos_O[0] + self.pointer_gx * self.distance, self.pos_O[1] + self.pointer_gy * self.distance
        self.pointer = self.canva.create_oval(
            self.canva_x + self.pointer_padding, self.canva_y + self.pointer_padding, 
            self.canva_x + self.pointer_size + self.pointer_padding, self.canva_y + self.pointer_size + self.pointer_padding, 
            fill="deepskyblue", outline="black", width=2, tag=(self.tag, )
        )
        self.pointer_moving_TF = False

        # flag
        self.flag = None
        self.flag_gx = self.flag_gy = -1

    def __block(self, color):
        self.blocks_store[self.ground_y][self.ground_x] = self.canva.create_rectangle(
            self.canva_x, self.canva_y, self.canva_x + self.distance, self.canva_y + self.distance, 
            fill=color, outline=color, width=0, tag=(self.tag, )
        )
    
    # 顯示
    def show(self):
        self.canva.itemconfigure(self.tag, state="normal")

    # 隱藏
    def hide(self):
        self.canva.itemconfigure(self.tag, state="hidden")

    # control pointer
    def pointer_move(self, delta_gpos):
        if self.ground_data[self.pointer_gy + delta_gpos[1]][self.pointer_gx + delta_gpos[0]] > 0:
            self.pointer_moving_TF = True
            step = self.distance / 4
            x_move = delta_gpos[0] * step
            y_move = delta_gpos[1] * step
            if x_move:  # right or left  =>  j
                trace_tag = f"j {self.pointer_gy} {self.pointer_gx if (x_move > 0) else self.pointer_gx - 1}"  # x_move > 0  =>  right
            else:  # up or down  =>  i
                trace_tag = f"i {self.pointer_gx} {self.pointer_gy if (y_move > 0) else self.pointer_gy - 1}"  # y_move < 0  =>  down
            if trace_tag not in self.trace_tags:
                self.trace_tags.add(trace_tag)
                trace_TF = True
            else:
                trace_TF = False
            
            for i in range(4):
                if trace_TF:
                    pointer_pos = self.canva.coords(self.pointer)
                    pointer_center = ((pointer_pos[0] + pointer_pos[2]) / 2, (pointer_pos[1] + pointer_pos[3]) / 2)
                    self.canva.create_line(
                        pointer_center[0], pointer_center[1], pointer_center[0] + x_move, pointer_center[1] + y_move, 
                        fill="deepskyblue", width=self.pointer_size, capstyle="round", tag=(trace_tag, self.tag)
                    )
                    self.canva.tag_raise(self.pointer)
                    if self.flag: self.canva.tag_raise(self.flag)
                self.canva.move(self.pointer, x_move, y_move)
                self.canva.update()
                time.sleep(0.02 + i * 0.01)
            self.pointer_gx += delta_gpos[0]
            self.pointer_gy += delta_gpos[1]
            self.pointer_moving_TF = False
    
    def place_flag(self, gx, gy):
        x = gx * self.distance
        y = gy * self.distance
        self.flag = self.canva.create_polygon(
            self.flag_style[0][0] + x, self.flag_style[0][1] + y, self.flag_style[1][0] + x, self.flag_style[1][1] + y, 
            self.flag_style[2][0] + x, self.flag_style[2][1] + y, self.flag_style[3][0] + x, self.flag_style[3][1] + y, 
            self.flag_style[4][0] + x, self.flag_style[4][1] + y, self.flag_style[5][0] + x, self.flag_style[5][1] + y, 
            self.flag_style[6][0] + x, self.flag_style[6][1] + y, self.flag_style[7][0] + x, self.flag_style[7][1] + y, 
            self.flag_style[8][0] + x, self.flag_style[8][1] + y, self.flag_style[9][0] + x, self.flag_style[9][1] + y, 
            fill="gold", outline="black", tag=(self.tag, )
        )
        self.canva.update()
        self.flag_gx = gx
        self.flag_gy = gy
    
    def remove_flag(self):
        self.canva.delete(self.flag)
        self.canva.update()
        self.flag_gx = self.flag_gy = -1
    
    def pointer_flag_same_pos_TF(self):
        if (self.pointer_gx, self.pointer_gy) == (self.flag_gx, self.flag_gy):
            return True
        else:
            return False
    
    def __pointer_go_to_pos(self, gx, gy):
        self.canva.move(self.pointer, (gx - self.pointer_gx) * self.distance, (gy - self.pointer_gy) * self.distance)
        self.canva.update()
        self.pointer_gx = gx
        self.pointer_gy = gy

    def pointer_go_to_flag_pos(self):
        self.__pointer_go_to_pos(self.flag_gx, self.flag_gy)
    
    def pointer_go_to_pos(self, gx, gy):
        if self.ground_data[gy][gx] > 0:
            self.__pointer_go_to_pos(gx, gy)


class output_maze():
    def output_as_photo():
        pass
    
    def output_as_list():
        #確定起終點都是1，如果不是，則刪掉

        #把迷宮上不是1的部分都刪掉
        for y in range(maze_obj.yd):
            for x in range(maze_obj.xd):
                if maze_obj.ground[y][x] != 1:
                    maze_obj.ground[y][x] = 0


#GUI
class GUI():
    class struct_edit_section():
        padding_x = 3
        padding_y = 1
        def __init__(self, struct_name, container, root, new_TF = False):
            self.name = struct_name
            self.container = container
            self.root = root
            self.struct_right_button_mode = 0   # 0=刪除結構, 1=取消編輯
            self.struct_construct_button_mode = 0   # 0=未選, 1=選取, 2=選擇放置位置
            self.new_name = tk.StringVar()
            self.new_name.set("未命名")
            self.frame = tk.Frame(self.container)
            self.struct_right_button = tk.Button(self.frame, width=6, height=1, text="刪除", font="微軟正黑體 15", bg="crimson", command=self.__struct_right_btn)
            self.struct_construct_button = tk.Button(self.frame, width=6, height=1, text="未放置", font="微軟正黑體 15", bg="whitesmoke", command=self.__struct_construct_btn)
            self.rename_entry = tk.Entry(self.frame, width=20, relief="solid", font="微軟正黑體 15", textvariable=self.new_name)

            if new_TF:   # self.name = None
                self.struct_left_button_mode = 2   # 0=無, 1=檢視模式, 2=編輯模式
                self.struct_left_button = tk.Button(self.frame, width=12, height=1, text="未命名", font="微軟正黑體 15", bg="limegreen", command=self.__struct_left_btn)
                self.struct_right_button.grid(row=0, column=1, padx=self.padding_x, pady=self.padding_y)
            else:
                self.struct_left_button_mode = 0   # 0=無, 1=檢視模式, 2=編輯模式
                self.struct_left_button = tk.Button(self.frame, width=12, height=1, text=self.name, font="微軟正黑體 15", bg="whitesmoke", command=self.__struct_left_btn)
                self.struct_construct_button.grid(row=0, column=1, padx=self.padding_x, pady=self.padding_y)
            
            self.struct_left_button.grid(row=0, column=0, padx=self.padding_x)
        
        def quit_editing(self):
            if self.struct_left_button_mode:
                self.__left_mode_0()
                if self.struct_right_button_mode == 1:
                    self.__right_mode_1()
            elif self.struct_construct_button_mode == 2:
                self.__construct_mode_0()
        
        # 調整模式與外觀
        def __left_mode_0(self):   # 轉成"無"。如果為"手動放置結構"，則隱藏放置座標
            self.struct_left_button_mode = 0
            self.struct_left_button.config(bg="whitesmoke")
            self.struct_right_button.grid_remove()
            self.struct_construct_button.grid(row=0, column=1, padx=self.padding_x, pady=self.padding_y)
            # if self.struct_construct_button_mode == 2:
            #     self.__construct_mode_0()
            self.root.mouse_click_mode = 0   # 0=無
            if self.root.struct_pos.get() == "manual":
                # 隱藏放置座標
                pass
        
        def __left_mode_1(self):   # 轉成"檢視模式"。如果為"手動放置結構"，則顯示放置座標
            if self.struct_left_button_mode != 2:
                if self.struct_construct_button_mode == 2:
                    self.__construct_mode_0()
                else:
                    self.root.editing(self.name)
                self.struct_construct_button.grid_remove()
                self.struct_right_button.grid(row=0, column=1, padx=self.padding_x, pady=self.padding_y)
                self.mouse_click_mode = 2   # 2=編輯結構
            self.struct_left_button_mode = 1
            self.struct_left_button.config(bg="gold")
            self.__right_mode_0()
            if self.root.struct_pos.get() == "manual":
                # 顯示放置座標
                pass
        
        def __left_mode_2(self):   # 轉成"編輯模式"。如果為"手動放置結構"，則隱藏放置座標
            if self.struct_left_button_mode != 1:
                self.root.editing(self.name)
                self.struct_construct_button.grid_remove()
                self.struct_right_button.grid(row=0, column=1, padx=self.padding_x, pady=self.padding_y)
                self.mouse_click_mode = 2   # 2=編輯結構
            self.struct_left_button_mode = 2
            self.struct_left_button.config(bg="limegreen")
            self.__right_mode_1()
            if self.root.struct_pos.get() == "manual":
                # 隱藏放置座標
                pass
        

        def __right_mode_0(self):   # 刪除結構
            self.struct_right_button.config(text="刪除")
        
        def __right_mode_1(self):   # 取消編輯
            # 刪除原先製作的東西  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            self.struct_right_button_mode = 0
            self.struct_right_button.config(text="取消")
        

        def __construct_mode_0(self):   # 未放置
            self.struct_construct_button_mode = 0
            self.struct_construct_button.config(bg="whitesmoke", text="未放置")
            # self.root.mouse_click_mode = 0   # 0=無
        
        def __construct_mode_1(self):   # 已放置
            self.struct_construct_button_mode = 1
            self.struct_construct_button.config(bg="gold", text="已放置")
            self.root.mouse_click_mode = 0   # 0=無
        
        def __construct_mode_2(self):   # 選擇放置位置 (選取中)
            self.root.editing(self.name)   # 取得編輯權
            self.struct_construct_button_mode = 2
            self.struct_construct_button.config(bg="lightskyblue", text="選取中")
            self.root.mouse_click_mode = 1   # 1=選起終點位置or選結構位置
            pass


        def __struct_left_btn(self):          
            if self.struct_left_button_mode == 0:   # 0=無 => 轉成"檢視模式"。如果為"手動放置結構"，則顯示放置座標
                self.__left_mode_1()
            elif self.struct_left_button_mode == 1:   # 1=檢視模式 => 轉成"無"。如果為"手動放置結構"，則隱藏放置座標
                self.__left_mode_0()
                self.root.editing_struct_name = None
                pass
            elif self.struct_left_button_mode == 2:   # 2=編輯模式 => 轉成"檢視模式"，儲存編輯後的結構。如果為"手動放置結構"，則顯示放置座標
                self.__left_mode_1()
                pass
        
        def delete(self):
            self.frame.destroy()
            self.struct_left_button.destroy()
            self.struct_right_button.destroy()
            self.struct_construct_button.destroy()
            self.root.editing_struct_name = None

        def __struct_right_btn(self):
            if self.struct_right_button_mode == 0:   # 0=刪除結構
                self.delete()
                if self.name == None:
                    self.root.add_struct_button.grid(row=len(self.root.construct_structs), pady=1)
                    del self.root.control_struct_new_section
                    self.root.control_struct_new_section = None   # ???????????????
                else:
                    del self.root.control_struct_edit_sections[self.name]
            elif self.struct_right_button_mode == 1:   # 1=取消編輯
                self.__left_mode_1()
                pass
        
        def __struct_construct_btn(self):
            if self.struct_construct_button_mode == 0:   # 0=未放置 => 轉成"已放置"or"選擇放置位置"
                if self.root.struct_pos.get() == "start":
                    self.__construct_mode_1()
                elif self.root.struct_pos.get() == "manual":
                    self.__construct_mode_2()
                    pass
            elif self.struct_construct_button_mode == 1:   # 1=已放置 => 轉成"未放置"，取消放置
                self.__construct_mode_0()
                """# 如果別人的left = 1，有可能不能編輯，因為mouse_click_mode = 0  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   解決"""
            elif self.struct_construct_button_mode == 2:   # 2=選擇放置位置 => 轉成"未放置"
                self.__construct_mode_0()
                self.root.editing_struct_name = None
                pass
    
    padding_x = 5
    padding_y = 5
    canva_width = 760
    canva_height = 760
    auto_scroll_trigger_max = 10

    def __init__(self, title):
        self.main_window = tk.Tk()
        self.main_window.title(title)
        self.window_xd = self.main_window.winfo_width()
        self.window_yd = self.main_window.winfo_height()

        self.__setting()
        self.__struct_prepare()
    
    def load(self):
        self.__create_control_frame()
        self.__create_canva_frame()
        self.__show_control_frame()
        self.__show_canva_frame()
        self.__event_bind()
    
    def __event_bind(self):
        self.mouse_x, self.mouse_y = None, None
        self.mouse_cx, self.mouse_cy = None, None
        self.flag_placed_TF = False
        # self.canva.bind("<Motion>", self.__get_mouse_pos)
        self.canva.bind("<B2-Motion>", self.__drag_mouse_2)  # 按住中鍵
        self.canva.bind("<Button-1>", self.__click_mouse_1)
        self.canva.bind("<Button-2>", self.__click_mouse_2)  # 中鍵
        self.canva.bind("<Button-3>", self.__click_mouse_3)  # 右鍵
        # control pointer & flag
        self.canva.bind_all("<Key-Up>", self.__control_pointer)
        self.canva.bind_all("<Key-Left>", self.__control_pointer)
        self.canva.bind_all("<Key-Down>", self.__control_pointer)
        self.canva.bind_all("<Key-Right>", self.__control_pointer)
        self.canva.bind_all("<KeyPress-w>", self.__control_pointer)
        self.canva.bind_all("<KeyPress-a>", self.__control_pointer)
        self.canva.bind_all("<KeyPress-s>", self.__control_pointer)
        self.canva.bind_all("<KeyPress-d>", self.__control_pointer)
        self.canva.bind_all("<KeyPress-f>", self.__set_flag)  # flag
        self.canva.bind_all("<KeyPress-r>", self.__back_to_flag)  # tp flag
        # move pointer (飄移)
        self.canva.bind_all("<KeyPress-g>", self.__back_to_flag)
        self.canva.bind_all("<KeyPress-x>", self.__back_to_flag)
        self.canva.bind_all("<KeyPress-y>", self.__back_to_flag)
        
        self.exit_entry.bind_class("Entry", "<Return>", self.__entry_unfocus)
    
    def __setting(self):
        self.ground = None
        self.GUI_show_ground = None
        self.mouse_click_mode = 0   # 0=無, 1=選起終點位置or選結構位置, 2=編輯結構
        self.struct_TF = tk.BooleanVar()
        self.struct_TF.set(False)
        self.struct_pos = tk.StringVar()
        self.struct_pos.set("start")
        self.random_TF = tk.BooleanVar()
        self.random_TF.set(True)

    def __struct_prepare(self):
        A_55 = [[-1, -1,  1, -1, -1], 
                [-1,  1,  1,  1, -1], 
                [ 1,  1, -1,  1,  1], 
                [-1,  1,  1,  1, -1], 
                [-1, -1,  1, -1, -1]]
        self.construct_structs = dict()#{"sample" : maze(copy.deepcopy(A_55), (1, 1))}
        self.control_struct_edit_sections = dict()
        self.editing_struct_name = None
        self.control_struct_new_section = None
        
    def add_struct(self, name, struct):
        self.construct_structs[name] = struct

    def execute(self):
        self.main_window.mainloop()
    
    def __create_control_frame(self):
        self.control_frame = tk.Frame(self.main_window)

        self.control_xd_frame = tk.Frame(self.control_frame)
        self.xd_label = tk.Label(self.control_xd_frame, width=20, height=1, text="迷宮寬度(x軸)", font="微軟正黑體 15 bold", anchor="w")
        self.xd_entry = tk.Entry(self.control_xd_frame, width=20, relief="solid", font="微軟正黑體 15")
        self.xd_entry.insert(0, "32")

        self.control_yd_frame = tk.Frame(self.control_frame)
        self.yd_label = tk.Label(self.control_yd_frame, width=20, height=1, text="迷宮高度(y軸)", font="微軟正黑體 15 bold", anchor="w")
        self.yd_entry = tk.Entry(self.control_yd_frame, width=20, relief="solid", font="微軟正黑體 15")
        self.yd_entry.insert(0, "32")

        self.control_exit_frame = tk.Frame(self.control_frame)
        self.exit_label = tk.Label(self.control_exit_frame, width=20, height=1, text="出口數", font="微軟正黑體 15 bold", anchor="w")
        self.exit_entry = tk.Entry(self.control_exit_frame, width=20, relief="solid", font="微軟正黑體 15")
        self.exit_entry.insert(0, "1")

        self.control_struct_frame = tk.Frame(self.control_frame)
        self.struct_label = tk.Label(self.control_struct_frame, width=20, height=1, text="是否放置結構", font="微軟正黑體 15 bold", anchor="w")
        self.struct_T_radiobutton = tk.Radiobutton(
            self.control_struct_frame, width=9, height=1, variable=self.struct_TF, value=True, 
            text="放置", indicatoron=0, font="微軟正黑體 15", bg="forestgreen", command=self.__struct_T_rbtn
        )
        self.struct_F_radiobutton = tk.Radiobutton(
            self.control_struct_frame, width=9, height=1, variable=self.struct_TF, value=False, 
            text="不放置", indicatoron=0, font="微軟正黑體 15", bg="crimson", state="disable", command=self.__struct_F_rbtn
        )
        self.control_struct_pos_frame = tk.Frame(self.control_frame)
        self.struct_pos_label = tk.Label(self.control_struct_pos_frame, width=20, height=1, text="結構放置位置", font="微軟正黑體 15 bold", anchor="w")
        self.struct_pos_start_radiobutton = tk.Radiobutton(
            self.control_struct_pos_frame, width=9, height=1, variable=self.struct_pos, value="start", 
            text="起終點", indicatoron=0, font="微軟正黑體 15", bg="forestgreen", state="disable", command=self.__struct_pos_start_rbtn
        )
        self.struct_pos_manual_radiobutton = tk.Radiobutton(
            self.control_struct_pos_frame, width=9, height=1, variable=self.struct_pos, value="manual", 
            text="手動", indicatoron=0, font="微軟正黑體 15", bg="crimson", command=self.__struct_pos_manual_rbtn
        )
        self.control_struct_choose_frame = tk.Frame(self.control_frame)
        for struct_name in self.construct_structs.keys():
            self.control_struct_edit_sections[struct_name] = self.struct_edit_section(struct_name, self.control_struct_choose_frame, self)
        self.add_struct_button = tk.Button(self.control_struct_choose_frame, width=20, height=1, text="新增", font="微軟正黑體 15 bold", bg="lightyellow", command=self.__add_struct_btn)

        self.control_random_frame = tk.Frame(self.control_frame)
        self.random_label = tk.Label(self.control_random_frame, width=20, height=1, text="選擇起終點座標", font="微軟正黑體 15 bold", anchor="w")
        self.random_T_radiobutton = tk.Radiobutton(
            self.control_random_frame, width=9, height=1, variable=self.random_TF, value=True, 
            text="自動", indicatoron=0, font="微軟正黑體 15", bg="limegreen", state="disable", command=self.__random_T_rbtn
        )
        self.random_F_radiobutton = tk.Radiobutton(
            self.control_random_frame, width=9, height=1, variable=self.random_TF, value=False, 
            text="手動", indicatoron=0, font="微軟正黑體 15", bg="orange", command=self.__random_F_rbtn
        )
        self.manual_label = tk.Label(self.control_frame, width=20, height=1, text="請點選起終點位置→", font="微軟正黑體", anchor="e")

        self.create_maze_button = tk.Button(
            self.control_frame, width=20, height=1, text="製作迷宮", font="微軟正黑體 15 bold", bg="limegreen", command=self.__create_maze_btn
        )
    
    def __create_canva_frame(self):
        self.canva_frame = tk.Frame(self.main_window)
        self.scrollbar_y = tk.Scrollbar(self.canva_frame, orient="vertical")
        
        self.canva_inner_frame = tk.Frame(self.canva_frame, width=self.canva_width, height=self.canva_height + 20)
        self.scrollbar_x = tk.Scrollbar(self.canva_inner_frame, orient="horizontal")
        self.canva = tk.Canvas(self.canva_inner_frame, width=self.canva_width, height=self.canva_height, scrollregion=(0, 0, self.canva_width, self.canva_height), xscrollincrement=2, yscrollincrement=2)
        
        self.scrollbar_x.config(command=self.canva.xview)
        self.scrollbar_y.config(command=self.canva.yview)
        self.canva.config(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
    
    def __show_control_frame(self):
        self.control_frame.pack(side="left", fill="y", padx=self.padding_x, pady=self.padding_y)

        self.control_xd_frame.grid(row=0, padx=self.padding_x, pady=self.padding_y)
        self.xd_label.pack()
        self.xd_entry.pack()

        self.control_yd_frame.grid(row=1, padx=self.padding_x, pady=self.padding_y)
        self.yd_label.pack()
        self.yd_entry.pack()

        self.control_exit_frame.grid(row=2, padx=self.padding_x, pady=self.padding_y)
        self.exit_label.pack()
        self.exit_entry.pack()

        self.control_struct_frame.grid(row=3, padx=self.padding_x, pady=self.padding_y)
        self.struct_label.grid(row=0, columnspan=2)
        self.struct_T_radiobutton.grid(row=1, column=0)
        self.struct_F_radiobutton.grid(row=1, column=1)

        # control_struct_pos_frame row=4
        self.struct_pos_label.grid(row=0, columnspan=2)
        self.struct_pos_start_radiobutton.grid(row=1, column=0)
        self.struct_pos_manual_radiobutton.grid(row=1, column=1)

        # control_struct_choose_frame row=5
        i = 0  #
        for i, struct_name in enumerate(list(self.construct_structs.keys())):
            self.control_struct_edit_sections[struct_name].frame.grid(row=i, pady=2)
        self.add_struct_button.grid(row=i+1, pady=1)

        self.control_random_frame.grid(row=6, padx=self.padding_x, pady=self.padding_y)
        self.random_label.grid(row=0, columnspan=2)
        self.random_T_radiobutton.grid(row=1, column=0)
        self.random_F_radiobutton.grid(row=1, column=1)

        # manual_label row=7

        self.create_maze_button.grid(row=8, columnspan=2, padx=self.padding_x, pady=self.padding_y)

    def __show_canva_frame(self):
        self.canva_frame.pack(side="right", padx=self.padding_x, pady=self.padding_y, fill="both")
        self.canva_inner_frame.pack(side="left", fill="both")
        self.canva.pack(side="top", fill="x")
    
    def __change_show_ground(self, to):
        # 改變畫布顯示的東西
        pass
    
    def __show_hide_scrollbar(self):
        # 是否顯示scrollbar
        if self.GUI_show_ground.x_side > self.canva_width:
            self.scrollbar_x.pack(side="bottom", fill="x")
        else:
            self.scrollbar_x.pack_forget()
        if self.GUI_show_ground.y_side > self.canva_height:
            self.scrollbar_y.pack(side="right", fill="y")
        else:
            self.scrollbar_y.pack_forget()

    # 編輯模式 canva
    def __edit_ground(self):
        xd = int(self.xd_entry.get())
        yd = int(self.yd_entry.get())
        for i in range(xd - 1):
            self.canva.create_line(0, 0, )
        pass

    # 是否放置結構
    def __struct_T_rbtn(self):
        self.struct_T_radiobutton.config(state="disable")
        self.struct_F_radiobutton.config(state="normal")
        self.control_struct_pos_frame.grid(row=4, padx=self.padding_x, pady=self.padding_y)
        self.control_struct_choose_frame.grid(row=5, padx=self.padding_x, pady=self.padding_y)

    def __struct_F_rbtn(self):
        self.struct_F_radiobutton.config(state="disable")
        self.struct_T_radiobutton.config(state="normal")
        self.control_struct_pos_frame.grid_remove()
        self.control_struct_choose_frame.grid_remove()
    
    # 結構放置位置
    def __struct_pos_start_rbtn(self):
        self.struct_pos_start_radiobutton.config(state="disable")
        self.struct_pos_manual_radiobutton.config(state="normal")
        for section in self.control_struct_edit_sections.values():   # 還原
            if section.struct_construct_button_mode == 2:
                section.quit_editing()

    def __struct_pos_manual_rbtn(self):
        self.struct_pos_manual_radiobutton.config(state="disable")
        self.struct_pos_start_radiobutton.config(state="normal")
    
    # 編輯、放置結構
    def editing(self, name):  # 誰可以操作canva
        if self.editing_struct_name != None and self.editing_struct_name != name:
            self.control_struct_edit_sections[self.editing_struct_name].quit_editing()
        self.editing_struct_name = name
    
    def __change_struct_name(self, original_name, new_name):
        pass

    # 新增結構
    def __add_struct_btn(self):
        self.add_struct_button.grid_remove()
        self.editing(1)
        self.mouse_click_mode = 2   # 2=編輯結構
        self.control_struct_new_section = self.struct_edit_section(None, self.control_struct_choose_frame, self, True)
        self.control_struct_new_section.frame.grid(row=len(self.construct_structs), pady=2)

    # 選擇起終點座標
    def __random_T_rbtn(self):
        self.random_T_radiobutton.config(state="disable")
        self.random_F_radiobutton.config(state="normal")
        self.manual_label.grid_remove()
        self.create_maze_button.config(bg="limegreen", state="normal")
        del self.assign_exit

    def __random_F_rbtn(self):
        self.random_F_radiobutton.config(state="disable")
        self.random_T_radiobutton.config(state="normal")
        self.manual_label.grid(row=7, columnspan=2, padx=self.padding_x, pady=self.padding_y)
        self.create_maze_button.config(bg="orange")
        self.assign_exit = 0
        try:
            if int(self.exit_entry.get()) > self.assign_exit:
                self.create_maze_button.config(state="disable")
        except: pass

    def __create_maze_btn(self):
        try:
            xd = int(self.xd_entry.get())   #迷宮大小(x軸)   185
            if xd <= 0:
                raise Exception("資料值錯誤，請重新輸入")
            yd = int(self.yd_entry.get())   #迷宮大小(y軸)   95
            if yd <= 0:
                raise Exception("資料值錯誤，請重新輸入")
            Max_ending = xd * yd - 1
            ending = int(self.exit_entry.get())    #出口數   20
            if ending > Max_ending:
                raise Exception("資料值大於%d，請重新輸入" % Max_ending)
        except ValueError:
            print("資料型態錯誤，請重新輸入")
        except Exception as e:
            print(str(e))
        else:
            if self.ground:
                self.ground.delete()
                del self.ground
                self.GUI_show_ground.delete()
                del self.GUI_show_ground
            self.ground = maze(maze.create_list2(xd, yd))
            if self.struct_TF.get():
                structs = dict()
                for struct_name, section in self.control_struct_edit_sections.items():
                    if section.struct_construct_button_mode == 1:
                        structs[struct_name] = self.construct_structs[struct_name]
                if not structs:
                    struct_name = random.choice(list(self.construct_structs.keys()))  #隨機放置結構
                    structs[struct_name] = self.construct_structs[struct_name]
                create_in_out(self.ground, ending, self.random_TF.get(), structs)
            else:
                create_in_out(self.ground, ending, self.random_TF.get())
            self.ground.create_random_maze()
            print("製作迷宮時間：", time.process_time())
            self.GUI_show_ground = show_maze(self.canva, self.ground)
            self.GUI_show_ground.draw()
            print("繪製迷宮時間：", time.process_time())

            # scrollbar show TF
            self.__show_hide_scrollbar()
            
            self.__entry_unfocus(None)

    # event
    def __mouse_pos_translate(self, event_x, event_y):
        # screen的座標
        self.mouse_x = event_x
        self.mouse_y = event_y
        # input screen的座標 return canva內的座標
        self.mouse_cx = int(self.canva.canvasx(self.mouse_x))
        self.mouse_cy = int(self.canva.canvasy(self.mouse_y))
        if self.GUI_show_ground:  # ground 座標換算
            self.mouse_gx = int((self.mouse_cx - self.GUI_show_ground.pos_O[0]) // self.GUI_show_ground.distance)
            self.mouse_gy = int((self.mouse_cy - self.GUI_show_ground.pos_O[1]) // self.GUI_show_ground.distance)

    def __get_mouse_pos(self, event):
        self.__mouse_pos_translate(event.x, event.y)

    def __drag_mouse_2(self, event):
        # 用中鍵滑動canva
        self.canva.scan_dragto(event.x, event.y, 1)
    
    def __click_mouse_1(self, event):
        self.__mouse_pos_translate(event.x, event.y)
        if self.mouse_click_mode == 0 and self.GUI_show_ground:
            # 瞬間移動pointer位置
            self.GUI_show_ground.pointer_go_to_pos(self.mouse_gx, self.mouse_gy)
        elif self.mouse_click_mode == 1:
            # 是終點就消除，不是就新增
            pass
        elif self.mouse_click_mode == 2:
            # 是牆壁就消除，不是就新增
            pass
    
    def __click_mouse_2(self, event):
        # 用中鍵滑動canva
        self.canva.scan_mark(event.x, event.y)
    
    def __click_mouse_3(self, event):
        self.__mouse_pos_translate(event.x, event.y)
        if self.mouse_click_mode == 2:
            # 是終點就消除，不是就新增
            pass
    
    def __control_pointer(self, event):
        if self.mouse_click_mode == 0 and self.GUI_show_ground and not self.GUI_show_ground.pointer_moving_TF:
            if event.keysym == "w" or event.keysym == "Up":
                self.GUI_show_ground.pointer_move((0, -1))
            elif event.keysym == "a" or event.keysym == "Left":
                self.GUI_show_ground.pointer_move((-1, 0))
            elif event.keysym == "s" or event.keysym == "Down":
                self.GUI_show_ground.pointer_move((0, 1))
            elif event.keysym == "d" or event.keysym == "Right":
                self.GUI_show_ground.pointer_move((1, 0))
    
    def __set_flag(self, event):
        if self.flag_placed_TF:
            if self.GUI_show_ground.pointer_flag_same_pos_TF():
                self.GUI_show_ground.remove_flag()
                self.flag_placed_TF = False
            else:
                self.GUI_show_ground.remove_flag()
                self.GUI_show_ground.place_flag(self.GUI_show_ground.pointer_gx, self.GUI_show_ground.pointer_gy)
        else:
            self.GUI_show_ground.place_flag(self.GUI_show_ground.pointer_gx, self.GUI_show_ground.pointer_gy)
            self.flag_placed_TF = True

    def __back_to_flag(self, event):
        if self.flag_placed_TF:
            self.GUI_show_ground.pointer_go_to_flag_pos()
    
    def __entry_unfocus(self, event):
        self.main_window.focus()
    

random_maze = GUI("random maze")


B_55 = [[ 1,  1,  1,  1,  1], 
        [-1, -1, -1, -1, -1], 
        [ 2,  2,  2, -1,  3], 
        [ 2, -1, -1, -1,  3], 
        [ 2,  2,  2,  3,  3]]

A_77 = [[-1, -1, -1,  1, -1, -1, -1], 
        [-1,  1,  1,  1,  1,  1, -1], 
        [-1,  1, -1, -1, -1,  1, -1], 
        [ 1,  1, -1, -1, -1,  1,  1], 
        [-1,  1, -1, -1, -1,  1, -1], 
        [-1,  1,  1,  1,  1,  1, -1], 
        [-1, -1, -1,  1, -1, -1, -1]]

# random_maze.add_struct("B_55", maze(copy.deepcopy(B_55)[::-1], (0, 0)))
# random_maze.add_struct("A_77", maze(copy.deepcopy(A_77), (1, 1)))

random_maze.load()
random_maze.execute()

