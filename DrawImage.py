import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False


def main():
    root = 'C:\\Users\\Delon\\Desktop\\邻线干扰电容故障遍历_1125\\'
    # file = '站内电容故障.xlsx'
    file = '电容故障汇总.xlsx'
    df_input = pd.read_excel(root + file, '数据输出')


    # fig = plt.figure(figsize=(16, 9), dpi=100)
    # fig.subplots_adjust(hspace=0.4)
    # # fig.suptitle('test')

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '图表汇总\\电容断线_%s' % timestamp

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    sec_length = {
        # '区间-普铁': [500],
        '区间-普铁': [1400, 1000, 500],
        '区间-高铁': [1400, 1000, 500],
        '站内-有选频': [650, 500, 350],
        '站内-无选频': [650, 500, 350],
    }


    for sec_type, len_list in sec_length.items():
        df1 = df_input.loc[df_input["主串区段类型"] == sec_type].copy()

        for length in len_list:
            df2 = df1.loc[df1["主串区段长度(m)"] == length].copy()

            for error_type in ['断线', '减半']:
                df3 = df2.loc[df2["故障类型"].isin([error_type, '正常'])].copy()

                fig = plt.figure(figsize=(16, 9), dpi=100)
                fig.subplots_adjust(hspace=0.4)

                error_show = {
                    '断线': '电容断线',
                    '减半': '容值减半',
                }

                fig_tittle = '%s_%sm_%s_干扰值变化百分比' % (sec_type, length, error_show[error_type])
                # fig_tittle = '%s_%sm_%s_最大干扰值' % (sec_type, length, error_show[error_type])
                fig.suptitle(fig_tittle, fontsize=30)

                for index, freq_zhu in enumerate([1700, 2000, 2300, 2600]):
                    ax = fig.add_subplot(2, 2, index+1)
                    title = '主串频率-%sHz' % freq_zhu
                    ax.set_title(title)


                    df4 = df3.loc[df3["主串频率(Hz)"] == freq_zhu].copy()

                    # draw_sub_plot_value(df4, ax)
                    draw_sub_plot_percent(df4, ax)

                filename1 = '%s\\%s.png' % (res_dir, fig_tittle)
                fig.savefig(filename1)
                # plt.show()
                #
                # return

def draw_sub_plot_value(df, ax):
    x_label = pd.Series()

    freq_list = [1700, 2000, 2300, 2600]
    yy = []

    for freq_bei in freq_list:
        df1 = df.loc[df["被串频率(Hz)"] == freq_bei, ['故障位置', '被串最大干扰电流(A)']].copy()
        if len(df1['故障位置']) > len(x_label):
            x_label = df1['故障位置']
        yy.append(df1['被串最大干扰电流(A)'].values * 1000)

    # print(x_label)
    # print(yy)
    x_label = x_label.copy()
    x_label.iloc[0] = '正常'
    length = x_label.size

    xx = np.arange(length)
    # yy = res.values
    # yy2 = np.ones(length) * threshold / 1000
    # yy3 = np.ones(length) * normal
    # yy4 = np.ones(length) * threshold / 1000 * 0.75

    ax.set_xlabel('故障电容C位置')
    ax.set_ylabel('被串最大干扰电流(mA)')

    ax.yaxis.grid(True, which='major')


    txt = '最大干扰电流值%.2fmA' % max(df['被串最大干扰电流(A)'].values * 1000)
    ax.text(0.05, 0.95, txt, fontsize=10, color='blue', va='top', ha='left', transform=ax.transAxes)

    # ax.plot(xx, yy2, linestyle='--', alpha=0.8, color='orange', label='门限值')
    # ax.plot(xx, yy4, linestyle='--', alpha=0.8, color='r', label='门限值75%')
    # ax.plot(xx, yy3, linestyle='--', alpha=0.8, color='g', label='正常情况')

    color_list = ['orange', 'r', 'g', 'blue']
    for index, y_tmp in enumerate(yy):
        ax.plot(
            xx[:len(y_tmp)],
            y_tmp,
            linestyle='-',
            alpha=0.8,
            color=color_list[index],
            label='被串%sHz' % freq_list[index],
        )

    ax.set_xticks(xx)
    ax.set_xticklabels(x_label)

    # ax.legend(0.95, 0.95, transform=ax.transAxes)
    ax.legend(loc='upper right')

    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(90)

        label.set_color('gray')
        # label.set_font(8)


def draw_sub_plot_percent(df, ax):
    x_label = pd.Series()

    freq_list = [1700, 2000, 2300, 2600]
    yy = []
    max_val = 0
    min_val = 0

    for freq_bei in freq_list:
        df1 = df.loc[df["被串频率(Hz)"] == freq_bei, ['故障位置', '干扰值变化']].copy()
        if len(df1['故障位置']) > len(x_label):
            x_label = df1['故障位置']
        yy.append(df1['干扰值变化'].values * 100)

        max_val = max(max(yy[-1]), max_val)
        min_val = min(min(yy[-1]), min_val)

    max_val = max(max_val + 5, 70)
    min_val = min(min_val - 5, -70)
    # print(x_label)
    # print(yy)
    x_label = x_label.copy()
    x_label.iloc[0] = '正常'
    length = x_label.size

    xx = np.arange(length)
    # yy = res.values
    # yy2 = np.ones(length) * threshold / 1000
    # yy3 = np.ones(length) * normal
    # yy4 = np.ones(length) * threshold / 1000 * 0.75
    #

    ax.set_xlabel('故障电容C位置')
    ax.set_ylabel('干扰值变化(%)')

    ax.yaxis.grid(True, which='major')
    ax.set_ylim([min_val, max_val])

    txt = '最大干扰电流变化%.2f%%' % max(df['干扰值变化'].values * 100)
    ax.text(0.05, 0.95, txt, fontsize=10, color='blue', va='top', ha='left', transform=ax.transAxes)

    # ax.plot(xx, yy2, linestyle='--', alpha=0.8, color='orange', label='门限值')
    # ax.plot(xx, yy4, linestyle='--', alpha=0.8, color='r', label='门限值75%')
    # ax.plot(xx, yy3, linestyle='--', alpha=0.8, color='g', label='正常情况')

    color_list = ['orange', 'r', 'g', 'blue']
    for index, y_tmp in enumerate(yy):
        ax.plot(
            xx[:len(y_tmp)],
            y_tmp,
            linestyle='-',
            alpha=0.8,
            color=color_list[index],
            label='被串%sHz' % freq_list[index],
        )

    ax.set_xticks(xx)
    ax.set_xticklabels(x_label)

    # ax.legend(0.95, 0.95, transform=ax.transAxes)
    ax.legend(loc='upper right')

    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(90)

        label.set_color('gray')
        # label.set_font(8)


def generate_plot(df_input, c_num, freq, pop_num, ax):

    df = df_input.loc[
        (df_input["主串电容数(含TB)"] == c_num) & (df_input["主串频率(Hz)"] == freq),
        ['被串拆卸情况', '被串最大干扰电流(A)', '被串最大干扰位置(m)']
    ].copy()
    df.index = df['被串拆卸情况'].map(format_c_pop)

    normal = df.loc['正常', '被串最大干扰电流(A)']
    # print(normal)

    if pop_num == 1:
        res = df.loc[df['被串拆卸情况'].map(lambda x: len(eval(x)) == 1), '被串最大干扰电流(A)']
    elif pop_num == 2:
        res = df.loc[df['被串拆卸情况'].map(lambda x: len(eval(x)) == 2), '被串最大干扰电流(A)']

    # print(res)

    condition = '断%s个电容' % pop_num

    x_label = res.index

    length = res.size

    tmp = {
        1700: 263,
        2000: 234,
        2300: 217,
        2600: 200,
    }

    threshold = tmp[freq]

    xx = np.arange(length)
    yy = res.values
    yy2 = np.ones(length) * threshold / 1000
    yy3 = np.ones(length) * normal
    yy4 = np.ones(length) * threshold / 1000 * 0.75

    title = '被串钢轨电流-%sHz-%s' % (freq, condition)

    ax.set_title(title)
    ax.set_xlabel('断开电容')
    ax.set_ylabel('邻线干扰钢轨电流(A)')

    ax.yaxis.grid(True, which='major')
    ax.set_ylim([0, 0.3])

    txt = '最大干扰电流%.2fmA，门限值%sfmA' % (np.max(yy) * 1000, threshold)
    ax.text(0.05, 0.95, txt, fontsize=10, color='blue', va='top', ha='left', transform=ax.transAxes)

    ax.plot(xx, yy2, linestyle='--', alpha=0.8, color='orange', label='门限值')
    ax.plot(xx, yy4, linestyle='--', alpha=0.8, color='r', label='门限值75%')
    ax.plot(xx, yy3, linestyle='--', alpha=0.8, color='g', label='正常情况')
    ax.plot(xx, yy, linestyle='-', alpha=0.8, color='blue', label=condition)

    ax.set_xticks(xx)
    ax.set_xticklabels(x_label)

    # ax.legend(0.95, 0.95, transform=ax.transAxes)
    ax.legend(loc='upper right')

    for label in ax.xaxis.get_ticklabels():
        if pop_num > 1:
            label.set_rotation(90)

        label.set_color('blue')
        # label.set_font(8)


def format_c_pop(str_c_pop):
    tmp = eval(str_c_pop)
    if len(tmp) == 0:
        ret = '正常'
    elif len(tmp) == 1:
        ret = 'C%s' % tmp[0]
    else:
        ret = 'C%s C%s' % tmp

    return ret

# def main():
#     root = 'C:\\Users\\Delon\\Desktop\\邻线干扰电容故障遍历_1125\\'
#     file = '站内电容故障.xlsx'
#     df_src = pd.read_excel(root + file, '数据输出')
#
#     print(df_src)


def draw_image_1128():
    # plt.rcParams['font.size'] = 20
    # root = 'C:\\Users\\Delon\\Desktop\\峨广邻线干扰\\'
    root = 'C:\\Users\\李继隆\\Desktop\\峨广邻线干扰\\'
    # file = '仿真输出_双区段.xlsx'
    file = '仿真输出_20221205141447_500-600m错位遍历2.xlsx'
    df_input = pd.read_excel(root + file, '数据输出')
    df_data = pd.read_excel(root + file, '被串钢轨电流')

    # fig = plt.figure(figsize=(16, 9), dpi=100)
    # fig.subplots_adjust(hspace=0.4)
    # # fig.suptitle('test')

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '图表汇总\\峨广邻线干扰_%s' % timestamp

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    sift_list = [
        400, '左发',
        500, '右发',

    ]
    sift_list = [
        [500, '左发'],
        [500, '右发'],
        [600, '左发'],
        [600, '右发'],
    ]

    for val in sift_list:
        sec_length = val[0]
        sec_sr_mode = val[1]

        dir_dict = {
            '左发': '反向',
            '右发': '正向',
        }

        df1 = df_input.loc[df_input["主串区段长度(m)"] == sec_length].copy()
        df2 = df1.loc[df1["被串方向"] == sec_sr_mode].copy()

        index = df2['序号'].values
        print(index)

        if len(index) == 0:
            continue

        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(hspace=1)

        ax = fig.add_subplot(1, 1, 1)

        ###################################################################

        # title = '主串2600Hz正向-被串2300Hz%s-区段长度%sm' % (dir_dict[sec_sr_mode], sec_length)
        title = '主串2600Hz正向-被串1700Hz%s-区段长度%sm' % (dir_dict[sec_sr_mode], sec_length)
        ax.set_title(title, x=0.5, y=1.04, fontsize=30)

        # fig.suptitle(title, fontsize=30)

        ax.set_xlabel('被串分路位置', fontsize=20)
        ax.set_ylabel('邻线干扰钢轨电流(A)', fontsize=20)

        ax.yaxis.grid(True, which='major')
        # ax.yaxis.set_font(20)
        # ax.set_ylim([0, 1])

        data = df_data.iloc[index, :].copy()
        data = data.dropna(how='all', axis=1)

        max_i = 0
        size0 = data.index.size

        column_size = 0
        for i, _ in enumerate(index):
            row = data.iloc[i, :].copy()
            yy = row.values / 24 * 30

            # yy = yy[sec_length:]
            yy = yy[:-sec_length]

            column_size = yy.size
            xx = np.arange(yy.size)

            width = 2 if i == 20 else 0.5
            alpha = 1 if i == 20 else 0.7

            ax.plot(
                xx,
                yy,
                linestyle='-',
                alpha=alpha,
                color=cm.twilight(i / size0),
                label='s0',
                linewidth=width,
            )

            max_i = max(max_i, max(yy))

        t = np.arange(0, sec_length + 1, 100)
        x_ticks = [0, 29, sec_length, sec_length + 29] + list(t + 14.5)
        x_label = ['发\n送', '接\n收', '发\n送', '接\n收'] + list(t)

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_label)

        # ax.legend(loc='upper right')

        cb_pos = 0.11
        # cb_pos = 0.9

        cmap = mpl.cm.twilight
        cax = fig.add_axes([cb_pos, 0.45, 0.01, 0.4])  # 四个参数分别是左、下、宽、长

        norm = mpl.colors.Normalize(vmin=-100, vmax=100)
        bounds = [tmp for tmp in np.linspace(-100, 100, size0+1)]
        cb = mpl.colorbar.ColorbarBase(
            ax=cax,
            cmap=cmap,
            norm=norm,
            # to use 'extend', you must
            # specify two extra boundaries:
            # boundaries=[1.2] + bounds + [2.6],
            boundaries=bounds,
            # extend='both',
            # ticks=[1.3, 2.5],  # optional
            # ticks=[-100, 100],  # optional
            ticks=[],  # optional
            # spacing='proportional',
            orientation='vertical'
        )

        cb.set_ticks([-100, 0, 100])
        cb.set_ticklabels(['-200m', ' 0m', ' 200m'])

        cax.tick_params(labelsize=16)

        txt = '调\n谐\n区\n错\n位'
        ax.text(
            -1.5, 0.5,
            txt,
            fontsize=16,
            color='black',
            va='center',
            ha='center',
            transform=cax.transAxes,
        )

        yy = np.ones(column_size) * max_i
        xx = np.arange(yy.size)

        ax.plot(
            xx,
            yy,
            linestyle='--',
            alpha=1,
            color='blue',
            linewidth=1,
        )

        txt = '最大干扰电流%.2fmA' % (max_i * 1000)
        ax.text(
            0.2, 0.9,
            txt,
            fontsize=16,
            color='blue',
            va='center',
            ha='left',
            transform=ax.transAxes,
        )

        ax.tick_params(
            # axis='y',
            labelsize=16,  # y轴字体大小设置
            # color='r',  # y轴标签颜色设置
            # labelcolor='b',  # y轴字体颜色设置
            direction='in',  # y轴标签方向设置
            # pad=10,
        )

        plt.tight_layout()

        # plt.show()
        # return

        filename1 = '%s\\%s.png' % (res_dir, title)
        fig.savefig(filename1)


def draw_image_1128_typical():
    # plt.rcParams['font.size'] = 20
    # root = 'C:\\Users\\Delon\\Desktop\\峨广邻线干扰\\'
    root = 'C:\\Users\\李继隆\\Desktop\\峨广邻线干扰\\'
    # file = '仿真输出_双区段.xlsx'

    # file = '仿真输出_20221129202757_被串改方.xlsx'
    # df_input = pd.read_excel(root + file, '参数设置')

    file = '仿真输出_20221129211606_被串正常.xlsx'
    df_input = pd.read_excel(root + file, '数据输出')

    df_data = pd.read_excel(root + file, '被串钢轨电流')

    # fig = plt.figure(figsize=(16, 9), dpi=100)
    # fig.subplots_adjust(hspace=0.4)
    # # fig.suptitle('test')

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '图表汇总\\峨广邻线干扰_%s' % timestamp

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    # sift_list = [
    #     [500, '左发'],
    #     [500, '右发'],
    #     [600, '左发'],
    #     [600, '右发'],
    # ]

    for val in range(2):
        sec_length = 615

        dir_dict = {
            '左发': '反向',
            '右发': '正向',
        }

        # df1 = df_input.loc[df_input["主串区段长度(m)"] == sec_length].copy()
        df1 = df_input.iloc[val, :].copy()

        sec_name = df1['被串区段']
        sec_sr_mode = df1['被串方向']

        # index = df2['序号'].values
        # print(index)
        #
        # if len(index) == 0:
        #     continue

        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(hspace=1)

        ax = fig.add_subplot(1, 1, 1)

        ###################################################################

        title = '被串%s-%s-2600Hz干扰' % (sec_name, dir_dict[sec_sr_mode])
        ax.set_title(title, x=0.5, y=1.04, fontsize=30)

        # fig.suptitle(title, fontsize=30)

        ax.set_xlabel('被串分路位置', fontsize=20)
        ax.set_ylabel('邻线干扰钢轨电流(A)', fontsize=20)

        ax.yaxis.grid(True, which='major')
        # ax.yaxis.set_font(20)
        ax.set_ylim([0, 1])

        row = df_data.iloc[val, :].copy()

        k1 = 1
        # if sec_name == '2973BG':
        #     k1 = 1.35
        # elif sec_name == '2961BG':
        #     k1 = 1.1
        # else:
        #     raise KeyboardInterrupt('k1 error')

        yy = row.values / 24 * 30 * k1

        xx = np.arange(yy.size)

        ax.plot(
            xx,
            yy,
            linestyle='-',
            alpha=1,
            color='r',
            # linewidth=width,
            label='被串%s-%s' % (sec_name, dir_dict[sec_sr_mode]),
        )

        ax.set_ylim([0, 1])

        # yy2 = np.ones(yy.size) * max_i
        #
        # ax.plot(
        #     xx,
        #     yy2,
        #     linestyle='--',
        #     alpha=1,
        #     color='blue',
        #     linewidth=1,
        # )

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

        l0 = 615 - 29
        t = np.linspace(0, l0, 8)
        t = t[:-1]
        t = t + l0 / 14 + 29

        c_label = map(lambda x: 'C'+str(x+1), range(6, -1, -1))
        # c_label = map(lambda x: 'C'+str(x+1), range(7))

        x_ticks = [0, 29, sec_length, sec_length + 29] + list(t)
        x_label = ['发\n送', '接\n收', '发\n送', '接\n收'] + list(c_label)

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_label)

        ax.legend(loc='upper right', fontsize=20)

        ax.tick_params(
            # axis='y',
            labelsize=16,  # y轴字体大小设置
            # color='r',  # y轴标签颜色设置
            # labelcolor='b',  # y轴字体颜色设置
            direction='in',  # y轴标签方向设置
            # pad=10,
        )

        plt.tight_layout()

        filename1 = '%s\\%s.png' % (res_dir, title)
        fig.savefig(filename1)

        # plt.show()
        # return


if __name__ == '__main__':
    # draw_image_1128()
    draw_image_1128_typical()
