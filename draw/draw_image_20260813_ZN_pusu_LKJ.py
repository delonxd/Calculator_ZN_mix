import os
import time
import numpy as np
import pandas as pd
# import matplotlib as mpl

import matplotlib.pyplot as plt
import itertools
from matplotlib import cm


def config_file(parent_root, sub_dir):
    # root = 'C:\\Users\\Delon\\Desktop\\普速列控邻线干扰\\数据汇总\\4-1-1遍历频率\\'
    # file = '仿真输出_20260813_普速列控_4-1-1遍历频率.xlsx'
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df_data1 = pd.read_excel(root + file, '数据输出')
    df_data2 = pd.read_excel(root + file, '被串钢轨电流')
    df_combine = pd.concat([df_data1, df_data2], axis=1)

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = root + '生成2col图片_%s' % timestamp

    return df_combine, res_dir


def config_fig(fig, fig_title):
    ######################################################################################################
    # 主图设置

    ax_rows = 4
    ax_height = 1 / (ax_rows + 1)
    top = 1 - 0.11/0.2* ax_height
    bottom = 0.09/0.2* ax_height

    fig.subplots_adjust(hspace=0.3, wspace=0.1, left=0.12, right=0.88, top=top, bottom=bottom)
    # fig.subplots_adjust(hspace=0.4, wspace=0.1, top=0.8, left=0.15, right=0.85)

    pos = 1 - 0.03/0.2 * ax_height
    fig.suptitle(
        fig_title, x=0.5, y=pos, va='center', ha='center',
        fontsize=15, fontfamily='SimSun',
    )

    ######################################################################################################
    # 主图坐标轴

    pos = bottom / 2
    plt.text(
        0.5, pos, '被串分路位置/m',
        va='top', ha='center', transform=fig.transFigure,
        fontsize=10, weight='bold',
    )

    plt.text(
        0.05, 0.5, '邻线干扰电流/mA',
        va='center', ha='center', transform=fig.transFigure,
        fontsize=10, weight='bold', rotation=90,
    )

    ######################################################################################################
    # # 调整位置
    # plt.tight_layout()


def config_ax(ax, ax_title, sec_length, row=0, col=0, legend_mode='out'):
    ######################################################################################################
    # 子图设置

    ax.set_title(ax_title, pad=3, fontsize=8)
    # ax.set_title(title, x=0.5, y=1.04, fontsize=30)

    ax.xaxis.grid(True, which='major', linestyle='--')
    ax.yaxis.grid(True, which='major', linestyle='--')
    # fig.suptitle(title, fontsize=30)

    ######################################################################################################
    # 坐标轴

    # ax.set_xlabel('被串分路位置(m)', fontsize=18)
    # ax.set_ylabel('邻线干扰钢轨电流(mA)', fontsize=20)

    # ax.yaxis.set_font(20)
    # ax.set_ylim([0, 0.5])

    t = np.arange(0, sec_length + 1, 100)
    x_ticks = list(t)
    x_ticks_labels = list(map(lambda x: f'{x}m', t))
    x_ticks_labels[0] = '发送'

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks_labels)

    ax.tick_params(
        labelsize=5,
        direction='in',
    )

    ######################################################################################################
    # 图例
    _, labels = ax.get_legend_handles_labels()

    if legend_mode == 'out':
        if col == 1:
            ncol = (len(labels)+9) // 10
            ax.legend(
                bbox_to_anchor=(1.025, 0.5),
                loc='center left',
                fontsize=5,
                borderaxespad=0.,
                # ncol=ncol,
            )

    elif legend_mode == 'out-one':
        if col == 1 and row == 0:
            ax.legend(
                bbox_to_anchor=(1.05, 0),
                loc='center left',
                fontsize=5,
                borderaxespad=0.
            )

    elif legend_mode == '4in':
        ax.legend(loc='upper right', fontsize=5)

    # ax.legend(
    #     loc='upper right',
    #     # bbox_to_anchor=(0.96, 0.9),
    #     bbox_to_anchor=(0.46, 0.9),
    #     # ncol=2,
    #     # title='Legend Title',
    #     fontsize=13,
    # )

    ######################################################################################################
    # # 颜色条
    # cb_x = 0.2
    # cb_y = 0.59
    # # cb_pos = 0.9
    #
    # cax = fig.add_axes([cb_x, cb_y, 0.01, 0.25])  # 四个参数分别是左、下、宽、长
    #
    # norm = mpl.colors.Normalize(vmin=0, vmax=800)
    # bounds = [tmp for tmp in np.linspace(0, 800, size0+1)]
    # cb = mpl.colorbar.ColorbarBase(
    #     ax=cax,
    #     cmap=c_map,
    #     norm=norm,
    #     # to use 'extend', you must
    #     # specify two extra boundaries:
    #     # boundaries=[1.2] + bounds + [2.6],
    #     boundaries=bounds,
    #     # extend='both',
    #     # ticks=[1.3, 2.5],  # optional
    #     # ticks=[-100, 100],  # optional
    #     ticks=[],  # optional
    #     # spacing='proportional',
    #     orientation='vertical'
    # )
    #
    # cb.set_ticks([0, 400, 800])
    # cb.set_ticklabels(['0m', '400m', '800m'])
    #
    # cax.tick_params(labelsize=14, direction='out')

    ######################################################################################################
    # # 标签
    # txt = '主串列车\n距发送器\n距离(m)'
    # # txt = '\n'.join(list(txt))
    # ax.text(
    #     -0.5, 0.5,
    #     txt,
    #     fontsize=14,
    #     color='black',
    #     va='center',
    #     ha='right',
    #     transform=cax.transAxes,
    # )

    ######################################################################################################
    # # 辅助直线
    #
    # yy = np.ones(column_size) * max_i
    # xx = np.arange(yy.size)
    #
    # ax.plot(
    #     xx,
    #     yy,
    #     linestyle='--',
    #     alpha=1,
    #     color='blue',
    #     linewidth=1,
    # )

    ######################################################################################################
    # # 辅助文本
    #
    # txt = '最大干扰电流%.2fmA' % (max_i * 1000)
    # ax.text(
    #     0.2, 0.9,
    #     txt,
    #     fontsize=16,
    #     color='blue',
    #     va='center',
    #     ha='left',
    #     transform=ax.transAxes,
    # )
    #
    ######################################################################################################
    # # 箭头
    #
    # # y1 = min(max_list)
    # # x1 = max_list.index(y1)
    #
    # y1 = max_i_value
    # x1 = max_i_posi
    #
    # # txt = '最优扼流变比$\mathrm{%s:1}$\n最大干扰电流$\mathrm{%.2fmA}$' % (x1+5, y1)
    # txt = '最大干扰位置%sm\n干扰电流%.2fmA' % (x1, y1*1000)
    #
    # ax.annotate(
    #     txt, (x1, y1),
    #     xytext=(x1 - 50, y1 - 0.04),
    #     ha="right", va="center",
    #     # textcoords='offset points',
    #     fontsize=12,
    #     color='blue',
    #     arrowprops=dict(
    #         # facecolor='#74C476',
    #         alpha=0.6,
    #         arrowstyle='fancy',
    #         # connectionstyle='arc3,rad=0.5',
    #         color='blue',
    #     )
    # )


def config_file_4col(parent_root, sub_dir):
    root = f'{parent_root}\\{sub_dir}\\'
    file = f'仿真输出_20260813_普速列控_{sub_dir}.xlsx'

    df_data1 = pd.read_excel(root + file, '数据输出')
    df_data2 = pd.read_excel(root + file, '被串钢轨电流')
    df_combine = pd.concat([df_data1, df_data2], axis=1)

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = root + '生成4col图片_%s' % timestamp

    return df_combine, res_dir


def config_fig_4col(fig, fig_title, ax_rows, ax_cols):
    ######################################################################################################
    # 主图设置

    ax_height = 1 / (ax_rows + 1)
    top = 1 - 0.11/0.2* ax_height
    bottom = 0.09/0.2* ax_height

    fig.subplots_adjust(hspace=0.3, wspace=0.1, left=0.12, right=0.88, top=top, bottom=bottom)
    # fig.subplots_adjust(hspace=0.4, wspace=0.1, top=0.8, left=0.15, right=0.85)

    pos = 1 - 0.03/0.2 * ax_height
    fig.suptitle(
        fig_title, x=0.5, y=pos, va='center', ha='center',
        fontsize=15, fontfamily='SimSun',
    )

    ######################################################################################################
    # 主图坐标轴

    pos = bottom / 2
    plt.text(
        0.5, pos, '被串分路位置/m',
        va='top', ha='center', transform=fig.transFigure,
        fontsize=10, fontweight='normal',
    )

    plt.text(
        0.05, 0.5, '邻线干扰电流/mA',
        va='center', ha='center', transform=fig.transFigure,
        fontsize=10, fontweight='normal', rotation=90,
    )

    # ######################################################################################################
    # # 调整位置
    # plt.tight_layout()


def config_ax_4col(
        ax, ax_title, sec_length, row, col,
        y_ticks=None, one_legend=False,
        ylim=200, row_titles=None,
):
    ######################################################################################################
    # 子图设置

    if row == 0:
        ax.set_title(ax_title, pad=3, fontsize=8)
    # ax.set_title(title, x=0.5, y=1.04, fontsize=30)

    ax.xaxis.grid(True, which='major', linestyle='--')
    ax.yaxis.grid(True, which='major', linestyle='--')
    # fig.suptitle(title, fontsize=30)

    ######################################################################################################
    # 坐标轴

    # ax.set_xlabel('被串分路位置(m)', fontsize=18)
    # ax.set_ylabel('邻线干扰钢轨电流(mA)', fontsize=9, rotation=90)

    if row_titles is not None:
        row_title = row_titles.get(row)
        if row_title is not None:
            if col == 0:
                ax.set_ylabel(
                    row_title, fontsize=8, rotation=90,
                    ha='center', va='bottom',
                    # labelpad=15,
                )
                ax.yaxis.set_label_coords(-0.15, 0.5)
                print(row_title)

    # ax.yaxis.set_font(20)
    ax.set_ylim([0, ylim])

    if y_ticks is None:
        y_ticks = [0, 50, 100, 150, 200]

    if col == 0:
        y_ticks_labels = y_ticks
    else:
        y_ticks_labels = [''] * len(y_ticks)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks_labels)

    t = np.arange(0, sec_length + 1, 200)
    x_ticks = list(t)
    x_ticks_labels = list(map(lambda x: f'{x}m', t))
    x_ticks_labels[0] = '发送'

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks_labels)

    ax.tick_params(
        # axis='y',
        labelsize=5,  # y轴字体大小设置
        # color='r',  # y轴标签颜色设置
        # labelcolor='b',  # y轴字体颜色设置
        direction='in',  # y轴标签方向设置
        # pad=10,
    )

    ######################################################################################################
    # 图例
    _, labels = ax.get_legend_handles_labels()
    if one_legend is True:
        if col == 3 and row == 1:
            ax.legend(bbox_to_anchor=(1.05, 0), loc='center left', fontsize=5, borderaxespad=0.)
    else:
        if col == 3:
            # ncol = (len(labels)+9) // 10
            print(len(labels))
            # ax.legend(loc='upper right', fontsize=5, ncol=ncol)
            ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left', fontsize=5, borderaxespad=0.)


# 4-1-1遍历频率
def draw_image_4_1_1(parent_root):
    sub_dir = '4-1-1遍历频率'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [600]

    for sec_length in list1:

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m'
        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            freq_bei_list = [1700, 2000, 2300, 2600]
            for i, freq_bei in enumerate(freq_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串频率(Hz)"] == freq_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'被串{freq_bei}Hz'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)
        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-1遍历频率-4col
def draw_image_4_1_1_4col(parent_root):
    sub_dir = '4-1-1遍历频率'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历区段长度'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)
            freq_bei_list = [1700, 2000, 2300, 2600]
            for i, freq_bei in enumerate(freq_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串频率(Hz)"] == freq_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.25
                label = f'被串{freq_bei}Hz'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)

# 4-1-2遍历长度
def draw_image_4_1_2(parent_root):
    sub_dir = '4-1-2遍历长度'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # 配置 fig
    fig = plt.figure(figsize=(7, 4), dpi=200)
    fig_title = f'等长对位-遍历区段长度'
    fig_path = res_dir + f'\\{fig_title}.png'

    ax_list = []

    freq_zhu_list = [1700, 2000, 2300, 2600]
    for j, freq_zhu in enumerate(freq_zhu_list):

        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()

        ax = fig.add_subplot(2, 2, j + 1)
        ax_list.append(ax)

        ax_title = f'主串频率-{freq_zhu}Hz'

        ######################################################################################################
        # 画线
        sec_length_list = [400, 500, 600, 700, 800, 900, 1000]

        for i, sec_length in enumerate(sec_length_list):

            df1 = df.loc[df["主串区段长度(m)"] == sec_length]

            if len(df1.index) != 1:
                raise KeyboardInterrupt('error: len(index) != 1')

            yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()
            xx1 = range(sec_length + 1)

            color = cm.rainbow(i / len(sec_length_list))

            width = 0.5
            label = f'区段长度{sec_length}m'
            ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

        col = j % 2
        config_ax(ax, ax_title, 1000, col=col)

    config_fig(fig, fig_title)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-3遍历方向
def draw_image_4_1_3(parent_root):
    sub_dir = '4-1-3遍历方向'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]

    for sec_length in list1:

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m'
        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            dir_zhu_list = ['右发', '左发']

            dir_table = {
                '右发': '反向',
                '左发': '同向',
            }

            for i, dir_zhu in enumerate(dir_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串方向"] == dir_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.5
                label = dir_table[dir_zhu]
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)
        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-3遍历方向-4col
def draw_image_4_1_3_4col(parent_root):
    sub_dir = '4-1-3遍历方向'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历发送方向'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)
            dir_zhu_list = ['右发', '左发']
            dir_table = {
                '右发': '反向',
                '左发': '同向',
            }
            for i, dir_zhu in enumerate(dir_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串方向"] == dir_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.25
                label = dir_table[dir_zhu]
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-4遍历分路模式
def draw_image_4_1_4(parent_root):
    sub_dir = '4-1-4遍历分路模式'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]

    for sec_length in list1:

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m'
        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            sht_mode_list = ['主串调整被串分路', '主被串同时分路']
            show_table = {
                '主串调整被串分路': '主调整被分路',
                '主被串同时分路': '主被同时分路',
            }
            for i, sht_mode in enumerate(sht_mode_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["分路模式"] == sht_mode)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.5
                label = show_table[sht_mode]
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)
        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-4遍历分路模式-4col
def draw_image_4_1_4_4col(parent_root):
    sub_dir = '4-1-4遍历分路模式'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历分路模式'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            sht_mode_list = ['主串调整被串分路', '主被串同时分路']

            show_table = {
                '主串调整被串分路': '主调整被分路',
                '主被串同时分路': '主被同时分路',
            }
            for i, sht_mode in enumerate(sht_mode_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["分路模式"] == sht_mode)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.25
                label = show_table[sht_mode]
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-5遍历电容间距
def draw_image_4_1_5(parent_root):
    sub_dir = '4-1-5遍历电容间距'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]

    for sec_length in list1:

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-遍历电容间距-区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            interval_list = ['50m', '60m', '70m', '80m', '90m', '100m', '110m', '120m', '130m', '140m', '150m']

            for i, interval in enumerate(interval_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电容间隔"] == interval)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(interval_list))
                width = 0.5
                label = f'电容间距{interval}'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-5遍历电容间距-4col
def draw_image_4_1_5_4col(parent_root):
    sub_dir = '4-1-5遍历电容间距'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历分路模式'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            interval_list = ['50m', '60m', '70m', '80m', '90m', '100m', '110m', '120m', '130m', '140m', '150m']

            for i, interval in enumerate(interval_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电容间隔"] == interval)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(interval_list))
                width = 0.5
                label = f'电容间距{interval}'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-6-1遍历电容容值主串
def draw_image_4_1_6_1(parent_root):
    sub_dir = '4-1-6-1遍历电容容值主串'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list2 = ['普速既有', 25, 50]
    list2 = [50]

    clist = list(itertools.product(list1, list2))

    c_mode_table = {
        '普速既有': '普速既有容值',
        25: '25μF',
        50: '50μF',
    }
    for val in clist:

        sec_length = val[0]
        c_mode_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串电容值配置"] == c_mode_bei)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-被串容值{c_mode_table[c_mode_bei]}'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_mode_zhu_list = ['普速既有', 25, 50]
            for i, c_mode_zhu in enumerate(c_mode_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电容值配置"] == c_mode_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                c_value_zhu = df1.iloc[0, :]['主串电容值(μF)']
                # c_value_bei = df1.iloc[0, :]['被串电容值(μF)']

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                if c_mode_zhu == '普速既有':
                    label = f'主串容值{c_value_zhu}μF\n(既有)'
                else:
                    label = f'主串容值{c_value_zhu}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col, legend_mode='4in')

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-6-1遍历电容容值主串-4col
def draw_image_4_1_6_1_4col(parent_root):
    sub_dir = '4-1-6-1遍历电容容值主串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [50]
    clist = list(itertools.product(list1, list2))

    c_mode_table = {
        '普速既有': '普速既有容值',
        25: '25μF',
        50: '50μF',
    }

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历主串电容容值'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        c_mode_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串电容值配置"] == c_mode_bei)
        ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_mode_zhu_list = ['普速既有', 25, 50]
            for i, c_mode_zhu in enumerate(c_mode_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电容值配置"] == c_mode_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                c_value_zhu = df1.iloc[0, :]['主串电容值(μF)']
                # c_value_bei = df1.iloc[0, :]['被串电容值(μF)']

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                if c_mode_zhu == '普速既有':
                    label = f'主串容值既有'
                else:
                    label = f'主串容值{c_value_zhu}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-6-2遍历电容容值被串
def draw_image_4_1_6_2(parent_root):
    sub_dir = '4-1-6-2遍历电容容值被串'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list2 = ['普速既有', 25, 50]
    list2 = [50]

    clist = list(itertools.product(list1, list2))

    c_mode_table = {
        '普速既有': '普速既有容值',
        25: '25μF',
        50: '50μF',
    }
    for val in clist:

        sec_length = val[0]
        c_mode_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串电容值配置"] == c_mode_zhu)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-主串容值{c_mode_table[c_mode_zhu]}'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_mode_bei_list = ['普速既有', 25, 50]
            for i, c_mode_bei in enumerate(c_mode_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串电容值配置"] == c_mode_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                # c_value_zhu = df1.iloc[0, :]['主串电容值(μF)']
                c_value_bei = df1.iloc[0, :]['被串电容值(μF)']

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                if c_mode_bei == '普速既有':
                    label = f'被串容值{c_value_bei}μF\n(既有)'
                else:
                    label = f'被串容值{c_value_bei}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col, legend_mode='4in')

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-6-2遍历电容容值被串-4col
def draw_image_4_1_6_2_4col(parent_root):
    sub_dir = '4-1-6-2遍历电容容值被串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [50]
    clist = list(itertools.product(list1, list2))

    c_mode_table = {
        '普速既有': '普速既有容值',
        25: '25μF',
        50: '50μF',
    }

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历被串电容容值'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        c_mode_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串电容值配置"] == c_mode_zhu)
        ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_mode_bei_list = ['普速既有', 25, 50]
            for i, c_mode_bei in enumerate(c_mode_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串电容值配置"] == c_mode_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                # c_value_zhu = df1.iloc[0, :]['主串电容值(μF)']
                c_value_bei = df1.iloc[0, :]['被串电容值(μF)']

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                if c_mode_bei == '普速既有':
                    label = f'被串容值既有'
                else:
                    label = f'被串容值{c_value_bei}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)
            ######################################################################################################

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    plt.show()
    raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-7-1遍历调整电阻主串
def draw_image_4_1_7_1(parent_root):
    sub_dir = '4-1-7-1遍历调整电阻主串'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list2 = ['普速既有', 25, 50]
    # list2 = [50, 100, 150, 200]
    list2 = [100]

    clist = list(itertools.product(list1, list2))

    for val in clist:

        sec_length = val[0]
        r_adj_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串调整电阻(Ω)"] == r_adj_bei)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-被串调整电阻{r_adj_bei}Ω'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            r_adj_zhu_list = [50, 100, 150, 200]
            for i, r_adj_zhu in enumerate(r_adj_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串调整电阻(Ω)"] == r_adj_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'主串调整电阻\n{r_adj_zhu}Ω'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-7-1遍历调整电阻主串-4col
def draw_image_4_1_7_1_4col(parent_root):
    sub_dir = '4-1-7-1遍历调整电阻主串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [100]
    clist = list(itertools.product(list1, list2))

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历主串调整电阻'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        r_adj_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串调整电阻(Ω)"] == r_adj_bei)
        ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            r_adj_zhu_list = [50, 100, 150, 200]
            for i, r_adj_zhu in enumerate(r_adj_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串调整电阻(Ω)"] == r_adj_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'主串调整电阻\n{r_adj_zhu}Ω'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-7-2遍历调整电阻被串
def draw_image_4_1_7_2(parent_root):
    sub_dir = '4-1-7-2遍历调整电阻被串'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list2 = ['普速既有', 25, 50]
    # list2 = [50, 100, 150, 200]
    list2 = [100]

    clist = list(itertools.product(list1, list2))

    for val in clist:

        sec_length = val[0]
        r_adj_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串调整电阻(Ω)"] == r_adj_zhu)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-主串调整电阻{r_adj_zhu}Ω'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            r_adj_bei_list = [50, 100, 150, 200]
            for i, r_adj_bei in enumerate(r_adj_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串调整电阻(Ω)"] == r_adj_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'被串调整电阻\n{r_adj_bei}Ω'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-7-2遍历调整电阻被串-4col
def draw_image_4_1_7_2_4col(parent_root):
    sub_dir = '4-1-7-2遍历调整电阻被串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [100]
    clist = list(itertools.product(list1, list2))

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历被串调整电阻'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        r_adj_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串调整电阻(Ω)"] == r_adj_zhu)
        ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            r_adj_bei_list = [50, 100, 150, 200]
            for i, r_adj_bei in enumerate(r_adj_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串调整电阻(Ω)"] == r_adj_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'被串调整电阻\n{r_adj_bei}Ω'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-8-1遍历FT1U输出电压主串
def draw_image_4_1_8_1(parent_root):
    sub_dir = '4-1-8-1遍历FT1U输出电压主串'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    list2 = [60]

    clist = list(itertools.product(list1, list2))

    for val in clist:

        sec_length = val[0]
        v_adj_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串FT1U输出电压(V)"] == v_adj_bei)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-被串FT1U输出电压{v_adj_bei}V'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            v_adj_zhu_list = [60, 80, 100]
            for i, v_adj_zhu in enumerate(v_adj_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串FT1U输出电压(V)"] == v_adj_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'主串FT1U\n输出电压{v_adj_zhu}V'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-8-1遍历FT1U输出电压主串-4col
def draw_image_4_1_8_1_4col(parent_root):
    sub_dir = '4-1-8-1遍历FT1U输出电压主串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [60]
    clist = list(itertools.product(list1, list2))

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历主串FT1U输出电压'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        v_adj_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串FT1U输出电压(V)"] == v_adj_bei)
            ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            v_adj_zhu_list = [60, 80, 100]
            for i, v_adj_zhu in enumerate(v_adj_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串FT1U输出电压(V)"] == v_adj_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'主串FT1U\n输出电压{v_adj_zhu}V'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True, ylim=300)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-8-2遍历FT1U输出电压被串
def draw_image_4_1_8_2(parent_root):
    sub_dir = '4-1-8-2遍历FT1U输出电压被串'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    list2 = [60]

    clist = list(itertools.product(list1, list2))

    for val in clist:

        sec_length = val[0]
        v_adj_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串FT1U输出电压(V)"] == v_adj_zhu)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-主串FT1U输出电压{v_adj_zhu}V'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            v_adj_bei_list = [60, 80, 100]
            for i, v_adj_bei in enumerate(v_adj_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串FT1U输出电压(V)"] == v_adj_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'被串FT1U\n输出电压{v_adj_bei}V'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-8-2遍历FT1U输出电压被串-4col
def draw_image_4_1_8_2_4col(parent_root):
    sub_dir = '4-1-8-2遍历FT1U输出电压被串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [60]
    clist = list(itertools.product(list1, list2))

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历被串FT1U输出电压'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        v_adj_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串FT1U输出电压(V)"] == v_adj_zhu)
        ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            v_adj_bei_list = [60, 80, 100]
            for i, v_adj_bei in enumerate(v_adj_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串FT1U输出电压(V)"] == v_adj_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color_list = [
                    'red',
                    'orange',
                    'blue',
                    'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'被串FT1U\n输出电压{v_adj_bei}V'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True, ylim=300)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-9遍历电缆长度
def draw_image_4_1_9(parent_root):
    sub_dir = '4-1-9遍历电缆长度'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]

    for val in list1:

        sec_length = val
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            cable_length_list = [5, 6, 7, 8, 9, 10]

            for i, cable_length in enumerate(cable_length_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电缆长度(km)"] == cable_length)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(cable_length_list))
                width = 0.5
                label = f'电缆长度{cable_length}km'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-9遍历电缆长度-4col
def draw_image_4_1_9_4col(parent_root):
    sub_dir = '4-1-9遍历电缆长度'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历电缆长度'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            cable_length_list = [5, 6, 7, 8, 9, 10]

            for i, cable_length in enumerate(cable_length_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电缆长度(km)"] == cable_length)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(cable_length_list))
                width = 0.25
                label = f'电缆长度{cable_length}km'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, ylim=250, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-1-10遍历被串是否发码
def draw_image_4_1_10(parent_root):
    sub_dir = '4-1-10遍历被串是否发码'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]

    for val in list1:

        sec_length = val
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            sr_mode_list = ['是', '不发码']
            sr_table = {
                '是': '被串发码',
                '不发码': '被串不发码',
            }
            for i, sr_mode in enumerate(sr_mode_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串是否发码"] == sr_mode)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'{sr_table[sr_mode]}'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, sec_length, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-10遍历被串是否发码-4col
def draw_image_4_1_10_4col(parent_root):
    sub_dir = '4-1-10遍历被串是否发码'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历被串是否发码'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            sr_mode_list = ['是', '不发码']
            sr_table = {
                '是': '被串发码',
                '不发码': '被串不发码',
            }
            for i, sr_mode in enumerate(sr_mode_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串是否发码"] == sr_mode)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.25
                label = f'{sr_table[sr_mode]}'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, ylim=250, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-2-1遍历错位 (向内/向外)
def draw_image_4_2_1(parent_root):
    sub_dir = '4-2-1遍历错位'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]

    for val in list1:

        sec_length = val
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长错位-区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            offset_list = df2["被串相对位置(m)"].copy().tolist()
            for i, offset in enumerate(offset_list):

                df1 = df2.loc[
                    (df2["被串相对位置(m)"] == offset)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.winter(i / len(offset_list))
                if offset == 0:
                    width = 1
                else:
                    width = 0.25
                label = f'错位{offset}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            row = j // 2
            col = j % 2
            config_ax(ax, ax_title, sec_length, row=row, col=col, legend_mode='out-one')

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-2-1遍历错位-4col
def draw_image_4_2_1_4col(parent_root):
    sub_dir = '4-2-1遍历错位'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长错位-遍历相对位置'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()
            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            offset_list = df2["被串相对位置(m)"].copy().tolist()
            for i, offset in enumerate(offset_list):

                df1 = df2.loc[
                    (df2["被串相对位置(m)"] == offset)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.winter(i / len(offset_list))
                if offset == 0:
                    width = 1
                else:
                    width = 0.25
                label = f'错位{offset}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, ylim=250, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)



# 4-2-3遍历方向
def draw_image_4_2_3(parent_root):
    sub_dir = '4-2-3遍历方向'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    for val in list1:
        sec_length = val
        # offset_list = range(-sec_length, sec_length+1, 100)
        offset_list = [-200, 0, 200]

        print(offset_list)
        for offset in offset_list:

            df = df0.loc[
                (df0["主串区段长度(m)"] == sec_length) &
                (df0["被串相对位置(m)"] == offset)
            ].copy()

            # 配置 fig
            fig = plt.figure(figsize=(7, 4), dpi=200)
            fig_title = f'等长错位-主串调整-区段长度{sec_length}m-错位{offset}m'

            fig_path = res_dir + f'\\{fig_title}.png'

            ax_list = []

            freq_zhu_list = [1700, 2000, 2300, 2600]
            for j, freq_zhu in enumerate(freq_zhu_list):

                ax = fig.add_subplot(2, 2, j + 1)
                ax_list.append(ax)

                ax_title = f'主串频率-{freq_zhu}Hz'

                ######################################################################################################
                # 画线

                xx1 = range(sec_length+1)

                dir_zhu_list = ['右发', '左发']

                dir_table = {
                    '右发': '反向',
                    '左发': '同向',
                }

                for i, dir_zhu in enumerate(dir_zhu_list):

                    df1 = df.loc[
                        (df["主串频率(Hz)"] == freq_zhu) &
                        (df["主串方向"] == dir_zhu)
                        ]

                    if len(df1.index) != 1:
                        raise KeyboardInterrupt('error: len(index) != 1')

                    yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                    color_list = [
                        'red',
                        # 'orange',
                        'blue',
                        # 'green',
                    ]

                    color = color_list[i]
                    width = 0.5
                    label = dir_table[dir_zhu]
                    ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

                col = j % 2
                config_ax(ax, ax_title, sec_length, col=col)

            config_fig(fig, fig_title)

            #################################################################################################
            # 保存
            # plt.show()
            # raise KeyboardInterrupt()

            if not os.path.exists(res_dir):
                os.makedirs(res_dir)

            fig.savefig(fig_path, transparent=True)


# 4-2-4遍历分路模式
def draw_image_4_2_4(parent_root):
    sub_dir = '4-2-4遍历分路模式'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    for val in list1:
        sec_length = val
        # offset_list = range(-sec_length, sec_length+1, 100)
        offset_list = [-200, 0, 200]

        print(offset_list)
        for offset in offset_list:

            df = df0.loc[
                (df0["主串区段长度(m)"] == sec_length) &
                (df0["被串相对位置(m)"] == offset)
            ].copy()

            # 配置 fig
            fig = plt.figure(figsize=(7, 4), dpi=200)
            fig_title = f'等长错位-主被同向-区段长度{sec_length}m-错位{offset}m'

            fig_path = res_dir + f'\\{fig_title}.png'

            ax_list = []

            freq_zhu_list = [1700, 2000, 2300, 2600]
            for j, freq_zhu in enumerate(freq_zhu_list):

                ax = fig.add_subplot(2, 2, j + 1)
                ax_list.append(ax)

                ax_title = f'主串频率-{freq_zhu}Hz'

                ######################################################################################################
                # 画线

                xx1 = range(sec_length+1)

                sht_mode_list = ['主串调整被串分路', '主被串同时分路']
                show_table = {
                    '主串调整被串分路': '主调整被分路',
                    '主被串同时分路': '主被同时分路',
                }

                for i, sht_mode in enumerate(sht_mode_list):

                    df1 = df.loc[
                        (df["主串频率(Hz)"] == freq_zhu) &
                        (df["分路模式"] == sht_mode)
                        ]

                    if len(df1.index) != 1:
                        raise KeyboardInterrupt('error: len(index) != 1')

                    yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                    color_list = [
                        'red',
                        # 'orange',
                        'blue',
                        # 'green',
                    ]

                    color = color_list[i]
                    width = 0.5
                    label = show_table[sht_mode]
                    ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

                col = j % 2
                config_ax(ax, ax_title, sec_length, col=col)

            config_fig(fig, fig_title)

            #################################################################################################
            # 保存
            # plt.show()
            # raise KeyboardInterrupt()

            if not os.path.exists(res_dir):
                os.makedirs(res_dir)

            fig.savefig(fig_path, transparent=True)

# 4-2-4遍历分路模式-4col
def draw_image_4_2_4_4col(parent_root):
    sub_dir = '4-2-4遍历分路模式'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list1 = [400, 600, 800, 1000]
    list1 = [-400, -200, 0, 200, 400]
    row_titles = {index: f'相对{value}m' for index, value in enumerate(list1)}

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    sec_length = 600

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长错位-{sec_length}m-遍历分路模式'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, offset in enumerate(list1):

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串相对位置(m)"] == offset)
            ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length + 1)

            sht_mode_list = ['主串调整被串分路', '主被串同时分路']
            show_table = {
                '主串调整被串分路': '主调整被分路',
                '主被串同时分路': '主被同时分路',
            }

            for i, sht_mode in enumerate(sht_mode_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["分路模式"] == sht_mode)
                    ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.5
                label = show_table[sht_mode]
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, ylim=250, one_legend=True, row_titles=row_titles)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-2-5遍历被串是否发码
def draw_image_4_2_5(parent_root):
    sub_dir = '4-2-5遍历被串是否发码'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]

    for val in list1:
        sec_length = val
        # offset_list = range(-sec_length, sec_length+1, 100)
        offset_list = [-200, 0, 200]

        print(offset_list)
        for offset in offset_list:

            df = df0.loc[
                (df0["主串区段长度(m)"] == sec_length) &
                (df0["被串相对位置(m)"] == offset)
            ].copy()

            # 配置 fig
            fig = plt.figure(figsize=(7, 4), dpi=200)
            fig_title = f'等长错位-主被同向-区段长度{sec_length}m-错位{offset}m'
            fig_path = res_dir + f'\\{fig_title}.png'

            ax_list = []

            freq_zhu_list = [1700, 2000, 2300, 2600]
            for j, freq_zhu in enumerate(freq_zhu_list):

                ax = fig.add_subplot(2, 2, j + 1)
                ax_list.append(ax)

                ax_title = f'主串频率-{freq_zhu}Hz'

                ######################################################################################################
                # 画线

                xx1 = range(sec_length+1)

                sr_mode_list = ['是', '不发码']
                sr_table = {
                    '是': '被串发码',
                    '不发码': '被串不发码',
                }
                for i, sr_mode in enumerate(sr_mode_list):

                    df1 = df.loc[
                        (df["主串频率(Hz)"] == freq_zhu) &
                        (df["被串是否发码"] == sr_mode)
                        ]

                    if len(df1.index) != 1:
                        raise KeyboardInterrupt('error: len(index) != 1')

                    yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                    color_list = [
                        'red',
                        # 'orange',
                        'blue',
                        # 'green',
                    ]

                    color = color_list[i]
                    width = 0.5
                    label = f'{sr_table[sr_mode]}'
                    ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

                col = j % 2
                config_ax(ax, ax_title, sec_length, col=col)
            config_fig(fig, fig_title)

            #################################################################################################
            # 保存
            # plt.show()
            # raise KeyboardInterrupt()

            if not os.path.exists(res_dir):
                os.makedirs(res_dir)

            fig.savefig(fig_path, transparent=True)


# 4-2-5遍历被串是否发码-4col
def draw_image_4_2_5_4col(parent_root):
    sub_dir = '4-2-5遍历被串是否发码'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list1 = [400, 600, 800, 1000]
    list1 = [-400, -200, 0, 200, 400]
    row_titles = {index: f'相对{value}m' for index, value in enumerate(list1)}

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    sec_length = 600

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长错位-{sec_length}m-遍历被串是否发码'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, offset in enumerate(list1):

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串相对位置(m)"] == offset)
            ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length + 1)

            sr_mode_list = ['是', '不发码']
            sr_table = {
                '是': '被串发码',
                '不发码': '被串不发码',
            }
            for i, sr_mode in enumerate(sr_mode_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串是否发码"] == sr_mode)
                    ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                color_list = [
                    'red',
                    # 'orange',
                    'blue',
                    # 'green',
                ]

                color = color_list[i]
                width = 0.5
                label = f'{sr_table[sr_mode]}'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, ylim=250, one_legend=True, row_titles=row_titles)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-3-1-1遍历一端对齐主串
def draw_image_4_3_1_1(parent_root):
    sub_dir = '4-3-1-1遍历一端对齐主串'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list1 = [400, 600, 800, 1000]

    for val in list1:

        sec_length = val
        df = df0.loc[df0["被串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'发送端对齐-被串区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            length_zhu_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_zhu in enumerate(length_zhu_list):

                df1 = df2.loc[
                    (df2["主串区段长度(m)"] == length_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_zhu_list))
                if length_zhu == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'主串长度{length_zhu}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            row = j // 2
            col = j % 2
            config_ax(ax, ax_title, sec_length, row=row, col=col, legend_mode='out-one')
        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)

# 4-3-1-1遍历一端对齐主串-4col
def draw_image_4_3_1_1_4col(parent_root):
    sub_dir = '4-3-1-1遍历一端对齐主串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    row_titles = {index: f'被串{value}m' for index, value in enumerate(list1)}

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'发送端对齐-遍历主串区段长度'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["被串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            length_zhu_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_zhu in enumerate(length_zhu_list):

                df1 = df2.loc[
                    (df2["主串区段长度(m)"] == length_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_zhu_list))
                if length_zhu == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'主串长度{length_zhu}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, row_titles=row_titles)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-3-1-2遍历一端对齐被串
def draw_image_4_3_1_2(parent_root):
    sub_dir = '4-3-1-2遍历一端对齐被串'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list1 = [400, 600, 800, 1000]

    for val in list1:

        sec_length = val
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'发送端对齐-主串区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            # xx1 = range(sec_length+1)

            length_bei_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_bei in enumerate(length_bei_list):

                df1 = df2.loc[
                    (df2["被串区段长度(m)"] == length_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                xx1 = range(length_bei + 1)
                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_bei_list))
                if length_bei == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'被串区段长度{length_bei}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, 1000, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)

# 4-3-1-2遍历一端对齐被串-4col
def draw_image_4_3_1_2_4col(parent_root):
    sub_dir = '4-3-1-2遍历一端对齐被串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    row_titles = {index: f'主串{value}m' for index, value in enumerate(list1)}

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'发送端对齐-遍历被串区段长度'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            # xx1 = range(sec_length+1)

            length_bei_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_bei in enumerate(length_bei_list):

                df1 = df2.loc[
                    (df2["被串区段长度(m)"] == length_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                xx1 = range(length_bei + 1)
                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_bei_list))
                if length_bei == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'被串长度{length_bei}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, row_titles=row_titles)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-3-3遍历方向
def draw_image_4_3_3(parent_root):
    sub_dir = '4-3-3遍历方向'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    length_zhu_list = [400, 600, 800, 1000]

    for length_zhu in length_zhu_list:

        length_bei_list = [400, 600, 800, 1000]

        for length_bei in length_bei_list:

            df = df0.loc[
                (df0["主串区段长度(m)"] == length_zhu) &
                (df0["被串区段长度(m)"] == length_bei)
            ].copy()

            # 配置 fig
            fig = plt.figure(figsize=(7, 4), dpi=200)
            fig_title = f'一端对齐-遍历发送方向-主串{length_zhu}m-被串{length_bei}m'

            fig_path = res_dir + f'\\{fig_title}.png'

            ax_list = []

            freq_zhu_list = [1700, 2000, 2300, 2600]
            for j, freq_zhu in enumerate(freq_zhu_list):

                ax = fig.add_subplot(2, 2, j + 1)
                ax_list.append(ax)

                ax_title = f'主串频率-{freq_zhu}Hz'

                ######################################################################################################
                # 画线

                xx1 = range(length_bei+1)

                dir_zhu_list = ['右发', '左发']

                dir_table = {
                    '右发': '反向',
                    '左发': '同向',
                }

                for i, dir_zhu in enumerate(dir_zhu_list):

                    df1 = df.loc[
                        (df["主串频率(Hz)"] == freq_zhu) &
                        (df["主串方向"] == dir_zhu)
                        ]

                    if len(df1.index) != 1:
                        raise KeyboardInterrupt('error: len(index) != 1')

                    yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                    color_list = [
                        'red',
                        # 'orange',
                        'blue',
                        # 'green',
                    ]

                    color = color_list[i]
                    width = 0.5
                    label = dir_table[dir_zhu]
                    ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

                col = j % 2
                config_ax(ax, ax_title, length_bei, col=col)

            config_fig(fig, fig_title)

            #################################################################################################
            # 保存
            # plt.show()
            # raise KeyboardInterrupt()

            if not os.path.exists(res_dir):
                os.makedirs(res_dir)

            fig.savefig(fig_path, transparent=True)


# 4-3-4遍历分路模式
def draw_image_4_3_4(parent_root):
    sub_dir = '4-3-4遍历分路模式'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    length_zhu_list = [400, 600, 800, 1000]

    for length_zhu in length_zhu_list:

        length_bei_list = [400, 600, 800, 1000]

        for length_bei in length_bei_list:

            df = df0.loc[
                (df0["主串区段长度(m)"] == length_zhu) &
                (df0["被串区段长度(m)"] == length_bei)
            ].copy()

            # 配置 fig
            fig = plt.figure(figsize=(7, 4), dpi=200)
            fig_title = f'一端对齐-主串调整-主串{length_zhu}m-被串{length_bei}m'

            fig_path = res_dir + f'\\{fig_title}.png'

            ax_list = []

            freq_zhu_list = [1700, 2000, 2300, 2600]
            for j, freq_zhu in enumerate(freq_zhu_list):

                ax = fig.add_subplot(2, 2, j + 1)
                ax_list.append(ax)

                ax_title = f'主串频率-{freq_zhu}Hz'

                ######################################################################################################
                # 画线

                xx1 = range(length_bei+1)

                sht_mode_list = ['主串调整被串分路', '主被串同时分路']

                for i, sht_mode in enumerate(sht_mode_list):

                    df1 = df.loc[
                        (df["主串频率(Hz)"] == freq_zhu) &
                        (df["分路模式"] == sht_mode)
                        ]

                    if len(df1.index) != 1:
                        raise KeyboardInterrupt('error: len(index) != 1')

                    yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                    color_list = [
                        'red',
                        # 'orange',
                        'blue',
                        # 'green',
                    ]
                    # ax.plot(xx1, yy2, linestyle='--', alpha=0.8, color=color_list[i], label='被串%sHz-2000A' % freq_bei)

                    color = color_list[i]
                    width = 0.5
                    label = sht_mode
                    ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

                col = j % 2
                config_ax(ax, ax_title, length_bei, col=col)

            config_fig(fig, fig_title)

            #################################################################################################
            # 保存
            # plt.show()
            # raise KeyboardInterrupt()

            if not os.path.exists(res_dir):
                os.makedirs(res_dir)

            fig.savefig(fig_path, transparent=True)


# 4-3-5遍历被串是否发码
def draw_image_4_3_5(parent_root):
    sub_dir = '4-3-5遍历被串是否发码'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    length_zhu_list = [400, 600, 800, 1000]

    for length_zhu in length_zhu_list:

        length_bei_list = [400, 600, 800, 1000]

        for length_bei in length_bei_list:

            df = df0.loc[
                (df0["主串区段长度(m)"] == length_zhu) &
                (df0["被串区段长度(m)"] == length_bei)
            ].copy()

            # 配置 fig
            fig = plt.figure(figsize=(7, 4), dpi=200)
            fig_title = f'一端对齐-主串调整-主串{length_zhu}m-被串{length_bei}m'

            fig_path = res_dir + f'\\{fig_title}.png'

            ax_list = []

            freq_zhu_list = [1700, 2000, 2300, 2600]
            for j, freq_zhu in enumerate(freq_zhu_list):

                ax = fig.add_subplot(2, 2, j + 1)
                ax_list.append(ax)

                ax_title = f'主串频率-{freq_zhu}Hz'

                ######################################################################################################
                # 画线

                xx1 = range(length_bei+1)

                sr_mode_list = ['是', '不发码']
                sr_table = {
                    '是': '被串发码',
                    '不发码': '被串不发码',
                }
                for i, sr_mode in enumerate(sr_mode_list):

                    df1 = df.loc[
                        (df["主串频率(Hz)"] == freq_zhu) &
                        (df["被串是否发码"] == sr_mode)
                        ]

                    if len(df1.index) != 1:
                        raise KeyboardInterrupt('error: len(index) != 1')

                    yy1 = (df1.iloc[0, pre_size:].copy().dropna() * 1000).tolist()

                    color_list = [
                        'red',
                        # 'orange',
                        'blue',
                        # 'green',
                    ]

                    color = color_list[i]
                    width = 0.5
                    label = f'{sr_table[sr_mode]}'
                    ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

                col = j % 2
                config_ax(ax, ax_title, length_bei, col=col)

            config_fig(fig, fig_title)

            #################################################################################################
            # 保存
            # plt.show()
            # raise KeyboardInterrupt()

            if not os.path.exists(res_dir):
                os.makedirs(res_dir)

            fig.savefig(fig_path, transparent=True)


# 4-3-6-1遍历接收端对齐主串
def draw_image_4_3_6_1(parent_root):
    sub_dir = '4-3-6-1遍历接收端对齐主串'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list1 = [400, 600, 800, 1000]

    for val in list1:

        sec_length = val
        df = df0.loc[df0["被串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'接收端对齐-被串区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            length_zhu_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_zhu in enumerate(length_zhu_list):

                df1 = df2.loc[
                    (df2["主串区段长度(m)"] == length_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_zhu_list))
                if length_zhu == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'主串长度{length_zhu}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            row = j // 2
            col = j % 2
            config_ax(ax, ax_title, sec_length, row=row, col=col, legend_mode='out-one')
        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)

# 4-3-6-1遍历接收端对齐主串-4col
def draw_image_4_3_6_1_4col(parent_root):
    sub_dir = '4-3-6-1遍历接收端对齐主串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    row_titles = {index: f'被串{value}m' for index, value in enumerate(list1)}

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'接收端对齐-遍历主串区段长度'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["被串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            length_zhu_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_zhu in enumerate(length_zhu_list):

                df1 = df2.loc[
                    (df2["主串区段长度(m)"] == length_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_zhu_list))
                if length_zhu == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'主串长度{length_zhu}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, row_titles=row_titles)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-3-6-2遍历接收端对齐被串
def draw_image_4_3_6_2(parent_root):
    sub_dir = '4-3-6-2遍历接收端对齐被串'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list1 = [400, 600, 800, 1000]

    for val in list1:

        sec_length = val
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'接收端对齐-主串区段长度{sec_length}m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            # xx1 = range(sec_length+1)

            length_bei_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_bei in enumerate(length_bei_list):

                df1 = df2.loc[
                    (df2["被串区段长度(m)"] == length_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                xx1 = range(length_bei + 1)
                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_bei_list))
                if length_bei == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'被串区段长度{length_bei}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            col = j % 2
            config_ax(ax, ax_title, 1000, col=col)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)

# 4-3-6-2遍历接收端对齐被串-4col
def draw_image_4_3_6_2_4col(parent_root):
    sub_dir = '4-3-6-2遍历接收端对齐被串'
    df0, res_dir = config_file_4col(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    row_titles = {index: f'主串{value}m' for index, value in enumerate(list1)}

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'接收端对齐-遍历被串区段长度'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, sec_length in enumerate(list1):

        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            # xx1 = range(sec_length+1)

            length_bei_list = [400, 500, 600, 700, 800, 900, 1000]

            for i, length_bei in enumerate(length_bei_list):

                df1 = df2.loc[
                    (df2["被串区段长度(m)"] == length_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                xx1 = range(length_bei + 1)
                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.rainbow(i / len(length_bei_list))
                if length_bei == sec_length:
                    width = 1.5
                else:
                    width = 0.5
                label = f'被串长度{length_bei}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, row_titles=row_titles)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-4-1遍历主串电容容值
def draw_image_4_4_1(parent_root):
    sub_dir = '4-4-1遍历主串电容容值'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list2 = ['普速既有', 25, 50]
    list2 = [50]

    clist = list(itertools.product(list1, list2))

    for val in clist:

        sec_length = val[0]
        c_value_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串电容值(μF)"] == c_value_bei)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-被串容值{c_value_bei}μF'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_value_zhu_list = [20, 25, 30, 35, 40, 45, 50, 55, 60]
            for i, c_value_zhu in enumerate(c_value_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电容值(μF)"] == c_value_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color = cm.rainbow(i / len(c_value_zhu_list))
                width = 0.5
                label = f'主串{c_value_zhu}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            row = j // 2
            col = j % 2
            config_ax(ax, ax_title, sec_length, row=row, col=col, legend_mode='out-one')

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-4-1遍历主串电容容值-4col
def draw_image_4_4_1_4col(parent_root):
    sub_dir = '4-4-1遍历主串电容容值'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [50]
    clist = list(itertools.product(list1, list2))

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历主串电容容值'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        c_value_bei = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["被串电容值(μF)"] == c_value_bei)
        ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_value_zhu_list = [20, 25, 30, 35, 40, 45, 50, 55, 60]
            for i, c_value_zhu in enumerate(c_value_zhu_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电容值(μF)"] == c_value_zhu)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color = cm.rainbow(i / len(c_value_zhu_list))
                width = 0.5
                label = f'主串{c_value_zhu}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-4-2遍历被串电容容值
def draw_image_4_4_2(parent_root):
    sub_dir = '4-4-2遍历被串电容容值'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    # list2 = ['普速既有', 25, 50]
    list2 = [50]

    clist = list(itertools.product(list1, list2))

    for val in clist:

        sec_length = val[0]
        c_value_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串电容值(μF)"] == c_value_zhu)
        ].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'等长对位-区段长度{sec_length}m-主串容值{c_value_zhu}μF'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_value_bei_list = [20, 25, 30, 35, 40, 45, 50, 55, 60]
            for i, c_value_bei in enumerate(c_value_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串电容值(μF)"] == c_value_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color = cm.rainbow(i / len(c_value_bei_list))
                width = 0.5
                label = f'被串{c_value_bei}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            row = j // 2
            col = j % 2
            config_ax(ax, ax_title, sec_length, row=row, col=col, legend_mode='out-one')

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-4-2遍历被串电容容值-4col
def draw_image_4_4_2_4col(parent_root):
    sub_dir = '4-4-2遍历被串电容容值'
    df0, res_dir = config_file_4col(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    # list1 = [400, 500, 600, 700, 800, 900, 1000]
    list1 = [400, 600, 800, 1000]
    list2 = [50]
    clist = list(itertools.product(list1, list2))

    ax_list = []

    ax_rows = len(list1)
    ax_cols = 4
    ax_index = 0

    v_height = 0.8
    fig_height = v_height * (ax_rows+1)

    # 配置 fig
    fig = plt.figure(figsize=(7, fig_height), dpi=200)
    fig_title = f'等长对位-遍历被串电容容值'
    fig_path = res_dir + f'\\{fig_title}.png'

    for row, val in enumerate(clist):

        sec_length = val[0]
        c_value_zhu = val[1]

        df = df0.loc[
            (df0["主串区段长度(m)"] == sec_length) &
            (df0["主串电容值(μF)"] == c_value_zhu)
        ].copy()

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for col, freq_zhu in enumerate(freq_zhu_list):

            ax_index = ax_index + 1
            ax = fig.add_subplot(ax_rows, ax_cols, ax_index)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            c_value_bei_list = [20, 25, 30, 35, 40, 45, 50, 55, 60]
            for i, c_value_bei in enumerate(c_value_bei_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["被串电容值(μF)"] == c_value_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                ax_title = f'频率{freq_zhu}Hz'

                color = cm.rainbow(i / len(c_value_bei_list))
                width = 0.5
                label = f'被串{c_value_bei}μF'

                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            # ylabel = f'区段长度{sec_length}m'

            config_ax_4col(ax, ax_title, sec_length, row, col, one_legend=True)
    config_fig_4col(fig, fig_title, ax_rows, ax_cols)

    #################################################################################################
    # 保存
    # plt.show()
    # raise KeyboardInterrupt()

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    fig.savefig(fig_path, transparent=True)


# 4-4-3不等长错位600m_800m
def draw_image_4_4_3(parent_root):
    sub_dir = '4-4-3不等长错位600m_800m'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [600]

    for length_bei in list1:

        df = df0.loc[df0["主串区段长度(m)"] == length_bei].copy()

        # 配置 fig
        fig = plt.figure(figsize=(7, 4), dpi=200)
        fig_title = f'不等长错位-主串600m-被串800m'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        freq_zhu_list = [1700, 2000, 2300, 2600]
        for j, freq_zhu in enumerate(freq_zhu_list):

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            ax_title = f'主串频率-{freq_zhu}Hz'

            df2 = df.loc[df["主串频率(Hz)"] == freq_zhu].copy()

            ######################################################################################################
            # 画线

            xx1 = range(sec_length+1)

            offset_list = df2["被串相对位置(m)"].copy().tolist()
            for i, offset in enumerate(offset_list):

                df1 = df2.loc[
                    (df2["被串相对位置(m)"] == offset)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                color = cm.winter(i / len(offset_list))
                if offset == 0:
                    width = 1
                else:
                    width = 0.25
                label = f'错位{offset}m'
                ax.plot(xx1, yy1, linestyle='-', color=color, alpha=1, linewidth=width, label=label)

            row = j // 2
            col = j % 2
            config_ax(ax, ax_title, sec_length, row=row, col=col, legend_mode='out-one')

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        plt.show()
        raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)



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

    # draw_image_4_1_1(parent_root)
    # draw_image_4_1_1_4col(parent_root)
    # draw_image_4_1_2(parent_root)
    # draw_image_4_1_3(parent_root)
    # draw_image_4_1_3_4col(parent_root)
    # draw_image_4_1_4(parent_root)
    # draw_image_4_1_4_4col(parent_root)
    # draw_image_4_1_5(parent_root)
    # draw_image_4_1_5_4col(parent_root)
    # draw_image_4_1_6_1(parent_root)
    # draw_image_4_1_6_1_4col(parent_root)
    # draw_image_4_1_6_2(parent_root)
    # draw_image_4_1_6_2_4col(parent_root)
    # draw_image_4_1_7_1(parent_root)
    # draw_image_4_1_7_1_4col(parent_root)
    # draw_image_4_1_7_2(parent_root)
    # draw_image_4_1_7_2_4col(parent_root)
    # draw_image_4_1_8_1(parent_root)
    # draw_image_4_1_8_1_4col(parent_root)
    # draw_image_4_1_8_2(parent_root)
    # draw_image_4_1_8_2_4col(parent_root)
    # draw_image_4_1_9(parent_root)
    # draw_image_4_1_9_4col(parent_root)
    # draw_image_4_1_10(parent_root)
    # draw_image_4_1_10_4col(parent_root)
    # draw_image_4_2_1(parent_root)
    # draw_image_4_2_1_4col(parent_root)
    # draw_image_4_2_3(parent_root)
    # draw_image_4_2_4(parent_root)
    # draw_image_4_2_4_4col(parent_root)
    # draw_image_4_2_5(parent_root)
    # draw_image_4_2_5_4col(parent_root)
    # draw_image_4_3_1_1(parent_root)
    # draw_image_4_3_1_1_4col(parent_root)
    # draw_image_4_3_1_2(parent_root)
    # draw_image_4_3_1_2_4col(parent_root)
    # draw_image_4_3_3(parent_root)
    # draw_image_4_3_4(parent_root)
    # draw_image_4_3_5(parent_root)
    # draw_image_4_3_6_1(parent_root)
    draw_image_4_3_6_1_4col(parent_root)
    # draw_image_4_3_6_2(parent_root)
    draw_image_4_3_6_2_4col(parent_root)
    # draw_image_4_4_1(parent_root)
    # draw_image_4_4_1_4col(parent_root)
    # draw_image_4_4_2(parent_root)
    # draw_image_4_4_2_4col(parent_root)
    # draw_image_4_4_3(parent_root)


if __name__ == '__main__':
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 10000)
    main()
    pass
