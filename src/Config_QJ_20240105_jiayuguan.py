from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq
from src.Model.PreModel import PreModel

import os
import time
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False


# 配置输入
def config_input_20240105_jiayuguan():
    columns = [
        '序号',
        '分路电阻',
        '信号类型',
    ]

    df = pd.DataFrame(index=columns, dtype='object')

    r_list = [1e-7, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]

    signal_types = ['后方区段信号', '前方区段信号']
    counter = 0
    for val in r_list:

        for signal in signal_types:
            counter += 1

            s0 = pd.Series(name=counter, index=columns)

            s0['序号'] = s0.name
            s0['分路电阻'] = val
            s0['信号类型'] = signal

            print('generate row: %s --> %s' % (counter, s0.tolist()))

            df = pd.concat([df, s0], axis=1)

    df = df.transpose()

    return df


# 配置表头
def config_headlist_20240105_jiayuguan():
    head_list = [
        '序号',
        '备注',

        # '后方区段', '前方区段',

        '发送器方向',

        '后方区段长度(m)', '前方区段长度(m)',
        '信号类型',
        '信号频率(Hz)',
        '后方区段频率(Hz)', '前方区段频率(Hz)',

        '电容数量列表',
        '电容容值列表',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '道床电阻(Ω·km)',

        '分路电阻(Ω)',
        '电缆长度(km)',

        '分路间隔(m)',

        '电平级',
        '电源电压',

    ]

    return head_list


def generate_imp_list(src: list):
    ret = []
    for c_value in src:
        val = c_value * 1e-6
        tmp = ImpedanceMultiFreq()
        tmp.rlc_s = {
            1700: [10e-3, None, val],
            2000: [10e-3, None, val],
            2300: [10e-3, None, val],
            2600: [10e-3, None, val]}
        ret.append(tmp)

    return ret


# 配置行数据
def config_row_data_20240105_jiayuguan(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '无'

    # 区段名
    # data['主串区段'] = para['主串区段'] = '[邢贡线X1LQG]'
    # data['被串区段'] = para['被串区段'] = '[京九线X1LQBG, 京九线X1LQAG]'

    data['后方区段'] = para['后方区段'] = '后方区段'
    data['前方区段'] = para['前方区段'] = '前方区段'

    # 区段长度
    # data['后方区段长度(m)'] = para['后方区段长度']
    # data['前方区段长度(m)'] = para['前方区段长度']

    para['区段长度列表'] = [1300, 1300]

    data['后方区段长度(m)'] = para['后方区段长度'] = para['区段长度列表'][0]
    data['前方区段长度(m)'] = para['前方区段长度'] = para['区段长度列表'][1]
    # para['被串区段长度'] = [400, 500]

    # data['主串区段长度(m)'] = para['主串区段长度']
    # data['被串区段长度(m)'] = para['被串区段长度']

    # 相对位置
    # data['被串相对位置(m)'] = offset = -30

    para['offset_zhu'] = 0
    # para['offset_bei'] = 30

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = 20

    # 区段频率

    freq1 = data['前方区段频率(Hz)'] = 1700
    freq2 = data['后方区段频率(Hz)'] = 2300
    para['区段频率列表'] = [Freq(freq2), Freq(freq1)]
    para['freq_value_list'] = [freq2, freq1]

    data['信号类型'] = df_input['信号类型']

    tmp = {
        '后方区段信号': 2300,
        '前方区段信号': 1700,
    }

    data['信号频率(Hz)'] = para['freq_主'] = freq = tmp[data['信号类型']]
    data['freq'] = para['freq'] = Freq(freq)

    # para['freq_主'] = freq1 = data['主串频率(Hz)'] = 1700
    # para['freq_被'] = freq2 = data['被串频率(Hz)'] = 2300
    # freq = freq1
    # data['freq'] = para['freq'] = Freq(freq1)
    # para['主串频率列表'] = [Freq(1700)]
    # para['被串频率列表'] = [Freq(1700), Freq(2300)]

    # data['主串区段类型'] = '高铁区间'
    # data['被串区段类型'] = '高铁区间'

    # # 电容配置
    # c_pack_zhu = config_c_pack_20230908_offset(para['主串频率列表'], para['主串区段长度'], [25])
    # c_pack_bei = config_c_pack_20230908_offset(para['被串频率列表'], para['被串区段长度'], [25, 25, 25])

    # 电容内置参数
    data['电容数量列表'] = para['电容数量列表'] = [16, 14]
    data['电容容值列表'] = [46, 55]
    para['电容阻抗列表'] = generate_imp_list(data['电容容值列表'])

    # para['主串电容数'] = [9]
    # para['被串电容数'] = [4, 6]

    # c_value_zhu = [55]
    # c_value_bei = [55, 46]

    # para['主串阻抗列表'] = generate_imp_list(c_value_zhu)
    # para['被串阻抗列表'] = generate_imp_list(c_value_bei)

    # 电容参数输出

    # data['主串电容数量列表'] = para['主串电容数']
    # data['被串电容数量列表'] = para['被串电容数']

    # data['主串电容容值列表'] = c_value_zhu
    # data['被串电容容值列表'] = c_value_bei

    # data['主串电容数(含TB)'] = para['主串电容数']
    # data['被串电容数(含TB)'] = para['被串电容数']
    #
    # data['主串电容值(μF)'] = c_value_zhu[0]
    # data['被串电容值(μF)'] = c_value_bei[1]

    # 道床电阻
    rd = 10000
    data['道床电阻(Ω·km)'] = rd
    para['道床电阻'] = Constant(data['道床电阻(Ω·km)'])

    # data['主串道床电阻(Ω·km)'] = rd
    # data['被串道床电阻(Ω·km)'] = rd
    #
    # para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
    # para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])

    para['Rd'].value = rd

    # 钢轨阻抗
    data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
    data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)

    para['钢轨阻抗'] = para['Trk_z']

    # para['主串钢轨阻抗'] = para['Trk_z']
    # para['被串钢轨阻抗'] = para['Trk_z']

    # 发码方向
    # data['主串方向'] = para['sr_mod_主'] = '左发'
    # data['被串方向'] = para['sr_mod_被'] = '左发'

    data['发送器方向'] = para['sr_mod_主'] = '右发'

    # 电缆参数
    data['电缆电阻最大(Ω/km)'] = 45
    data['电缆电阻最小(Ω/km)'] = 43
    data['电缆电容最大(F/km)'] = 28e-9
    data['电缆电容最小(F/km)'] = 28e-9

    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
    para['Cable_C'].value = data['电缆电容最大(F/km)']

    # 电缆长度
    cab_len = 10
    para['cab_len'] = cab_len
    data['电缆长度(km)'] = para['电缆长度'] = cab_len
    # data['主串电缆长度(km)'] = para['主串电缆长度'] = cab_len
    # data['被串电缆长度(km)'] = para['被串电缆长度'] = cab_len

    # 分路电阻
    # mode = df_input['分路模式']
    # data['分路模式'] = df_input['分路模式']

    r_sht = df_input['分路电阻']

    data['分路电阻(Ω)'] = para['分路电阻'] = r_sht

    # if mode == '主串调整被串分路':
    #     data['主串分路电阻(Ω)'] = para['主串分路电阻'] = 1e10
    #     data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
    #     data['主串分路电阻(Ω)'] = 'None'
    #
    # elif mode == '主被串同时分路':
    #
    #     data['主串分路电阻(Ω)'] = para['主串分路电阻'] = r_sht
    #     data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
    # else:
    #     raise KeyboardInterrupt('分路模式错误')

    # 功出电源
    # data['主串电平级'] = para['send_level'] = 3
    data['电平级'] = para['send_level'] = 3
    # data['电源电压'] = para['pwr_v_flg'] = '最大'
    data['电源电压'] = para['pwr_v_flg'] = 130

    # 特殊位置
    data['极性交叉位置'] = para['极性交叉位置'] = []
    data['特殊位置'] = para['special_point'] = data['极性交叉位置']
    data['节点选取模式'] = para['节点选取模式'] = '特殊'

    # 机车信号
    data['最小机车信号位置'] = '-'
    data['机车信号感应系数'] = \
        str(para['机车信号比例V']) + '/' + str(para['机车信号比例I'][freq])
    para['机车信号系数值'] = para['机车信号比例V'] / para['机车信号比例I'][freq]

    # 分路间隔
    data['分路间隔(m)'] = 1
    data['分路起点'] = 1200 - 14.5
    # data['分路终点'] = sum(para['区段长度列表']) + 14.5
    data['分路终点'] = 1400 + 14.5


class PreModel_20240105_QJ_jiayuguan(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        # self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        self.train1['分路电阻1'].z = para['分路电阻']
        # self.train2['分路电阻1'].z = para['主串分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=2,
                           m_frqs=para['区段频率列表'],
                           m_lens=para['区段长度列表'],
                           j_lens=[29, 29, 29],
                           m_typs=['2000A'] * 2,
                           c_nums=para['电容数量列表'],
                           sr_mods=[para['sr_mod_主']] * 2,
                           send_lvs=[send_level] * 2,
                           parameter=parameter)

        freq = para['freq_主']
        freq_list = para['freq_value_list']

        focus_index = int(freq_list.index(freq) + 1)
        sec_name = '区段%s' % focus_index

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3[sec_name]['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3[sec_name]['右调谐单元'].set_power_voltage(flg)

        # freq_tmp = Freq(para['freq_被'])
        # freq_tmp.change_freq()
        #
        # # m_num = len(para['被串区段长度'])
        # # j_num = m_num + 1
        # sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=2,
        #                    m_frqs=para['被串频率列表'],
        #                    m_lens=para['被串区段长度'],
        #                    j_lens=[29, 29, 0],
        #                    m_typs=['2000A'] * 2,
        #                    c_nums=para['被串电容数'],
        #                    sr_mods=[para['sr_mod_被']] * 2,
        #                    send_lvs=[send_level] * 2,
        #                    parameter=parameter)

        self.section_group3 = sg3
        # self.section_group4 = sg4

        self.change_c_value()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        # self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
        #                     parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['Trk_z'], rd=para['Trk_z'])
        # self.set_rail_para(line=l4, z_trk=para['Trk_z'], rd=para['Trk_z'])

        # self.lg = LineGroup(l3, l4, name_base='线路组')
        self.lg = LineGroup(l3, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for index, sec in enumerate(self.section_group3.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['电容阻抗列表'][index]
        #
        # for index, sec in enumerate(self.section_group4.element.values()):
        #     for ele in sec.element.values():
        #         if isinstance(ele, CapC):
        #             ele.z = para['被串阻抗列表'][index]

    def add_train(self):
        para = self.parameter
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train1])
        self.l3 = l3

        # l4 = Line(name_base='线路4', sec_group=self.section_group4,
        #           parameter=self.parameter, train=[self.train1])
        # self.l4 = l4

        self.set_rail_para(line=l3, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])
        # self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        # self.set_rail_para(line=l4, z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        # self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg = LineGroup(self.l3, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()


def draw_image_20240105_jiayuguan(root, file):
    # plt.rcParams['font.size'] = 20

    # 创建文件夹
    # timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # res_dir = '%s图表汇总\\站内邻线干扰_%s' % (root, timestamp)

    str1 = file.split('.')[0]
    res_dir = '%s\\图表汇总\\%s' % (root, str1)

    # 读取数据

    path = '%s\\%s' % (root, file)
    df_input = pd.read_excel(path, '数据输出')
    df_data = pd.read_excel(path, '前方钢轨电流')

    df_rcv1 = pd.read_excel(path, '后方区段接收端轨入电压')
    df_rcv2 = pd.read_excel(path, '前方区段接收端轨入电压')

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    df_tmp = df_input[df_input['信号类型'] == '后方区段信号']
    r_sht_list = df_tmp['分路电阻(Ω)'].tolist()

    # 前方钢轨电流
    for index0, r_sht in enumerate(r_sht_list):

        # 数据处理
        # df1 = df_input.copy()

        ###################################################################

        # 创建图表
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(hspace=1)
        ax = fig.add_subplot(1, 1, 1)

        # 图表标题
        # title = file.split('.')[0]

        title = '%s嘉峪关分路不良-前方钢轨电流-分路电阻%sΩ' % (index0+1, r_sht)
        ax.set_title(title, x=0.5, y=1.04, fontsize=30)

        # fig.suptitle(title, fontsize=30)

        # 横纵坐标
        # 坐标名
        ax.set_xlabel('分路位置', fontsize=20)
        ax.set_ylabel('前方钢轨电流(A)', fontsize=20)

        # 纵坐标
        ax.yaxis.grid(True, which='major')
        # ax.yaxis.set_font(20)
        # ax.set_ylim([0, 3])

        # 横坐标
        # x_ticks = [0, 100, 200, 300, 400]
        # x_label = ['接收', '100m', '200m', '300m', '发送']

        # ax.set_xticks(x_ticks)
        # ax.set_xticklabels(x_label)

        # 坐标轴字体
        ax.tick_params(
            # axis='y',
            labelsize=14,       # y轴字体大小设置
            # color='r',        # y轴标签颜色设置
            # labelcolor='b',   # y轴字体颜色设置
            direction='in',     # y轴标签方向设置
            # pad=10,
        )

        ###################################################################

        signal_type_list = ['前方区段信号', '后方区段信号']

        # 画曲线

        for j, signal_type in enumerate(signal_type_list):
            df_tmp1 = df_input[df_input['分路电阻(Ω)'] == r_sht]
            df_tmp2 = df_tmp1[df_tmp1['信号类型'] == signal_type]

            i = df_tmp2['序号'].tolist()[0] - 1

            row = df_data.iloc[i, :].copy()

            row_output = df_input.iloc[i, :].copy()
            signal_type = row_output['信号类型']
            # r_sht = row_output['分路电阻(Ω)']

            label = '%s' % signal_type

            xx = np.arange(row.size)
            yy = row.values

            color = ['red', 'blue'][j]
            ax.plot(
                xx,
                yy,
                linestyle='-',
                alpha=1,
                color=color,
                # color=cm.twilight(i / size0),
                label=label,
                # linewidth=width,
            )

        ax.legend(loc='upper right', fontsize=13)

        ###################################################################

        plt.tight_layout()

        filename1 = '%s\\%s.png' % (res_dir, title)
        fig.savefig(filename1)

        # plt.show()

    # 轨入电压
    for index0, r_sht in enumerate(r_sht_list):

        ###################################################################

        # 创建图表
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(hspace=1)
        ax = fig.add_subplot(1, 1, 1)

        # 图表标题
        # title = file.split('.')[0]

        title = '%s嘉峪关分路不良-轨入电压-分路电阻%sΩ' % (index0+1, r_sht)
        ax.set_title(title, x=0.5, y=1.04, fontsize=30)

        # fig.suptitle(title, fontsize=30)

        # 横纵坐标
        # 坐标名
        ax.set_xlabel('分路位置', fontsize=20)
        ax.set_ylabel('轨入电压(V)', fontsize=20)

        # 纵坐标
        ax.yaxis.grid(True, which='major')
        # ax.yaxis.set_font(20)
        # ax.set_ylim([0, 3])

        # 横坐标
        # x_ticks = [0, 100, 200, 300, 400]
        # x_label = ['接收', '100m', '200m', '300m', '发送']

        # ax.set_xticks(x_ticks)
        # ax.set_xticklabels(x_label)

        # 坐标轴字体
        ax.tick_params(
            # axis='y',
            labelsize=14,       # y轴字体大小设置
            # color='r',        # y轴标签颜色设置
            # labelcolor='b',   # y轴字体颜色设置
            direction='in',     # y轴标签方向设置
            # pad=10,
        )

        ###################################################################

        # 画曲线

        df_tmp1 = df_input[df_input['分路电阻(Ω)'] == r_sht]

        df_tmp2 = df_tmp1[df_tmp1['信号类型'] == '前方区段信号']
        i = df_tmp2['序号'].tolist()[0] - 1
        xx = np.arange(df_rcv2.iloc[i, :].copy().size)
        yy1 = df_rcv2.iloc[i, :].copy().values

        ax.plot(xx, yy1, linestyle='-', color='red', label='前方区段主轨轨入')

        df_tmp2 = df_tmp1[df_tmp1['信号类型'] == '后方区段信号']
        i = df_tmp2['序号'].tolist()[0] - 1
        yy2 = df_rcv1.iloc[i, :].copy().values
        yy3 = df_rcv2.iloc[i, :].copy().values

        ax.plot(xx, yy2, linestyle='-', color='blue', label='后方区段主轨轨入')
        ax.plot(xx, yy3, linestyle='-', color='green', label='后方区段小轨轨入')

        # for j, signal_type in enumerate(signal_type_list):
        #     df_tmp2 = df_tmp1[df_tmp1['信号类型'] == signal_type]
        #
        #     i = df_tmp2['序号'].tolist()[0] - 1
        #
        #     row = df_data.iloc[i, :].copy()
        #
        #     row_output = df_input.iloc[i, :].copy()
        #     signal_type = row_output['信号类型']
        #     # r_sht = row_output['分路电阻(Ω)']
        #
        #     label = '%s' % signal_type
        #
        #     xx = np.arange(row.size)
        #     yy = row.values
        #
        #     color = ['red', 'blue'][j]
        #     ax.plot(
        #         xx,
        #         yy,
        #         linestyle='-',
        #         alpha=1,
        #         color=color,
        #         label=label,
        #     )

        ax.legend(loc='upper right', fontsize=13)

        ###################################################################

        plt.tight_layout()

        filename1 = '%s\\%s.png' % (res_dir, title)
        fig.savefig(filename1)


if __name__ == '__main__':
    draw_image_20240105_jiayuguan(
        '..\\20240105_嘉峪关分路不良',
        '仿真输出_嘉峪关分路不良_20240105140612.xlsx',
    )