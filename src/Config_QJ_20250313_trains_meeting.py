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

import pandas as pd
import numpy as np


# 配置输入
def config_input_20250313_trains_meeting(list_type, list_length, list_freq):
    columns = [
        '序号',

        '主串类型',
        '被串类型',

        '区段长度',
        '主串频率',
        '被串频率',
        '相对位置',

        '主串分路位置',

        # '主串方向',
        # '被串方向',
    ]

    df = pd.DataFrame(index=columns, dtype='object')

    counter = 1
    for val_zhu_dir in ['左发', '右发']:
        for val_type in list_type:
            for val_length in list_length:
                for val_freq in list_freq:

                    length = val_length
                    offset = -length/2

                    while offset <= length:

                        list_zhu_sht = list(range(0, length, 5))
                        list_zhu_sht.insert(0, '同位置')
                        list_zhu_sht.insert(0, '调整')
                        for val_zhu_sht in list_zhu_sht:
                            s0 = pd.Series(name=counter, index=columns)

                            s0['序号'] = s0.name

                            s0['主串类型'] = val_type[0]
                            s0['被串类型'] = val_type[1]

                            s0['区段长度'] = length

                            s0['主串频率'] = val_freq[0]
                            s0['被串频率'] = val_freq[1]

                            s0['相对位置'] = offset

                            s0['主串分路位置'] = val_zhu_sht
                            s0['主串方向'] = val_zhu_dir

                            print('generate row: %s --> %s' % (counter, s0.tolist()))

                            df = pd.concat([df, s0], axis=1)
                            counter += 1

                            # if counter == 5:
                            #     df = df.transpose()
                            #     return df

                        offset += 5000

    df = df.transpose()

    return df


# 配置表头
def config_headlist_20250313_trains_meeting():
    head_list = [
        '序号',
        # '备注',
        # '线路名称', '车站名称',
        # '主串区段', '被串区段',

        # '线间距(m)',
        '耦合系数(μH/km)',
        # '并行长度(m)',
        # '被串相对位置(m)',

        '主串方向', '被串方向',
        '主串分路位置(m)',

        # '线间距(m)',
        # '耦合系数(μH/km)',
        # '并行长度(m)',

        # '调谐区错位(m)',
        '被串相对位置(m)',
        '主串区段长度(m)', '被串区段长度(m)',
        # '主串左端坐标', '被串左端坐标',

        # '主串区段类型', '被串区段类型',
        '主串频率(Hz)', '被串频率(Hz)',

        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        '主串电容数量列表', '被串电容数量列表',
        '主串电容容值列表', '被串电容容值列表',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',

        # '主串TB模式', '被串TB模式',

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


def config_c_num_20250313_trains_meeting(freq: Freq, length, sec_type):
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


def config_c_value_20250313_trains_meeting(freq: Freq, sec_type):
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


def config_c_pack_20250313_trains_meeting(freq_list, length_list, sec_type):
    if len(freq_list) != len(length_list):
        raise KeyboardInterrupt('config_c_pack_20230908_offset error: 列表长度不等')

    c_num_list = []
    c_imp_list = []
    c_val_list = []

    for index in range(len(freq_list)):
        freq = freq_list[index]
        length = length_list[index]

        c_val = config_c_value_20250313_trains_meeting(freq, sec_type)
        c_num = config_c_num_20250313_trains_meeting(freq, length, sec_type)

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
def config_row_data_20250313_trains_meeting(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '无'

    # 区段名
    data['主串区段'] = para['主串区段'] = ''
    data['被串区段'] = para['被串区段'] = ''

    # 区段类型
    data['主串区段类型'] = df_input['主串类型']
    data['被串区段类型'] = df_input['被串类型']

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['区段长度']
    length2 = data['被串区段长度(m)'] = df_input['区段长度']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = [length2, length2, length2]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['相对位置']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset - length2

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = 20

    # 区段频率
    para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率']
    para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率']
    freq = freq1
    data['freq'] = para['freq'] = Freq(freq1)
    para['主串频率列表'] = [Freq(freq1)]
    para['被串频率列表'] = generate_frqs(Freq(freq2), 3, flip_flag=True)

    # 电容配置
    c_pack_zhu = config_c_pack_20250313_trains_meeting(para['主串频率列表'], para['主串区段长度'], data['主串区段类型'])
    c_pack_bei = config_c_pack_20250313_trains_meeting(para['被串频率列表'], para['被串区段长度'], data['被串区段类型'])

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
    data['被串方向'] = para['sr_mod_被'] = '右发'

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

    sht_position = df_input['主串分路位置']

    r_sht = 1e-7

    if sht_position == '调整':
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = 1e10
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
        data['主串分路电阻(Ω)'] = 'None'
        para['主串分路位置'] = 0
        data['主串分路位置(m)'] = '主串调整'
    else:
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = r_sht
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht

        if sht_position == '同位置':
            para['主串分路位置'] = '同位置'
            data['主串分路位置(m)'] = '与被串位置相同'
        else:
            # para['主串分路位置'] = length2 - 14.5 - sht_position
            para['主串分路位置'] = 14.5 + sht_position
            data['主串分路位置(m)'] = sht_position

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


class PreModel_QJ_20250313_trains_meeting(PreModel):
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

        freq_tmp = Freq(para['freq_被'])
        freq_tmp.change_freq()

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


def write_to_excel2(df, writer, sheet_name, format_dict=None):
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    if format_dict is not None:
        workbook = writer.book
        header_format = workbook.add_format(format_dict)

        worksheet = writer.sheets[sheet_name]
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)


def generate_data_df():
    import os
    import time

    sub_name = '..\\20240408_区间复线不同频遍历'
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())

    dir_path = '%s\\仿真输出_区间复线不同频遍历_20241216114835' % sub_name
    new_dir = '%s\\数据简化_区间复线不同频遍历_%s' % (sub_name, timestamp)

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    for file in os.listdir(dir_path):
        if file[-5:] != '.xlsx':
            continue

        file_path = os.path.join(dir_path, file)
        print('copy %s' % file_path)

        base_name = os.path.basename(file_path)
        new_path = os.path.join(new_dir, base_name)
        df_input = pd.read_excel(file_path, sheet_name=None)

        writer = pd.ExcelWriter(new_path, engine='xlsxwriter')

        for sheet_name, df_output in df_input.items():

            format_dict = {
                'bold': True,  # 字体加粗
                'text_wrap': True,  # 是否自动换行
                'valign': 'vcenter',  # 垂直对齐方式
                'align': 'center',  # 水平对齐方式
                'border': 1
            }

            if sheet_name[:4] in ['参数设置', '数据输出']:
                write_to_excel2(df_output, writer, sheet_name, format_dict=format_dict)

        writer.save()


def draw_image_20250313_trains_meeting():
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import matplotlib as mpl
    import os
    import time

    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['STSong']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False

    # root = 'C:\\Users\\Delon\\Desktop\\峨广邻线干扰\\'
    root = 'C:\\Users\\李继隆\\Desktop\\会车邻线干扰分析\\数据汇总\\'
    # file = '仿真输出_双区段.xlsx'
    # file = '区间会车_对向行驶_800m_主串2600Hz_被串1700Hz.xlsx'
    file = '区间会车_同向行驶_800m_主串2600Hz_被串1700Hz.xlsx'
    # file = '区间会车_800m_主串2600Hz_被串2300Hz.xlsx'
    df_input = pd.read_excel(root + file, '数据输出')
    df_data = pd.read_excel(root + file, '被串钢轨电流')

    # fig = plt.figure(figsize=(16, 9), dpi=100)
    # fig.subplots_adjust(hspace=0.4)
    # # fig.suptitle('test')

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '..\\20250313_区间列车会车\\图表汇总_区间会车_%s' % timestamp

    sift_list = [
        [800, '左发'],
        [800, '右发'],
    ]

    c_map = cm.winter

    for val in sift_list:
        sec_length = val[0]
        sec_sr_mode = val[1]

        dir_dict = {
            '左发': '对向行驶',
            '右发': '同向行驶',
        }

        df1 = df_input.loc[df_input["主串区段长度(m)"] == sec_length].copy()
        df2 = df1.loc[df1["主串方向"] == sec_sr_mode].copy()

        if df2.size == 0:
            continue

        posi_zhu_list = [
            '主串调整',
            '与被串位置相同',
        ]

        df3 = df2.loc[~df2["主串分路位置(m)"].isin(posi_zhu_list)].copy()

        max_i_list = df3['被串最大干扰电流(A)'].tolist()
        max_i_value = max(max_i_list)
        max_index = max_i_list.index(max_i_value)
        max_i_posi = df3['被串最大干扰位置(m)'].values[max_index]

        index = df3['序号'].values.tolist()
        index_extend = df2.loc[df2["主串分路位置(m)"].isin(posi_zhu_list)]['序号'].values.tolist()

        index.extend(index_extend)
        index = list(map(lambda x: x-1, index))

        if len(index) == 0:
            continue

        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(hspace=1)

        ax = fig.add_subplot(1, 1, 1)

        freq_zhu = df3['主串频率(Hz)'].values[0]
        freq_bei = df3['被串频率(Hz)'].values[0]

        ###################################################################

        # title = '主串2600Hz正向-被串2300Hz%s-区段长度%sm' % (dir_dict[sec_sr_mode], sec_length)
        # title = '主串2600Hz-被串2300Hz-%s' % (dir_dict[sec_sr_mode])
        title = '主串%sHz-被串%sHz-%s' % (freq_zhu, freq_bei, dir_dict[sec_sr_mode])

        ax.set_title(title, x=0.5, y=1.04, fontsize=30)

        # fig.suptitle(title, fontsize=30)

        ax.set_xlabel('被串分路位置(m)', fontsize=18)
        ax.set_ylabel('邻线干扰钢轨电流(A)', fontsize=20)

        ax.yaxis.grid(True, which='major')
        # ax.yaxis.set_font(20)
        ax.set_ylim([0, 0.5])

        data = df_data.iloc[index, :].copy()
        data_output = df_input.iloc[index, :].copy()

        print(data)
        data = data.dropna(how='all', axis=1)

        max_i = 0
        size0 = data.index.size - 2

        # column_size = 0

        counter = 0
        for i, _ in enumerate(index):
            row = data.iloc[i, :].copy()
            input_row = data_output.iloc[i, :].copy()

            posi_zhu = input_row["主串分路位置(m)"]
            # yy = row.values / 24 * 30
            yy = row.values

            # yy = yy[sec_length:]
            # yy = yy[:-sec_length]

            # column_size = yy.size
            xx = np.arange(yy.size)

            width = 2
            alpha = 1
            line_style = '-'
            label = None

            if posi_zhu == '主串调整':
                width = 3
                color = 'red'
                label = '主串调整状态'
            elif posi_zhu == '与被串位置相同':
                color = 'yellow'
                label = '主串列车与被串分路位置相同'
            else:
                if counter == max_index:
                    width = 3
                    label = '主串列车距离发送器%sm(最大)' % posi_zhu
                else:
                    width = 0.5
                    alpha = 0.3
                color = c_map(counter / size0)
                counter += 1

            ax.plot(
                xx,
                yy,
                linestyle=line_style,
                alpha=alpha,
                color=color,
                label=label,
                linewidth=width,
            )

            max_i = max(max_i, max(yy))

        ######################################################################################################
        # 坐标轴
        t = np.arange(100, sec_length, 100)
        x_ticks = [0, 29, sec_length, sec_length + 29] + list(t + 14.5)
        x_label = ['发\n送', '接\n收', '发\n送', '接\n收'] + list(t)

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_label, fontsize=1)

        ax.tick_params(
            # axis='y',
            labelsize=12,  # y轴字体大小设置
            # color='r',  # y轴标签颜色设置
            # labelcolor='b',  # y轴字体颜色设置
            direction='in',  # y轴标签方向设置
            # pad=10,
        )

        ######################################################################################################
        # 图例
        ax.legend(
            loc='upper right',
            # bbox_to_anchor=(0.96, 0.9),
            bbox_to_anchor=(0.46, 0.9),
            # ncol=2,
            # title='Legend Title',
            fontsize=13,
        )

        ######################################################################################################
        # 颜色条
        cb_x = 0.2
        cb_y = 0.59
        # cb_pos = 0.9

        cax = fig.add_axes([cb_x, cb_y, 0.01, 0.25])  # 四个参数分别是左、下、宽、长

        norm = mpl.colors.Normalize(vmin=0, vmax=800)
        bounds = [tmp for tmp in np.linspace(0, 800, size0+1)]
        cb = mpl.colorbar.ColorbarBase(
            ax=cax,
            cmap=c_map,
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

        cb.set_ticks([0, 400, 800])
        cb.set_ticklabels(['0m', '400m', '800m'])

        cax.tick_params(labelsize=14, direction='out')

        ######################################################################################################
        # 标签
        txt = '主串列车\n距发送器\n距离(m)'
        # txt = '\n'.join(list(txt))
        ax.text(
            -0.5, 0.5,
            txt,
            fontsize=14,
            color='black',
            va='center',
            ha='right',
            transform=cax.transAxes,
        )

        ######################################################################################################
        # # 辅助直线
        #
        # yy = np.ones(column_size) * max_i
        # xx = np.arange(yy.size)
        #
        # ax.plot(
        #     xx,
        #     yy,
        #     linestyle='--',
        #     alpha=1,
        #     color='blue',
        #     linewidth=1,
        # )

        ######################################################################################################
        # # 辅助文本
        #
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

        ######################################################################################################
        # 箭头

        # y1 = min(max_list)
        # x1 = max_list.index(y1)

        y1 = max_i_value
        x1 = max_i_posi

        # txt = '最优扼流变比$\mathrm{%s:1}$\n最大干扰电流$\mathrm{%.2fmA}$' % (x1+5, y1)
        txt = '最大干扰位置%sm\n干扰电流%.2fmA' % (x1, y1*1000)

        ax.annotate(
            txt, (x1, y1),
            xytext=(x1 - 50, y1 - 0.04),
            ha="right", va="center",
            # textcoords='offset points',
            fontsize=12,
            color='blue',
            arrowprops=dict(
                # facecolor='#74C476',
                alpha=0.6,
                arrowstyle='fancy',
                # connectionstyle='arc3,rad=0.5',
                color='blue',
            )
        )

        ######################################################################################################

        # plt.tight_layout()

        # plt.show()
        # return

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        filename1 = '%s\\%s-钢轨电流曲线.png' % (res_dir, title)
        fig.savefig(filename1)


def draw_image2_20250313_trains_meeting():
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import matplotlib as mpl
    import os
    import time

    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['STSong']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    # plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False

    # root = 'C:\\Users\\Delon\\Desktop\\峨广邻线干扰\\'
    root = 'C:\\Users\\李继隆\\Desktop\\会车邻线干扰分析\\数据汇总\\'
    # file = '仿真输出_双区段.xlsx'
    # file = '区间会车_对向行驶_800m_主串2600Hz_被串1700Hz.xlsx'
    file = '区间会车_同向行驶_800m_主串2600Hz_被串1700Hz.xlsx'
    # file = '区间会车_800m_主串2600Hz_被串2300Hz.xlsx'
    df_input = pd.read_excel(root + file, '数据输出')
    # df_data = pd.read_excel(root + file, '被串钢轨电流')

    # fig = plt.figure(figsize=(16, 9), dpi=100)
    # fig.subplots_adjust(hspace=0.4)
    # # fig.suptitle('test')

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '..\\20250313_区间列车会车\\图表汇总_区间会车_%s' % timestamp

    sift_list = [
        [800, '左发'],
        [800, '右发'],
    ]

    for val in sift_list:
        sec_length = val[0]
        sec_sr_mode = val[1]

        dir_dict = {
            '左发': '对向行驶',
            '右发': '同向行驶',
        }

        df1 = df_input.loc[df_input["主串区段长度(m)"] == sec_length].copy()
        df2 = df1.loc[df1["主串方向"] == sec_sr_mode].copy()

        if df2.size == 0:
            continue

        posi_zhu_list = [
            '主串调整',
            '与被串位置相同',
        ]

        df3 = df2.loc[~df2["主串分路位置(m)"].isin(posi_zhu_list)].copy()

        i_adjust = df2.loc[df2["主串分路位置(m)"] == '主串调整']['被串最大干扰电流(A)'].values[0]
        print(i_adjust)

        max_i_list = df3['被串最大干扰电流(A)'].tolist()
        max_i_list_except_joint = df3['被串最大干扰电流(A)(不含调谐区)'].tolist()
        max_i_value = max(max_i_list)
        max_index = max_i_list.index(max_i_value)

        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(hspace=1)

        ax = fig.add_subplot(1, 1, 1)

        ###################################################################

        # title = '主串2600Hz正向-被串2300Hz%s-区段长度%sm' % (dir_dict[sec_sr_mode], sec_length)

        freq_zhu = df3['主串频率(Hz)'].values[0]
        freq_bei = df3['被串频率(Hz)'].values[0]
        title = '主串%sHz-被串%sHz-%s-最大干扰电流' % (freq_zhu, freq_bei, dir_dict[sec_sr_mode])

        ax.set_title(title, x=0.5, y=1.04, fontsize=30)

        # fig.suptitle(title, fontsize=30)

        ax.set_xlabel('主串分路位置(m)', fontsize=18)
        ax.set_ylabel('邻线干扰钢轨电流(A)', fontsize=20)

        ax.yaxis.grid(True, which='major')
        # ax.yaxis.set_font(20)
        ax.set_ylim([0, 0.5])

        size0 = len(max_i_list)

        ax.plot(
            np.arange(0, size0*5, 5),
            np.array(max_i_list_except_joint),
            linestyle='-',
            alpha=1,
            color='gray',
            label='主串分路/被串不含调谐区',
            linewidth=2,
        )

        ax.plot(
            np.arange(0, size0*5, 5),
            np.array(max_i_list),
            linestyle='-',
            alpha=1,
            color='blue',
            label='主串分路/被串含调谐区',
            linewidth=2,
        )

        ######################################################################################################
        # 坐标轴
        t = np.arange(100, sec_length+1, 100)
        x_ticks = [0] + list(t)
        x_label = ['发送'] + list(t)

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_label, fontsize=1)

        ax.tick_params(
            # axis='y',
            labelsize=13,  # y轴字体大小设置
            # color='r',  # y轴标签颜色设置
            # labelcolor='b',  # y轴字体颜色设置
            direction='in',  # y轴标签方向设置
            # pad=10,
        )

        ######################################################################################################
        # 辅助直线

        yy = np.ones(800) * i_adjust
        xx = np.arange(800)

        ax.plot(
            xx,
            yy,
            linestyle='--',
            alpha=1,
            color='red',
            linewidth=2,
            label='主串调整/被串含调谐区',
        )

        pos_x = 0
        ax.annotate('调整状态\n最大干扰电流%.2fmA' % (i_adjust*1000), (pos_x, i_adjust),
                    xytext=(pos_x, i_adjust + 0.01),
                    ha="left",
                    fontsize=12, color='red')
        ######################################################################################################
        # # 辅助文本
        #
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

        ######################################################################################################
        # 箭头

        # y1 = min(max_list)
        # x1 = max_list.index(y1)

        y1 = max_i_value
        x1 = max_index*5

        # txt = '最优扼流变比$\mathrm{%s:1}$\n最大干扰电流$\mathrm{%.2fmA}$' % (x1+5, y1)
        txt = '主串列车位置%sm\n最大干扰电流%.2fmA' % (x1, y1*1000)

        ax.annotate(
            txt, (x1, y1),
            xytext=(x1+100, y1 - 0.02),
            # xytext=(x1, y1 - 0.06),
            ha="center", va="center",
            # textcoords='offset points',
            fontsize=12,
            color='blue',
            arrowprops=dict(
                # facecolor='#74C476',
                alpha=0.6,
                arrowstyle='fancy',
                # connectionstyle='arc3,rad=0.5',
                color='blue',
            )
        )

        ######################################################################################################
        # 图例
        ax.legend(
            loc='upper right',
            bbox_to_anchor=(0.98, 0.95),
            # bbox_to_anchor=(0.46, 0.9),
            # ncol=2,
            # title='Legend Title',
            fontsize=13,
        )

        ######################################################################################################

        # plt.tight_layout()

        # plt.show()
        # return

        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        filename1 = '%s\\%s.png' % (res_dir, title)
        fig.savefig(filename1)


if __name__ == '__main__':
    # generate_data_df()
    draw_image_20250313_trains_meeting()
    # draw_image2_20250313_trains_meeting()
