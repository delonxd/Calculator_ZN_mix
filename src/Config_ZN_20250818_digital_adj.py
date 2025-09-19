from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant
from src.FrequencyType import Freq

from src.Module.TcsrLib import ZPW2000A_ZN_Digital_adj
from src.Module.OutsideElement import CapC
from src.Module.JumperWire import JumperWire

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line

from src.Model.PreModel import PreModel
from src.Model.MainModel import MainModel

from src.Method import config_jumpergroup
from src.Method import get_i_trk

import math
import pandas as pd
import numpy as np

# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimSun']
# plt.rcParams['mathtext.fontset'] = 'stix'
# plt.rcParams['axes.unicode_minus'] = False


########################################################################################################################

# 配置输入
def config_input_20250818_digital(mode):

    if mode == '一送一受':
        columns = [
            '区段名称',
            '钢轨类型',
            '载频频率(Hz)',
            '电缆长度(km)',
            '送端实际电缆长度(km)',
            '受端实际电缆长度(km)',
            '室外传输单元变比',
            'Rf(Ω)',
            'rd  (Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',
        ]

        path = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——一送一受.xlsx'
        df_input = pd.read_excel(path)

        df = df_input.iloc[:, :13]
        df = df.drop(df.columns[2], axis=1)
        df = df.drop([0, 1, 2], axis=0)
        df.columns = columns
        df['序号'] = range(1, df.shape[0]+1)
        df['备注'] = ''
        df['功出电平级'] = 1

    elif mode == '两送一受':
        columns = [
            '区段名称',
            '钢轨类型',
            '载频1频率(Hz)',
            '载频2频率(Hz)',
            '电缆长度(km)',
            '送端1实际电缆长度(km)',
            '送端2实际电缆长度(km)',
            '受端实际电缆长度(km)',
            '送端BE变比',
            '受端BE变比',
            'Rf(Ω)',
            'rd  (Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',
        ]

        path = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——两送一受.xlsx'
        df_input = pd.read_excel(path)

        df = df_input.iloc[:, :16]
        df = df.drop(df.columns[2], axis=1)
        df = df.drop([0, 1, 2], axis=0)
        df.columns = columns

        df_tmp = df

        columns = [
            '区段名称',
            '钢轨类型',
            '载频频率(Hz)',
            '电缆长度(km)',
            '本载频端实际电缆长度(km)',
            '非载频端实际电缆长度(km)',
            '受端实际电缆长度(km)',
            '室外传输单元变比',
            'Rf(Ω)',
            'rd  (Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',
        ]

        df = pd.DataFrame(columns=columns)

        counter = 0
        for num, row in df_tmp.iterrows():
            counter += 1
            s0 = row.copy()
            s0['载频频率(Hz)'] = s0['载频1频率(Hz)']
            s0['本载频端实际电缆长度(km)'] = s0['送端1实际电缆长度(km)']
            s0['非载频端实际电缆长度(km)'] = s0['送端2实际电缆长度(km)']
            s0['室外传输单元变比'] = s0['送端BE变比']
            s0 = s0.reindex(columns)
            df = pd.concat([df, pd.DataFrame(s0).T], axis=0)

            counter += 1
            s0 = row.copy()
            s0['载频频率(Hz)'] = s0['载频2频率(Hz)']
            s0['本载频端实际电缆长度(km)'] = s0['送端2实际电缆长度(km)']
            s0['非载频端实际电缆长度(km)'] = s0['送端1实际电缆长度(km)']
            s0['室外传输单元变比'] = s0['送端BE变比']
            s0 = s0.reindex(columns)
            df = pd.concat([df, pd.DataFrame(s0).T], axis=0)

        df['序号'] = range(1, df.shape[0]+1)
        df['备注'] = ''
        df['功出电平级'] = 1

    elif mode == '一送两受':
        columns = [
            '区段名称',
            '钢轨类型',
            '载频频率(Hz)',
            '电缆长度(km)',
            '送端实际电缆长度(km)',
            '受端1实际电缆长度(km)',
            '受端2实际电缆长度(km)',
            'BE变比',
            'Rf(Ω)',
            'rd  (Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',
            '岔尖位置',
            '岔尾位置',
        ]

        path = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——一送两受.xlsx'
        df_input = pd.read_excel(path)

        df = df_input.iloc[:, :16]
        df = df.drop(df.columns[2], axis=1)
        df = df.drop([0, 1, 2], axis=0)
        df.columns = columns

        df_tmp = df

        columns = [
            '区段名称',
            '钢轨类型',
            '载频频率(Hz)',
            '电缆长度(km)',
            '送端实际电缆长度(km)',
            '受端1实际电缆长度(km)',
            '受端2实际电缆长度(km)',
            '室外传输单元变比',
            'Rf(Ω)',
            'rd  (Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',
            '岔尖位置',
            '岔尾位置',
        ]

        df = pd.DataFrame(columns=columns)

        counter = 0
        for num, row in df_tmp.iterrows():
            counter += 1
            s0 = row.copy()
            s0['室外传输单元变比'] = s0['BE变比']
            s0 = s0.reindex(columns)
            df = pd.concat([df, pd.DataFrame(s0).T], axis=0)

            counter += 1
            s0 = row.copy()
            len1 = s0['送端实际电缆长度(km)']
            len2 = s0['受端1实际电缆长度(km)']
            s0['受端1实际电缆长度(km)'] = len1
            s0['送端实际电缆长度(km)'] = len2
            s0['室外传输单元变比'] = s0['BE变比']
            posi1 = s0['轨道电路长度(m)'] - s0['岔尖位置']
            posi2 = s0['轨道电路长度(m)'] - s0['岔尾位置']
            s0['岔尖位置'] = posi1
            s0['岔尾位置'] = posi2

            s0 = s0.reindex(columns)
            df = pd.concat([df, pd.DataFrame(s0).T], axis=0)

        df['序号'] = range(1, df.shape[0]+1)
        df['备注'] = ''
        df['功出电平级'] = 1

    else:
        raise KeyboardInterrupt('送受模式错误')

    print(df)
    return df


########################################################################################################################

# 配置表头
def config_headlist_20250818_digital(mode):
    if mode == '一送一受':
        head_list = [
            '区段名称',
            '钢轨类型',
            '载频频率(Hz)',
            '电缆长度(km)',
            '送端实际电缆长度(km)',
            '受端实际电缆长度(km)',
            '室外传输单元变比',
            '分路电阻(Ω)',
            '道床电阻(Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',
            '岔尖位置',
            '岔尾位置',

            '功出电平级',
            'Krv',

            '接收端_Vr1r2轨出_min(V)',
            '接收端_Vr1r2轨出_max(V)',

            '接收端_Vv1v2轨入_min(V)',
            '接收端_Vv1v2轨入_max(V)',

            '接收端_轨面电压_min(V)',
            '接收端_轨面电压_max(V)',

            '发送端_轨面电压_min(V)',
            '发送端_轨面电压_max(V)',

            '发送端_功出电压_min(V)',
            '发送端_功出电压_max(V)',

            '发送端_功出电流_min(A)',
            '发送端_功出电流_max(A)',

            '最小机车电流(A)',
            '最大分路残压(V)',
            '最大功出电流(A)',
        ]

    elif mode == '两送一受':
        head_list = [
            '区段名称',
            '钢轨类型',
            '载频频率(Hz)',
            '电缆长度(km)',
            '本载频端实际电缆长度(km)',
            '非载频端实际电缆长度(km)',
            '受端实际电缆长度(km)',
            '室外传输单元变比',
            '分路电阻(Ω)',
            '道床电阻(Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',

            '功出电平级',
            'Krv',

            '接收端_Vr1r2轨出_min(V)',
            '接收端_Vr1r2轨出_max(V)',

            '接收端_Vv1v2轨入_min(V)',
            '接收端_Vv1v2轨入_max(V)',

            '接收端_轨面电压_min(V)',
            '接收端_轨面电压_max(V)',

            '发送端_轨面电压_min(V)',
            '发送端_轨面电压_max(V)',

            '发送端_功出电压_min(V)',
            '发送端_功出电压_max(V)',

            '发送端_功出电流_min(A)',
            '发送端_功出电流_max(A)',

            '最小机车电流(A)',
            '最大分路残压(V)',
            '最大功出电流(A)',
        ]

    elif mode == '一送两受':
        head_list = [
            '区段名称',
            '钢轨类型',
            '载频频率(Hz)',
            '电缆长度(km)',
            '送端实际电缆长度(km)',
            '受端1实际电缆长度(km)',
            '受端2实际电缆长度(km)',
            '室外传输单元变比',
            '分路电阻(Ω)',
            '道床电阻(Ω·km)',
            '补偿电容(μF)',
            '轨道电路长度(m)',
            '补偿电容总个数',

            '功出电平级',
            'Krv1',
            'Krv2',

            '接收端1_Vr1r2轨出_min(V)',
            '接收端1_Vr1r2轨出_max(V)',

            '接收端1_Vv1v2轨入_min(V)',
            '接收端1_Vv1v2轨入_max(V)',

            '接收端1_轨面电压_min(V)',
            '接收端1_轨面电压_max(V)',

            '接收端2_Vr1r2轨出_min(V)',
            '接收端2_Vr1r2轨出_max(V)',

            '接收端2_Vv1v2轨入_min(V)',
            '接收端2_Vv1v2轨入_max(V)',

            '接收端2_轨面电压_min(V)',
            '接收端2_轨面电压_max(V)',

            '发送端_轨面电压_min(V)',
            '发送端_轨面电压_max(V)',

            '发送端_功出电压_min(V)',
            '发送端_功出电压_max(V)',

            '发送端_功出电流_min(A)',
            '发送端_功出电流_max(A)',

            '最小机车电流(A)',
            '最大分路残压1(V)',
            '最大分路残压2(V)',
            '最大功出电流(A)',
        ]
    else:
        raise KeyboardInterrupt('送受模式错误')

    return head_list


########################################################################################################################

# 配置行数据
def config_row_data_digital_adj(df_input, para, data, mode):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = df_input['备注']

    # 区段名
    data['区段名称'] = para['区段名称'] = df_input['区段名称']

    # 区段长度
    length1 = data['轨道电路长度(m)'] = df_input['轨道电路长度(m)']
    para['区段长度'] = [length1]

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = 10

    # 区段频率
    para['freq_主'] = freq = data['载频频率(Hz)'] = df_input['载频频率(Hz)']
    data['freq'] = para['freq'] = Freq(freq)
    para['频率列表'] = [Freq(freq)]

    # 电容数量
    data['补偿电容总个数'] = c_num1 = df_input['补偿电容总个数']
    data['电容数量列表'] = para['电容数'] = [c_num1]

    # 电容容值
    data['补偿电容(μF)'] = df_input['补偿电容(μF)']

    val_tmp = data['补偿电容(μF)'] * 1e-6
    c_imp = ImpedanceMultiFreq()
    c_imp.rlc_s = {
        1700: [10e-3, None, val_tmp],
        2000: [10e-3, None, val_tmp],
        2300: [10e-3, None, val_tmp],
        2600: [10e-3, None, val_tmp]}
    para['电容容值列表'] = [c_imp]

    # 道床电阻
    data['道床电阻(Ω·km)'] = df_input['rd  (Ω·km)']
    para['道床电阻'] = Constant(data['道床电阻(Ω·km)'])
    para['Rd'].value = data['道床电阻(Ω·km)']

    # 钢轨阻抗
    data['钢轨类型'] = trk_type = df_input['钢轨类型']

    if trk_type == 21:
        trk_21 = ImpedanceMultiFreq()
        trk_21.rlc_s = {
            1700: [1.177, 1.314e-3, None],
            2000: [1.306, 1.304e-3, None],
            2300: [1.435, 1.297e-3, None],
            2600: [1.558, 1.291e-3, None]}

        para['Trk_z'].rlc_s = trk_21.rlc_s
    else:
        raise KeyboardInterrupt('钢轨类型错误：目前只支持21')

    data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
    data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)
    para['钢轨阻抗'] = para['Trk_z']

    # 电缆参数
    data['电缆电阻最大(Ω/km)'] = 45
    data['电缆电阻最小(Ω/km)'] = 43
    data['电缆电容最大(F/km)'] = 28e-9
    data['电缆电容最小(F/km)'] = 28e-9

    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
    para['Cable_C'].value = data['电缆电容最大(F/km)']

    # 电缆长度
    data['电缆长度(km)'] = para['cab_len'] = para['电缆长度'] = df_input['电缆长度(km)']
    para['cab_len_default'] = 2

    # 1Ω标准电阻
    para['unit_1'] = ImpedanceMultiFreq()
    para['unit_1'].rlc_s = {
        1700: [1, None, None],
        2000: [1, None, None],
        2300: [1, None, None],
        2600: [1, None, None]}

    # 分路电阻
    data['分路电阻(Ω)'] = para['分路电阻'] = para['Rsht_z'] = df_input['Rf(Ω)']

    # 功出电源
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

    data['分路起点'] = 0
    data['分路终点'] = length1

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
    n = 1/1.095
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
        2600: [0.47802, None, 598.01 * 1e-9],
    }
    # 扼流变压器
    data['室外传输单元变比'] = para['变压器变比'] = n = df_input['室外传输单元变比']

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

    freq = data['载频频率(Hz)']
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

    if mode == '一送一受':

        # 发码方向
        data['发码方向'] = para['sr_mod'] = '右发'

        # 电缆长度
        data['电缆长度(km)'] = para['cab_len'] = para['电缆长度'] = df_input['电缆长度(km)']

        data['送端实际电缆长度(km)'] = para['cab_len_s'] = df_input['送端实际电缆长度(km)']
        data['受端实际电缆长度(km)'] = para['cab_len_r'] = df_input['受端实际电缆长度(km)']

        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25

        data['送端补偿电缆长度(km)'] = para['cab_len_s_adj']
        data['受端补偿电缆长度(km)'] = para['cab_len_r_adj']

    elif mode == '两送一受':

        # 发码方向
        data['发码方向'] = para['sr_mod'] = '双端'

        # 电缆长度
        data['电缆长度(km)'] = para['cab_len'] = para['电缆长度'] = df_input['电缆长度(km)']

        data['本载频端实际电缆长度(km)'] = para['cab_len_s1'] = df_input['本载频端实际电缆长度(km)']
        data['非载频端实际电缆长度(km)'] = para['cab_len_s2'] = df_input['非载频端实际电缆长度(km)']
        data['受端实际电缆长度(km)'] = para['cab_len_r'] = df_input['受端实际电缆长度(km)']

        para['cab_len_s1_adj'] = ((para['cab_len'] - para['cab_len_s1']) // 0.25) * 0.25
        para['cab_len_s2_adj'] = ((para['cab_len'] - para['cab_len_s2']) // 0.25) * 0.25
        para['cab_len_r_adj'] = 3.75

        data['本载频端补偿电缆长度(km)'] = para['cab_len_s1_adj']
        data['非载频端补偿电缆长度(km)'] = para['cab_len_s2_adj']
        data['受端补偿电缆长度(km)'] = para['cab_len_r_adj']

    elif mode == '一送两受':

        # 道岔位置
        data['岔尖位置'] = para['岔尖位置'] = df_input['岔尖位置']
        data['岔尾位置'] = df_input['岔尾位置']

        if data['岔尖位置'] > data['岔尾位置']:
            para['岔长'] = data['岔尖位置'] - data['岔尾位置']
            para['道岔相对位置'] = data['岔尾位置']
            para['道岔方向'] = '道岔左接收'
            para['跳线位置'] = para['岔长']
        else:
            para['岔长'] = data['岔尾位置'] - data['岔尖位置']
            para['道岔相对位置'] = data['岔尖位置']
            para['道岔方向'] = '道岔右接收'
            para['跳线位置'] = 0

        # 发码方向
        data['发码方向'] = para['sr_mod'] = '右发'

        # 电缆长度
        data['电缆长度(km)'] = para['cab_len'] = para['电缆长度'] = df_input['电缆长度(km)']

        data['送端实际电缆长度(km)'] = para['cab_len_s'] = df_input['送端实际电缆长度(km)']
        data['受端1实际电缆长度(km)'] = para['cab_len_r'] = df_input['受端1实际电缆长度(km)']
        data['受端2实际电缆长度(km)'] = para['cab_len_r2'] = df_input['受端2实际电缆长度(km)']

        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25
        para['cab_len_r2_adj'] = 3.75

        data['送端补偿电缆长度(km)'] = para['cab_len_s_adj']
        data['受端1补偿电缆长度(km)'] = para['cab_len_r_adj']
        data['受端2补偿电缆长度(km)'] = para['cab_len_r2_adj']

    else:
        raise KeyboardInterrupt('送受模式错误')


########################################################################################################################

# 计算数据
def calculate_row_data_adj(df_input, para, data, data2excel, mode):

    if mode == '一送一受':
        calculate_row_data_adj_1_1(df_input, para, data, data2excel)
    elif mode == '两送一受':
        calculate_row_data_adj_2_1(df_input, para, data, data2excel)
    elif mode == '一送两受':
        calculate_row_data_adj_1_2(df_input, para, data, data2excel)
    else:
        raise KeyboardInterrupt('送受模式错误')


########################################################################################################################

# 获取功出电平级
def get_pwr_level_digital_adj(min_i_trk, freq):
    pwr_list = [132, 117, 102, 90, 80, 70, 54, 47, 40, 27]
    max_current = {
        1700: 0.5,
        2000: 0.5,
        2300: 0.5,
        2600: 0.45,
    }

    ret = 10
    for pwr_u in pwr_list[::-1]:
        i_trk = min_i_trk * pwr_u / 132
        if i_trk >= max_current[freq]:
            break
        ret -= 1
    if ret == 0:
        ret = 1
    i_trk = min_i_trk * pwr_list[ret-1] / 132

    print(ret, i_trk)
    return ret, i_trk


########################################################################################################################

# 配置场景数据 一送一受
def config_sub_para_adj_1_1(para, data, mode):
    if mode == '最小机车电流':
        para['pwr_v_flg'] = '最小'
        para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
        para['cab_len_s_adj'] = para['cab_len'] - para['cab_len_s']
        para['cab_len_r_adj'] = para['cab_len'] - para['cab_len_r']

        rd = data['道床电阻(Ω·km)']
        r_sht = data['分路电阻(Ω)']

    elif mode == '最大分路残压':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25

        rd = 10000
        r_sht = data['分路电阻(Ω)']

    elif mode == '最大功出电流':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25

        rd = data['道床电阻(Ω·km)']
        r_sht = 1e-10

    elif mode == '调整最大轨入':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25

        rd = 10000
        r_sht = 1e10

    elif mode == '调整最小轨入':
        para['pwr_v_flg'] = '最小'
        para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
        para['cab_len_s_adj'] = para['cab_len'] - para['cab_len_s']
        para['cab_len_r_adj'] = para['cab_len'] - para['cab_len_r']

        rd = data['道床电阻(Ω·km)']
        r_sht = 1e10

    else:
        raise KeyboardInterrupt('配置模式错误')

    para['道床电阻'] = Constant(rd)
    para['Rd'].value = rd
    para['分路电阻'] = para['Rsht_z'] = r_sht


# 计算行数据 一送一受
def calculate_row_data_adj_1_1(df_input, para, data, data2excel):
    data2excel.add_new_row()
    config_row_data_digital_adj(df_input, para, data, '一送一受')
    data['功出电平级'] = para['send_level'] = 1

    interval = data['分路间隔(m)']

    #################################################################################

    # 1.计算功出电平级
    config_sub_para_adj_1_1(para, data, '最小机车电流')
    md = PreModel_20250818_ZN_digital_adj_1_1(parameter=para)
    md.add_train()

    flag_l = data['分路起点']
    flag_r = data['分路终点']
    posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

    i_trk_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        m1 = MainModel(md.lg, md=md)

        i_sht = md.lg['线路3']['列车1']['分路电阻1']['I'].value_c
        i_trk = get_i_trk(line=m1['线路3'], posi=posi, direct='右')

        i_trk_list.append(i_trk)

        data2excel.add_data(sheet_name="钢轨电流", data1=i_trk)
        data2excel.add_data(sheet_name="分路电流", data1=i_sht)

    min_i_trk = min(i_trk_list[:-1])
    pwr_level, min_i_trk = get_pwr_level_digital_adj(min_i_trk, data['载频频率(Hz)'])

    data['功出电平级'] = para['send_level'] = pwr_level
    data['最小机车电流(A)'] = min_i_trk

    #################################################################################
    # 2.计算调整状态最小值
    config_sub_para_adj_1_1(para, data, '调整最小轨入')
    md = PreModel_20250818_ZN_digital_adj_1_1(parameter=para)
    MainModel(md.lg, md=md)
    data['发送端_功出电压_min(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
    data['发送端_功出电流_max(A)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
    data['发送端_轨面电压_min(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
    data['接收端_轨面电压_min(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c
    data['接收端_Vv1v2轨入_min(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
    data['接收端_Vr1r2轨出_min(V)'] = 0.24
    data['Krv'] = math.ceil(116 * 0.24 / data['接收端_Vv1v2轨入_min(V)'])

    #################################################################################
    # 3.计算调整状态最大值
    config_sub_para_adj_1_1(para, data, '调整最大轨入')
    md = PreModel_20250818_ZN_digital_adj_1_1(parameter=para)
    MainModel(md.lg, md=md)

    data['发送端_功出电压_max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
    data['发送端_功出电流_min(A)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
    data['发送端_轨面电压_max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
    data['接收端_轨面电压_max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c
    data['接收端_Vv1v2轨入_max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
    data['接收端_Vr1r2轨出_max(V)'] = data['接收端_Vv1v2轨入_max(V)'] * data['Krv'] / 116

    #################################################################################
    # 4.计算分路残压最大值
    config_sub_para_adj_1_1(para, data, '最大分路残压')
    md = PreModel_20250818_ZN_digital_adj_1_1(parameter=para)
    md.add_train()

    flag_l = data['分路起点']
    flag_r = data['分路终点']
    posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

    v_rcv_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        v_rcv = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        v_rcv_list.append(v_rcv)

    max_v_rcv = max(v_rcv_list)
    data['最大分路残压(V)'] = max_v_rcv * data['Krv'] / 116

    #################################################################################
    # 5.计算功出电流最大值
    config_sub_para_adj_1_1(para, data, '最大功出电流')
    md = PreModel_20250818_ZN_digital_adj_1_1(parameter=para)
    md.add_train()

    flag_l = data['分路起点']
    flag_r = data['分路终点']
    posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

    i_pwr_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        i_pwr = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
        i_pwr_list.append(i_pwr)

    max_i_pwr = max(i_pwr_list)
    data['最大功出电流(A)'] = max_i_pwr


########################################################################################################################

# 配置场景数据 两送一受
def config_sub_para_adj_2_1(para, data, mode):
    if mode == '最小机车电流':
        para['pwr_v_flg'] = '最小'
        para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
        para['cab_len_s1_adj'] = para['cab_len'] - para['cab_len_s1']
        para['cab_len_s2_adj'] = para['cab_len'] - para['cab_len_s2']

        rd = data['道床电阻(Ω·km)']
        r_sht = data['分路电阻(Ω)']

    elif mode == '最大分路残压':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s1_adj'] = ((para['cab_len'] - para['cab_len_s1']) // 0.25) * 0.25
        para['cab_len_s2_adj'] = ((para['cab_len'] - para['cab_len_s2']) // 0.25) * 0.25

        rd = 10000
        r_sht = data['分路电阻(Ω)']

    elif mode == '最大功出电流':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s1_adj'] = ((para['cab_len'] - para['cab_len_s1']) // 0.25) * 0.25
        para['cab_len_s2_adj'] = ((para['cab_len'] - para['cab_len_s2']) // 0.25) * 0.25

        rd = data['道床电阻(Ω·km)']
        r_sht = 1e-10

    elif mode == '调整最大轨入':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s1_adj'] = ((para['cab_len'] - para['cab_len_s1']) // 0.25) * 0.25
        para['cab_len_s2_adj'] = ((para['cab_len'] - para['cab_len_s2']) // 0.25) * 0.25

        rd = 10000
        r_sht = 1e10

    elif mode == '调整最小轨入':
        para['pwr_v_flg'] = '最小'
        para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
        para['cab_len_s1_adj'] = para['cab_len'] - para['cab_len_s1']
        para['cab_len_s2_adj'] = para['cab_len'] - para['cab_len_s2']

        rd = data['道床电阻(Ω·km)']
        r_sht = 1e10

    else:
        raise KeyboardInterrupt('配置模式错误')

    para['道床电阻'] = Constant(rd)
    para['Rd'].value = rd
    para['分路电阻'] = para['Rsht_z'] = r_sht


# 计算行数据 两送一受
def calculate_row_data_adj_2_1(df_input, para, data, data2excel):
    data2excel.add_new_row()
    config_row_data_digital_adj(df_input, para, data, '两送一受')
    data['功出电平级'] = para['send_level'] = 1

    interval = data['分路间隔(m)']

    #################################################################################

    # 1.计算功出电平级
    config_sub_para_adj_2_1(para, data, '最小机车电流')
    md = PreModel_20250818_ZN_digital_adj_2_1(parameter=para)
    md.add_train()

    flag_l = data['分路起点']
    flag_r = data['分路终点']
    posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

    i_trk_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        m1 = MainModel(md.lg, md=md)

        i_sht = md.lg['线路3']['列车1']['分路电阻1']['I'].value_c
        i_trk = get_i_trk(line=m1['线路3'], posi=posi, direct='右')

        i_trk_list.append(i_trk)

        data2excel.add_data(sheet_name="钢轨电流", data1=i_trk)
        data2excel.add_data(sheet_name="分路电流", data1=i_sht)

    min_i_trk = min(i_trk_list[:-1])
    pwr_level, min_i_trk = get_pwr_level_digital_adj(min_i_trk, data['载频频率(Hz)'])

    data['功出电平级'] = para['send_level'] = pwr_level
    data['最小机车电流(A)'] = min_i_trk

    #################################################################################
    # 2.计算调整状态最小值
    config_sub_para_adj_2_1(para, data, '调整最小轨入')
    md = PreModel_20250818_ZN_digital_adj_2_1(parameter=para)
    MainModel(md.lg, md=md)
    data['发送端_功出电压_min(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
    data['发送端_功出电流_max(A)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
    data['发送端_轨面电压_min(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
    data['接收端_轨面电压_min(V)'] = md.lg['线路3']['地面']['区段1']['中间接收'].md_list[-1]['U2'].value_c
    data['接收端_Vv1v2轨入_min(V)'] = md.lg['线路3']['地面']['区段1']['中间接收']['1接收器']['U'].value_c
    data['接收端_Vr1r2轨出_min(V)'] = 0.24
    data['Krv'] = math.ceil(116 * 0.24 / data['接收端_Vv1v2轨入_min(V)'])

    #################################################################################
    # 3.计算调整状态最大值
    config_sub_para_adj_2_1(para, data, '调整最大轨入')
    md = PreModel_20250818_ZN_digital_adj_2_1(parameter=para)
    MainModel(md.lg, md=md)

    data['发送端_功出电压_max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
    data['发送端_功出电流_min(A)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
    data['发送端_轨面电压_max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
    data['接收端_轨面电压_max(V)'] = md.lg['线路3']['地面']['区段1']['中间接收'].md_list[-1]['U2'].value_c
    data['接收端_Vv1v2轨入_max(V)'] = md.lg['线路3']['地面']['区段1']['中间接收']['1接收器']['U'].value_c
    data['接收端_Vr1r2轨出_max(V)'] = data['接收端_Vv1v2轨入_max(V)'] * data['Krv'] / 116

    #################################################################################
    # 4.计算分路残压最大值
    config_sub_para_adj_2_1(para, data, '最大分路残压')
    md = PreModel_20250818_ZN_digital_adj_2_1(parameter=para)
    md.add_train()

    flag_l = data['分路起点']
    flag_r = data['分路终点']
    posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

    v_rcv_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        v_rcv = md.lg['线路3']['地面']['区段1']['中间接收']['1接收器']['U'].value_c
        v_rcv_list.append(v_rcv)

    max_v_rcv = max(v_rcv_list)
    data['最大分路残压(V)'] = max_v_rcv * data['Krv'] / 116

    #################################################################################
    # 5.计算功出电流最大值
    config_sub_para_adj_2_1(para, data, '最大功出电流')
    md = PreModel_20250818_ZN_digital_adj_2_1(parameter=para)
    md.add_train()

    flag_l = data['分路起点']
    flag_r = data['分路终点']
    posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

    i_pwr_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        i_pwr = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
        i_pwr_list.append(i_pwr)

    max_i_pwr = max(i_pwr_list)
    data['最大功出电流(A)'] = max_i_pwr


########################################################################################################################

# 配置场景数据 一送两受
def config_sub_para_adj_1_2(para, data, mode):
    if mode == '最小机车电流':
        para['pwr_v_flg'] = '最小'
        para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
        para['cab_len_s_adj'] = para['cab_len'] - para['cab_len_s']
        para['cab_len_r_adj'] = para['cab_len'] - para['cab_len_r']

        rd = data['道床电阻(Ω·km)']
        r_sht = data['分路电阻(Ω)']

    elif mode == '最大分路残压':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25

        rd = 10000
        r_sht = data['分路电阻(Ω)']

    elif mode == '最大功出电流':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25

        rd = data['道床电阻(Ω·km)']
        r_sht = 1e-10

    elif mode == '调整最大轨入':
        para['pwr_v_flg'] = '最大'
        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['cab_len_s_adj'] = ((para['cab_len'] - para['cab_len_s']) // 0.25) * 0.25
        para['cab_len_r_adj'] = ((para['cab_len'] - para['cab_len_r']) // 0.25) * 0.25

        rd = 10000
        r_sht = 1e10

    elif mode == '调整最小轨入':
        para['pwr_v_flg'] = '最小'
        para['Cable_R'].value = data['电缆电阻最大(Ω/km)']
        para['cab_len_s_adj'] = para['cab_len'] - para['cab_len_s']
        para['cab_len_r_adj'] = para['cab_len'] - para['cab_len_r']

        rd = data['道床电阻(Ω·km)']
        r_sht = 1e10

    else:
        raise KeyboardInterrupt('配置模式错误')

    para['道床电阻'] = Constant(rd)
    para['Rd'].value = rd
    para['分路电阻'] = para['Rsht_z'] = r_sht


# 计算行数据 一送两受
def calculate_row_data_adj_1_2(df_input, para, data, data2excel):
    data2excel.add_new_row()
    config_row_data_digital_adj(df_input, para, data, '一送两受')

    data['功出电平级'] = para['send_level'] = 1
    interval = data['分路间隔(m)']

    if para['道岔方向'] == '道岔右接收':
        turnout_tcsr = '右调谐单元'
        turnout_direct = '左'
        turnout_posi_list = np.arange(data['岔尾位置'], data['岔尖位置'], -interval)

    elif para['道岔方向'] == '道岔左接收':
        turnout_tcsr = '左调谐单元'
        turnout_direct = '右'
        turnout_posi_list = np.arange(data['岔尾位置'], data['岔尖位置'], +interval)

    else:
        raise KeyboardInterrupt()

    #################################################################################

    # 1.计算功出电平级
    config_sub_para_adj_1_2(para, data, '最小机车电流')

    #################################################################################
    # 股道分路
    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    para['列车位置'] = '股道'
    md.add_train()

    posi_list = np.arange(data['分路起点'], data['分路终点'], +interval)

    i_trk_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        m1 = MainModel(md.lg, md=md)

        i_sht = md.lg['线路3']['列车1']['分路电阻1']['I'].value_c
        i_trk = get_i_trk(line=m1['线路3'], posi=posi, direct='右')

        i_trk_list.append(i_trk)

        data2excel.add_data(sheet_name="钢轨电流", data1=i_trk)
        data2excel.add_data(sheet_name="分路电流", data1=i_sht)

    #################################################################################
    # 道岔分路

    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    para['列车位置'] = '道岔'
    md.add_train()

    for posi in turnout_posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        m1 = MainModel(md.lg, md=md)

        i_sht = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c
        i_trk = get_i_trk(line=m1['线路4'], posi=posi, direct=turnout_direct)

        i_trk_list.append(i_trk)

        data2excel.add_data(sheet_name="钢轨电流", data1=i_trk)
        data2excel.add_data(sheet_name="分路电流", data1=i_sht)

    min_i_trk = min(i_trk_list)
    pwr_level, min_i_trk = get_pwr_level_digital_adj(min_i_trk, data['载频频率(Hz)'])

    data['功出电平级'] = para['send_level'] = pwr_level
    data['最小机车电流(A)'] = min_i_trk

    #################################################################################
    # 2.计算调整状态最小值
    config_sub_para_adj_1_2(para, data, '调整最小轨入')
    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    MainModel(md.lg, md=md)
    data['发送端_功出电压_min(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
    data['发送端_功出电流_max(A)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
    data['发送端_轨面电压_min(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c

    data['接收端1_轨面电压_min(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c
    data['接收端1_Vv1v2轨入_min(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
    data['接收端1_Vr1r2轨出_min(V)'] = 0.24
    data['Krv1'] = math.ceil(116 * 0.24 / data['接收端1_Vv1v2轨入_min(V)'])

    data['接收端2_轨面电压_min(V)'] = md.lg['线路4']['地面']['区段1'][turnout_tcsr].md_list[-1]['U2'].value_c
    data['接收端2_Vv1v2轨入_min(V)'] = md.lg['线路4']['地面']['区段1'][turnout_tcsr]['1接收器']['U'].value_c
    data['接收端2_Vr1r2轨出_min(V)'] = 0.24
    data['Krv2'] = math.ceil(116 * 0.24 / data['接收端2_Vv1v2轨入_min(V)'])

    #################################################################################
    # 3.计算调整状态最大值
    config_sub_para_adj_1_2(para, data, '调整最大轨入')
    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    MainModel(md.lg, md=md)

    data['发送端_功出电压_max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
    data['发送端_功出电流_min(A)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
    data['发送端_轨面电压_max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c

    data['接收端1_轨面电压_max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c
    data['接收端1_Vv1v2轨入_max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
    data['接收端1_Vr1r2轨出_max(V)'] = data['接收端1_Vv1v2轨入_max(V)'] * data['Krv1'] / 116

    data['接收端2_轨面电压_max(V)'] = md.lg['线路4']['地面']['区段1'][turnout_tcsr].md_list[-1]['U2'].value_c
    data['接收端2_Vv1v2轨入_max(V)'] = md.lg['线路4']['地面']['区段1'][turnout_tcsr]['1接收器']['U'].value_c
    data['接收端2_Vr1r2轨出_max(V)'] = data['接收端2_Vv1v2轨入_max(V)'] * data['Krv2'] / 116

    #################################################################################
    # 4.计算分路残压最大值
    config_sub_para_adj_1_2(para, data, '最大分路残压')
    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    para['列车位置'] = '股道'
    md.add_train()

    posi_list = np.arange(data['分路起点'], data['分路终点'] + 0.0001, +interval)

    v_rcv_list1 = []
    v_rcv_list2 = []

    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        v_rcv1 = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        v_rcv2 = md.lg['线路4']['地面']['区段1'][turnout_tcsr]['1接收器']['U'].value_c
        v_rcv_list1.append(v_rcv1)
        v_rcv_list2.append(v_rcv2)

    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    para['列车位置'] = '道岔'
    md.add_train()

    for posi in turnout_posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        v_rcv1 = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        v_rcv2 = md.lg['线路4']['地面']['区段1'][turnout_tcsr]['1接收器']['U'].value_c
        v_rcv_list1.append(v_rcv1)
        v_rcv_list2.append(v_rcv2)

    max_v_rcv1 = max(v_rcv_list1)
    max_v_rcv2 = max(v_rcv_list2)
    data['最大分路残压1(V)'] = max_v_rcv1 * data['Krv1'] / 116
    data['最大分路残压2(V)'] = max_v_rcv2 * data['Krv2'] / 116

    #################################################################################
    # 5.计算功出电流最大值
    config_sub_para_adj_1_2(para, data, '最大功出电流')
    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    para['列车位置'] = '股道'
    md.add_train()

    posi_list = np.arange(data['分路起点'], data['分路终点'] + 0.0001, +interval)

    i_pwr_list = []
    for posi in posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        i_pwr = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
        i_pwr_list.append(i_pwr)

    md = PreModel_20250818_ZN_digital_adj_1_2(parameter=para)
    para['列车位置'] = '道岔'
    md.add_train()

    for posi in turnout_posi_list:
        para['分路位置'] = posi

        md.train1.posi_rlt = posi
        md.train1.set_posi_abs(0)

        MainModel(md.lg, md=md)

        i_pwr = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
        i_pwr_list.append(i_pwr)

    max_i_pwr = max(i_pwr_list)
    data['最大功出电流(A)'] = max_i_pwr


########################################################################################################################

class PreModel_20250818_ZN_digital_adj_1_1(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train1['分路电阻1'].z = para['分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=para['频率列表'],
                           m_lens=para['区段长度'],
                           j_lens=[0, 0],
                           m_typs=['2000A_ZN_Digital_adj_1_1'],
                           c_nums=para['电容数'],
                           sr_mods=[para['sr_mod']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        self.section_group3 = sg3

        self.change_c_value()
        self.change_cable_length()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])

        self.lg = LineGroup(l3, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for index, sec in enumerate(self.section_group3.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['电容容值列表'][index]

    def add_train(self):
        para = self.parameter
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train1])
        self.l3 = l3

        self.set_rail_para(line=l3, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])

        self.lg = LineGroup(self.l3, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()

    def change_cable_length(self):
        para = self.parameter
        z_unit = para['unit_1'] * para['Cable_R'].value
        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_adj):
                if ele.mode == '发送':
                    ele['2补偿电缆'].z = para['cab_len_s_adj'] * z_unit
                    ele['4实际电缆'].length = para['cab_len_s']
                if ele.mode == '接收':
                    ele['2补偿电缆'].z = para['cab_len_r_adj'] * z_unit
                    ele['4实际电缆'].length = para['cab_len_r']


########################################################################################################################

class PreModel_20250818_ZN_digital_adj_2_1(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train1['分路电阻1'].z = para['分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=para['频率列表'],
                           m_lens=para['区段长度'],
                           j_lens=[0, 0],
                           m_typs=['2000A_ZN_Digital_adj_2_1'],
                           c_nums=para['电容数'],
                           sr_mods=[para['sr_mod']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod'] == '双端':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        self.section_group3 = sg3

        self.change_c_value()
        self.change_cable_length()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])

        self.lg = LineGroup(l3, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for index, sec in enumerate(self.section_group3.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['电容容值列表'][index]

    def add_train(self):
        para = self.parameter
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train1])
        self.l3 = l3

        self.set_rail_para(line=l3, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])

        self.lg = LineGroup(self.l3, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()

    def change_cable_length(self):
        para = self.parameter
        z_unit = para['unit_1'] * para['Cable_R'].value
        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_adj):
                if ele.mode == '发送':
                    if ele.posi_flag == '左':
                        ele['2补偿电缆'].z = para['cab_len_s2_adj'] * z_unit
                        ele['4实际电缆'].length = para['cab_len_s2']
                    if ele.posi_flag == '右':
                        ele['2补偿电缆'].z = para['cab_len_s1_adj'] * z_unit
                        ele['4实际电缆'].length = para['cab_len_s1']

                if ele.mode == '接收':
                    ele['2补偿电缆'].z = para['cab_len_r_adj'] * z_unit
                    ele['4实际电缆'].length = para['cab_len_r']


########################################################################################################################

class PreModel_20250818_ZN_digital_adj_1_2(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train1['分路电阻1'].z = para['分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=para['频率列表'],
                           m_lens=para['区段长度'],
                           j_lens=[0, 0],
                           m_typs=['2000A_ZN_Digital_adj_1_1'],
                           c_nums=para['电容数'],
                           sr_mods=[para['sr_mod']],
                           send_lvs=[send_level],
                           parameter=parameter)

        sg4 = SectionGroup(name_base='地面', posi=para['道岔相对位置'], m_num=1,
                           m_frqs=para['频率列表'],
                           m_lens=[para['岔长']],
                           j_lens=[0, 0],
                           m_typs=['2000A_ZN_Digital_adj_turnout'],
                           c_nums=[0],
                           sr_mods=[para['道岔方向']],
                           send_lvs=[send_level],
                           parameter=parameter)

        ele = JumperWire(parent_ins=sg3['区段1'], name_base='跳线', posi=para['岔尖位置'])
        sg3['区段1'].add_child('跳线', ele)
        ele.set_posi_abs(0)
        self.jumper1 = ele

        ele = JumperWire(parent_ins=sg4['区段1'], name_base='跳线', posi=para['跳线位置'])
        sg4['区段1'].add_child('跳线', ele)
        ele.set_posi_abs(0)
        self.jumper2 = ele

        config_jumpergroup(self.jumper1, self.jumper2)

        flg = para['pwr_v_flg']
        if para['sr_mod'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.change_cable_length()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)

        self.set_rail_para(line=l3, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for index, sec in enumerate(self.section_group3.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['电容容值列表'][index]

    def add_train(self):
        para = self.parameter
        sec = para['列车位置']

        if sec == '股道':
            self.l3 = l3 = Line(name_base='线路3', sec_group=self.section_group3,
                                parameter=para, train=[self.train1])
            self.l4 = l4 = Line(name_base='线路4', sec_group=self.section_group4,
                                parameter=para)
        elif sec == '道岔':
            self.l3 = l3 = Line(name_base='线路3', sec_group=self.section_group3,
                                parameter=para)
            self.l4 = l4 = Line(name_base='线路4', sec_group=self.section_group4,
                                parameter=para, train=[self.train1])
        else:
            raise KeyboardInterrupt('列车位置错误')

        self.set_rail_para(line=l3, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['钢轨阻抗'], rd=para['道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()

    def change_cable_length(self):
        para = self.parameter

        z_unit = para['unit_1'] * para['Cable_R'].value
        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_adj):
                if ele.mode == '发送':
                    ele['2补偿电缆'].z = para['cab_len_s_adj'] * z_unit
                    ele['4实际电缆'].length = para['cab_len_s']
                if ele.mode == '接收':
                    ele['2补偿电缆'].z = para['cab_len_r_adj'] * z_unit
                    ele['4实际电缆'].length = para['cab_len_r']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, ZPW2000A_ZN_Digital_adj):
                if ele.mode == '岔尾':
                    ele['2补偿电缆'].z = para['cab_len_r2_adj'] * z_unit
                    ele['4实际电缆'].length = para['cab_len_r2']


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 10000)

    config_input_20250818_digital('一送两受')
    pass
