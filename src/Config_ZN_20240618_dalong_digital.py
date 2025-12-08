
from src.logMethod import MainLog
from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant
from src.FrequencyType import Freq

from src.Module.TcsrLib import ZPW2000A_ZN_Digital
from src.Module.TcsrLib import ZPW2000A_ZN_Digital_Middle
from src.Module.OutsideElement import CapC

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line
from src.Model.PreModel import PreModel

import os
import time
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
# from matplotlib import cm

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False


def config_input_20240618_dalong_digital():

    columns = [
        '序号',
        '备注',
        '主串区段',
        '被串区段',
        '主串区段长度(m)',
        '被串区段长度(m)',
        '被串相对位置(m)',

        '耦合系数(μH/km)',

        '主串频率(Hz)',
        '被串频率(Hz)',

        '主串电容数(含TB)',
        '被串电容数(含TB)',
        '主串电容值(μF)',
        '被串电容值(μF)',

        '主串道床电阻(Ω·km)',
        '被串道床电阻(Ω·km)',

        '主串方向',
        '被串方向',

        '主串电缆长度(km)',
        '被串电缆长度(km)',

        '分路模式',
        '分路电阻(Ω)',

        '主串电平级',
        '主串电源电压',

        '分路间隔(m)',

    ]

    df = pd.DataFrame(index=columns, dtype='object')

    sec_list = [
        ['IG', -550, 410, 2000, 11, '左发', [439.7, 516.15, 5, 6]],
        ['IG', -550, 410, 1700, 11, '右发', [439.7, 516.15, 5, 6]],
        ['IIG', -543, 341, 2600, 10, '左发', [436.06, 448.41, 5, 5]],
        ['IIG', -543, 341, 2300, 10, '右发', [436.06, 448.41, 5, 5]],
    ]

    condition_list = [
        ['主被串同时分路'],
    ]

    counter = 1

    pick_sec = [
        [0, 3],
        [1, 3],
        [2, 1],
        [3, 1],
    ]

    # sec_list = [
    #     ['IG', -550, 410, 2000, 11, '左发', [439.7, 516.15, 5, 6]],
    #     ['IG', -550, 410, 1700, 11, '右发', [439.7, 516.15, 5, 6]],
    #     ['IIG', -543, 341, 2600, 10, '左发', [436.06, 448.41, 5, 5]],
    #     ['IIG', -543, 341, 2300, 10, '右发', [436.06, 448.41, 5, 5]],
    #     ['3G', -592, 366, 2000, 10, '左发', [489.12, 473.32, 5, 5]],
    #     ['3G', -592, 366, 1700, 10, '右发', [489.12, 473.32, 5, 5]],
    # ]
    #
    # condition_list = [
    #     ['主串调整被串分路'],
    #     ['主被串同时分路'],
    # ]
    #
    # counter = 1
    #
    # pick_sec = [
    #     [0, 2],
    #     [0, 3],
    #     [1, 2],
    #     [1, 3],
    #     [2, 0],
    #     [2, 1],
    #     [3, 0],
    #     [3, 1],
    #     [2, 4],
    #     [2, 5],
    #     [3, 4],
    #     [3, 5],
    #     [4, 2],
    #     [4, 3],
    #     [5, 2],
    #     [5, 3],
    # ]

    # sec_list = [
    #     # ['IG', 0, 1050, 1700, 12, '右发'],
    #     # ['IG', 0, 1050, 1700, 12, '右发'],
    #     # ['IIG', -200, 850, 1700, 12, '右发'],
    #     # ['IIG', -200, 850, 1700, 12, '右发'],
    #
    #     ['IG', -550, 410, 2000, 12, '左发'],
    #     ['IG', -550, 410, 1700, 12, '右发'],
    #     ['IIG', -543, 341, 2600, 10, '左发'],
    #     ['IIG', -543, 341, 2300, 10, '右发'],
    # ]
    #
    # pick_sec = [
    #     [0, 2],
    #     # [1, 2],
    # ]

    for index1, index2 in pick_sec:
        for condition in condition_list:
            sec_zhu = sec_list[index1]
            sec_bei = sec_list[index2]
            s0 = pd.Series(name=counter, index=columns)

            s0['序号'] = s0.name
            s0['备注'] = '站内数字化两送一收'
            s0['主串区段'] = sec_zhu[0]
            s0['被串区段'] = sec_bei[0]

            info1 = s0['主串电容分布'] = sec_zhu[6]
            info2 = s0['被串电容分布'] = sec_bei[6]

            s0['主串区段长度(m)'] = info1[0] + info1[1]
            s0['被串区段长度(m)'] = info2[0] + info2[1]

            s0['被串相对位置(m)'] = sec_bei[1] - sec_zhu[1]

            s0['耦合系数(μH/km)'] = 21

            s0['主串频率(Hz)'] = sec_zhu[3]
            s0['被串频率(Hz)'] = sec_bei[3]

            s0['主串电容数(含TB)'] = sec_zhu[4]
            s0['被串电容数(含TB)'] = sec_bei[4]

            s0['主串电容值(μF)'] = 25
            s0['被串电容值(μF)'] = 25

            s0['主串道床电阻(Ω·km)'] = 10000
            s0['被串道床电阻(Ω·km)'] = 10000

            s0['主串方向'] = sec_zhu[5]
            s0['被串方向'] = sec_bei[5]

            s0['主串电缆长度(km)'] = 4
            s0['被串电缆长度(km)'] = 4

            s0['分路模式'] = condition[0]
            s0['分路电阻(Ω)'] = 1e-7

            s0['主串电平级'] = 1
            s0['主串电源电压'] = 80

            s0['分路间隔(m)'] = 1

            print('generate row: %s --> %s' % (counter, s0.tolist()))

            df = pd.concat([df, s0], axis=1, sort=False)
            counter += 1

            # if counter > 1:
            #     df = df.transpose()
            #     return df

    df = df.transpose()
    return df


# 配置表头
def config_headlist():
    head_list = [
        '序号',
        '备注',
        # '线路名称', '车站名称',
        '主串区段', '被串区段',

        '耦合系数(μH/km)',

        '主串方向', '被串方向',

        '主串区段长度(m)', '被串区段长度(m)',
        '主串接收位置(m)', '被串接收位置(m)',
        '被串相对位置(m)',

        '主串频率(Hz)', '被串频率(Hz)',

        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',

        '主串方向', '被串方向',
        # '主串TB模式', '被串TB模式',

        '主串电缆长度(km)', '被串电缆长度(km)',
        '分路模式',
        '主串分路电阻(Ω)', '被串分路电阻(Ω)',


        '主串电平级',
        '电源电压',

        '分路间隔(m)',

        '扼流变比',
        '扼流_Rs(Ω)',
        '扼流_Ls(μH)',
        '扼流_Rm(Ω)',
        '扼流_Lm(mH)',
        '隔直电容(μf)',


        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
    ]

    return head_list


# 配置行数据
def config_row_data(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = df_input['备注']

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['主串区段长度(m)']
    length2 = data['被串区段长度(m)'] = df_input['被串区段长度(m)']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = [length2]

    para['主串电容分布'] = df_input['主串电容分布']
    para['被串电容分布'] = df_input['被串电容分布']

    data['主串接收位置(m)'] = para['主串电容分布'][0]
    data['被串接收位置(m)'] = para['被串电容分布'][0]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = df_input['耦合系数(μH/km)']

    # 区段频率
    para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率(Hz)']
    para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率(Hz)']
    freq = freq1
    data['freq'] = para['freq'] = Freq(freq1)
    para['主串频率列表'] = [Freq(freq1)]
    para['被串频率列表'] = [Freq(freq2)]

    # 电容数量
    # data['主串电容数量列表'] = para['主串电容数'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = para['被串电容数'] = c_pack_bei['电容数量列表']

    c_num1 = df_input['主串电容数(含TB)']
    c_num2 = df_input['被串电容数(含TB)']

    data['主串电容数量列表'] = para['主串电容数'] = [c_num1]
    data['被串电容数量列表'] = para['被串电容数'] = [c_num2]

    data['主串电容数(含TB)'] = c_num1
    data['被串电容数(含TB)'] = c_num2

    # 电容容值
    data['主串电容值(μF)'] = df_input['主串电容值(μF)']
    data['被串电容值(μF)'] = df_input['被串电容值(μF)']

    # data['主串电容数量列表'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = c_pack_bei['电容数量列表']

    # data['主串电容容值列表'] = [25]
    # data['被串电容容值列表'] = [25]

    val_tmp_zhu = data['主串电容值(μF)'] * 1e-6
    val_tmp_bei = data['被串电容值(μF)'] * 1e-6

    c_imp_zhu = ImpedanceMultiFreq()
    c_imp_zhu.rlc_s = {
        1700: [10e-3, None, val_tmp_zhu],
        2000: [10e-3, None, val_tmp_zhu],
        2300: [10e-3, None, val_tmp_zhu],
        2600: [10e-3, None, val_tmp_zhu]}

    c_imp_bei = ImpedanceMultiFreq()
    c_imp_bei.rlc_s = {
        1700: [10e-3, None, val_tmp_bei],
        2000: [10e-3, None, val_tmp_bei],
        2300: [10e-3, None, val_tmp_bei],
        2600: [10e-3, None, val_tmp_bei]}

    para['主串容值列表'] = [c_imp_zhu]
    para['被串容值列表'] = [c_imp_bei]

    # 道床电阻
    data['主串道床电阻(Ω·km)'] = df_input['主串道床电阻(Ω·km)']
    data['被串道床电阻(Ω·km)'] = df_input['被串道床电阻(Ω·km)']

    para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
    para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])

    para['Rd'].value = df_input['主串道床电阻(Ω·km)']

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
    para['cab_len'] = 4
    data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)']
    data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)']

    # 分路电阻
    # 分路电阻

    data['分路模式'] = mode = df_input['分路模式']

    r_sht = df_input['分路电阻(Ω)']
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

    # data['主串分路电阻(Ω)'] = para['主串分路电阻'] = df_input['分路电阻(Ω)']
    # data['被串分路电阻(Ω)'] = para['被串分路电阻'] = df_input['分路电阻(Ω)']
    #
    # para['Rsht_z'] = df_input['分路电阻(Ω)']

    # 功出电源
    data['主串电平级'] = para['send_level'] = df_input['主串电平级']
    data['电源电压'] = para['pwr_v_flg'] = df_input['主串电源电压']

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
    data['分路间隔(m)'] = df_input['分路间隔(m)']

    if data['主串区段'] == 'IG' and data['被串区段'] == 'IIG':
        data['分路起点'] = offset
        data['分路终点'] = offset + length2
    elif data['主串区段'] == 'IIG' and data['被串区段'] == 'IG':
        data['分路起点'] = 0
        data['分路终点'] = 0 + length1
    else:
        raise KeyboardInterrupt('区段错误')

    # data['分路起点'] = offset
    # data['分路终点'] = offset + length2

    # TB模式
    data['主串TB模式'] = para['主串TB模式'] = '无TB'
    data['被串TB模式'] = para['被串TB模式'] = '无TB'

    #################################################################################

    # 站内数字化配置

    data['扼流变比'] = para['变压器变比'] = n = 10

    if n == 10:
        para['EL_0425_发送_zs'] = ImpedanceMultiFreq()
        para['EL_0425_发送_zs'].rlc_s = {
            1700: [1.74, 954.3e-6, None],
            2000: [1.84, 949.0e-6, None],
            2300: [1.94, 944.8e-6, None],
            2600: [2.04, 941.4e-6, None]}

        para['EL_0425_发送_zm'] = ImpedanceMultiFreq()
        para['EL_0425_发送_zm'].rlc_s = {
            1700: [30.46, 37.02e-3, None],
            2000: [44.32, 37.47e-3, None],
            2300: [58.35, 38.02e-3, None],
            2600: [75.18, 38.72e-3, None]}
        para['EL_0425_n'] = {
            1700: n,
            2000: n,
            2300: n,
            2600: n}

    else:
        raise KeyboardInterrupt('参数错误：扼流变比n固定为10')

    freq = data['主串频率(Hz)']
    data['扼流_Rs(Ω)'] = round(para['EL_0425_发送_zs'][freq].rlc_s[0], 3)
    data['扼流_Ls(μH)'] = round(para['EL_0425_发送_zs'][freq].rlc_s[1] * 1e6, 3)
    data['扼流_Rm(Ω)'] = round(para['EL_0425_发送_zm'][freq].rlc_s[0], 3)
    data['扼流_Lm(mH)'] = round(para['EL_0425_发送_zm'][freq].rlc_s[1] * 1e3, 3)

    # 隔直电容
    data['隔直电容(μf)'] = 0.6
    para['c_isolation'] = ImpedanceMultiFreq()
    para['c_isolation'].rlc_s = {
        1700: [0.17396, None, 597.60 * 1e-9],
        2000: [0.17853, None, 597.86 * 1e-9],
        2300: [0.22246, None, 598.29 * 1e-9],
        2600: [0.47802, None, 598.01 * 1e-9]}


class PreModel_20240618_ZN_Dalong_Digital(PreModel):
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
                           j_lens=[0, 0],
                           m_typs=['2000A_ZN_Digital_Double_Sending'],
                           c_nums=para['主串电容数'],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        freq_tmp = Freq(para['freq_被'])
        freq_tmp.change_freq()

        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[0, 0],
                           m_typs=['2000A_ZN_Digital_Double_Sending'],
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        # sg3['区段1'].load_TB_mode(para['主串TB模式'])
        # sg4['区段1'].load_TB_mode(para['被串TB模式'])
        # sg3.refresh()
        # sg4.refresh()

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()

        # self.change_para_el()
        self.change_cable_length()
        self.change_r_shunt()
        self.change_ele_position()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

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

    def change_cable_length(self):
        para = self.parameter

        if para['主串电缆长度'] is not None:
            for ele in self.section_group3['区段1'].element.values():
                if isinstance(ele, ZPW2000A_ZN_Digital):
                    ele_cab = ele['2Cab']
                    ele_cab.length = para['主串电缆长度']

        if para['被串电缆长度'] is not None:
            for ele in self.section_group4['区段1'].element.values():
                if isinstance(ele, ZPW2000A_ZN_Digital):
                    ele_cab = ele['2Cab']
                    ele_cab.length = para['被串电缆长度']

    def change_r_shunt(self):
        para = self.parameter
        self.train2['分路电阻1'].z = para['主串分路电阻']
        self.train1['分路电阻1'].z = para['被串分路电阻']

    def change_ele_position(self):
        para = self.parameter

        info1 = para['主串电容分布']
        info2 = para['被串电容分布']

        res_zhu = self.get_ele_position(*info1)
        res_bei = self.get_ele_position(*info2)

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_Middle):
                ele.default_position = res_zhu[0]

            if isinstance(ele, CapC):
                index = int(ele.name_base[1:]) - 1
                ele.init_position(res_zhu[1][index])

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_Middle):
                ele.default_position = res_bei[0]

            if isinstance(ele, CapC):
                index = int(ele.name_base[1:]) - 1
                ele.init_position(res_bei[1][index])

        self.section_group3.refresh()
        self.section_group4.refresh()

    @staticmethod
    def get_ele_position(length1, length2, c_num1, c_num2):
        rcv_position = length1
        interval1 = length1 / c_num1
        interval2 = length2 / c_num2
        c_list = []
        posi = 0
        for i in range(c_num1):
            if i == 0:
                posi += interval1 / 2
            else:
                posi += interval1
            c_list.append(posi)

        posi = length1
        for i in range(c_num2):
            if i == 0:
                posi += interval2 / 2
            else:
                posi += interval2
            c_list.append(posi)

        return rcv_position, c_list


def draw_image_20240618_dalong_digital():
    # plt.rcParams['font.size'] = 20

    # 根目录
    root = 'C:\\Users\\李继隆\\PycharmProjects\\Calculator_ZN_mix\\20240618_大龙村站内数字化\\图表汇总'

    # 创建文件夹
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '%s\\图表汇总_%s' % (root, timestamp)

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    # 读取数据

    path1 = '%s\\%s' % (root, '仿真输出_大龙村站内数字化_邻线干扰计算.xlsx')

    df_data1 = pd.read_excel(path1, '数据输出')
    MainLog.add_log_accurate('#' * 30)

    # df_data2 = pd.read_excel(path2, '数据输出')
    # df_i_trk_1 = pd.read_excel(path1, '被串钢轨电流')
    df_i_trk_1 = pd.read_excel(path1, '被串分路电流')
    MainLog.add_log_accurate('#' * 30)

    # df_i_trk_2 = pd.read_excel(path2, '被串钢轨电流')
    # MainLog.add_log_accurate('#' * 30)

    # length = df_data1.shape[1]
    # xx1 = list(range(length))

    # sec_length_list = [400, 600, 800, 1200]

    direction_list = [
        ['左发', '左发'],
        ['左发', '右发'],
        ['右发', '左发'],
        ['右发', '右发'],
    ]

    condition_list = [
        ['IG', 'IIG'],
        ['IIG', 'IG'],
        ['3G', 'IIG'],
        ['IIG', '3G'],
    ]

    sht_type_list = [
        '主串调整被串分路',
        '主被串同时分路',
    ]

    for condition in condition_list:
        sec_zhu = condition[0]
        sec_bei = condition[1]

        # 创建图表
        fig = plt.figure(figsize=(16, 8), dpi=100)
        # fig.subplots_adjust(hspace=0.4, wspace=0.1, top=0.8, left=0.15, right=0.85)
        fig.subplots_adjust(hspace=0.3, wspace=0.1, top=0.87, left=0.15, right=0.85)
        # fig.subplots_adjust(hspace=0.4)
        title = '%s(主串)对%s(被串)邻线干扰' % (sec_zhu, sec_bei)
        fig.suptitle(title, x=0.5, y=0.98, fontsize=25, fontfamily='SimHei')

        ax_list = []

        for j, dir_tup in enumerate(direction_list):
            dir_zhu = dir_tup[0]
            dir_bei = dir_tup[1]

            ax = fig.add_subplot(2, 2, j + 1)
            ax_list.append(ax)

            # sub_title = '主串方向:%s/被串方向:%s' % (dir_zhu, dir_bei)
            # ax.set_title(sub_title, pad=8, fontsize=12)

            # 纵坐标
            # ax.yaxis.grid(True, which='major')
            y_ticks = [0, 50, 100, 150, 200, 250]
            y_label = map(lambda x: r'$\mathrm{%.0f}$' % x, y_ticks)

            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_label)

            # ax.yaxis.set_font(20)
            ax.set_ylim([0, 300])

            # 横坐标

            # x_ticks = list(range(0, sec_length, 100))
            # x_label = map(lambda x: r'$\mathrm{%.0f}$' % x, x_ticks)
            #
            # ax.set_xticks(x_ticks)
            # ax.set_xticklabels(x_label)

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

            max_value = 0
            # max_index = None

            sec_length = 0

            for i, sht_type in enumerate(sht_type_list):

                row = df_data1.loc[
                    (df_data1["分路模式"] == sht_type) &
                    (df_data1["主串区段"] == sec_zhu) &
                    (df_data1["被串区段"] == sec_bei) &
                    (df_data1["主串方向"] == dir_zhu) &
                    (df_data1["被串方向"] == dir_bei)
                ]

                index = row['序号'].tolist()
                freq_zhu = row['主串频率(Hz)'].tolist()[0]

                tmp_dict = {
                    '左发': '向左',
                    '右发': '向右',
                }
                tmp_dir = tmp_dict[dir_bei]

                sub_title = '主串:80V/%s(Hz) 被串%s行驶' % (freq_zhu, tmp_dir)
                ax.set_title(sub_title, pad=8, fontsize=12)

                if len(index) == 1:
                    index = index[0] - 1
                else:
                    raise KeyboardInterrupt('error: len(index) != 1')

                yy1 = (df_i_trk_1.iloc[index, :].copy().dropna()*1000).tolist()

                sec_length = len(yy1)
                xx1 = range(sec_length)

                value = max(yy1)
                if value > max_value:
                    max_value = value
                    # max_index = index

                color_list = [
                    'red',
                    'blue',
                ]

                # color = cm.rainbow(i / len(offset_list))
                color = color_list[i]

                # ax.plot(xx1, yy1, linestyle='-', alpha=0.8, color=color, label='%sHz' % freq_zhu)
                ax.plot(xx1, yy1, linestyle='-', alpha=0.8, color=color, label='%s' % sht_type)

                # ax.legend(loc='upper right', fontsize=9)

                x_ticks = list(range(0, sec_length, 100))
                x_label = map(lambda x: r'$\mathrm{%.0f}$' % x, x_ticks)
                x_label = list(x_label)
                # x_label[0] = '被串接收'

                ax.set_xticks(x_ticks)
                ax.set_xticklabels(x_label)

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

            # # 箭头
            # s_tmp = df_data1.iloc[max_index, :]
            # arrow_x = s_tmp["被串最大干扰位置(m)"]
            # arrow_y = s_tmp["被串最大干扰电流(A)"] * 1000
            # offset_tmp = s_tmp["被串相对位置(m)"]
            #
            # txt = '最大干扰电流$\mathrm{%.2fmA}$\n主被串错位$\mathrm{%.0fm}$' % (arrow_y, offset_tmp)
            #
            # txt_y = 300 if arrow_y > 300 else arrow_y
            # txt_x = 50 if arrow_x < 50 else arrow_x
            # ax.annotate(
            #     txt, (arrow_x, arrow_y),
            #     xytext=(txt_x + 100, txt_y + 50),
            #     ha="center", va="center",
            #     # textcoords='offset points',
            #     fontsize=10,
            #     color='blue',
            #     arrowprops=dict(
            #         # facecolor='#74C476',
            #         alpha=0.6,
            #         arrowstyle='fancy',
            #         # connectionstyle='arc3,rad=0.5',
            #         color='blue',
            #     )
            # )

        plt.text(
            0.5, 0.07, '被串分路位置$\mathrm{(m)}$',
            va='top', ha='center', transform=fig.transFigure,
            fontsize=13,
        )

        # plt.text(
        #     0.12, 0.5, '邻线干扰电流$\mathrm{(mA)}$',
        #     va='center', ha='right', transform=fig.transFigure,
        #     fontsize=13, rotation=90,
        # )

        plt.text(
            0.12, 0.5, '邻线干扰分路线电流$\mathrm{(mA)}$',
            va='center', ha='right', transform=fig.transFigure,
            fontsize=13, rotation=90,
        )

        handles, labels = ax_list[0].get_legend_handles_labels()
        plt.legend(
            handles, labels,
            loc='center right',
            # ncol=3,
            bbox_to_anchor=(1.36, 1.2),
            fontsize=11,
        )

        # plt.show()
        # raise KeyboardInterrupt()

        filename1 = '%s\\大龙村站内数字化_主串%s_被串%s_分路线电流.png' % (res_dir, sec_zhu, sec_bei)
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
    draw_image_20240618_dalong_digital()
