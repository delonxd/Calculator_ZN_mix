from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant
from src.FrequencyType import Freq

from src.Module.TcsrLib import ZPW2000A_ZN_25Hz_Coding
from src.Module.TcsrLib import ZPW2000A_QJ_Normal
from src.Module.OutsideElement import CapC

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line
from src.Model.PreModel import PreModel

import pandas as pd


def config_input_20260703_25hz_2000a_mix():
    columns = [
        '序号',
        '备注',

        '主串区段索引',
        '被串区段索引',

        '主串区段',
        '被串区段',

        '主串区段长度(m)',
        '被串区段长度(m)',

        '主串调谐区长度',
        '被串调谐区长度',

        '被串相对位置(m)',

        '耦合系数(μH/km)',

        '主串频率(Hz)',
        '被串频率(Hz)',

        '主串电容数(含TB)',
        '被串电容数(含TB)',

        '主串电容值(μF)',
        '被串电容值(μF)',

        '主串区段类型',
        '被串区段类型',

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
        '分路起点',
        '分路终点',

        '被串是否发码',
        'FT1-U二次侧输出电压(V)',

        # '主串FT1U输出电压(V)',
        # '被串FT1U输出电压(V)',
        #
        # '主串调整电阻(Ω)',
        # '被串调整电阻(Ω)',

        '调整电阻(Ω)',
        '调整电感(H)',
        '调整电容(F)',
        '调整RLC模式',

        'NGL-C1(μF)',

        'WGL-C1(μF)',
        'WGL-C2(μF)',
        'WGL-L1-R(Ω)',
        'WGL-L1-L(H)',
        'WGL-L2-R(Ω)',
        'WGL-L2-L(mH)',
        'WGL-BPM变比',
        '扼流变压器变比',

        'BE-Rm(Ω)',
        'BE-Lm(H)',
    ]

    df = pd.DataFrame(index=columns, dtype='object')

    # sec_list = [
    #     ['IG', 880, 2000, 9, '左发', 80, 100, 0, 80],
    #     ['IG', 880, 1700, 9, '右发', 80, 100, 0, 80],
    #     ['IIG', 956, 2600, 10, '左发', 80, 100, -8, 60],
    #     ['IIG', 956, 2300, 10, '右发', 80, 100, -8, 60],
    # ]

    dict_l1 = {
        '区段名': ['IG'],
        '区段长度': [203],
        '调谐区长度': [0, 0],
        '区段频率': [2300],
        '电容数': [0],
        '电容容值': [25],
        '相对位置': 0,
        '区段类型': ['2000A_25Hz_Coding'],
        '电缆长度': [5],
        '发送电平级': [1],
        '发送电压': [170],
    }

    dict_l2 = {
        '区段名': ['IIAG', 'IIBG'],
        '区段长度': [684, 729],
        '调谐区长度': [0, 29, 29],
        '区段频率': [1700, 2300],
        '电容数': [11, 9],
        '电容容值': [25, 25],
        '相对位置': 128-684,
        '区段类型': ['2000A', '2000A'],
        '电缆长度': [10, 10],
        '发送电平级': [3, 3],
        '发送电压': ['最大', '最大'],
    }

    # sec1 = l1
    #
    # sec_list = [
    #     [['IG'], [203], [0, 0], [2300], [0], [25], 0, ['2000A_25Hz_Coding'], 0,
    #      [5], 1, 170],
    #     [['IIAG', 'IIBG'], [684, 729], [0, 29, 29], [1700, 2300], [11, 9], [25, 25], 128-684, ['2000A', '2000A'], 0],
    # ,
    #     [['IIAG', 'IIBG'], [684, 729], [0, 29, 29], [1700, 2300], [11, 9], [25, 25], 128-684, ['2000A', '2000A'], 1],
    # ]
    map_table = {
        '区段名': 0,
        '区段长度': 1,
        '调谐区长度': 2,
        '区段频率': 3,
        '电容数': 4,
        '电容容值': 5,
        '相对位置': 6,
        '区段类型': 7,
        '电缆长度': 8,
        '发送电平级': 9,
        '发送电压': 10,
        '区段索引': 11,
    }

    l1 = [dict_l1[key] for key in dict_l1 if key in map_table]
    l2 = [dict_l2[key] for key in dict_l2 if key in map_table]

    sec1 = l1.copy()
    sec2 = l2.copy()
    sec3 = l2.copy()

    sec1.append(0)
    sec2.append(0)
    sec3.append(1)

    sec_list = [sec1, sec2, sec3]

    condition_list = [
        ['主串调整被串分路', '否'],
        ['主被串同时分路', '否'],
        ['主串调整被串分路', '是'],
        ['主被串同时分路', '是'],
    ]

    direction_list = [
        ['左发', '左发'],
        ['左发', '右发'],
        ['右发', '左发'],
        ['右发', '右发'],
    ]
    counter = 1

    # posi_list = list(range(0, 780, 20))
    # # posi_list = posi_list[:2]

    pick_sec = [
        [0, 1],
        [0, 2],
        [1, 0],
        [2, 0],
    ]

    for index1, index2 in pick_sec:
        for condition in condition_list:
            for direction in direction_list:

                sec_zhu = sec_list[index1]
                sec_bei = sec_list[index2]
                s0 = pd.Series(name=counter, index=columns)

                s0['序号'] = s0.name
                s0['备注'] = ''

                s0['主串区段索引'] = index_zhu = sec_zhu[map_table['区段索引']]
                s0['被串区段索引'] = index_bei = sec_bei[map_table['区段索引']]

                s0['主串区段'] = sec_zhu[map_table['区段名']][index_zhu:index_zhu+1]
                s0['被串区段'] = sec_bei[map_table['区段名']]

                s0['主串区段长度(m)'] = sec_zhu[map_table['区段长度']][index_zhu:index_zhu+1]
                s0['被串区段长度(m)'] = sec_bei[map_table['区段长度']]

                s0['主串调谐区长度'] = sec_zhu[map_table['调谐区长度']][index_zhu:index_zhu+2]
                s0['被串调谐区长度'] = sec_bei[map_table['调谐区长度']]

                offset1 = sec_zhu[map_table['相对位置']] + sum(sec_zhu[map_table['区段长度']][:index_zhu])
                offset2 = sec_bei[map_table['相对位置']]

                s0['分路起点'] = sum(s0['被串区段长度(m)'][:index_bei]) - (s0['被串调谐区长度'][index_bei]/2)
                s0['分路终点'] = sum(s0['被串区段长度(m)'][:index_bei+1]) + (s0['被串调谐区长度'][index_bei+1]/2)

                s0['被串相对位置(m)'] = offset2 - offset1

                s0['分路起点'] = s0['分路起点'] + s0['被串相对位置(m)']
                s0['分路终点'] = s0['分路终点'] + s0['被串相对位置(m)']

                # s0['占车位置(m)'] = posi_zhu_0

                s0['耦合系数(μH/km)'] = 20

                s0['主串频率(Hz)'] = sec_zhu[map_table['区段频率']][index_zhu:index_zhu+1]
                s0['被串频率(Hz)'] = sec_bei[map_table['区段频率']]

                s0['主串电容数(含TB)'] = sec_zhu[map_table['电容数']][index_zhu:index_zhu+1]
                s0['被串电容数(含TB)'] = sec_bei[map_table['电容数']]

                s0['主串电容值(μF)'] = sec_zhu[map_table['电容容值']][index_zhu:index_zhu+1]
                s0['被串电容值(μF)'] = sec_bei[map_table['电容容值']]

                s0['主串区段类型'] = sec_zhu[map_table['区段类型']][index_zhu:index_zhu+1]
                s0['被串区段类型'] = sec_bei[map_table['区段类型']]

                if s0['被串区段类型'][0] == '2000A' and condition[1] == '否':
                    continue

                s0['主串道床电阻(Ω·km)'] = 10000
                s0['被串道床电阻(Ω·km)'] = 10000

                s0['主串方向'] = direction[0]
                s0['被串方向'] = direction[1]

                s0['主串电缆长度(km)'] = sec_zhu[map_table['电缆长度']][index_zhu]
                s0['被串电缆长度(km)'] = sec_bei[map_table['电缆长度']][index_bei]

                s0['分路模式'] = condition[0]
                s0['分路电阻(Ω)'] = 1e-7

                s0['主串电平级'] = sec_zhu[map_table['发送电平级']][index_zhu]
                s0['主串电源电压'] = sec_zhu[map_table['发送电压']][index_zhu]

                s0['分路间隔(m)'] = 1

                s0['被串是否发码'] = condition[1]
                s0['FT1-U二次侧输出电压(V)'] = 80

                # s0['主串FT1U输出电压(V)'] = 80
                # s0['被串FT1U输出电压(V)'] = 80
                #
                # s0['主串调整电阻(Ω)'] = 100
                # s0['被串调整电阻(Ω)'] = 100

                s0['调整电阻(Ω)'] = 100
                s0['调整电感(H)'] = None
                s0['调整电容(F)'] = None
                s0['调整RLC模式'] = '串联'

                s0['NGL-C1(μF)'] = 1
                s0['WGL-C1(μF)'] = 1
                s0['WGL-C2(μF)'] = 20
                s0['WGL-L1-R(Ω)'] = None
                s0['WGL-L1-L(H)'] = 0.5
                s0['WGL-L2-R(Ω)'] = None
                s0['WGL-L2-L(mH)'] = 5
                s0['WGL-BPM变比'] = 4

                s0['扼流变压器变比'] = 3
                s0['BE-Rm(Ω)'] = 110
                s0['BE-Lm(H)'] = 0.024

                print('generate row: %s --> %s' % (counter, s0.tolist()))

                df = pd.concat([df, s0], axis=1, sort=False)
                counter += 1

    df = df.transpose()

    return df


# 配置表头
def config_headlist_20260703_25hz_2000a_mix():
    head_list = [
        '序号',
        '备注',
        # '线路名称', '车站名称',
        '主串区段', '被串区段',
        '主串区段类型', '被串区段类型',

        '耦合系数(μH/km)',

        '主串方向', '被串方向',

        '主串区段长度(m)', '被串区段长度(m)',
        '主串调谐区长度(m)', '被串调谐区长度(m)',
        '被串相对位置(m)',

        # '占车位置(m)',

        '主串频率(Hz)',
        '被串频率(Hz)',

        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)',
        '被串电容值(μF)',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',

        # '主串TB模式', '被串TB模式',

        '主串电缆长度(km)', '被串电缆长度(km)',
        '分路模式',
        '主串分路电阻(Ω)', '被串分路电阻(Ω)',
        # '占车分路电阻(Ω)',

        '主串电平级',
        '电源电压',

        '分路间隔(m)',

        # '主串FT1U输出电压(V)',
        # '被串FT1U输出电压(V)',
        #
        # '主串调整电阻(Ω)',
        # '被串调整电阻(Ω)',

        '被串是否发码',
        'FT1-U二次侧输出电压(V)',

        '调整电阻(Ω)',
        '调整电感(H)',
        '调整电容(F)',
        '调整RLC模式',

        # 'NGL-C1(μF)',
        #
        # 'WGL-C1(μF)',
        # 'WGL-C2(μF)',
        # # 'WGL-L1-R(Ω)',
        # 'WGL-L1-L(H)',
        # # 'WGL-L2-R(Ω)',
        # 'WGL-L2-L(mH)',
        # 'WGL-BPM变比',
        # '扼流变压器变比',
        #
        # 'BE-Rm(Ω)',
        # 'BE-Lm(H)',

        '被串最大干扰电流(A)',
        '被串最大干扰位置(m)',
    ]

    return head_list


# 配置行数据
def config_row_data_20260703_25hz_2000a_mix(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = df_input['备注']

    data['主串区段索引'] = df_input['主串区段索引']
    data['被串区段索引'] = df_input['被串区段索引']
    index_bei = df_input['被串区段索引']

    # 区段名
    data['主串区段'] = df_input['主串区段'][0]
    data['被串区段'] = df_input['被串区段'][index_bei]

    para['主串区段数'] = len(df_input['主串区段'])
    para['被串区段数'] = len(df_input['被串区段'])

    # 区段长度
    # length1 = data['主串区段长度(m)'] = df_input['主串区段长度(m)']
    # length2 = data['被串区段长度(m)'] = df_input['被串区段长度(m)']
    # para['主串区段长度'] = [length1]
    # para['被串区段长度'] = [length2]

    para['主串区段长度'] = df_input['主串区段长度(m)']
    para['被串区段长度'] = df_input['被串区段长度(m)']
    data['主串区段长度(m)'] = df_input['主串区段长度(m)'][0]
    data['被串区段长度(m)'] = df_input['被串区段长度(m)'][index_bei]

    # 调谐区长度
    para['主串调谐区长度'] = df_input['主串调谐区长度']
    para['被串调谐区长度'] = df_input['被串调谐区长度']
    data['主串调谐区长度(m)'] = para['主串调谐区长度']
    data['被串调谐区长度(m)'] = [para['被串调谐区长度'][index_bei], para['被串调谐区长度'][index_bei+1]]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = df_input['耦合系数(μH/km)']

    # 区段频率
    # para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率(Hz)']
    # para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率(Hz)']
    # freq = freq1
    # data['freq'] = para['freq'] = Freq(freq1)
    # para['主串频率列表'] = [Freq(freq1)]
    # para['被串频率列表'] = [Freq(freq2)]

    para['freq_主'] = data['主串频率(Hz)'] = df_input['主串频率(Hz)'][0]
    para['freq_被'] = data['被串频率(Hz)'] = df_input['被串频率(Hz)'][index_bei]
    freq = para['freq_主']
    data['freq'] = para['freq'] = Freq(freq)

    para['主串频率列表'] = list(map(lambda x: Freq(x), df_input['主串频率(Hz)']))
    para['被串频率列表'] = list(map(lambda x: Freq(x), df_input['被串频率(Hz)']))

    # 电容数量
    # data['主串电容数量列表'] = para['主串电容数'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = para['被串电容数'] = c_pack_bei['电容数量列表']

    # c_num1 = df_input['主串电容数(含TB)']
    # c_num2 = df_input['被串电容数(含TB)']
    #
    # data['主串电容数量列表'] = para['主串电容数'] = [c_num1]
    # data['被串电容数量列表'] = para['被串电容数'] = [c_num2]
    #
    # data['主串电容数(含TB)'] = c_num1
    # data['被串电容数(含TB)'] = c_num2

    data['主串电容数量列表'] = para['主串电容数'] = df_input['主串电容数(含TB)']
    data['被串电容数量列表'] = para['被串电容数'] = df_input['被串电容数(含TB)']
    data['主串电容数(含TB)'] = df_input['主串电容数(含TB)'][0]
    data['被串电容数(含TB)'] = df_input['被串电容数(含TB)'][index_bei]

    # 电容容值
    # data['主串电容值(μF)'] = df_input['主串电容值(μF)']
    # data['被串电容值(μF)'] = df_input['被串电容值(μF)']
    #
    # # data['主串电容数量列表'] = c_pack_zhu['电容数量列表']
    # # data['被串电容数量列表'] = c_pack_bei['电容数量列表']
    #
    # # data['主串电容容值列表'] = [25]
    # # data['被串电容容值列表'] = [25]
    #
    # val_tmp_zhu = data['主串电容值(μF)'] * 1e-6
    # val_tmp_bei = data['被串电容值(μF)'] * 1e-6
    #
    # c_imp_zhu = ImpedanceMultiFreq()
    # c_imp_zhu.rlc_s = {
    #     1700: [10e-3, None, val_tmp_zhu],
    #     2000: [10e-3, None, val_tmp_zhu],
    #     2300: [10e-3, None, val_tmp_zhu],
    #     2600: [10e-3, None, val_tmp_zhu]}
    #
    # c_imp_bei = ImpedanceMultiFreq()
    # c_imp_bei.rlc_s = {
    #     1700: [10e-3, None, val_tmp_bei],
    #     2000: [10e-3, None, val_tmp_bei],
    #     2300: [10e-3, None, val_tmp_bei],
    #     2600: [10e-3, None, val_tmp_bei]}
    #
    # para['主串容值列表'] = [c_imp_zhu]
    # para['被串容值列表'] = [c_imp_bei]

    data['主串电容值(μF)'] = df_input['主串电容值(μF)'][0]
    data['被串电容值(μF)'] = df_input['被串电容值(μF)'][index_bei]
    para['主串容值列表'] = list(map(lambda x: get_c_imp(x), df_input['主串电容值(μF)']))
    para['被串容值列表'] = list(map(lambda x: get_c_imp(x), df_input['被串电容值(μF)']))

    # 区段类型
    type_table = {
        '2000A': '2000A区间',
        '2000A_25Hz_Coding': '2000A叠加电码化',
    }

    para['主串区段类型'] = df_input['主串区段类型']
    para['被串区段类型'] = df_input['被串区段类型']
    data['主串区段类型'] = type_table[df_input['主串区段类型'][0]]
    data['被串区段类型'] = type_table[df_input['被串区段类型'][index_bei]]

    # 道床电阻
    data['主串道床电阻(Ω·km)'] = df_input['主串道床电阻(Ω·km)']
    data['被串道床电阻(Ω·km)'] = df_input['被串道床电阻(Ω·km)']

    para['主串道床电阻'] = Constant(df_input['主串道床电阻(Ω·km)'])
    para['被串道床电阻'] = Constant(df_input['被串道床电阻(Ω·km)'])

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

    # data['占车分路电阻(Ω)'] = para['占车分路电阻'] = 1e-7
    # data['占车分路电阻(Ω)'] = para['占车分路电阻'] = 1e10
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
    data['分路起点'] = df_input['分路起点']
    data['分路终点'] = df_input['分路终点']
    # data['分路起点'] = 0
    # data['分路终点'] = 613

    # data['占车位置(m)'] = df_input['占车位置(m)']

    # # TB模式
    data['主串TB模式'] = para['主串TB模式'] = '无TB'
    data['被串TB模式'] = para['被串TB模式'] = '无TB'

    #################################################################################

    # 电码化配置

    # # 发码方向
    # if pd_read_flag:
    #     data['发码继电器状态'] = df_input['发码继电器状态']
    # else:
    #     # data['发码继电器状态'] = 1
    #     data['发码继电器状态'] = 0

    data['被串是否发码'] = df_input['被串是否发码']
    if data['被串是否发码'] == '否':
        data['被串是否发码'] = para['sr_mod_被'] = '不发码'

    #################################################################################

    # FT1-U参数
    # data['FT1-U短路阻抗-Rs(Ω)'] = value_r1 = df_input['FT1-U短路阻抗-Rs(Ω)'][temp_temp]
    # data['FT1-U短路阻抗-Ls(mH)'] = value_l1 = df_input['FT1-U短路阻抗-Ls(mH)'][temp_temp]
    # data['FT1-U开路阻抗-Rs(Ω)'] = value_r2 = df_input['FT1-U开路阻抗-Rs(Ω)'][temp_temp]
    # data['FT1-U开路阻抗-Ls(H)'] = value_l2 = df_input['FT1-U开路阻抗-Ls(H)'][temp_temp]
    #
    # value_l1 = value_l1 * 1e-3
    # para['zm_FT1u_25Hz_Coding'].rlc_s = {
    #     1700: [value_r2, value_l2, None],
    #     2000: [value_r2, value_l2, None],
    #     2300: [value_r2, value_l2, None],
    #     2600: [value_r2, value_l2, None]}
    #
    # para['zs_FT1u_25Hz_Coding'].rlc_s = {
    #     1700: [value_r1, value_l1, None],
    #     2000: [value_r1, value_l1, None],
    #     2300: [value_r1, value_l1, None],
    #     2600: [value_r1, value_l1, None]}

    data['FT1-U二次侧输出电压(V)'] = df_input['FT1-U二次侧输出电压(V)']

    value_n = 170 / data['FT1-U二次侧输出电压(V)']
    para['n_FT1u_25Hz_Coding'] = {
        1700: value_n,
        2000: value_n,
        2300: value_n,
        2600: value_n}

    #################################################################################

    # data['主串FT1U输出电压(V)'] = df_input['主串FT1U输出电压(V)']
    # data['被串FT1U输出电压(V)'] = df_input['被串FT1U输出电压(V)']
    #
    # r1 = data['主串调整电阻(Ω)'] = df_input['主串调整电阻(Ω)']
    # r2 = data['被串调整电阻(Ω)'] = df_input['被串调整电阻(Ω)']
    #
    # n1 = 170 / data['主串FT1U输出电压(V)']
    # n2 = 170 / data['被串FT1U输出电压(V)']
    #
    # para['主串FT1U变比'] = {
    #     1700: n1,
    #     2000: n1,
    #     2300: n1,
    #     2600: n1}
    # para['被串FT1U变比'] = {
    #     1700: n2,
    #     2000: n2,
    #     2300: n2,
    #     2600: n2}
    #
    # para['主串调整阻抗'] = ImpedanceMultiFreq()
    # para['主串调整阻抗'].rlc_s = {
    #     1700: [r1, None, None],
    #     2000: [r1, None, None],
    #     2300: [r1, None, None],
    #     2600: [r1, None, None],
    # }
    # para['被串调整阻抗'] = ImpedanceMultiFreq()
    # para['被串调整阻抗'].rlc_s = {
    #     1700: [r2, None, None],
    #     2000: [r2, None, None],
    #     2300: [r2, None, None],
    #     2600: [r2, None, None],
    # }

    # 设备参数
    data['调整电阻(Ω)'] = rt = df_input['调整电阻(Ω)']
    data['调整电感(H)'] = lt = df_input['调整电感(H)']
    data['调整电容(F)'] = ct = df_input['调整电容(F)']
    data['调整RLC模式'] = mode_rlc = df_input['调整RLC模式']

    # data['调整电阻(Ω)'] = Rt = 50
    # data['调整电感(H)'] = Lt = None
    # data['调整电容(F)'] = Ct = None
    # data['调整RLC模式'] = mode_rlc = '串联'

    zt = {
        1700: [rt, lt, ct],
        2000: [rt, lt, ct],
        2300: [rt, lt, ct],
        2600: [rt, lt, ct],
    }

    if mode_rlc == '串联':
        para['Rt_25Hz_Coding'].rlc_s = zt
    elif mode_rlc == '并联':
        para['Rt_25Hz_Coding'].rlc_p = zt

    #################################################################################

    # 室内隔离盒
    data['NGL-C1(μF)'] = value_c = df_input['NGL-C1(μF)']
    # data['NGL-C1(μF)'] = value_c = 1

    value_c = value_c * 1e-6
    para['C1_NGL_25Hz_Coding'].rlc_s = {
        1700: [None, None, value_c],
        2000: [None, None, value_c],
        2300: [None, None, value_c],
        2600: [None, None, value_c]}

    #################################################################################

    # 室外隔离盒
    data['WGL-C1(μF)'] = value_c1 = df_input['WGL-C1(μF)']
    data['WGL-C2(μF)'] = value_c2 = df_input['WGL-C2(μF)']
    data['WGL-L1-R(Ω)'] = value_r1 = df_input['WGL-L1-R(Ω)']
    data['WGL-L1-L(H)'] = value_l1 = df_input['WGL-L1-L(H)']
    data['WGL-L2-R(Ω)'] = value_r2 = df_input['WGL-L2-R(Ω)']
    data['WGL-L2-L(mH)'] = value_l2 = df_input['WGL-L2-L(mH)']
    data['WGL-BPM变比'] = value_n = df_input['WGL-BPM变比']

    # data['WGL-C1(μF)'] = value_c1 = 1
    # data['WGL-C2(μF)'] = value_c2 = 20
    # data['WGL-L1-R(Ω)'] = value_r1 = None
    # data['WGL-L1-L(H)'] = value_l1 = 0.5
    # data['WGL-L2-R(Ω)'] = value_r2 = None
    # data['WGL-L2-L(mH)'] = value_l2 = 5
    # data['WGL-BPM变比'] = value_n = 4

    value_c1 = value_c1 * 1e-6
    value_c2 = value_c2 * 1e-6
    value_l2 = value_l2 * 1e-3

    para['C1_WGL_25Hz_Coding'].rlc_s = {
        1700: [None, None, value_c1],
        2000: [None, None, value_c1],
        2300: [None, None, value_c1],
        2600: [None, None, value_c1]}

    para['C2_WGL_25Hz_Coding'].rlc_s = {
        1700: [None, None, value_c2],
        2000: [None, None, value_c2],
        2300: [None, None, value_c2],
        2600: [None, None, value_c2]}

    para['L1_WGL_25Hz_Coding'].rlc_s = {
        1700: [value_r1, value_l1, None],
        2000: [value_r1, value_l1, None],
        2300: [value_r1, value_l1, None],
        2600: [value_r1, value_l1, None]}

    para['L2_WGL_25Hz_Coding'].rlc_s = {
        1700: [value_r2, value_l2, None],
        2000: [value_r2, value_l2, None],
        2300: [value_r2, value_l2, None],
        2600: [value_r2, value_l2, None]}

    para['n_WGL_25Hz_Coding'] = {
        1700: value_n,
        2000: value_n,
        2300: value_n,
        2600: value_n}

    #################################################################################

    # 扼流变压器
    data['扼流变压器变比'] = value_n = df_input['扼流变压器变比']
    data['BE-Rm(Ω)'] = value_r = df_input['BE-Rm(Ω)']
    data['BE-Lm(H)'] = value_l = df_input['BE-Lm(H)']

    # data['扼流变压器变比'] = value_n = 3
    # data['BE-Rm(Ω)'] = value_r = 110
    # data['BE-Lm(H)'] = value_l = 0.024

    para['n_EL_25Hz_Coding'] = {
        1700: value_n,
        2000: value_n,
        2300: value_n,
        2600: value_n}

    para['zm_EL_25Hz_Coding'].rlc_s = {
        1700: [value_r, value_l, None],
        2000: [value_r, value_l, None],
        2300: [value_r, value_l, None],
        2600: [value_r, value_l, None]}


def get_c_imp(value):
    c_value = value * 1e-6
    ret = ImpedanceMultiFreq()
    ret.rlc_s = {
        1700: [10e-3, None, c_value],
        2000: [10e-3, None, c_value],
        2300: [10e-3, None, c_value],
        2600: [10e-3, None, c_value]}
    return ret


class PreModel_20260703_25hz_2000a_mix(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)

        self.train1['分路电阻1'].z = para['被串分路电阻']
        self.train2['分路电阻1'].z = para['主串分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=para['主串区段数'],
                           m_frqs=para['主串频率列表'],
                           m_lens=para['主串区段长度'],
                           j_lens=para['主串调谐区长度'],
                           m_typs=para['主串区段类型'],
                           c_nums=para['主串电容数'],
                           sr_mods=[para['sr_mod_主']]*para['主串区段数'],
                           send_lvs=[send_level]*para['主串区段数'],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        freq_tmp = Freq(para['freq_被'])
        freq_tmp.change_freq()

        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=para['被串区段数'],
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=para['被串调谐区长度'],
                           m_typs=para['被串区段类型'],
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']]*para['被串区段数'],
                           send_lvs=[send_level]*para['被串区段数'],
                           parameter=parameter)

        # sg3['区段1'].load_TB_mode(para['主串TB模式'])
        # sg4['区段1'].load_TB_mode(para['被串TB模式'])
        # sg3.refresh()
        # sg4.refresh()

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()

        # self.change_para_el()
        # self.change_cable_length()
        self.change_adjust_para()
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

    def change_adjust_para(self):
        para = self.parameter
        for index, sec in enumerate(self.section_group3.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, ZPW2000A_ZN_25Hz_Coding):
                    ele['4Cab'].length = para['主串电缆长度']
                if isinstance(ele, ZPW2000A_QJ_Normal):
                    ele['3Cab'].length = para['主串电缆长度']

        for index, sec in enumerate(self.section_group4.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, ZPW2000A_ZN_25Hz_Coding):
                    ele['4Cab'].length = para['被串电缆长度']
                if isinstance(ele, ZPW2000A_QJ_Normal):
                    ele['3Cab'].length = para['被串电缆长度']

    def change_r_shunt(self):
        para = self.parameter
        self.train1['分路电阻1'].z = para['被串分路电阻']
        self.train2['分路电阻1'].z = para['主串分路电阻']


if __name__ == '__main__':
    pass
