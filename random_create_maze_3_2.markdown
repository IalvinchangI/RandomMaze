# Maze
> ## 說明
> 1. 迷宮物件
> 2. 儲存所有同一個迷宮的相關資料的地方
> 3. 相關資料包含迷宮的屬性and隨機生成所需的暫存空間
> 4. 可輸出易懂的樣子（**Point** 的 _type、圖像）
> 5. __exit 的第一格最後會是整棵樹的頭

> ## attribution
> ### __ground
> > 存 **Point** 的 2維numpy.array
> 
> ### __width
> > maze 的寬
> 
> ### __height
> > maze 的高
> 
> ### __exit
> > 用 list 存出入口座標  
> > 沒特別指定誰是出口、誰是入口  
> > 但第一格最後會是整棵樹的頭  
> > 出入口編號 (_io_number) = 在 __exit 的 index

> ## property
> ### ground
> > **get :** return 2維list，裡面存 **Point** 的 _type
>
> ### exit
> > **get :** return __exit

> ## method
> ### __init__
> > 輸入 width 和 height  
> > 需要 `numpy`  
> > 自動生成存滿 **Point** 的 2維numpy.array
> 
> ### add_exit
> > 檢查座標，append 進 __exit
> 
> ### del_exit
> > 參數：座標 (x, y)  
> > 從 __exit 中找出傳入的座標，將其從 __exit 中 remove
>
> ### print_ground
> > print 出 __ground 內 **Point** 的 _type
>
> ### print_maze
> > print 出迷宮的樣子
> 
> ### image_maze
> > 用圖片輸出迷宮的樣子  
> > 需要 `pillow`

<br>
<br>
<br>

# Point
> ## 說明
> 1. 格子物件的基底
> 2. 預設存在 **Maze** 的 __ground 內

> ## attribution
> ### _type
> > 存 **Point** 是 路、牆、不可變（1, 0, -1）
> 
> ### _io_number
> > 存所屬的 出入口 的 __exit 的 index

<br>
<br>
<br>

# Branch
> ## 說明
> 1. 格子物件的變體，繼承自 **Point**
> 2. 預設存在 **Maze** 的 __ground 內
> 3. 會替換原先的 **Point**
> 4. 構成道路的基本元素
> 5. _branch_number = 該道路末端的 **Node** 編號 (node_number)

> ## attribution
> ### _type
> > 和 **Point** 同
>
> ### _io_number
> > 和 **Point** 同
> 
> ### _branch_number
> > 代表屬於同一條道路的編號  
> > 必須與尾端 **Node** 的 _node_number 相等
>
> ### _previous
> > 上一個同 _branch_number 的 **Branch** or **Node** 物件
>
> ### _next
> > 下一個同 _branch_number 的 **Branch** or **Node** 物件

<br>
<br>
<br>

# Node
> ## 說明
> 1. 格子物件的變體，繼承自 **Point**
> 2. 預設存在 **Maze** 的 __ground 內
> 3. 會替換原先的 **Point** or **Branch**
> 4. 會出現在道路末端 or 岔路點
> 5. 在出入口上的 **Node** 的 _node_number = _io_number

> ## attribution
> ### _type
> > 和 **Point** 同
>
> ### _io_number
> > 和 **Point** 同
>
> ### _node_number
> > node 編號  
> > 在同條道路上的 **Branch** 的 _branch_number 必須與尾端 **Node** 的 _node_number 相等
>
> ### _first
> > 該道路的起始點  
> > 存該道路的起始 **Branch**
> 
> ### _previous_node
> > 上一個 **Node** 物件
> 
> ### _next_node
> > 下1~3個 **Node** 物件  
> > [right, straight, left]

> ## property
> ### node_number
> > **get :** return _node_number