from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant
from src.FrequencyType import Freq

from src.Module.OutsideElement import CapC
from src.Module.TcsrLib import ZPW2000A_ZN_Digital_adj

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line

from src.Model.PreModel import PreModel

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False


def config_input_20251027_digital_iterate():
    columns = [
        '序号',
        '备注',
        '主串区段',
        '被串区段',

        '主串方向',
        '被串方向',

        '主串频率(Hz)',
        '被串频率(Hz)',

        '耦合系数(μH/km)',
        '被串相对位置(m)',

        '主串区段长度(m)',
        '被串区段长度(m)',

        '主串电容数(含TB)',
        '被串电容数(含TB)',

        '主串电容值(μF)',
        '被串电容值(μF)',

        '主串电缆长度(km)',
        '被串电缆长度(km)',

        # '钢轨电阻(Ω/km)',
        # '钢轨电感(H/km)',

        '主串道床电阻(Ω·km)',
        '被串道床电阻(Ω·km)',

        '主串分路电阻(Ω)',
        '被串分路电阻(Ω)',

        '分路模式',
        '分路间隔(m)',

        '主串电平级',
        '主串电源电压',

        '扼流变比',
    ]

    df = pd.DataFrame(index=columns, dtype='object')

    counter = 1

    cnd_list1 = [1700, 2000, 2300, 2600]
    cnd_list2 = [25, 50]

    for freq in cnd_list1:
        for c_cmp in cnd_list2:
            s0 = pd.Series(name=counter, index=columns)

            s0['序号'] = s0.name
            s0['备注'] = '车站数字化_两送一受遍历'
            s0['主串区段'] = 'IG'
            s0['被串区段'] = 'IIG'

            s0['主串区段长度(m)'] = 1050
            s0['被串区段长度(m)'] = 1050

            s0['被串相对位置(m)'] = 0

            s0['耦合系数(μH/km)'] = 19.6

            s0['主串频率(Hz)'] = freq
            s0['被串频率(Hz)'] = freq

            s0['主串电容数(含TB)'] = 12
            s0['被串电容数(含TB)'] = 12

            s0['主串电容值(μF)'] = c_cmp
            s0['被串电容值(μF)'] = c_cmp

            s0['主串道床电阻(Ω·km)'] = 10000
            s0['被串道床电阻(Ω·km)'] = 10000

            s0['主串方向'] = '双端'
            s0['被串方向'] = '双端'

            s0['主串电缆长度(km)'] = 4
            s0['被串电缆长度(km)'] = 4

            s0['分路模式'] = '主被串同时分路'
            s0['主串分路电阻(Ω)'] = 1e-7
            s0['被串分路电阻(Ω)'] = 1e-7

            s0['主串电平级'] = 6
            s0['主串电源电压'] = 140

            s0['分路间隔(m)'] = 1
            s0['扼流变比'] = 10

            print('generate row: %s --> %s' % (counter, s0.tolist()))

            df = pd.concat([df, s0], axis=1, sort=False)
            counter += 1

            # if counter > 1:
            #     df = df.transpose()
            #     return df

    df = df.transpose()
    print(df)
    return df


# 配置表头
def config_headlist_20251027_digital_iterate():
    head_list = [
        '序号',
        '备注',
        '主串区段',
        '被串区段',

        '主串方向',
        '被串方向',

        '主串频率(Hz)',
        '被串频率(Hz)',

        '耦合系数(μH/km)',

        '被串相对位置(m)',

        '主串区段长度(m)',
        '被串区段长度(m)',

        '主串电容数(含TB)',
        '被串电容数(含TB)',

        '主串电容值(μF)',
        '被串电容值(μF)',

        '主串电缆长度(km)',
        '被串电缆长度(km)',

        '钢轨电阻(Ω/km)',
        '钢轨电感(H/km)',

        '主串道床电阻(Ω·km)',
        '被串道床电阻(Ω·km)',

        '主串分路电阻(Ω)',
        '被串分路电阻(Ω)',

        '分路模式',
        '分路间隔(m)',

        '主串电平级',
        '主串电源电压',

        '扼流变比',
        # '扼流_Rs(Ω)',
        # '扼流_Ls(μH)',
        # '扼流_Rm(Ω)',
        # '扼流_Lm(mH)',
        # '隔直电容(μf)',

        '被串最大干扰电流(A)',
        '被串最大干扰位置(m)',
    ]

    return head_list


# 配置行数据
def config_row_data_20251027_digital_iterate(df_input, para, data):
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

    # para['主串电容分布'] = df_input['主串电容分布']
    # para['被串电容分布'] = df_input['被串电容分布']

    # data['主串接收位置(m)'] = para['主串电容分布'][0]
    # data['被串接收位置(m)'] = para['被串电容分布'][0]

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
    # r_trk = df_input['钢轨电阻(Ω/km)']
    # l_trk = df_input['钢轨电感(H/km)']

    trk_z = ImpedanceMultiFreq()
    trk_z.rlc_s = {
        1700: [1.177, 1.314e-3, None],
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}

    data['钢轨电阻(Ω/km)'] = round(trk_z.rlc_s[freq][0], 10)
    data['钢轨电感(H/km)'] = round(trk_z.rlc_s[freq][1], 10)

    # if r_trk is not None and l_trk is not None:
    #     trk_z.rlc_s = {
    #         1700: [r_trk, l_trk, None],
    #         2000: [r_trk, l_trk, None],
    #         2300: [r_trk, l_trk, None],
    #         2600: [r_trk, l_trk, None]}
    #
    #     data['钢轨电阻(Ω/km)'] = r_trk
    #     data['钢轨电感(H/km)'] = l_trk

    para['Trk_z'] = trk_z
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

    # 1Ω标准电阻
    para['unit_1'] = ImpedanceMultiFreq()
    para['unit_1'].rlc_s = {
        1700: [1, None, None],
        2000: [1, None, None],
        2300: [1, None, None],
        2600: [1, None, None]}

    # 电缆长度
    para['cab_len'] = 4
    para['cab_len_default'] = 0

    data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)']
    data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)']

    # 分路电阻
    data['分路模式'] = df_input['分路模式']

    data['主串分路电阻(Ω)'] = para['主串分路电阻'] = df_input['主串分路电阻(Ω)']
    data['被串分路电阻(Ω)'] = para['被串分路电阻'] = df_input['被串分路电阻(Ω)']

    para['Rsht_z'] = 1e-7

    # data['主串分路电阻(Ω)'] = para['主串分路电阻'] = df_input['分路电阻(Ω)']
    # data['被串分路电阻(Ω)'] = para['被串分路电阻'] = df_input['分路电阻(Ω)']
    #
    # para['Rsht_z'] = df_input['分路电阻(Ω)']

    # 功出电源
    data['主串电平级'] = para['send_level'] = df_input['主串电平级']
    data['主串电源电压'] = para['pwr_v_flg'] = df_input['主串电源电压']

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

    # # TB模式
    # data['主串TB模式'] = para['主串TB模式'] = '无TB'
    # data['被串TB模式'] = para['被串TB模式'] = '无TB'

    #################################################################################

    # 站内数字化配置

    # 发送器
    z_pwr = ImpedanceMultiFreq()
    z_pwr.z = {
        1700: (5.80 + 6.50j),
        2000: (5.70 + 7.55j),
        2300: (5.85 + 8.64j),
        2600: (6.00 + 9.65j),
    }

    para['z_pwr_车站数字化'] = dict()
    for i in range(1, 11, 1):
        para['z_pwr_车站数字化'][i] = z_pwr

    # 接收端
    z_rcv1 = ImpedanceMultiFreq()
    z_rcv1.rlc_s = {
        1700: (23e3, None, None),
        2000: (23e3, None, None),
        2300: (23e3, None, None),
        2600: (23e3, None, None)}

    z_rcv2 = ImpedanceMultiFreq()
    z_rcv2.rlc_s = {
        1700: (1.21, 3.3e-3, None),
        2000: (1.21, 3.3e-3, None),
        2300: (1.21, 3.3e-3, None),
        2600: (1.21, 3.3e-3, None)}

    para['z_rcv_车站数字化'] = z_rcv1 // z_rcv2

    # 防雷变压器
    para['FL_z1_车站数字化'] = ImpedanceMultiFreq()
    para['FL_z1_车站数字化'].rlc_s = {
        1700: [4.79, 1.22e-3, None],
        2000: [4.83, 1.22e-3, None],
        2300: [4.88, 1.22e-3, None],
        2600: [4.93, 1.22e-3, None]}

    para['FL_z2_车站数字化'] = ImpedanceMultiFreq()
    para['FL_z2_车站数字化'].rlc_s = {
        1700: [3110, 361.02e-3, None],
        2000: [3560, 323.73e-3, None],
        2300: [3920, 296.38e-3, None],
        2600: [4240, 275.18e-3, None]}
    # n = 1/1.095
    n = 1/1.04
    para['FL_n_车站数字化'] = {
        1700: n,
        2000: n,
        2300: n,
        2600: n}

    # 隔直电容
    data['隔直电容(μf)'] = 0.6
    para['c_isolation'] = ImpedanceMultiFreq()
    para['c_isolation'].rlc_s = {
        1700: [0.17396, None, 597.60 * 1e-9],
        2000: [0.17853, None, 597.86 * 1e-9],
        2300: [0.22246, None, 598.29 * 1e-9],
        2600: [0.47802, None, 598.01 * 1e-9]}

    # 扼流变压器
    data['扼流变比'] = para['变压器变比'] = n = df_input['扼流变比']

    if n == 10:
        para['EL_0425_发送_zs'] = ImpedanceMultiFreq()
        para['EL_0425_发送_zs'].rlc_s = {
            1700: [3.744, 0.994e-3, None],
            2000: [3.862, 0.986e-3, None],
            2300: [3.980, 0.980e-3, None],
            2600: [4.099, 0.975e-3, None]}

        para['EL_0425_发送_zm'] = ImpedanceMultiFreq()
        para['EL_0425_发送_zm'].rlc_s = {
            1700: [34.26, 38.35e-3, None],
            2000: [46.35, 38.97e-3, None],
            2300: [61.11, 39.77e-3, None],
            2600: [79.37, 40.77e-3, None]}
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

    # 引接线
    para['z_CA_车站数字化'] = ImpedanceMultiFreq()
    para['z_CA_车站数字化'].rlc_s = {
        1700: [10.35e-3, 4.68e-6, None],
        2000: [11.71e-3, 4.49e-6, None],
        2300: [13.01e-3, 4.40e-6, None],
        2600: [14.55e-3, 4.59e-6, None],
    }


class PreModel_20251027_digital_iterate(PreModel):
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
                           m_typs=['2000A_ZN_Digital_adj_2_1'],
                           c_nums=para['主串电容数'],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '双端':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        # freq_tmp = Freq(para['freq_被'])
        # freq_tmp.change_freq()

        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[0, 0],
                           m_typs=['2000A_ZN_Digital_adj_2_1'],
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
        self.change_cable_length()
        self.change_r_shunt()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

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

    def change_cable_length(self):
        para = self.parameter
        z_unit = para['unit_1'] * para['Cable_R'].value

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_adj):
                ele['2补偿电缆'].z = 3.75 * z_unit
                ele['4实际电缆'].length = 0

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_adj):
                ele['2补偿电缆'].z = 3.75 * z_unit
                ele['4实际电缆'].length = 0

    def change_r_shunt(self):
        para = self.parameter
        self.train2['分路电阻1'].z = para['主串分路电阻']
        self.train1['分路电阻1'].z = para['被串分路电阻']


if __name__ == '__main__':
    pass
