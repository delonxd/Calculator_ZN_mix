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
    res_dir = root + '生成图片_%s' % timestamp

    return df_combine, res_dir


def config_fig(fig, fig_title):
    ######################################################################################################
    # 主图设置

    fig.subplots_adjust(hspace=0.4, wspace=0.1, left=0.05, right=0.95)
    # fig.subplots_adjust(hspace=0.4, wspace=0.1, top=0.8, left=0.15, right=0.85)
    # fig.subplots_adjust(hspace=0.4)

    # fig.suptitle(title, x=0.5, y=0.98, fontsize=25, fontfamily='SimHei')
    fig.suptitle(fig_title, x=0.5, y=0.98, fontsize=25, fontfamily='SimSun')

    ######################################################################################################
    # 主图坐标轴

    plt.text(
        0.5, 0.07, '被串分路位置(m)',
        va='top', ha='center', transform=fig.transFigure,
        fontsize=13,
    )

    plt.text(
        0.02, 0.5, '邻线干扰电流(mA)',
        va='center', ha='right', transform=fig.transFigure,
        fontsize=13, rotation=90,
    )

    ######################################################################################################
    # # 调整位置
    # plt.tight_layout()


def config_ax(ax, ax_title, sec_length):
    ######################################################################################################
    # 子图设置

    ax.set_title(ax_title, pad=8, fontsize=12)
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

    # t = np.arange(100, sec_length, 100)
    # x_ticks = [0, 29, sec_length, sec_length + 29] + list(t + 14.5)
    # x_label = ['发\n送', '接\n收', '发\n送', '接\n收'] + list(t)

    t = np.arange(0, sec_length + 1, 100)
    x_ticks = list(t)
    x_label = list(map(lambda x: f'{x}m', t))
    x_label[0] = '发送'

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_label, fontsize=1)

    ax.tick_params(
        # axis='y',
        labelsize=12,  # y轴字体大小设置
        # color='r',  # y轴标签颜色设置
        # labelcolor='b',  # y轴字体颜色设置
        direction='in',  # y轴标签方向设置
        # pad=10,
    )

    ######################################################################################################
    # 图例
    ax.legend(loc='upper right', fontsize=9)

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


# 4-1-1遍历频率
def draw_image_4_1_1(parent_root):
    sub_dir = '4-1-1遍历频率'
    df0, res_dir = config_file(parent_root, sub_dir)

    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    sift_list = [
        [400],
        [500],
        [600],
        [700],
        [800],
        [900],
        [1000],
    ]

    for val in sift_list:

        sec_length = val[0]
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(16, 8), dpi=100)
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
                # ax.plot(xx1, yy2, linestyle='--', alpha=0.8, color=color_list[i], label='被串%sHz-2000A' % freq_bei)

                line_style = '-'
                color = color_list[i]
                alpha = 1
                width = 1
                label = f'被串{freq_bei}Hz'

                ax.plot(xx1, yy1, linestyle=line_style, color=color, alpha=alpha, linewidth=width, label=label)

                # max_i = max(max_i, max(yy))

                # yy2 = df2.iloc[i, :].tolist()
                # ax.scatter(
                #     xx2,
                #     yy2,
                #     marker='x',
                #     color='r',
                # )

            config_ax(ax, ax_title, sec_length)

        config_fig(fig, fig_title)

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

    sift_list = [1700, 2000, 2300, 2600]

    for freq_zhu in sift_list:

        df = df0.loc[df0["主串频率(Hz)"] == freq_zhu].copy()

        # 配置 fig
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig_title = f'等长对位-主串频率{freq_zhu}Hz'

        fig_path = res_dir + f'\\{fig_title}.png'

        ax_list = []

        ax = fig.add_subplot(1, 1, 1)
        ax_list.append(ax)

        # ax_title = f'等长对位-主串频率-{freq_zhu}Hz'
        ax_title = f''

        ######################################################################################################
        # 画线
        sec_length_list = [400, 500, 600, 700, 800, 900, 1000]

        for i, sec_length in enumerate(sec_length_list):

            df1 = df.loc[df["主串区段长度(m)"] == sec_length]

            if len(df1.index) != 1:
                raise KeyboardInterrupt('error: len(index) != 1')

            yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()
            xx1 = range(sec_length + 1)

            line_style = '-'
            color = cm.rainbow(i / len(sec_length_list))

            alpha = 1
            width = 1
            label = f'区段长度{sec_length}m'

            ax.plot(xx1, yy1, linestyle=line_style, color=color, alpha=alpha, linewidth=width, label=label)

            # max_i = max(max_i, max(yy))

            # yy2 = df2.iloc[i, :].tolist()
            # ax.scatter(
            #     xx2,
            #     yy2,
            #     marker='x',
            #     color='r',
            # )

        config_ax(ax, ax_title, 1000)

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

    sift_list = [
        [400],
        [500],
        [600],
        [700],
        [800],
        [900],
        [1000],
    ]

    for val in sift_list:

        sec_length = val[0]
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(16, 8), dpi=100)
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
                # ax.plot(xx1, yy2, linestyle='--', alpha=0.8, color=color_list[i], label='被串%sHz-2000A' % freq_bei)

                line_style = '-'
                color = color_list[i]
                alpha = 1
                width = 1
                label = dir_table[dir_zhu]

                ax.plot(xx1, yy1, linestyle=line_style, color=color, alpha=alpha, linewidth=width, label=label)

                # max_i = max(max_i, max(yy))

                # yy2 = df2.iloc[i, :].tolist()
                # ax.scatter(
                #     xx2,
                #     yy2,
                #     marker='x',
                #     color='r',
                # )

            config_ax(ax, ax_title, sec_length)

        config_fig(fig, fig_title)

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

    sift_list = [
        [400],
        [500],
        [600],
        [700],
        [800],
        [900],
        [1000],
    ]

    for val in sift_list:

        sec_length = val[0]
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(16, 8), dpi=100)
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
                # ax.plot(xx1, yy2, linestyle='--', alpha=0.8, color=color_list[i], label='被串%sHz-2000A' % freq_bei)

                line_style = '-'
                color = color_list[i]
                alpha = 1
                width = 1
                label = sht_mode

                ax.plot(xx1, yy1, linestyle=line_style, color=color, alpha=alpha, linewidth=width, label=label)

                # max_i = max(max_i, max(yy))

                # yy2 = df2.iloc[i, :].tolist()
                # ax.scatter(
                #     xx2,
                #     yy2,
                #     marker='x',
                #     color='r',
                # )

            config_ax(ax, ax_title, sec_length)

        config_fig(fig, fig_title)

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

    sift_list = [
        [400],
        [500],
        [600],
        [700],
        [800],
        [900],
        [1000],
    ]

    for val in sift_list:

        sec_length = val[0]
        df = df0.loc[df0["主串区段长度(m)"] == sec_length].copy()

        # 配置 fig
        fig = plt.figure(figsize=(16, 8), dpi=100)
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

            interval_list = ['50m', '60m', '70m', '80m', '90m', '100m', '110m', '120m', '130m', '140m', '150m']

            for i, interval in enumerate(interval_list):

                df1 = df.loc[
                    (df["主串频率(Hz)"] == freq_zhu) &
                    (df["主串电容间隔"] == interval)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                line_style = '-'
                color = cm.rainbow(i / len(interval_list))
                alpha = 1
                width = 1
                label = f'电容间隔{interval}'

                ax.plot(xx1, yy1, linestyle=line_style, color=color, alpha=alpha, linewidth=width, label=label)

                # max_i = max(max_i, max(yy))

                # yy2 = df2.iloc[i, :].tolist()
                # ax.scatter(
                #     xx2,
                #     yy2,
                #     marker='x',
                #     color='r',
                # )

            config_ax(ax, ax_title, sec_length)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


# 4-1-6遍历电容容值
def draw_image_4_1_6(parent_root):
    sub_dir = '4-1-6遍历电容容值'
    df0, res_dir = config_file(parent_root, sub_dir)
    pre_size = len([col for col in df0.columns if not isinstance(col, (int, float))])

    list1 = [400, 500, 600, 700, 800, 900, 1000]
    list2 = ['普速既有', 25, 50]

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
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig_title = f'等长对位-区段长度{sec_length}m-{c_mode_table[c_mode_zhu]}'

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
                    (df["被串电容间隔"] == c_mode_bei)
                ]

                if len(df1.index) != 1:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df1.iloc[0, pre_size:].copy().dropna()*1000).tolist()

                line_style = '-'
                color = cm.rainbow(i / len(interval_list))
                alpha = 1
                width = 1
                label = f'电容间隔{interval}'

                ax.plot(xx1, yy1, linestyle=line_style, color=color, alpha=alpha, linewidth=width, label=label)

                # max_i = max(max_i, max(yy))

                # yy2 = df2.iloc[i, :].tolist()
                # ax.scatter(
                #     xx2,
                #     yy2,
                #     marker='x',
                #     color='r',
                # )

            config_ax(ax, ax_title, sec_length)

        config_fig(fig, fig_title)

        #################################################################################################
        # 保存
        # plt.show()
        # raise KeyboardInterrupt()

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        fig.savefig(fig_path, transparent=True)


def main():
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['STSong']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False

    # parent_root = 'C:\\Users\\Delon\\Desktop\\普速列控邻线干扰\\数据汇总'
    parent_root = 'C:\\Users\\李继隆\\Desktop\\普速铁路新一代列控系统项目\\数据汇总'

    # draw_image_4_1_1(parent_root)
    # draw_image_4_1_2(parent_root)
    # draw_image_4_1_3(parent_root)
    # draw_image_4_1_4(parent_root)
    # draw_image_4_1_5(parent_root)
    draw_image_4_1_6(parent_root)


if __name__ == '__main__':
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 10000)
    main()
    pass
