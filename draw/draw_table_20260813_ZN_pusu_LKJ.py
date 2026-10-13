import os
import time
import numpy as np
import pandas as pd
# import matplotlib as mpl

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import itertools
from matplotlib import cm


def table_003():


    # 1. 准备数据
    data = {
        '指标名称': ['准确率 (Acc)', '召回率 (Recall)', 'F1值', '推理耗时 (s)'],
        'Baseline': [0.852, 0.841, 0.846, 12.5],
        'Our Model': [0.923, 0.915, 0.919, 14.1],
    }
    df = pd.DataFrame(data)

    # 2. 创建画布
    fig, ax = plt.subplots(figsize=(6, 2.5))
    ax.axis('off')
    # ax.axis('tight')

    # 3. 绘制表格，初始设为全空边框 (edges='open')
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        edges='open',  # 初始不绘制任何默认边框
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.5)  # 调整行高，让表格更舒展

    # 4. 核心改造：精细控制三条线（顶线、表头底线、底线）
    n_rows = len(df)

    for (row, col), cell in table.get_celld().items():
      if row == 0:
        # 【线 1 & 线 2】：表头行，需要顶部粗线和底部中等粗线
        cell.set_linewidth(2)  # 设置线条加粗
        cell.visible_edges = 'T'  # 仅显示 Top（顶线）和 Bottom（表头底线）
      elif row == n_rows:
        # 【线 3】：最后一行数据，需要底部粗线
        cell.set_linewidth(2)
        cell.visible_edges = 'B'  # 仅显示 Bottom（底线）
      elif row == 1:
          cell.set_linewidth(1)
          cell.visible_edges = 'T'  # 仅显示 Bottom（底线）
      else:
        # 中间的数据行：不显示任何横线和竖线
        cell.set_linewidth(0)
        cell.visible_edges = ''

    plt.show()
    # 5. 保存为高清图片
    # plt.savefig('three_line_table.png', bbox_inches='tight', dpi=300)
    # plt.close()

    print('标准三线表图片生成成功！')

def table_005():
    # 1. 创建画布
    fig, ax = plt.subplots(figsize=(6, 3), dpi=500)
    ax.axis('off')
    ax.axis('tight')
    # 原始数据
    data = [
        ['部门', '姓名', '绩效'],
        ['技术部', '张三', 90],
        ['技术部', '李四', 85],
        ['财务部', '王五', 92],
    ]

    table = ax.table(
        cellText=data, cellLoc='center', loc='center', edges='closed'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.8)

    # ==========================================================
    # 【核心关键步】必须先让画布渲染一次，底层单元格的绝对坐标才能被算出来！
    fig.canvas.draw()

    # ==========================================================

    # --- 示例应用 ---

    # 1. 纵向合并：“技术部”（第 1 行第 0 列 到 第 2 行第 0 列）
    matplotlib_merge(
        table, ax, start_row=1, start_col=0, end_row=2, end_col=0, text='技术\n部'
    )

    # 2. 横向合并：“张三 / 李四”（第 1 行的第 1 列到第 2 列）
    matplotlib_merge(
        table,
        ax,
        start_row=1,
        start_col=1,
        end_row=1,
        end_col=2,
        text='张三 / 李四 (联合考核)',
    )

    # # 4. 保存为高清晰度图片
    # plt.savefig('matplotlib_pure_merged.png', bbox_inches='tight', dpi=300)
    # plt.close()

    print('纯 Matplotlib 单元格合并成功，图片已保存！')
    plt.show()

def config_file(root, file):
    # root = 'C:\\Users\\Delon\\Desktop\\普速列控邻线干扰\\数据汇总\\4-1-1遍历频率\\'
    # file = '仿真输出_20260813_普速列控_4-1-1遍历频率.xlsx'

    df_data1 = pd.read_excel(root + file, '数据输出')
    # df_data2 = pd.read_excel(root + file, '被串钢轨电流')
    # df_combine = pd.concat([df_data1, df_data2], axis=1)

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = root + '生成表格_%s' % timestamp

    return df_data1, res_dir


def draw_line(
        table, ax, data, row, start=None, end=None,
        edge='T', color='black', linewidth=1.0, zorder=3,
):
    if start is None:
        start = 0

    if end is None:
        n_cols = len(data[0])
        end = n_cols-1

    cell1 = table.get_celld()[(row, start)]
    cell2 = table.get_celld()[(row, end)]
    x0 = cell1.get_x()
    x1 = cell2.get_x() + cell2.get_width()

    if edge == 'T':
        y0 = cell1.get_y() + cell1.get_height()
    elif edge == 'B':
        y0 = cell1.get_y()
    else:
        raise KeyboardInterrupt()

    ax.axhline(
        y=y0, xmin=x0, xmax=x1, color=color, linewidth=linewidth, zorder=zorder,
    )

def merge_duplicate(table, ax, data, index=0, mode='row'):
    if mode == 'row':
        lst = data[index].copy()
    elif mode == 'col':
        lst = []
        for val in data:
            lst.append(val[index])
    else:
        return

    txt = ''
    start = -1
    size = len(lst)
    lst.append(None)
    merge_list = []
    for i, val in enumerate(lst):
        if i == 0:
            start = 0
            txt = val
        else:
            if val != txt or i == size:
                if (i - start) > 1:
                    if mode == 'row':
                        tmp = [index, start, index, i-1, txt]
                    elif mode == 'col':
                        tmp = [start, index, i-1, index, txt]
                    else:
                        raise KeyboardInterrupt()
                    merge_list.append(tmp)
                start = i
                txt = val

    for val in merge_list:
        matplotlib_merge(
            table,
            ax,
            start_row=val[0],
            start_col=val[1],
            end_row=val[2],
            end_col=val[3],
            text=val[4],
        )

    return merge_list


# 封装一个专属于 Matplotlib 的安全合并函数
def matplotlib_merge(
        table, ax, start_row, start_col, end_row, end_col, text
):

    # 1. 清空被合并区域内所有格子的文字
    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            # table.get_celld()[(r, c)].set_text_props(text='')
            table.get_celld()[(r, c)].set_text_props(text='')

    # # 2. 自动处理边框：去掉合并区域内部的线条，保留外围边框
    # for r in range(start_row, end_row + 1):
    #     for c in range(start_col, end_col + 1):
    #         cell = table.get_celld()[(r, c)]
    #         edges = set(cell.visible_edges)
    #         if c > start_col:
    #             edges.discard('L')  # 去掉左内边框
    #         if c < end_col:
    #             edges.discard('R')  # 去掉右内边框
    #         if r > start_row:
    #             edges.discard('T')  # 去掉上内边框
    #         if r < end_row:
    #             edges.discard('B')  # 去掉下内边框
    #         cell.visible_edges = ''.join(edges)

    # 3. 获取合并区域的边界坐标（此时由于前面执行了 draw()，坐标绝对准确）
    cell_start = table.get_celld()[(start_row, start_col)]
    cell_end = table.get_celld()[(end_row, end_col)]

    x0 = cell_start.get_x()
    x1 = cell_end.get_x() + cell_end.get_width()
    y0 = cell_end.get_y()
    y1 = cell_start.get_y() + cell_start.get_height()

    # 计算绝对正中心
    center_x = x0 + (x1 - x0) / 2
    center_y = y0 + (y1 - y0) / 2

    face_color = cell_start.get_facecolor()
    edge_color = cell_start.get_edgecolor()
    linewidth = cell_start.get_linewidth()
    font_size = cell_start.get_text().get_fontsize()

    rect = patches.Rectangle(
        xy=(x0, y0),  # 左下角坐标 (x=2, y=3)
        width=x1-x0,  # 宽度为 5
        height=y1-y0,  # 高度为 3
        facecolor=face_color,  # 背景填充色（浅蓝）
        edgecolor=edge_color,  # 边框颜色（深蓝）
        linewidth=linewidth,  # 边框粗细
        linestyle='-',  # 边框样式（如 '-' 实线, '--' 虚线）
        transform=table.get_transform(),  # 绑定到表格自身的坐标系
    )
    ax.add_patch(rect)

    ax.text(
        center_x,
        center_y,
        text,
        transform=table.get_transform(),  # 绑定到表格自身的坐标系
        ha='center',
        va='center',
        fontsize=font_size,
        weight='bold',
    )


def config_ax(data, color='#e6f2ff'):
    v_height = 0.18
    v_pad = 0.1
    fig_height = v_height * len(data) + v_pad

    fig, ax = plt.subplots(figsize=(7, fig_height), dpi=200)
    ax.axis('off')
    # ax.axis('tight')
    ax.set_position([0.02, 0, 0.96, 1])

    row_colors = [[color] * len(data[0]) for _ in range(len(data))]

    table = ax.table(
        cellText=data, cellLoc='center', loc='center', edges='closed',
        cellColours=row_colors,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    # table.scale(1, 1.8)

    for (_, _), cell in table.get_celld().items():
        # cell.set_fill(True)
        # cell.set_edgecolor('#333333')
        cell.set_edgecolor('white')
        cell.set_linewidth(0.6)
        cell.set_visible(True)  # 确保可见

        # print(cell.get_width())
        # print(cell.get_height())

        # cell.set_width(0.25)
        # cell.set_height(0.033)
        cell.set_height(v_height/fig_height)
        # cell.set_facecolor('red')

        # if row <= 1:
        #     cell.set_facecolor('#2b5c8f')
        # cell.get_text().set_facecolor('#2b5c8f')
        # cell.get_text().set_color('red')
        # cell.get_text().set_weight('bold')
        pass

    fig.canvas.draw()

    return fig, ax, table


# 4-1-1遍历频率
def draw_table_4_1_1(parent_root):
    sub_dir = '4-1-1遍历频率'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-1遍历主被串频率'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'
            s2 = df['被串频率(Hz)'].astype(str) + 'Hz'
            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            header1 = ['区段长度', '被串频率']
            header2 = ['区段长度', '被串频率']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 4 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-2遍历长度
def draw_table_4_1_2(parent_root):
    sub_dir = '4-1-2遍历长度'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-2遍历长度'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[
            df0["主串频率(Hz)"] == freq_zhu
        ].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'
            ret = pd.concat([ret, s1], axis=1, sort=False)
            header1 = ['区段长度']
            header2 = ['区段长度']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    # merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=1, edge='T', linewidth=1)

        # elif row % 4 == 1:
        #     draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)



# 4-1-3遍历方向
def draw_table_4_1_3(parent_root):
    sub_dir = '4-1-3遍历方向'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-3遍历方向'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'

            dir_table = {
                '右发': '反向',
                '左发': '同向',
            }

            s2 = df['主串方向'].astype(str).apply(lambda x: dir_table[x])
            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            header1 = ['区段长度', '发送方向']
            header2 = ['区段长度', '发送方向']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 2 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-4遍历分路模式
def draw_table_4_1_4(parent_root):
    sub_dir = '4-1-4遍历分路模式'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-4遍历分路模式'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'

            show_table = {
                '主串调整被串分路': '主串调整',
                '主被串同时分路': '同时分路',
            }

            s2 = df['分路模式'].astype(str).apply(lambda x: show_table[x])

            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            header1 = ['区段长度', '分路模式']
            header2 = ['区段长度', '分路模式']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 2 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-5遍历电容间距
def draw_table_4_1_5(parent_root):
    sub_dir = '4-1-5遍历电容间距'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-5遍历电容间距'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'


    list1 = [400, 600, 800, 1000]
    df0 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'

            # show_table = {
            #     '主串调整被串分路': '主串调整',
            #     '主被串同时分路': '同时分路',
            # }
            #
            # s2 = df['主串电容间隔'].astype(str).apply(lambda x: show_table[x])

            s2 = df['主串电容间隔'].astype(str)
            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            header1 = ['区段长度', '电容间隔']
            header2 = ['区段长度', '电容间隔']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 11 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-6-1遍历电容容值主串
def draw_table_4_1_6_1(parent_root):
    sub_dir = '4-1-6-1遍历电容容值主串'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-6-1遍历电容容值'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    list1 = [400, 600, 800, 1000]
    df0 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'

            show_table = {
                '普速既有': '普速既有',
                '25': '25μF',
                '50': '50μF',
            }

            s2 = df['主串电容值配置'].astype(str).apply(lambda x: show_table[x])
            s3 = df['被串电容值配置'].astype(str).apply(lambda x: show_table[x])
            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            ret = pd.concat([ret, s3], axis=1, sort=False)

            header1 = ['区段长度', '主串\n电容配置','被串\n电容配置']
            header2 = ['区段长度', '主串\n电容配置','被串\n电容配置']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

        elif row % 9 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-7-1遍历调整电阻主串
def draw_table_4_1_7_1(parent_root):
    sub_dir = '4-1-7-1遍历调整电阻主串'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-7-1遍历调整电阻'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    list1 = [600, 800, 1000]
    df0 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'

            s2 = df['主串调整电阻(Ω)'].astype(str) + 'Ω'
            s3 = df['被串调整电阻(Ω)'].astype(str) + 'Ω'
            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            ret = pd.concat([ret, s3], axis=1, sort=False)

            header1 = ['区段长度', '主串\n调整电阻','被串\n调整电阻']
            header2 = ['区段长度', '主串\n调整电阻','被串\n调整电阻']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

        elif row % 16 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-8-1遍历FT1U输出电压主串
def draw_table_4_1_8_1(parent_root):
    sub_dir = '4-1-8-1遍历FT1U输出电压主串'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-8-1遍历FT1U输出电压'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    list1 = [400, 600, 800, 1000]
    df0 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'

            s2 = df['主串FT1U输出电压(V)'].astype(str) + 'V'
            s3 = df['被串FT1U输出电压(V)'].astype(str) + 'V'
            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            ret = pd.concat([ret, s3], axis=1, sort=False)

            header1 = ['区段长度', '主串\nFT1U电压','被串\nFT1U电压']
            header2 = ['区段长度', '主串\nFT1U电压','被串\nFT1U电压']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

        elif row % 9 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-9遍历电缆长度
def draw_table_4_1_9(parent_root):
    sub_dir = '4-1-9遍历电缆长度'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-9遍历电缆长度'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'


    list1 = [400, 500, 600, 700, 800, 900, 1000]
    df0 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'


            s2 = df['主串电缆长度(km)'].astype(str) + 'km'
            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            header1 = ['区段长度', '电缆长度']
            header2 = ['区段长度', '电缆长度']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 6 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-1-10遍历被串是否发码
def draw_table_4_1_10(parent_root):
    sub_dir = '4-1-10遍历被串是否发码'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-1-10遍历被串是否发码'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'

            show_table = {
                '是': '发码',
                '不发码': '不发码',
            }

            s2 = df['被串是否发码'].astype(str).apply(lambda x: show_table[x])

            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)
            header1 = ['区段长度', '被串\n是否发码']
            header2 = ['区段长度', '被串\n是否发码']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 2 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-2-1遍历错位
def draw_table_4_2_1(parent_root):
    sub_dir = '4-2-1遍历错位'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        # [800, 1000],
        [400, 600, 800, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-2-1遍历错位_{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'

                s2 = df['被串相对位置(m)'].astype(str) + 'm'
                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                header1 = ['区段长度', '相对位置']
                header2 = ['区段长度', '相对位置']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')


        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '区段长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-2-3遍历方向
def draw_table_4_2_3(parent_root):
    sub_dir = '4-2-3遍历方向'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        [600, 800],
        [1000],
        # [400, 600, 800, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-2-3遍历方向_{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df = df.sort_values(by=['主串区段长度(m)', '被串相对位置(m)'])
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'
                s2 = df['被串相对位置(m)'].astype(str) + 'm'

                show_table = {
                    '右发': '反向',
                    '左发': '同向',
                }

                s3 = df['主串方向'].astype(str).apply(lambda x: show_table[x])

                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                ret = pd.concat([ret, s3], axis=1, sort=False)
                header1 = ['区段长度', '相对位置', '发送方向']
                header2 = ['区段长度', '相对位置', '发送方向']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')


        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '区段长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.7)

            elif row % 2 == 1:
                draw_line(table, ax, data, row, start=1, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-2-4遍历分路模式
def draw_table_4_2_4(parent_root):
    sub_dir = '4-2-4遍历分路模式'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        [600],
        # [600, 800],
        # [1000],
        # [400, 600, 800, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-2-4遍历分路模式_{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df = df.sort_values(by=['主串区段长度(m)', '被串相对位置(m)'])
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'
                s2 = df['被串相对位置(m)'].astype(str) + 'm'

                show_table = {
                    '主串调整被串分路': '主串调整',
                    '主被串同时分路': '同时分路',
                }

                s3 = df['分路模式'].astype(str).apply(lambda x: show_table[x])

                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                ret = pd.concat([ret, s3], axis=1, sort=False)
                header1 = ['区段长度', '相对位置', '分路模式']
                header2 = ['区段长度', '相对位置', '分路模式']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')


        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '区段长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.7)

            elif row % 2 == 1:
                draw_line(table, ax, data, row, start=1, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-2-5遍历被串是否发码
def draw_table_4_2_5(parent_root):
    sub_dir = '4-2-5遍历被串是否发码'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        [600, 800],
        [1000],
        # [400, 600, 800, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-2-5遍历被串是否发码{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df = df.sort_values(by=['主串区段长度(m)', '被串相对位置(m)'])
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'
                s2 = df['被串相对位置(m)'].astype(str) + 'm'

                show_table = {
                    '是': '发码',
                    '不发码': '不发码',
                }

                s3 = df['被串是否发码'].astype(str).apply(lambda x: show_table[x])

                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                ret = pd.concat([ret, s3], axis=1, sort=False)
                header1 = ['区段长度', '相对位置', '被串\n是否发码']
                header2 = ['区段长度', '相对位置', '被串\n是否发码']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')

        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '区段长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.7)

            elif row % 2 == 1:
                draw_line(table, ax, data, row, start=1, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-3-1-1遍历一端对齐主串
def draw_table_4_3_1_1(parent_root):
    sub_dir = '4-3-1-1遍历一端对齐主串'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        # [800, 1000],
        # [400, 600, 800, 1000],
        [400, 500, 600, 700, 800, 900, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-3-1遍历一端对齐_{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'
                s2 = df['被串区段长度(m)'].astype(str) + 'm'
                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                header1 = ['主串长度', '被串长度']
                header2 = ['主串长度', '被串长度']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')

        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '主串长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-3-3遍历方向
def draw_table_4_3_3(parent_root):
    sub_dir = '4-3-3遍历方向'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        # [600, 800],
        # [1000],
        [400, 600, 800, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-3-3遍历方向_{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df = df.sort_values(by=['主串区段长度(m)', '被串区段长度(m)'])
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'
                s2 = df['被串区段长度(m)'].astype(str) + 'm'

                show_table = {
                    '右发': '反向',
                    '左发': '同向',
                }

                s3 = df['主串方向'].astype(str).apply(lambda x: show_table[x])

                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                ret = pd.concat([ret, s3], axis=1, sort=False)
                header1 = ['主串长度', '被串长度', '发送方向']
                header2 = ['主串长度', '被串长度', '发送方向']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')


        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '区段长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.7)

            elif row % 2 == 1:
                draw_line(table, ax, data, row, start=1, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-3-4遍历分路模式
def draw_table_4_3_4(parent_root):
    sub_dir = '4-3-4遍历分路模式'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        # [600, 800],
        # [1000],
        [400, 600, 800, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-3-4遍历分路模式_{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df = df.sort_values(by=['主串区段长度(m)', '被串区段长度(m)'])
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'
                s2 = df['被串区段长度(m)'].astype(str) + 'm'

                show_table = {
                    '主串调整被串分路': '主串调整',
                    '主被串同时分路': '同时分路',
                }

                s3 = df['分路模式'].astype(str).apply(lambda x: show_table[x])

                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                ret = pd.concat([ret, s3], axis=1, sort=False)
                header1 = ['主串长度', '被串长度', '分路模式']
                header2 = ['主串长度', '被串长度', '分路模式']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')


        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '区段长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.7)

            elif row % 2 == 1:
                draw_line(table, ax, data, row, start=1, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-3-5遍历被串是否发码
def draw_table_4_3_5(parent_root):
    sub_dir = '4-3-5遍历被串是否发码'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'
    df0, res_dir = config_file(root, file)

    list0 = [
        # [400, 600],
        # [600, 800],
        # [1000],
        [400, 600, 800, 1000],
    ]

    for index, list1 in enumerate(list0):

        fig_name = f'4-3-5遍历被串是否发码_{index+1}'
        # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
        fig_path = res_dir + f'\\{fig_name}.png'

        df1 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

        ret = pd.DataFrame()

        freq_zhu_list = [1700, 2000, 2300, 2600]

        header1 = []
        header2 = []

        for i, freq_zhu in enumerate(freq_zhu_list):
            df = df1.loc[df1["主串频率(Hz)"] == freq_zhu].copy()
            df = df.sort_values(by=['主串区段长度(m)', '被串区段长度(m)'])
            df.index = range(df.shape[0])

            if i == 0 :
                s1 = df['主串区段长度(m)'].astype(str) + 'm'
                s2 = df['被串区段长度(m)'].astype(str) + 'm'

                show_table = {
                    '是': '发码',
                    '不发码': '不发码',
                }

                s3 = df['被串是否发码'].astype(str).apply(lambda x: show_table[x])

                ret = pd.concat([ret, s1], axis=1, sort=False)
                ret = pd.concat([ret, s2], axis=1, sort=False)
                ret = pd.concat([ret, s3], axis=1, sort=False)
                header1 = ['主串长度', '被串长度', '被串\n是否发码']
                header2 = ['主串长度', '被串长度', '被串\n是否发码']

            s1 = df['被串最大干扰电流(A)'].copy()
            s1 = s1 * 1000
            s1 = s1.apply(lambda x: f"{x:,.2f}")
            # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
            ret = pd.concat([ret, s1], axis=1, sort=False)


            s2 = df['被串最大干扰位置(m)'].copy()
            s2 = s2.apply(lambda x: f"{x:,.0f}")
            # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1.append(f'主串频率{freq_zhu}Hz')
            header1.append(f'主串频率{freq_zhu}Hz')
            header2.append(f'最大值/mA')
            header2.append(f'位置/m')

        data = ret.values.tolist()
        data = [header1] + [header2] + data
        for val in data:
            print(val)

        #################################################################################################
        # 画表格
        # fig, ax, table = config_ax(data=data, color='#e2efda')
        fig, ax, table = config_ax(data=data, color='#d9ead3')


        merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
        m_lst = merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
        merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

        row_list = []
        for val in m_lst:
            if val[-1] != '区段长度':
                row_list.append(val[2])

        n_rows = len(data)
        for row in range(n_rows):

            if row == 0:
                draw_line(table, ax, data, row, edge='T', linewidth=2)

            elif row == n_rows-1:
                draw_line(table, ax, data, row, edge='B', linewidth=2)

            elif row == 1:
                draw_line(table, ax, data, row, edge='B', linewidth=1)
                draw_line(table, ax, data, row,start=3, edge='T', linewidth=1)

            elif row in row_list:
                draw_line(table, ax, data, row, edge='B', linewidth=0.7)

            elif row % 2 == 1:
                draw_line(table, ax, data, row, start=1, edge='B', linewidth=0.2)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path)


# 4-4-1遍历主串电容容值
def draw_table_4_4_1(parent_root):
    sub_dir = '4-4-1遍历主串电容容值'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-4-1遍历主串电容容值'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    list1 = [400, 600, 800, 1000]
    df0 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'
            s2 = df['主串电容值(μF)'].astype(str).apply(lambda x: f'{x}μF')

            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1 = ['区段长度', '主串电容值']
            header2 = ['区段长度', '主串电容值']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 9 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


# 4-4-2遍历被串电容容值
def draw_table_4_4_2(parent_root):
    sub_dir = '4-4-2遍历被串电容容值'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df0, res_dir = config_file(root, file)
    fig_name = '4-4-2遍历被串电容容值'
    # pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])
    fig_path = res_dir + f'\\{fig_name}.png'

    list1 = [400, 600, 800, 1000]
    df0 = df0.loc[df0["主串区段长度(m)"].isin(list1)].copy()

    ret = pd.DataFrame()

    freq_zhu_list = [1700, 2000, 2300, 2600]

    header1 = []
    header2 = []

    for i, freq_zhu in enumerate(freq_zhu_list):
        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()
        df.index = range(df.shape[0])

        if i == 0 :
            s1 = df['主串区段长度(m)'].astype(str) + 'm'
            s2 = df['被串电容值(μF)'].astype(str).apply(lambda x: f'{x}μF')

            ret = pd.concat([ret, s1], axis=1, sort=False)
            ret = pd.concat([ret, s2], axis=1, sort=False)

            header1 = ['区段长度', '被串电容值']
            header2 = ['区段长度', '被串电容值']

        s1 = df['被串最大干扰电流(A)'].copy()
        s1 = s1 * 1000
        s1 = s1.apply(lambda x: f"{x:,.2f}")
        # s1.name = f'被串频率{freq_bei}Hz\n最大干扰电流(mA)'
        ret = pd.concat([ret, s1], axis=1, sort=False)


        s2 = df['被串最大干扰位置(m)'].copy()
        s2 = s2.apply(lambda x: f"{x:,.0f}")
        # s2.name = f'被串频率{freq_bei}Hz\n最大干扰位置(m)'
        ret = pd.concat([ret, s2], axis=1, sort=False)

        header1.append(f'主串频率{freq_zhu}Hz')
        header1.append(f'主串频率{freq_zhu}Hz')
        header2.append(f'最大值/mA')
        header2.append(f'位置/m')

    data = ret.values.tolist()
    data = [header1] + [header2] + data
    for val in data:
        print(val)

    #################################################################################################
    # 画表格

    fig, ax, table = config_ax(data=data)

    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='row')
    merge_duplicate(table=table, ax=ax, data=data, index=0, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=1, mode='col')
    merge_duplicate(table=table, ax=ax, data=data, index=2, mode='col')

    n_rows = len(data)
    for row in range(n_rows):

        if row == 0:
            draw_line(table, ax, data, row, edge='T', linewidth=2)

        elif row == n_rows-1:
            draw_line(table, ax, data, row, edge='B', linewidth=2)

        elif row == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=1)
            draw_line(table, ax, data, row,start=2, edge='T', linewidth=1)

        elif row % 9 == 1:
            draw_line(table, ax, data, row, edge='B', linewidth=0.2)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path)


def main():
    import matplotlib.font_manager as fm
    from matplotlib.font_manager import ttfFontProperty
    from matplotlib.ft2font import FT2Font

    font_path = r'C:\Windows\Fonts\simsun.ttc'
    font_prop = fm.FontProperties(fname=font_path)
    # font_name = font_prop.get_name()
    font_entry = ttfFontProperty(FT2Font(font_path))
    fm.fontManager.ttflist.append(font_entry)

    # plt.rcParams['font.family'] = 'serif'
    # plt.rcParams['font.serif'] = ['Times New Roman', 'SimSun']  # 用来正常显示中文标签

    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['STSong']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False

    # plt.rcParams['mathtext.fontset'] = 'stix'  # 数学公式使用与Times兼容的STIX字体
    # plt.rcParams['axes.unicode_minus'] = False

    parent_root = 'C:\\Users\\Delon\\Desktop\\普速列控邻线干扰\\数据汇总'
    # parent_root = 'C:\\Users\\李继隆\\Desktop\\普速铁路新一代列控系统项目\\数据汇总'


    # draw_table_4_1_1(parent_root)
    draw_table_4_1_2(parent_root)
    # draw_table_4_1_3(parent_root)
    # draw_table_4_1_4(parent_root)
    # draw_table_4_1_5(parent_root)
    # draw_table_4_1_6_1(parent_root)
    # draw_table_4_1_7_1(parent_root)
    # draw_table_4_1_8_1(parent_root)
    # draw_table_4_1_9(parent_root)
    # draw_table_4_1_10(parent_root)
    # draw_table_4_2_1(parent_root)
    # draw_table_4_2_3(parent_root)
    # draw_table_4_2_4(parent_root)
    # draw_table_4_2_5(parent_root)
    # draw_table_4_3_1_1(parent_root)
    # draw_table_4_3_3(parent_root)
    # draw_table_4_3_4(parent_root)
    # draw_table_4_3_5(parent_root)
    # draw_table_4_4_1(parent_root)
    # draw_table_4_4_2(parent_root)


if __name__ == '__main__':
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 10000)
    main()
    pass
