
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


# 配置输入
def config_input_20240408_double_line(list_type, list_length, list_freq):

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
    for val_type in list_type:
        for val_length in list_length:
            for val_freq in list_freq:

                length = val_length
                offset = -length

                while offset <= length:

                    list_zhu_sht = list(range(0, length, 50))
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

                        print('generate row: %s --> %s' % (counter, s0.tolist()))

                        df = pd.concat([df, s0], axis=1)
                        counter += 1

                        # if counter == 5:
                        #     df = df.transpose()
                        #     return df

                    offset += 50

    df = df.transpose()

    return df


# 配置表头
def config_headlist_20240408_double_line():
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


def config_c_num_20240408_double_line(freq: Freq, length, sec_type):
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


def config_c_value_20240408_double_line(freq: Freq, sec_type):
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


def config_c_pack_20240408_double_line(freq_list, length_list, sec_type):
    if len(freq_list) != len(length_list):
        raise KeyboardInterrupt('config_c_pack_20230908_offset error: 列表长度不等')

    c_num_list = []
    c_imp_list = []
    c_val_list = []

    for index in range(len(freq_list)):
        freq = freq_list[index]
        length = length_list[index]

        c_val = config_c_value_20240408_double_line(freq, sec_type)
        c_num = config_c_num_20240408_double_line(freq, length, sec_type)

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
def config_row_data_20240408_double_line(df_input, para, data):
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
    c_pack_zhu = config_c_pack_20240408_double_line(para['主串频率列表'], para['主串区段长度'], data['主串区段类型'])
    c_pack_bei = config_c_pack_20240408_double_line(para['被串频率列表'], para['被串区段长度'], data['被串区段类型'])

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
    data['主串方向'] = para['sr_mod_主'] = '右发'
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
            para['主串分路位置'] = length2 - 14.5 - sht_position
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


class PreModel_QJ_20240408_double_line(PreModel):
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


if __name__ == '__main__':
    generate_data_df()
