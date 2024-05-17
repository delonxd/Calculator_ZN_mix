# from src.TrackCircuitElement.SectionGroup import *
# from src.TrackCircuitElement.Train import *
# from src.TrackCircuitElement.Line import *
# from src.TrackCircuitElement.LineGroup import *
# from src.Model.MainModel import *
# from src.Model.ModelParameter import *
# from src.FrequencyType import Freq
# from src.Model.PreModel import PreModel
from src.logMethod import *
from src.Data2Excel import *

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False


def draw_image_20240507_digital():
    # plt.rcParams['font.size'] = 20

    # 根目录
    # root = 'C:\\Users\\李继隆\\PycharmProjects\\Calculator_ZN_mix\\20230801_无死区\\无死区仿真结果汇总'
    root = 'C:\\Users\\李继隆\\Desktop\\站内数字化轨道电路\\站内数字化_20240507'
    # 创建文件夹
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '%s\\图表汇总_%s' % (root, timestamp)

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

    # path1 = '%s\\%s' % (root, '仿真输出_20240507_对位遍历_数据整理.xlsx')
    # path1 = '%s\\%s' % (root, '仿真输出_20240507_错位遍历_数据整理.xlsx')
    path1 = '%s\\%s' % (root, '仿真输出_20240507_错位遍历_数据整理_300m.xlsx')
    # path2 = '%s\\%s' % (root, '2000A邻线干扰_长度遍历2.xlsx')

    df_data1 = pd.read_excel(path1, '数据输出')
    MainLog.add_log_accurate('#' * 30)

    # df_data2 = pd.read_excel(path2, '数据输出')
    df_i_trk_1 = pd.read_excel(path1, '被串钢轨电流')
    MainLog.add_log_accurate('#' * 30)

    # df_i_trk_2 = pd.read_excel(path2, '被串钢轨电流')
    # MainLog.add_log_accurate('#' * 30)

    # length = df_data1.shape[1]
    # xx1 = list(range(length))

    # sec_length_list = [400, 600, 800, 1200]
    freq_list = [1700, 2000, 2300, 2600]

    condition_list = [
        ['两送一受', 1050, 12, 80],
        ['两送一受', 1050, 10, 90],
        ['两送一受', 850, 10, 60],
        ['两送一受', 850, 8, 60],
        ['一送一受', 1200, 12, 70],
        ['一送一受', 1200, 11, 70],
        ['一送一受', 600, 6, 40],
        ['一送一受', 600, 5, 40],
    ]

    sht_type_list = [
        '主串调整',
        '同位置分路',
    ]

    for sht_type in sht_type_list:
        for condition in condition_list:
            sec_type = condition[0]
            sec_length = condition[1]
            c_num = condition[2]
            power_voltage = condition[3]

            # 创建图表
            fig = plt.figure(figsize=(16, 8), dpi=100)
            # fig.subplots_adjust(hspace=0.4, wspace=0.1, top=0.8, left=0.15, right=0.85)
            fig.subplots_adjust(hspace=0.3, wspace=0.1, top=0.87, left=0.15, right=0.85)
            # fig.subplots_adjust(hspace=0.4)
            title = '%s-%sm(%sV)-%s个电容-%s' % (sec_type, sec_length, power_voltage,  c_num, sht_type)
            fig.suptitle(title, x=0.5, y=0.98, fontsize=25, fontfamily='SimHei')

            ax_list = []

            for j, freq_zhu in enumerate(freq_list):
                ax = fig.add_subplot(2, 2, j + 1)
                ax_list.append(ax)

                sub_title = '主串频率$\mathrm{%sHz}$' % freq_zhu
                ax.set_title(sub_title, pad=8, fontsize=12)

                # 纵坐标
                # ax.yaxis.grid(True, which='major')
                y_ticks = [0, 100, 200, 300]
                y_label = map(lambda x: r'$\mathrm{%.0f}$' % x, y_ticks)

                ax.set_yticks(y_ticks)
                ax.set_yticklabels(y_label)

                # ax.yaxis.set_font(20)
                ax.set_ylim([0, 350])

                # 横坐标

                x_ticks = list(range(0, sec_length, 100))
                x_label = map(lambda x: r'$\mathrm{%.0f}$' % x, x_ticks)

                ax.set_xticks(x_ticks)
                ax.set_xticklabels(x_label)

                # if pos_index in [13, 14, 15, 16]:
                #     ax.set_xticklabels(x_label)
                # else:
                #     ax.set_xticklabels([''] * len(x_ticks))
                # ax.set_yticklabels(fontfamily="Times New Roman")

                # 坐标轴字体
                ax.tick_params(
                    # axis='y',
                    labelsize=9,  # y轴字体大小设置
                    # color='r',        # y轴标签颜色设置
                    # labelcolor='b',   # y轴字体颜色设置
                    direction='in',  # y轴标签方向设置
                    # pad=10,
                )

                ###################################

                # offset_list = [0]
                offset_list = list(range(-300, 301, 100))

                max_value = 0
                max_index = None

                for i, offset in enumerate(offset_list):
                    index = df_data1.loc[
                        (df_data1["主串分路位置"] == sht_type) &
                        (df_data1["送受类型"] == sec_type) &
                        (df_data1["主串区段长度(m)"] == sec_length) &
                        (df_data1["主串电容数(含TB)"] == c_num) &
                        (df_data1["电源电压"] == power_voltage) &
                        (df_data1["主串频率(Hz)"] == freq_zhu) &
                        (df_data1["被串相对位置(m)"] == offset)
                    ]['序号'].tolist()

                    if len(index) == 1:
                        index = index[0] - 1
                    else:
                        raise KeyboardInterrupt('error: len(index) != 1')

                    yy1 = (df_i_trk_1.iloc[index, :].copy().dropna()*1000).tolist()
                    xx1 = range(len(yy1))

                    value = max(yy1)
                    if value > max_value:
                        max_value = value
                        max_index = index

                    color_list = [
                        'gray',
                        'red',
                        'orange',
                        'blue',
                        'green',
                    ]

                    color = cm.rainbow(i / len(offset_list))
                    # ax.plot(xx1, yy1, linestyle='-', alpha=0.8, color=color, label='%sHz' % freq_zhu)
                    ax.plot(xx1, yy1, linestyle='-', alpha=0.8, color=color, label='错位$\mathrm{%sm}$' % offset)

                    # ax.legend(loc='upper right', fontsize=9)

                    # yy2 = df2.iloc[i, :].tolist()
                    # ax.scatter(
                    #     xx2,
                    #     yy2,
                    #     marker='x',
                    #     color='r',
                    # )

                threshold_dict = {
                    1700: 263,
                    2000: 234,
                    2300: 217,
                    2600: 200,
                }

                threshold = threshold_dict[freq_zhu]

                length_x = sec_length
                xx = np.arange(length_x)
                # yy = np.ones(length_x) * min(max_list)

                yy2 = np.ones(length_x) * threshold
                yy3 = yy2 * 0.75

                # ax.plot(xx, yy, linestyle='--', alpha=0.8, color='blue', label='最优值')
                ax.plot(xx, yy2, linestyle='--', alpha=0.8, color='orange', label='门限值')
                ax.plot(xx, yy3, linestyle='--', alpha=0.8, color='r', label=r'门限值$\mathrm{75\%}$')

                pos_x = length_x + 10
                ax.annotate(r'$\mathrm{%.0fmA}$' % yy2[0], (pos_x, yy2[0]), xytext=(pos_x, yy2[0] + 10), ha="right",
                            fontsize=9, color='orange')
                ax.annotate(r'$\mathrm{%.0fmA}$' % yy3[0], (pos_x, yy3[0]), xytext=(pos_x, yy3[0] + 10), ha="right",
                            fontsize=9, color='r')

                # # y轴 双坐标轴
                # ax2 = ax.twinx()
                #
                # ax2.set_ylim([0, 300])
                #
                # y2_ticks = [threshold, threshold * 0.75]
                # y2_label = map(lambda x: r'$\mathrm{%.0fmA}$' % x, y2_ticks)
                #
                # ax2.set_yticks(y2_ticks)
                # ax2.set_yticklabels(y2_label)
                # ax2.tick_params(labelsize=9, direction='in')
                #
                # ax2.get_yticklabels()[0].set_color('orange')
                # ax2.get_yticklabels()[1].set_color('r')

                # 箭头
                s_tmp = df_data1.iloc[max_index, :]
                arrow_x = s_tmp["被串最大干扰位置(m)"]
                arrow_y = s_tmp["被串最大干扰电流(A)"] * 1000
                offset_tmp = s_tmp["被串相对位置(m)"]

                txt = '最大干扰电流$\mathrm{%.2fmA}$\n主被串错位$\mathrm{%.0fm}$' % (arrow_y, offset_tmp)

                txt_y = 300 if arrow_y > 300 else arrow_y
                txt_x = 50 if arrow_x < 50 else arrow_x
                ax.annotate(
                    txt, (arrow_x, arrow_y),
                    xytext=(txt_x + 100, txt_y + 50),
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

            plt.text(
                0.5, 0.07, '被串分路位置$\mathrm{(m)}$',
                va='top', ha='center', transform=fig.transFigure,
                fontsize=13,
            )

            plt.text(
                0.12, 0.5, '邻线干扰电流$\mathrm{(mA)}$',
                va='center', ha='right', transform=fig.transFigure,
                fontsize=13, rotation=90,
            )

            handles, labels = ax_list[0].get_legend_handles_labels()
            plt.legend(
                handles, labels,
                loc='center right',
                # ncol=3,
                bbox_to_anchor=(1.34, 1.2),
                fontsize=11,
            )

            # plt.show()
            # raise KeyboardInterrupt()

            filename1 = '%s\\站内数字化邻线干扰_%s_%sm_%s个电容_%s.png' % (res_dir, sec_type, sec_length, c_num, sht_type)
            MainLog.add_log_accurate('save figure --> %s' % filename1)
            fig.savefig(filename1, transparent=True)

    # # 创建图表
    # fig = plt.figure(figsize=(16, 8), dpi=100)
    # fig.subplots_adjust(hspace=0.4)
    # title = '区段配置：%s  电容配置：%s' % (send_type, c_type)
    # fig.suptitle(title, x=0.5, y=0.98, fontsize=25, fontfamily='SimHei')

    # ax_list = []
    # plt.show()


if __name__ == '__main__':
    draw_image_20240507_digital()
