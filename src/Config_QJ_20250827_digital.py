
from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant
from src.FrequencyType import Freq
from src.Method import generate_frqs

from src.Module.OutsideElement import CapC

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line
from src.Model.PreModel import PreModel

import itertools
import pandas as pd

# from openpyxl import Workbook, load_workbook
# from openpyxl.styles import PatternFill, Alignment, Font, Border, Side

import matplotlib.pyplot as plt
# from matplotlib import cm

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False


# 配置输入
def config_input_20250827_qj_digital():

    columns = [
        '序号',

        '主串频率(Hz)',
        '被串频率(Hz)',

        '主串区段长度(m)',
        '被串区段长度(m)',
        '被串相对位置(m)',

        '主串电缆长度(km)',
        '被串电缆长度(km)',
        '电缆类型',
        '发送器调整电阻(Ω)',
        '匹配变压器类型',

        '分路模式',
        '主串方向',
        '被串方向',

    ]

    df = pd.DataFrame(index=columns, dtype='object')

    list1 = [
        [25, 0, '粗电缆', '10:1变压器', 800],
        [10, 0, '细电缆', '既有变压器', 800],
        [10, 0, '细电缆', '既有变压器', 1400],
        [10, 0, '细电缆', '10:1变压器', 1400],
        [2, 247.5, '细电缆', '既有变压器', 1400],
        [2, 247.5, '细电缆', '10:1变压器', 1400],
    ]

    list2 = list(itertools.product(
        ['主串调整被串分路', '主被串同时分路'],
        ['对位', '错位'],
        [
            ['左发', '左发'],
            ['左发', '右发'],
            ['右发', '左发'],
            ['右发', '右发'],
        ],
        [
            [1700, 1700],
            [1700, 2300],
            [2300, 1700],
            [2300, 2300],
            [2000, 2000],
            [2000, 2600],
            [2600, 2000],
            [2600, 2600],
        ],
    ))

    counter = 1
    for cnd1 in list1:
        for cnd2 in list2:
            s0 = pd.Series(name=counter, index=columns)

            s0['序号'] = s0.name

            s0['主串电缆长度(km)'] = cnd1[0]
            s0['被串电缆长度(km)'] = cnd1[0]

            s0['发送器调整电阻(Ω)'] = cnd1[1]
            s0['电缆类型'] = cnd1[2]
            s0['匹配变压器类型'] = cnd1[3]

            s0['主串区段长度(m)'] = cnd1[4]
            s0['被串区段长度(m)'] = cnd1[4]

            s0['分路模式'] = cnd2[0]

            if cnd2[1] == '对位':
                s0['被串相对位置(m)'] = 0
            elif cnd2[1] == '错位':
                s0['被串相对位置(m)'] = cnd1[4] / 2
            else:
                raise KeyboardInterrupt('被串相对位置错误')

            s0['主串方向'] = cnd2[2][0]
            s0['被串方向'] = cnd2[2][1]

            s0['主串频率(Hz)'] = cnd2[3][0]
            s0['被串频率(Hz)'] = cnd2[3][1]

            print('generate row: %s --> %s' % (counter, s0.tolist()))

            df = pd.concat([df, s0], axis=1, sort=False)
            counter += 1
            # break

    df = df.transpose()

    print(df)
    return df


# 配置表头
def config_headlist_20250827_qj_digital():
    head_list = [
        '序号',

        '耦合系数(μH/km)',

        '电缆类型',
        '主串电缆长度(km)', '被串电缆长度(km)',
        '发送器调整电阻(Ω)',
        '匹配变压器类型',

        '分路模式',

        '主串区段类型', '被串区段类型',
        '主串方向', '被串方向',
        # '主串分路位置(m)',
        # '是否换装TB',

        '被串相对位置(m)',
        '主串区段长度(m)', '被串区段长度(m)',

        '主串频率(Hz)', '被串频率(Hz)',

        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        '主串电容数量列表', '被串电容数量列表',
        '主串电容容值列表', '被串电容容值列表',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',

        # '主串TB模式', '被串TB模式',

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


def config_c_num_20250827_qj_digital(freq: Freq, length, sec_type):
    freq_value = freq.value

    if 0 < length <= 300:
        key = 0
    elif length > 300:
        key = int((length - 251) / 50)
    else:
        raise KeyboardInterrupt('config_c_num error: 区段长度错误')

    table_j = {
        0: [0, 0, 0, 0],
        1: [4, 4, 3, 3],
        2: [4, 4, 4, 4],
        3: [5, 5, 5, 6],
        4: [6, 6, 6, 6],
        5: [6, 6, 6, 6],
        6: [6, 7, 6, 7],
        7: [7, 7, 7, 7],
        8: [8, 8, 8, 8],
        9: [8, 8, 8, 8],
        10: [9, 9, 9, 9],
        11: [9, 9, 9, 9],
        12: [9, 9, 9, 9],
        13: [10, 10, 10, 10],
        14: [10, 10, 10, 10],
        15: [11, 11, 11, 11],
        16: [11, 11, 11, 11],
        17: [12, 12, 12, 12],
        18: [12, 12, 12, 14],
        19: [13, 13, 13, 15],
        20: [14, 14, 16, 16],
        21: [16, 16, 18, 20],
        22: [18, 18, 18, 20],
    }

    table_t = {
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

    if sec_type == '普速':
        table = table_j
    elif sec_type == '客专':
        table = table_t
    else:
        raise KeyboardInterrupt('config_c_num error: 区段类型错误')

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


def config_c_value_20250827_qj_digital(freq: Freq, sec_type):
    freq_value = freq.value

    value_dict = {
        1700: 55,
        2000: 50,
        2300: 46,
        2600: 40,
    }

    if freq_value not in value_dict.keys():
        raise KeyboardInterrupt('config_c_value_imp error: 区段频率错误')

    if sec_type == '普速':
        c_value = value_dict[freq_value]
    elif sec_type == '客专':
        c_value = 25
    else:
        raise KeyboardInterrupt('config_c_value_imp error: 区段类型错误')

    return c_value


def config_c_pack_20250827_qj_digital(freq_list, length_list, sec_type):
    if len(freq_list) != len(length_list):
        raise KeyboardInterrupt('config_c_pack_20250519_with_tb error: 列表长度不等')

    c_num_list = []
    c_imp_list = []
    c_val_list = []

    for index in range(len(freq_list)):
        freq = freq_list[index]
        length = length_list[index]

        c_val = config_c_value_20250827_qj_digital(freq, sec_type)
        c_num = config_c_num_20250827_qj_digital(freq, length, sec_type)

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
def config_row_data_20250827_qj_digital(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '无'

    # 区段名
    data['主串区段'] = para['主串区段'] = ''
    data['被串区段'] = para['被串区段'] = ''

    # 区段类型
    data['主串区段类型'] = '客专'
    data['被串区段类型'] = '客专'

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['主串区段长度(m)']
    length2 = data['被串区段长度(m)'] = df_input['被串区段长度(m)']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = [length2, length2, length2]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset - length2

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = 20

    # 区段频率
    para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率(Hz)']
    para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率(Hz)']
    freq = freq1
    data['freq'] = para['freq'] = Freq(freq1)
    para['主串频率列表'] = [Freq(freq1)]
    para['被串频率列表'] = generate_frqs(Freq(freq2), 3, flip_flag=True)

    # 电容配置
    c_pack_zhu = config_c_pack_20250827_qj_digital(para['主串频率列表'], para['主串区段长度'], data['主串区段类型'])
    c_pack_bei = config_c_pack_20250827_qj_digital(para['被串频率列表'], para['被串区段长度'], data['被串区段类型'])

    # 电容数量
    para['主串电容数'] = c_pack_zhu['电容数量列表']
    para['被串电容数'] = c_pack_bei['电容数量列表']

    data['主串电容数(含TB)'] = para['主串电容数'][0]
    data['被串电容数(含TB)'] = para['被串电容数'][1]

    # 电容容值
    data['主串电容值(μF)'] = c_pack_zhu['电容容值列表'][0]
    data['被串电容值(μF)'] = c_pack_bei['电容容值列表'][1]

    data['主串电容数量列表'] = c_pack_zhu['电容数量列表']
    data['被串电容数量列表'] = c_pack_bei['电容数量列表']

    data['主串电容容值列表'] = c_pack_zhu['电容容值列表']
    data['被串电容容值列表'] = c_pack_bei['电容容值列表']

    para['主串容值列表'] = c_pack_zhu['电容阻抗列表']
    para['被串容值列表'] = c_pack_bei['电容阻抗列表']

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
    cable_type = df_input['电缆类型']
    data['电缆类型'] = cable_type

    if cable_type == '粗电缆':
        data['电缆电阻(Ω/km)'] = 28
    elif cable_type == '细电缆':
        data['电缆电阻(Ω/km)'] = 43
    else:
        raise KeyboardInterrupt('电缆类型错误')

    data['电缆电感(H/km)'] = 825e-6
    data['电缆电容(F/km)'] = 28e-9

    para['Cable_R_区间数字化'] = para['Cable_R']
    para['Cable_L_区间数字化'] = para['Cable_L']
    para['Cable_C_区间数字化'] = para['Cable_C']

    para['Cable_R_区间数字化'].value = data['电缆电阻(Ω/km)']
    para['Cable_L_区间数字化'].value = data['电缆电感(H/km)']
    para['Cable_C_区间数字化'].value = data['电缆电容(F/km)']

    # 电缆长度
    data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)']
    data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)']
    para['cab_len'] = para['主串电缆长度']

    # 分路电阻

    sht_mode = df_input['分路模式']
    data['分路模式'] = sht_mode
    r_sht = 1e-7

    if sht_mode == '主串调整被串分路':
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = 1e10
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
        data['主串分路电阻(Ω)'] = 'None'

    elif sht_mode == '主被串同时分路':
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
    data['分路终点'] = offset + length2 + 14.5

    # 发送器调整电阻
    r_adj = df_input['发送器调整电阻(Ω)']
    data['发送器调整电阻(Ω)'] = r_adj

    if r_adj == 0:
        r1 = 1e-10
    elif r_adj == 247.5:
        r1 = 247.5
    else:
        raise KeyboardInterrupt('发送器调整电阻错误')

    para['Rt_区间数字化'] = ImpedanceMultiFreq()
    para['Rt_区间数字化'].rlc_s = {
        1700: [r1, None, None],
        2000: [r1, None, None],
        2300: [r1, None, None],
        2600: [r1, None, None],
    }

    # 防雷变压器
    para['FL_z1_区间数字化'] = ImpedanceMultiFreq()
    para['FL_z1_区间数字化'].rlc_s = {
        1700: (7.14, 1.70e-3, None),
        2000: (7.24, 1.70e-3, None),
        2300: (7.35, 1.69e-3, None),
        2600: (7.48, 1.69e-3, None)}

    para['FL_z2_区间数字化'] = ImpedanceMultiFreq()
    para['FL_z2_区间数字化'].rlc_s = {
        1700: (2520, 529.86e-3, None),
        2000: (3100, 500.44e-3, None),
        2300: (3620, 475.13e-3, None),
        2600: (4120, 454.44e-3, None)}

    n_fl = 1/1.04
    para['FL_n_区间数字化'] = {
        1700: n_fl,
        2000: n_fl,
        2300: n_fl,
        2600: n_fl}

    # 匹配变压器
    tad_type = df_input['匹配变压器类型']
    data['匹配变压器类型'] = para['匹配变压器类型'] = tad_type

    if tad_type == '既有变压器':
        pass

    elif tad_type == '10:1变压器':
        para['TAD_z1_区间数字化'] = ImpedanceMultiFreq()
        para['TAD_z1_区间数字化'].rlc_s = {
            1700: (5.43, 0.810e-3, None),
            2000: (5.61, 0.809e-3, None),
            2300: (5.76, 0.806e-3, None),
            2600: (5.97, 0.803e-3, None)}

        para['TAD_z2_区间数字化'] = ImpedanceMultiFreq()
        para['TAD_z2_区间数字化'].rlc_s = {
            1700: (631.24, 165.07e-3, None),
            2000: (716.66, 156.27e-3, None),
            2300: (790.26, 148.25e-3, None),
            2600: (863.02, 142.06e-3, None)}

        para['TAD_n_区间数字化'] = {
            1700: 10,
            2000: 10,
            2300: 10,
            2600: 10,
        }

        para['TAD_c_区间数字化'] = ImpedanceMultiFreq()
        para['TAD_c_区间数字化'].rlc_s = {
            1700: (None, None, 0.4e-3),
            2000: (None, None, 0.4e-3),
            2300: (None, None, 0.4e-3),
            2600: (None, None, 0.4e-3)}

    else:
        raise KeyboardInterrupt('发送器调整电阻错误')


class PreModel_QJ_20250827_digital(PreModel):
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
                           m_typs=['2000A_QJ_Digital'],
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
                           m_typs=['2000A_QJ_Digital'] * m_num,
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']] * m_num,
                           send_lvs=[send_level] * m_num,
                           parameter=parameter)

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.change_cable_length()

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
    config_input_20250827_qj_digital()

    pass
