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


def get_guangzhan_info():
    # info_line1 = [
    #     -36,
    #     ('0132AG', 2000, 475, 8),
    #     ('0132BG', 2600, 475, 6),
    #     ('0132CG', 2000, 500, 8),
    #     ('0148AG', 2600, 400, 5),
    #     ('0148BG', 2000, 600, 10),
    #     ('0148CG', 2600, 500, 6),
    #     ('0162AG', 2000, 551, 10),
    #     ('0162BG-1', 2600, 551, 7),
    #     ('0162BG-2', 2000, 400, 6),
    #     ('0178AG', 2600, 700, 8),
    # ]

    info_line1 = [
        -244,
        ('广湛NS1LQAG', 2000, 537, 9),
        ('广湛5578CG', 2600, 470, 6),
        ('广湛5578BG', 2000, 625, 10),
        ('广湛5578AG', 2600, 745, 9),
        ('广湛5560CG', 2000, 505, 9),
        ('广湛5560BG', 2600, 625, 8),
        ('广湛5560AG', 2000, 760, 13),
        ('广湛5542CG', 2600, 490, 6),
        ('广湛5542BG', 2000, 560, 10),
        ('广湛5542AG', 2600, 800, 10),
    ]

    info_line2 = [
        -294,
        ('南广NS1LQAG', 2000, 537, 9),
        ('南广5578CG', 2600, 470, 6),
        ('南广5578BG', 2000, 625, 10),
        ('南广5578AG', 2600, 745, 9),
        ('南广5560CG', 2000, 505, 9),
        ('南广5560BG', 2600, 625, 8),
        ('南广5560AG', 2000, 760, 13),
        ('南广5542CG', 2600, 490, 6),
        ('南广5542BG', 2000, 560, 10),
        ('南广5542AG', 2600, 800, 10),
    ]

    info_line3 = [
        -615,
        ('S1LQBG', 2600, 464, 6),
        ('S1LQAG', 2000, 464, 8),
        ('8420DG', 2600, 625, 8),
        ('8420CG', 2000, 745, 12),
        ('8420BG', 2600, 505, 7),
        ('8420AG', 2000, 625, 10),
        ('8394CG', 2600, 766, 10),
        ('8394BG', 2000, 490, 8),
        ('8394AG', 2600, 550, 7),
        ('8376CG', 2000, 810, 14),
    ]

    ret = []
    ret.extend(get_line_info(info_line1, info_line2))
    ret.extend(get_line_info(info_line2, info_line1))
    # ret.extend(get_line_info(info_line2, info_line3))
    # ret.extend(get_line_info(info_line3, info_line2))

    # ret = ret[:1]

    return ret


def get_guangzhan_test_info():
    # info_line1 = [
    #     0,
    #     ('广湛测试区段2600Hz', 2600, 625, 8),
    # ]
    #
    # # info_line2 = [
    # #     0,
    # #     ('广湛测试区段2000Hz', 2000, 625, 10),
    # # ]
    #
    # info_line3 = [
    #     -470,
    #     ('5578CG', 2600, 470, 6),
    #     ('5578BG', 2000, 625, 10),
    #     ('5578AG', 2600, 745, 9),
    # ]
    #
    # info_line4 = [
    #     -400,
    #     ('8420DG', 2600, 625, 8),
    # ]
    #
    # info_line5 = [
    #     -470,
    #     ('5578CG', 2600, 470, 6),
    #     ('5578BG', 2000, 625, 10),
    # ]

    ret = []
    # ret.extend(get_line_info(info_line1, info_line3))
    # ret.extend(get_line_info(info_line4, info_line5))

    for offset in range(-450, 451, 50):
        info_line1 = [
            offset,
            ('广湛测试区段2600Hz', 2600, 500, 0),
        ]

        info_line2 = [
            -470,
            ('5578CG', 2600, 470, 6),
            ('5578BG', 2000, 625, 10),
            ('5578AG', 2600, 745, 9),
        ]

        ret.extend(get_line_info(info_line1, info_line2))

    # ret.extend(get_line_info(info_line3, info_line1))
    # ret.extend(get_line_info(info_line2, info_line3))
    # ret.extend(get_line_info(info_line3, info_line2))

    return ret


# 获得区段位置信息
def get_line_info(line1, line2):
    line1 = line1.copy()
    line2 = line2.copy()

    offset = line2[0] - line1[0]
    line1.pop(0)
    line2.pop(0)

    zhu_left = zhu_right = 0
    res = []
    for sec_zhu in line1:
        zhu_left = zhu_right
        zhu_right = zhu_left + sec_zhu[2]

        bei_list = []
        bei_offset = 0

        bei_left = bei_right = offset
        for sec_bei in line2:
            bei_left = bei_right
            bei_right = bei_left + sec_bei[2]

            if bei_right < (zhu_left - 60):
                continue

            if bei_left > (zhu_right + 60):
                continue

            if len(bei_list) == 0:
                bei_offset = bei_left - zhu_left

            bei_list.append(sec_bei)

        res.append((sec_zhu, bei_list, bei_offset))

    return res


# 配置输入
def config_input_20231011_guangzhan():

    columns = [
        '序号',
        '分路模式',
        '主串区段',
        '被串区段',
        '主串频率',
        '被串频率',
        '主串区段长度',
        '被串区段长度',
        '主串电容数',
        '被串电容数',
        '被串相对位置',
        '主串方向',
        '被串方向',
    ]

    direction_list = [
        ('左发', '左发'),
        ('左发', '右发'),
        ('右发', '左发'),
        ('右发', '右发'),
    ]

    mode_list = [
        '主串调整被串分路',
        '主被串同时分路',
    ]

    src = get_guangzhan_info()
    # src = get_guangzhan_test_info()

    df = pd.DataFrame(index=columns, dtype='object')

    counter = 0
    for mode in mode_list:
        for val in src:

            for direction in direction_list:
                counter += 1

                s0 = pd.Series(name=counter, index=columns)

                s0['序号'] = s0.name
                s0['分路模式'] = mode

                zhu_info = val[0]
                bei_info = list(zip(*val[1]))

                s0['主串区段'] = zhu_info[0]
                s0['被串区段'] = list(bei_info[0])

                s0['主串频率'] = zhu_info[1]
                s0['被串频率'] = list(bei_info[1])

                s0['主串区段长度'] = zhu_info[2]
                s0['被串区段长度'] = list(bei_info[2])

                s0['主串电容数'] = zhu_info[3]
                s0['被串电容数'] = list(bei_info[3])

                s0['被串相对位置'] = val[2]

                s0['主串方向'] = direction[0]
                s0['被串方向'] = direction[1]

                print('generate row: %s --> %s' % (counter, s0.tolist()))

                df = pd.concat([df, s0], axis=1)

                # if counter == 4:
                #     return df.transpose()

    df = df.transpose()
    return df


# 配置表头
def config_headlist_20231011_guangzhan():
    head_list = [
        '序号',
        '备注',
        '分路模式',

        '耦合系数(μH/km)',

        # '线路名称', '车站名称',
        '主串区段', '被串区段',

        # '线间距(m)',
        # '并行长度(m)',
        # '被串相对位置(m)',

        '主串方向', '被串方向',
        # '线间距(m)',
        # '耦合系数(μH/km)',
        # '并行长度(m)',

        # '调谐区错位(m)',
        '主串区段长度(m)', '被串区段长度(m)',
        '被串相对位置(m)',

        # '主串左端坐标', '被串左端坐标',

        # '主串区段类型', '被串区段类型',
        '主串频率(Hz)', '被串频率(Hz)',

        # '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容数', '被串电容数',
        '主串电容值(μF)', '被串电容值(μF)',

        # '主串电容数量列表', '被串电容数量列表',
        # '主串电容容值列表', '被串电容容值列表',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串分路电阻(Ω)', '被串分路电阻(Ω)',

        '主串电缆长度(km)', '被串电缆长度(km)',

        '分路间隔(m)',

        '主串电平级',
        '电源电压',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        # '故障位置', '故障类型',
        # '干扰值变化',
    ]

    return head_list


def config_c_pack_20231011_guangzhan(src):
    c_num_list = []
    c_imp_list = []
    c_val_list = []

    for c_num in src:
        c_val = 25
        val_tmp = c_val * 1e-6

        c_imp = ImpedanceMultiFreq()
        c_imp.rlc_s = {
            1700: [10e-3, None, val_tmp],
            2000: [10e-3, None, val_tmp],
            2300: [10e-3, None, val_tmp],
            2600: [10e-3, None, val_tmp]}

        c_num_list.append(c_num)
        c_val_list.append(c_val)
        c_imp_list.append(c_imp)

    ret = {
        '电容数量列表': c_num_list,
        '电容容值列表': c_val_list,
        '电容阻抗列表': c_imp_list,
    }

    return ret


# 配置行数据
def config_row_data_20231011_guangzhan(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '广湛六线并行'
    data['分路模式'] = df_input['分路模式']

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['主串区段长度']
    length2 = data['被串区段长度(m)'] = df_input['被串区段长度']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = length2

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = 20

    # 区段频率
    para['freq_主'] = freq = df_input['主串频率']
    para['freq'] = Freq(freq)

    para['主串频率列表'] = [para['freq']]
    para['被串频率列表'] = list(map(lambda x: Freq(x), df_input['被串频率']))

    data['主串频率(Hz)'] = df_input['主串频率']
    data['被串频率(Hz)'] = df_input['被串频率']

    # data['主串区段类型'] = '高铁区间'
    # data['被串区段类型'] = '高铁区间'

    # 电容配置
    c_pack_zhu = config_c_pack_20231011_guangzhan([df_input['主串电容数']])
    c_pack_bei = config_c_pack_20231011_guangzhan(df_input['被串电容数'])

    # 电容模型参数
    para['主串电容数'] = c_pack_zhu['电容数量列表']
    para['被串电容数'] = c_pack_bei['电容数量列表']

    para['主串容值列表'] = c_pack_zhu['电容阻抗列表']
    para['被串容值列表'] = c_pack_bei['电容阻抗列表']

    # 电容参数输出
    data['主串电容数(含TB)'] = df_input['主串电容数']
    data['被串电容数(含TB)'] = df_input['被串电容数']

    data['主串电容数'] = df_input['主串电容数']
    data['被串电容数'] = df_input['被串电容数']

    data['主串电容值(μF)'] = c_pack_zhu['电容容值列表'][0]
    data['被串电容值(μF)'] = c_pack_bei['电容容值列表'][0]

    # data['主串电容数量列表'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = c_pack_bei['电容数量列表']

    # data['主串电容容值列表'] = c_pack_zhu['电容容值列表']
    # data['被串电容容值列表'] = c_pack_bei['电容容值列表']

    # 道床电阻
    rd = 10000
    data['主串道床电阻(Ω·km)'] = rd
    data['被串道床电阻(Ω·km)'] = rd

    para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
    para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])

    para['Rd'].value = rd

    # 钢轨阻抗
    data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
    data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)

    para['主串钢轨阻抗'] = para['Trk_z']
    para['被串钢轨阻抗'] = para['Trk_z']

    # 发码方向
    data['主串方向'] = para['sr_mod_主'] = df_input['主串方向']
    data['被串方向'] = para['sr_mod_被'] = df_input['被串方向']

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
    data['主串电缆长度(km)'] = para['主串电缆长度'] = cab_len
    data['被串电缆长度(km)'] = para['被串电缆长度'] = cab_len

    # 分路电阻

    mode = df_input['分路模式']

    r_sht = 1e-7
    if mode == '主串调整被串分路':
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = 1e10
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
        data['主串分路电阻(Ω)'] = 'None'

    elif mode == '主被串同时分路':

        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = r_sht
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
    else:
        raise KeyboardInterrupt('分路模式错误')

    para['Rsht_z'] = r_sht

    # 功出电源
    data['主串电平级'] = para['send_level'] = 3
    data['电源电压'] = para['pwr_v_flg'] = '最大'

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
    data['分路起点'] = offset - 14.5
    data['分路终点'] = offset + sum(length2) + 14.5

    # # focus_sec = '3778G'
    # focus_sec = '5578BG'
    # index_bei = data['被串区段'].index(focus_sec)
    #
    # l_point = offset + sum(length2[0:index_bei]) - 14.5
    # r_point = l_point + length2[index_bei] + 29
    #
    # data['分路起点'] = l_point
    # data['分路终点'] = r_point
    #
    # data['分路起点'] = offset - 14.5 + length2[0]
    # data['分路终点'] = offset + length2[0] + length2[1] + 14.5


class PreModel_QJ_20231011_guangzhan(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        self.train1['分路电阻1'].z = para['被串分路电阻']
        self.train2['分路电阻1'].z = para['主串分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=para['主串频率列表'],
                           m_lens=para['主串区段长度'],
                           j_lens=[29, 29],
                           m_typs=['2000A'],
                           c_nums=para['主串电容数'],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        # freq_tmp = Freq(para['freq_被'])
        # freq_tmp.change_freq()

        m_num = len(para['被串区段长度'])
        j_num = m_num + 1
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=m_num,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[29] * j_num,
                           m_typs=['2000A'] * m_num,
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']] * m_num,
                           send_lvs=[send_level] * m_num,
                           parameter=parameter)

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['Trk_z'], rd=para['Trk_z'])
        self.set_rail_para(line=l4, z_trk=para['Trk_z'], rd=para['Trk_z'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for index, sec in enumerate(self.section_group3.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['主串容值列表'][index]

        for index, sec in enumerate(self.section_group4.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['被串容值列表'][index]

    def add_train(self):
        para = self.parameter
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train2])
        self.l3 = l3

        l4 = Line(name_base='线路4', sec_group=self.section_group4,
                  parameter=self.parameter, train=[self.train1])
        self.l4 = l4

        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()


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


def draw_image_2021023_guangzhan():
    # plt.rcParams['font.size'] = 20

    # 根目录
    root = 'C:\\Users\\李继隆\\Desktop\\广湛六线并行\\'

    # 创建文件夹
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '%s图表汇总\\图表汇总_广湛六线并行_%s' % (root, timestamp)

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

    # 创建图表
    fig = plt.figure(figsize=(16, 8), dpi=100)
    fig.subplots_adjust(hspace=0.1, wspace=0.1, top=0.8, left=0.15, right=0.85)
    # title = '站内数字化轨道电路邻线干扰仿真：不同扼流变比'
    # fig.suptitle(title, x=0.5, y=0.93, fontsize=25, fontfamily='SimHei')

    file = '广湛六线并行_测试结果对比.xlsx'
    path = '%s%s' % (root, file)
    df1 = pd.read_excel(path, '仿真结果')
    df2 = pd.read_excel(path, '测试结果')
    xx2 = df2.columns.tolist()

    # print(df1)
    # print(df2)
    ax_list = []

    length = df1.shape[1]
    xx1 = list(range(length))

    for i in range(4):
        ax = fig.add_subplot(2, 2, i+1)
        ax_list.append(ax)

        yy1 = (df1.iloc[i, :]*1000).tolist()
        ax.plot(xx1, yy1, linestyle='-', alpha=0.8, color='blue')

        yy2 = df2.iloc[i, :].tolist()
        ax.scatter(
            xx2,
            yy2,
            marker='x',
            color='r',
        )

    # # 创建图表
    # fig = plt.figure(figsize=(16, 8), dpi=100)
    # fig.subplots_adjust(hspace=0.4)
    # title = '区段配置：%s  电容配置：%s' % (send_type, c_type)
    # fig.suptitle(title, x=0.5, y=0.98, fontsize=25, fontfamily='SimHei')

    # ax_list = []
    plt.show()


def analyse_complex_add():
    path = 'C:\\Users\\李继隆\\Desktop\\广湛六线并行\\仿真输出_广湛六线并行_复数形式.xlsx'
    df = pd.read_excel(path, sheet_name='被串分路电流复数')

    s1 = df.iloc[2, :]
    s2 = df.iloc[3, :]
    s1 = s1.apply(lambda x: complex(x)).values
    s2 = s2.apply(lambda x: complex(x)).values

    df2 = pd.DataFrame()
    for theta in range(0, 360, 10):
        k = 1j * np.sin(theta / 180 * np.pi) + np.cos(theta / 180 * np.pi)
        s3 = np.ones(len(s1)) * k

        s4 = pd.Series((s1 * s3) + s2, name=theta)
        s5 = s4.apply(lambda x: abs(x))
        df2 = pd.concat([df2, s5], axis=1)

    df2 = df2.transpose()
    print(df2)

    path2 = 'C:\\Users\\李继隆\\Desktop\\广湛六线并行\\结果导出\\广湛六线并行_复数形式处理_同时分路.xlsx'

    df2.to_excel(path2, sheet_name='result', index=False)


if __name__ == '__main__':
    # draw_image_20230904_digital()
    # draw_image_2021023_guangzhan()
    analyse_complex_add()
