import os
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm

# # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
# # plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False


# from matplotlib import rcParams

# matplotlib.use("pgf")
# pgf_config = {
#     "font.family":'serif',
#     "font.size": 20,
#     "pgf.rcfonts": False,
#     "text.usetex": True,
#     "pgf.preamble": [
#         r"\usepackage{unicode-math}",
#         #r"\setmathfont{XITS Math}",
#         # 这里注释掉了公式的XITS字体，可以自行修改
#         r"\setmainfont{Times New Roman}",
#         r"\usepackage{xeCJK}",
#         r"\xeCJKsetup{CJKmath=true}",
#         r"\setCJKmainfont{SimSun}",
#     ],
# }
# rcParams.update(pgf_config)


def draw_image_20230904_digital():
    # plt.rcParams['font.size'] = 20

    # 根目录
    # root = 'C:\\Users\\李继隆\\PycharmProjects\\Calculator_ZN_mix\\20230901_站内400m遍历\\'
    root = 'C:\\Users\\李继隆\\Desktop\\站内数字化轨道电路\\站内数字化_20230417\\'

    # 创建文件夹
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '%s图表汇总_站内邻线干扰_%s' % (root, timestamp)

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    # 读取数据

    # file = '仿真输出_站内400m邻线干扰_主串1700_被串2300.xlsx'
    # file = '站内数字化_两送一收_数据输出.xlsx'
    # file = '站内数字化_一送一收_数据输出.xlsx'

    # path = '%s%s' % (root, file)
    # df_input = pd.read_excel(path, '数据输出')

    # path2 = '%s%s' % (root, '站内数字化_一送一收_数据输出.xlsx')
    # with pd.ExcelWriter(path2) as writer:
    #     df_input.to_excel(writer, sheet_name="数据输出", index=True)
    # df_data = pd.read_excel(path, '被串钢轨电流')

    scenes = [
        '一送一收|[距离/100]',
        '一送一收|[距离/100]-1',
        '两送一收|[距离/200]*2',
        '两送一收|[距离/200]*2-2',
    ]

    # 创建图表
    fig = plt.figure(figsize=(16, 8), dpi=100)
    fig.subplots_adjust(hspace=0.1, wspace=0.1, top=0.8, left=0.15, right=0.85)
    # title = '站内数字化轨道电路邻线干扰仿真：不同扼流变比'
    # fig.suptitle(title, x=0.5, y=0.93, fontsize=25, fontfamily='SimHei')

    total_index = -1
    ax_list = []

    for s_index, scene in enumerate(scenes):

        print(scene)
        send_type, c_type = scene.split('|')

        file = '站内数字化_%s_数据输出.xlsx' % send_type
        path = '%s%s' % (root, file)
        df_input = pd.read_excel(path, '数据输出')

        # # 创建图表
        # fig = plt.figure(figsize=(16, 8), dpi=100)
        # fig.subplots_adjust(hspace=0.4)
        # title = '区段配置：%s  电容配置：%s' % (send_type, c_type)
        # fig.suptitle(title, x=0.5, y=0.98, fontsize=25, fontfamily='SimHei')

        # ax_list = []

        for sub_index, freq in enumerate([1700, 2000, 2300, 2600]):
            total_index += 1

            df1 = df_input.loc[df_input["主串频率(Hz)"] == freq].copy()

            # 数据处理

            ###################################################################

            # ax = fig.add_subplot(2, 2, sub_index+1)

            pos_index = (total_index % 4) * 4 + total_index // 4 + 1
            ax = fig.add_subplot(4, 4, pos_index)
            ax_list.append(ax)

            # 图表标题
            # sub_title = '主串频率$\mathrm{%sHz}$' % freq
            # ax.set_title(sub_title, x=0.5, y=1.04, fontsize=17)
            if pos_index in [1, 2, 3, 4]:
                sub_title = '模式：%s\n电容数：%s' % (send_type, c_type)
                ax.set_title(sub_title, pad=8, fontsize=12)

            # fig.suptitle(title, fontsize=30)

            # 横纵坐标
            # # 坐标名
            # if pos_index in [13, 14, 15, 16]:
            #     ax.set_xlabel('扼流变压器变比', fontsize=12)

            if pos_index in [1, 5, 9, 13]:
                ax.set_ylabel('频率：\n$\mathrm{%sHz}$' % freq, fontsize=12, rotation=0, va='center', ha='right')
            # ax.set_ylabel(r'最大邻线干扰电流$\mathrm{(mA)}$', fontsize=12)

            # 纵坐标
            # ax.yaxis.grid(True, which='major')
            y_ticks = [0, 100, 200, 300]
            y_label = map(lambda x: r'$\mathrm{%.0f}$' % x, y_ticks)

            ax.set_yticks(y_ticks)
            if pos_index in [1, 5, 9, 13]:
                ax.set_yticklabels(y_label)
            else:
                ax.set_yticklabels(['']*len(y_ticks))

            # ax.yaxis.set_font(20)
            ax.set_ylim([0, 300])

            # 横坐标
            n_transformer = list(range(5, 16, 1))

            x_ticks = list(map(lambda x: x - 5, n_transformer))
            x_label = map(lambda x: '%s:1' % x if x % 2 == 1 else '', n_transformer)

            ax.set_xticks(x_ticks)
            if pos_index in [13, 14, 15, 16]:
                ax.set_xticklabels(x_label)
            else:
                ax.set_xticklabels(['']*len(x_ticks))
            # ax.set_yticklabels(fontfamily="Times New Roman")

            # 坐标轴字体
            ax.tick_params(
                # axis='y',
                labelsize=9,       # y轴字体大小设置
                # color='r',        # y轴标签颜色设置
                # labelcolor='b',   # y轴字体颜色设置
                direction='in',     # y轴标签方向设置
                # pad=10,
            )

            length_list = list(range(500, 1051, 50))
            size0 = len(length_list)

            max_list = [0] * len(n_transformer)

            for j, length in enumerate(length_list):

                df2 = df1.loc[df1["主串区段长度(m)"] == length].copy()

                if c_type == '[距离/100]':
                    c_num = -(-length // 100)
                elif c_type == '[距离/100]-1':
                    c_num = -(-length // 100) - 1
                elif c_type == '[距离/200]*2':
                    c_num = -(-length // 200) * 2
                elif c_type == '[距离/200]*2-2':
                    c_num = -(-length // 200) * 2 - 2
                else:
                    raise KeyboardInterrupt('电容配置错误')

                df2 = df2.loc[df2["主串电容数(含TB)"] == c_num].copy()

                ###################################################################

                # 画曲线

                xx = []
                yy = []
                for i, n in enumerate(n_transformer):
                    row = df2.loc[df2["变压器变比"] == n].copy()

                    value = row['被串最大干扰电流(A)'].values[0] * 1000

                    # row_output = df_input.iloc[i, :].copy()
                    # offset = row_output['被串相对位置(m)']

                    # label = '%sm' % offset

                    xx.append(i)
                    yy.append(value)

                    max_list[i] = max(max_list[i], value)

                ax.scatter(
                    xx,
                    yy,
                    marker='x',
                    color=cm.rainbow(j / size0),
                    # label=label,
                    label=r'$\mathrm{%sm}$' % length,
                )

            threshold_dict = {
                1700: 263,
                2000: 234,
                2300: 217,
                2600: 200,
            }

            threshold = threshold_dict[freq]

            length_x = len(n_transformer)
            xx = np.arange(length_x)
            yy = np.ones(length_x) * min(max_list)

            yy2 = np.ones(length_x) * threshold
            yy3 = yy2 * 0.75

            ax.plot(xx, yy, linestyle='--', alpha=0.8, color='blue', label='最优值')
            ax.plot(xx, yy2, linestyle='--', alpha=0.8, color='orange', label='门限值')
            ax.plot(xx, yy3, linestyle='--', alpha=0.8, color='r', label=r'门限值$\mathrm{75\%}$')

            if pos_index in [4, 8, 12, 16]:
                # ax.annotate('%.2fmA' % yy[0], (10, yy[0]), xytext=(10, yy[0]+10), ha="right", fontsize=11, color='blue')
                ax.annotate(r'$\mathrm{%.0fmA}$' % yy2[0], (11, yy2[0]), xytext=(11, yy2[0]+10), ha="right", fontsize=11, color='orange')
                ax.annotate(r'$\mathrm{%.0fmA}$' % yy3[0], (11, yy3[0]), xytext=(11, yy3[0]+10), ha="right", fontsize=11, color='r')

            # y轴 双坐标轴
            if pos_index in [4, 8, 12, 16]:
                ax2 = ax.twinx()

                ax2.set_ylim([0, 300])

                y2_ticks = [threshold, threshold * 0.75]
                y2_label = map(lambda x: r'$\mathrm{%.0fmA}$' % x, y2_ticks)

                ax2.set_yticks(y2_ticks)
                ax2.set_yticklabels(y2_label)
                ax2.tick_params(labelsize=9, direction='in')

                ax2.get_yticklabels()[0].set_color('orange')
                ax2.get_yticklabels()[1].set_color('r')

            y1 = min(max_list)
            x1 = max_list.index(y1)

            # txt = '最优扼流变比$\mathrm{%s:1}$\n最大干扰电流$\mathrm{%.2fmA}$' % (x1+5, y1)
            txt = '最优变比$\mathrm{%s:1}$\n干扰电流$\mathrm{%.2fmA}$' % (x1+5, y1)

            ax.annotate(
                txt, (x1, y1),
                xytext=(x1, y1+120),
                ha="center", va="center",
                # textcoords='offset points',
                fontsize=10,
                color='blue',
                arrowprops=dict(
                    # facecolor='#74C476',
                    alpha=0.6,
                    arrowstyle='fancy',
                    # connectionstyle='arc3,rad=0.5',
                    color='blue',
                )
                )
            # ax.text(0.05, 0.95, txt, va='top', ha='left', transform=ax.transAxes)

            ###################################################################

            # # 图例
            # cb_pos = 0.11
            # cax = fig.add_axes([cb_pos, 0.45, 0.01, 0.4])  # 四个参数分别是左、下、宽、长
            #
            # cmap = mpl.cm.twilight
            # norm = mpl.colors.Normalize(vmin=-100, vmax=100)
            # bounds = [tmp for tmp in np.linspace(-100, 100, size0 + 1)]
            # cb = mpl.colorbar.ColorbarBase(
            #     ax=cax,
            #     cmap=cmap,
            #     norm=norm,
            #     # to use 'extend', you must specify two extra boundaries:
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
            # cb.set_ticks([-100, 0, 100])
            # cb.set_ticklabels(['-350m', ' 0m', ' 350m'])
            #
            # cax.tick_params(labelsize=16)
            #
            # txt = '主\n被\n串\n错\n位'
            # ax.text(
            #     -1.5, 0.5,
            #     txt,
            #     fontsize=16,
            #     color='black',
            #     va='center',
            #     ha='center',
            #     transform=cax.transAxes,
            # )

            # ax.legend(loc='upper right', fontsize=11)

            ###################################################################

        # plt.tight_layout()

        # handles, labels = ax_list[0].get_legend_handles_labels()
        # plt.legend(
        #     handles, labels,
        #     loc='center right',
        #     # ncol=3,
        #     bbox_to_anchor=(1.29, 1.30),
        #     fontsize=12,
        # )

        # filename1 = '%s\\图表_%s.png' % (res_dir, s_index+1)
        # fig.savefig(filename1)

        # plt.show()
        # return

    plt.text(
        0.5, 0.07, '扼流变压器变比',
        va='top', ha='center', transform=fig.transFigure,
        fontsize=13,
    )

    plt.text(
        0.08, 0.5, r'最大邻线干扰电流$\mathrm{(mA)}$',
        va='center', ha='right', transform=fig.transFigure,
        fontsize=13, rotation=90,
    )

    handles, labels = ax_list[0].get_legend_handles_labels()
    plt.legend(
        handles, labels,
        loc='center right',
        # ncol=3,
        bbox_to_anchor=(1.74, 2.20),
        fontsize=11,
    )

    filename1 = '%s\\图表_%s.png' % (res_dir, '总图')
    fig.savefig(filename1, transparent=True)

    plt.show()
    return


def get_excel_data(n_transformer):
    # 根目录
    root = 'C:\\Users\\李继隆\\Desktop\\站内数字化轨道电路\\站内数字化_20230417\\'

    # 创建文件夹
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # res_dir = '%s数据提取_站内邻线干扰_%s' % (root, timestamp)
    #
    # if not os.path.exists(res_dir):
    #     os.makedirs(res_dir)

    scenes = [
        '一送一收|[距离/100]',
        '一送一收|[距离/100]-1',
        '两送一收|[距离/200]*2',
        '两送一收|[距离/200]*2-2',
    ]

    ret = pd.DataFrame()

    for s_index, scene in enumerate(scenes):

        print(scene)
        send_type, c_type = scene.split('|')

        file = '站内数字化_%s_数据输出.xlsx' % send_type
        path = '%s%s' % (root, file)
        df_input = pd.read_excel(path, '数据输出')

        df1 = df_input.loc[df_input["变压器变比"] == n_transformer].copy()

        row_list = []

        for freq in [1700, 2000, 2300, 2600]:

            df2 = df1.loc[df1["主串频率(Hz)"] == freq].copy()

            length_list = list(range(500, 1051, 50))

            max_current = 0
            for length in length_list:
                if c_type == '[距离/100]':
                    c_num = -(-length // 100)
                elif c_type == '[距离/100]-1':
                    c_num = -(-length // 100) - 1
                elif c_type == '[距离/200]*2':
                    c_num = -(-length // 200) * 2
                elif c_type == '[距离/200]*2-2':
                    c_num = -(-length // 200) * 2 - 2
                else:
                    raise KeyboardInterrupt('电容配置错误')
                row = df2.loc[df2["主串电容数(含TB)"] == c_num].copy()
                value = row['被串最大干扰电流(A)'].values[0] * 1000
                max_current = max(max_current, value)

            row_list.append(max_current)

        s0 = pd.Series(row_list, name=scene)

        ret = pd.concat([ret, s0], axis=1)

    s_np = np.array([263, 234, 217, 200])
    s0 = pd.Series(s_np * 0.75, name='门限值75%')
    ret = pd.concat([ret, s0], axis=1)

    ret = ret.transpose()
    f_list = [1700, 2000, 2300, 2600]
    ret.columns = map(lambda x: '%sHz' % x, f_list)
    print(ret)

    path2 = '%s%s' % (root, '站内数字化_数据整理_%s比1.xlsx' % n_transformer)
    with pd.ExcelWriter(path2) as writer:
        ret.to_excel(writer, sheet_name="变比_%s比1" % n_transformer, index=True)


if __name__ == '__main__':
    # draw_image_20230904_digital()
    get_excel_data(13)
    get_excel_data(14)
