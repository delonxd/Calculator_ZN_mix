
from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant
from src.FrequencyType import Freq

from src.Module.OutsideElement import CapC

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line
from src.Model.PreModel import PreModel

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


def config_input_20260313_daqin_2000a():

    columns = [
        '序号',
        '备注',
        '主串区段',
        '被串区段',
        '主串类型',
        '被串类型',
        '主串方向',
        '被串方向',
        '主串区段长度(m)',
        '被串区段长度(m)',
        '被串相对位置(m)',
        '耦合系数(μH/km)',
        '主串电平级',
        '主串频率(Hz)',
        '被串频率(Hz)',
        '主串电缆长度(km)',
        '被串电缆长度(km)',
        '主串电容数(含TB)',
        '被串电容数(含TB)',

        '主串电容值(μF)',
        '被串电容值(μF)',

        '主串道床电阻(Ω·km)',
        '被串道床电阻(Ω·km)',
        '分路模式',
        '分路间隔(m)',
        '分路电阻(Ω)',
        '主串TB模式',
        '被串TB模式',
    ]

    df = pd.DataFrame(index=columns, dtype='object')
    # [名称, 类型, 长度, 相对位置, 频率, 电容数, 电容值]
    sec_list = [
        ['IG', 'BPLN', 856, 0, 2000, 9, 50],
        ['IIG', 'PT', 826, 0, 2600, 9, 50],
    ]

    direction_list = [
        ['左发', '左发'],
        ['左发', '右发'],
        ['右发', '左发'],
        ['右发', '右发'],
    ]

    condition_list = [
        ['主串调整被串分路', '是'],
        # ['主串调整被串分路', '否'],
        ['主被串同时分路', '是'],
        # ['主被串同时分路', '否'],
    ]

    counter = 1

    pick_sec = [
        [0, 1],
        [1, 0],
    ]

    for val in pick_sec:
        sec_zhu = sec_list[val[0]]
        sec_bei = sec_list[val[1]]

        for dir_zhu, dir_bei in direction_list:
            for condition in condition_list:

                s0 = pd.Series(name=counter, index=columns)

                s0['序号'] = s0.name
                s0['备注'] = ''
                s0['主串区段'] = sec_zhu[0]
                s0['被串区段'] = sec_bei[0]
                s0['主串类型'] = sec_zhu[1]
                s0['被串类型'] = sec_bei[1]
                s0['主串方向'] = dir_zhu
                s0['被串方向'] = dir_bei
                s0['主串区段长度(m)'] = sec_zhu[2]
                s0['被串区段长度(m)'] = sec_bei[2]
                s0['被串相对位置(m)'] = sec_bei[3] - sec_zhu[3]
                s0['耦合系数(μH/km)'] = 20
                s0['主串电平级'] = 3
                s0['主串频率(Hz)'] = sec_zhu[4]
                s0['被串频率(Hz)'] = sec_bei[4]
                s0['主串电缆长度(km)'] = 10
                s0['被串电缆长度(km)'] = 10
                s0['主串电容数(含TB)'] = sec_zhu[5]
                s0['被串电容数(含TB)'] = sec_bei[5]
                s0['主串电容值(μF)'] = sec_zhu[6]
                s0['被串电容值(μF)'] = sec_bei[6]
                s0['主串道床电阻(Ω·km)'] = 10000
                s0['被串道床电阻(Ω·km)'] = 10000
                s0['分路模式'] = condition[0]
                s0['分路间隔(m)'] = 1
                s0['分路电阻(Ω)'] = 1e-7
                s0['主串TB模式'] = '无TB'
                s0['被串TB模式'] = '无TB'
                print('generate row: %s --> %s' % (counter, s0.tolist()))

                df = pd.concat([df, s0], axis=1)
                counter += 1

    df = df.transpose()

    return df


# 配置表头
def config_headlist_20260313_daqin_2000a():
    head_list = [
        '序号',
        '备注',
        # '线路名称', '车站名称',

        '主串区段', '被串区段',
        '主串类型', '被串类型',

        # '线间距(m)',
        # '并行长度(m)',

        '主串方向', '被串方向',

        # '调谐区错位(m)',
        '主串区段长度(m)', '被串区段长度(m)',
        '被串相对位置(m)',
        '耦合系数(μH/km)',

        # '主串左端坐标', '被串左端坐标',

        # '主串区段类型', '被串区段类型',
        '主串频率(Hz)', '被串频率(Hz)',

        # '主串电容数量列表', '被串电容数量列表',
        # '主串电容容值列表', '被串电容容值列表',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '主串电缆长度(km)', '被串电缆长度(km)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',

        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        '主串TB模式', '被串TB模式',

        '分路模式',
        '主串分路电阻(Ω)', '被串分路电阻(Ω)',

        '分路间隔(m)',

        '主串电平级',
        '电源电压',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        # '故障位置', '故障类型',
        # '干扰值变化',
    ]

    return head_list


# 配置行数据
def config_row_data_20260313_daqin_2000a(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = df_input['备注']

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']
    data['主串类型'] = para['主串类型'] = df_input['主串类型']
    data['被串类型'] = para['被串类型'] = df_input['被串类型']

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['主串区段长度(m)']
    length2 = data['被串区段长度(m)'] = df_input['被串区段长度(m)']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = [length2]

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
    data['主串电容值(μF)'] = c_value_zhu = df_input['主串电容值(μF)']
    data['被串电容值(μF)'] = c_value_bei = df_input['被串电容值(μF)']

    val_tmp = c_value_zhu * 1e-6
    c_imp = ImpedanceMultiFreq()
    c_imp.rlc_s = {
        1700: [10e-3, None, val_tmp],
        2000: [10e-3, None, val_tmp],
        2300: [10e-3, None, val_tmp],
        2600: [10e-3, None, val_tmp]}

    para['主串容值列表'] = [c_imp]

    val_tmp = c_value_bei * 1e-6
    c_imp = ImpedanceMultiFreq()
    c_imp.rlc_s = {
        1700: [10e-3, None, val_tmp],
        2000: [10e-3, None, val_tmp],
        2300: [10e-3, None, val_tmp],
        2600: [10e-3, None, val_tmp]}

    para['被串容值列表'] = [c_imp]

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
    para['cab_len'] = 10
    data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)']
    data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)']

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

    para['Rsht_z'] = df_input['分路电阻(Ω)']

    # 功出电源
    data['主串电平级'] = para['send_level'] = df_input['主串电平级']
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
    data['分路间隔(m)'] = df_input['分路间隔(m)']
    data['分路起点'] = offset
    data['分路终点'] = offset + length2

    # TB模式
    data['主串TB模式'] = para['主串TB模式'] = df_input['主串TB模式']
    data['被串TB模式'] = para['被串TB模式'] = df_input['被串TB模式']


class PreModel_20260313_ZN_daqin_2000a(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        self.train1['分路电阻1'].z = para['被串分路电阻']
        self.train2['分路电阻1'].z = para['主串分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        m_typs = self.get_m_typs(para['主串类型'])
        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=para['主串频率列表'],
                           m_lens=para['主串区段长度'],
                           j_lens=[0, 0],
                           m_typs=[m_typs],
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

        m_typs = self.get_m_typs(para['被串类型'])
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[0, 0],
                           m_typs=[m_typs],
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        sg3['区段1'].load_TB_mode(para['主串TB模式'])
        sg4['区段1'].load_TB_mode(para['被串TB模式'])
        sg3.refresh()
        sg4.refresh()

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


if __name__ == '__main__':
    pass
