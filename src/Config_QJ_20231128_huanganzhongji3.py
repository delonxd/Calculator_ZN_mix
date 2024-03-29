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


def get_huangan_info():
    ret = []

    # info_line1 = [
    #     0,
    #     ('3778G', 2600, 1273, 16),
    # ]
    #
    # info_line2 = [
    #     -863,
    #     ('3757G', 1700, 1384, 23),
    #     ('3771G', 2300, 1311, 17),
    # ]
    #
    # ret.extend(get_line_info(info_line1, info_line2))

    info_line3 = [
        0,
        ('3757G', 1700, 1384, 23),
    ]

    info_line4 = [
        -474,
        ('3766G', 2000, 1337, 22),
        ('3778G', 2600, 1273, 16),
    ]

    ret.extend(get_line_info(info_line3, info_line4))

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
def config_input_20231128_huangan():

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
        # ('左发', '左发'),
        # ('左发', '右发'),
        ('右发', '左发'),
        # ('右发', '右发'),
    ]

    mode_list = [
        # '主串调整被串分路',
        '主被串同时分路',
    ]

    src = get_huangan_info()

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
def config_headlist_20231128_huangan():
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


def config_c_pack_20231128_huangan(src):
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
def config_row_data_20231128_huangan(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '黄庵中继3'
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
    c_pack_zhu = config_c_pack_20231128_huangan([df_input['主串电容数']])
    c_pack_bei = config_c_pack_20231128_huangan(df_input['被串电容数'])

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
    data['分路模式'] = df_input['分路模式']

    r_sht = 1e-7
    if mode == '主串调整被串分路':
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = 1e10
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
        data['主串分路电阻(Ω)'] = '无'

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
    # data['分路起点'] = offset - 14.5
    # data['分路终点'] = offset + sum(length2) + 14.5

    data['分路起点'] = offset - 14.5
    data['分路终点'] = offset + length2[0] + length2[1] + 14.5

    # focus_sec = '3757G'
    focus_sec = '3778G'
    index_bei = data['被串区段'].index(focus_sec)

    data['被串区段'] = data['被串区段'][index_bei]
    data['被串区段长度(m)'] = data['被串区段长度(m)'][index_bei]
    data['被串频率(Hz)'] = data['被串频率(Hz)'][index_bei]
    data['被串电容数'] = data['被串电容数'][index_bei]

    l_point = offset + sum(length2[0:index_bei]) - 14.5
    r_point = l_point + length2[index_bei] + 29

    # l_point = -14.5
    # r_point = length1 + 14.5

    data['分路起点'] = l_point
    data['分路终点'] = r_point


class PreModel_QJ_20231128_huangan(PreModel):
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


def save2excel_20231128_huangan(path, data_output, head_list, data_detail):

    df_data = pd.DataFrame(data_output, columns=head_list)

    data_detail.config_header()
    data_detail["被串分路电流"].header[0] = '被串左端'
    data_detail["被串钢轨电流"].header[0] = '被串左端'

    # 保存到本地excel

    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    workbook = writer.book
    header_format = workbook.add_format({
        'bold': True,  # 字体加粗
        'text_wrap': True,  # 是否自动换行
        'valign': 'vcenter',  # 垂直对齐方式
        'align': 'center',  # 水平对齐方式
        'border': 1})

    # write_to_excel(df=df_input, writer=writer, sheet_name="参数设置", hfmt=header_format)
    write_to_excel(df=df_data, writer=writer, sheet_name="数据输出", hfmt=header_format)

    names = [
        "被串分路电流",
        "被串钢轨电流",
    ]

    data_detail.write2excel(sheet_names=names, writer=writer)
    writer.save()


def save2excel_20231205_huangan(path, data_output, head_list, data_detail):

    df_data = pd.DataFrame(data_output, columns=head_list)

    data_detail.config_header()
    data_detail["主串分路电流"].header[0] = '主串左端'
    data_detail["主串钢轨电流"].header[0] = '主串左端'

    # 保存到本地excel

    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    workbook = writer.book
    header_format = workbook.add_format({
        'bold': True,  # 字体加粗
        'text_wrap': True,  # 是否自动换行
        'valign': 'vcenter',  # 垂直对齐方式
        'align': 'center',  # 水平对齐方式
        'border': 1})

    # write_to_excel(df=df_input, writer=writer, sheet_name="参数设置", hfmt=header_format)
    write_to_excel(df=df_data, writer=writer, sheet_name="数据输出", hfmt=header_format)

    names = [
        "主串分路电流",
        "主串钢轨电流",
    ]

    data_detail.write2excel(sheet_names=names, writer=writer)
    writer.save()



if __name__ == '__main__':
    # draw_image_20230904_digital()
    # draw_image_2021023_guangzhan()
    # analyse_complex_add()
    pass
