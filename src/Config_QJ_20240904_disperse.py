from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq
from src.Model.PreModel import PreModel
from src.logMethod import *
from src.Data2Excel import *

import os
import time
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False


# 区间分散式轨道电路
# 配置输入
def config_input_20240904_disperse(cycle_para):
    columns = [
        '序号',
        '备注',
        '主串区段', '被串区段',
        '主串方向', '被串方向',

        '主串区段长度(m)', '被串区段长度(m)',

        '被串相对位置(m)',
        '耦合系数(μH/km)',

        '主串电平级',
        '主串频率(Hz)', '被串频率(Hz)',

        '主串电容数', '被串电容数',
        '主串电容值(μF)', '被串电容值(μF)',

        '补偿电阻(Ω)',
        '匹配变压器变比',

        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',

        '分路间隔(m)',
        '分路电阻(Ω)',
    ]

    # list1 = [
    #     25,
    #     50,
    # ]
    #
    # list2 = [1700, 2000, 2300, 2600]
    # list3 = [1700, 2000, 2300, 2600]

    list4 = [14, 18, 20, 24]
    list5 = list(range(50, 451, 50))
    list5.append(180)

    # list6 = list(range(5, 16, 1))
    list6 = [10]

    iter_list = list(itertools.product(
        list4, list5, list6))

    df = pd.DataFrame(index=columns, dtype='object')

    c_value, freq_zhu, freq_bei = cycle_para

    counter = 0
    for c_num, r_cable, n_tad in iter_list:
        counter += 1

        s0 = pd.Series(name=counter, index=columns)

        s0['序号'] = s0.name
        s0['备注'] = '分散式-主被串同时分路'

        s0['主串区段'] = 'IG'
        s0['被串区段'] = 'IIG'

        s0['主串方向'] = '右发'
        s0['被串方向'] = '右发'

        s0['主串区段长度(m)'] = 1400
        s0['被串区段长度(m)'] = 1400

        s0['被串相对位置(m)'] = 0
        s0['耦合系数(μH/km)'] = 20

        s0['主串电平级'] = 6

        s0['主串频率(Hz)'] = freq_zhu
        s0['被串频率(Hz)'] = freq_bei

        s0['主串电容数'] = c_num
        s0['被串电容数'] = c_num

        s0['主串电容值(μF)'] = c_value
        s0['被串电容值(μF)'] = c_value

        s0['补偿电阻(Ω)'] = r_cable
        s0['匹配变压器变比'] = n_tad

        s0['主串道床电阻(Ω·km)'] = 10000
        s0['被串道床电阻(Ω·km)'] = 10000

        s0['分路间隔(m)'] = 1
        s0['分路电阻(Ω)'] = 1e-7

        print('generate row: %s --> %s' % (counter, s0.tolist()))

        df = pd.concat([df, s0], axis=1)

        # if counter == 1:
        #     return df.transpose()

    df = df.transpose()
    return df


# 配置表头
def config_headlist_20240904_disperse():
    head_list = [
        '序号',
        '备注',
        # '线路名称', '车站名称',
        # '主串区段', '被串区段',

        # '线间距(m)',
        '耦合系数(μH/km)',

        '主串方向', '被串方向',

        # '调谐区错位(m)',
        '被串相对位置(m)',

        '主串区段长度(m)', '被串区段长度(m)',
        '主串频率(Hz)', '被串频率(Hz)',

        # '主串电容数量列表', '被串电容数量列表',
        # '主串电容容值列表', '被串电容容值列表',

        '主串电容数', '被串电容数',
        '主串电容值(μF)', '被串电容值(μF)',

        '补偿电阻(Ω)',
        '匹配变压器变比',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串分路电阻(Ω)', '被串分路电阻(Ω)',
        # '主串电缆长度(km)', '被串电缆长度(km)',

        '分路间隔(m)',

        '主串电平级',
        '电源电压',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        # '故障位置', '故障类型',
        # '干扰值变化',
    ]

    return head_list


def config_c_num_high_speed(freq: Freq, length):
    freq_value = freq.value

    if 0 < length <= 300:
        key = 0
    elif length > 300:
        key = int((length - 251) / 50)
    else:
        raise KeyboardInterrupt('config_c_num error: 区段长度错误')

    table = {
        0: [0, 0, 0, 0],
        1: [5, 5, 4, 4],
        2: [6, 6, 5, 5],
        3: [7, 7, 5, 5],
        4: [8, 8, 6, 6],
        5: [9, 9, 7, 7],
        6: [10, 10, 7, 7],
        7: [10, 10, 8, 8],
        8: [11, 11, 8, 8],
        9: [12, 12, 9, 9],
        10: [13, 13, 10, 10],
        11: [14, 14, 10, 10],
        12: [15, 15, 11, 11],
        13: [15, 15, 12, 12],
        14: [16, 16, 12, 12],
        15: [17, 17, 13, 13],
        16: [18, 18, 13, 13],
        17: [19, 19, 14, 14],
        18: [20, 20, 15, 15],
        19: [20, 20, 15, 15],
        20: [21, 21, 16, 16],
        21: [22, 22, 17, 17],
        22: [23, 23, 17, 17],
    }
    if key not in table.keys():
        raise KeyboardInterrupt('config_c_num error: 区段长度超长')

    index_dict = {
        1700: 0,
        2000: 1,
        2300: 2,
        2600: 3,
    }

    if freq_value not in index_dict.keys():
        raise KeyboardInterrupt('config_c_num error: 区段频率错误')

    c_num = table[key][index_dict[freq_value]]
    return c_num


def config_c_pack_20240904_disperse(freq_list, length_list, c_value_src):
    if len(freq_list) != len(length_list):
        raise KeyboardInterrupt('config_c_list_20230720_pusu error: 列表长度不等')

    c_num_list = []
    c_imp_list = []
    c_val_list = []

    for index in range(len(freq_list)):
        freq = freq_list[index]
        length = length_list[index]
        c_val = c_value_src[index]

        c_num = config_c_num_high_speed(freq, length)

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
def config_row_data_20240904_disperse(df_input, para, data):

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
    para['被串区段长度'] = [length2, length2, length2]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset - 1400

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = df_input['耦合系数(μH/km)']

    # 区段频率
    para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率(Hz)']
    para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率(Hz)']
    freq = freq1
    data['freq'] = para['freq'] = Freq(freq1)
    para['主串频率列表'] = [Freq(freq1)]
    para['被串频率列表'] = generate_frqs(Freq(freq2), 3, flip_flag=True)

    # 电容配置

    c_value1 = df_input['主串电容值(μF)']
    c_value2 = df_input['被串电容值(μF)']
    c_pack_zhu = config_c_pack_20240904_disperse(para['主串频率列表'], para['主串区段长度'], [c_value1])
    c_pack_bei = config_c_pack_20240904_disperse(para['被串频率列表'], para['被串区段长度'], [c_value2, c_value2, c_value2])

    # 电容数量
    # data['主串电容数量列表'] = para['主串电容数'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = para['被串电容数'] = c_pack_bei['电容数量列表']

    # c_num1 = df_input['主串电容数(含TB)']
    # c_num2 = df_input['被串电容数(含TB)']
    #
    # data['主串电容数量列表'] = para['主串电容数'] = [c_num1]
    # data['被串电容数量列表'] = para['被串电容数'] = [7, c_num2, 7]

    c_num1 = df_input['主串电容数']
    c_num2 = df_input['被串电容数']

    para['主串电容数'] = [c_num1]
    para['被串电容数'] = [c_num2, c_num2, c_num2]

    data['主串电容数'] = para['主串电容数'][0]
    data['被串电容数'] = para['被串电容数'][1]

    # 电容容值
    data['主串电容值(μF)'] = c_pack_zhu['电容容值列表'][0]
    data['被串电容值(μF)'] = c_pack_bei['电容容值列表'][1]

    # data['主串电容数量列表'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = c_pack_bei['电容数量列表']

    # data['主串电容容值列表'] = c_pack_zhu['电容容值列表']
    # data['被串电容容值列表'] = c_pack_bei['电容容值列表']

    para['主串容值列表'] = c_pack_zhu['电容阻抗列表']
    para['被串容值列表'] = c_pack_bei['电容阻抗列表']

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
    # data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)']
    # data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)']

    r_cable = data['补偿电阻(Ω)'] = df_input['补偿电阻(Ω)']
    para['补偿电阻_分散式'] = ImpedanceMultiFreq()
    para['补偿电阻_分散式'].rlc_s = {
        1700: [r_cable, None, None],
        2000: [r_cable, None, None],
        2300: [r_cable, None, None],
        2600: [r_cable, None, None]}

    # TAD参数
    data['匹配变压器变比'] = para['匹配变压器变比'] = df_input['匹配变压器变比']

    para['TAD_z1_分散式_发送端'] = ImpedanceMultiFreq()
    para['TAD_z1_分散式_发送端'].rlc_s = {
        1700: (3.9146, 581.14e-6, None),
        2000: (3.9695, 684.89e-6, None),
        2300: (3.8636, 769.06e-6, None),
        2600: (3.7937, 959.15e-6, None),
    }

    para['TAD_z2_分散式_发送端'] = ImpedanceMultiFreq()
    para['TAD_z2_分散式_发送端'].rlc_p = {
        1700: (3.0451e3, 551.191e-3, None),
        2000: (3.1163e3, 580.653e-3, None),
        2300: (3.1775e3, 605.011e-3, None),
        2600: (3.2591e3, 635.065e-3, None),
    }

    para['TAD_n_分散式_发送端'] = {
        1700: 8.9202,
        2000: 8.8912,
        2300: 8.8508,
        2600: 8.8688,
    }

    n1 = para['匹配变压器变比']
    n2 = para['TAD_n_分散式_发送端'][freq]
    k_fs = n1 * n1 / (n2 * n2)
    para['TAD_z1_分散式_发送端'] = para['TAD_z1_分散式_发送端'] * k_fs
    para['TAD_z2_分散式_发送端'] = para['TAD_z2_分散式_发送端'] * k_fs

    para['TAD_z1_分散式_接收端'] = ImpedanceMultiFreq()
    para['TAD_z1_分散式_接收端'].rlc_s = {
        1700: (2.5082, 313.43e-6, None),
        2000: (2.1881, 319.11e-6, None),
        2300: (1.5138, 260.17e-6, None),
        2600: (0.9564, 226.35e-6, None)}

    para['TAD_z2_分散式_接收端'] = ImpedanceMultiFreq()
    para['TAD_z2_分散式_接收端'].rlc_p = {
        1700: (2.5312e3, 0.284779, None),
        2000: (2.6386e3, 0.303275, None),
        2300: (2.7380e3, 0.312331, None),
        2600: (2.8293e3, 0.327270, None)}

    para['TAD_n_分散式_接收端'] = {
        1700: 8.7351,
        2000: 8.7384,
        2300: 8.6904,
        2600: 8.7085}

    n1 = para['匹配变压器变比']
    n2 = para['TAD_n_分散式_接收端'][freq]
    k_js = n1 * n1 / (n2 * n2)
    para['TAD_z1_分散式_接收端'] = para['TAD_z1_分散式_接收端'] * k_js
    para['TAD_z2_分散式_接收端'] = para['TAD_z2_分散式_接收端'] * k_js

    # 分路电阻
    data['主串分路电阻(Ω)'] = para['主串分路电阻'] = df_input['分路电阻(Ω)']
    data['被串分路电阻(Ω)'] = para['被串分路电阻'] = df_input['分路电阻(Ω)']

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
    data['分路起点'] = offset - 24.5 - length2
    data['分路终点'] = offset + length2 + 24.5 + length2


class PreModel_20240904_QJ_Disperse(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=para['主串频率列表'],
                           m_lens=para['主串区段长度'],
                           j_lens=[29, 29],
                           m_typs=['2000A_QJ_Disperse'],
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

        m_num = len(para['被串区段长度'])
        j_num = m_num + 1
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=m_num,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[29] * j_num,
                           m_typs=['2000A_QJ_Disperse'] * m_num,
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


if __name__ == '__main__':
    pass
