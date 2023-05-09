from src.FrequencyType import Freq
from src.ConstantType import *
from src.ImpedanceParaType import *
from src.Method import generate_frqs
import numpy as np


def config_row_data_1128(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '无'

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']

    # 区段长度
    data['主串区段长度(m)'] = para['主串区段长度'] = df_input['主串区段长度(m)']
    data['被串区段长度(m)'] = para['被串区段长度'] = df_input['被串区段长度(m)']

    # 相对位置
    data['调谐区错位(m)'] = df_input['错位']
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    data['主串左端里程标'] = para['offset_zhu'] = 0
    data['被串左端里程标'] = para['offset_bei'] = offset

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = df_input['耦合系数']

    # 区段频率
    data['主串频率(Hz)'] = para['freq_主'] = freq = df_input['主串频率(Hz)']
    data['被串频率(Hz)'] = para['freq_被'] = df_input['被串频率(Hz)']
    data['freq'] = para['freq'] = Freq(freq)

    # 电容数量
    data['主串电容数(含TB)'] = para['主串电容数'] = df_input['主串电容数(含TB)']
    data['被串电容数(含TB)'] = para['被串电容数'] = df_input['被串电容数(含TB)']

    # 电容容值
    data['主串电容值(μF)'] = c_value1 = df_input['主串电容值(μF)']
    data['被串电容值(μF)'] = c_value2 = df_input['被串电容值(μF)']

    c_value1 = c_value1 * 1e-6
    c_value2 = c_value2 * 1e-6

    para['Ccmp_z_change_zhu'].rlc_s = {
        1700: [10e-3, None, c_value1],
        2000: [10e-3, None, c_value1],
        2300: [10e-3, None, c_value1],
        2600: [10e-3, None, c_value1]}
    para['Ccmp_z_change_chuan'].rlc_s = {
        1700: [10e-3, None, c_value2],
        2000: [10e-3, None, c_value2],
        2300: [10e-3, None, c_value2],
        2600: [10e-3, None, c_value2]}

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
        str(para['机车信号比例V']) + '/' + str(para['机车信号比例I'][para['freq_主']])
    para['机车信号系数值'] = para['机车信号比例V'] / para['机车信号比例I'][para['freq_主']]

    # 分路间隔
    data['分路间隔(m)'] = df_input['分路间隔(m)']
    data['分路起点'] = df_input['分路起点']
    data['分路终点'] = df_input['分路终点']


def config_c_value_20230426(freq: Freq):
    d_temp = {
        1700: 55,
        2000: 50,
        2300: 46,
        2600: 40,
    }
    value = d_temp.get(freq.value)
    if value is None:
        raise KeyboardInterrupt('区段频率错误')
    value = value * 1e-6

    ret = ImpedanceMultiFreq()
    ret.rlc_s = {
        1700: [10e-3, None, value],
        2000: [10e-3, None, value],
        2300: [10e-3, None, value],
        2600: [10e-3, None, value]}
    return ret


def config_imp(mode, val1, val2, val3):
    ret = ImpedanceMultiFreq()
    if mode == 'rlc_s':
        ret.rlc_s = {
            1700: [val1, val2, val3],
            2000: [val1, val2, val3],
            2300: [val1, val2, val3],
            2600: [val1, val2, val3]}
    elif mode == 'rlc_p':
        ret.rlc_p = {
            1700: [val1, val2, val3],
            2000: [val1, val2, val3],
            2300: [val1, val2, val3],
            2600: [val1, val2, val3]}
    else:
        raise KeyboardInterrupt('config_imp 模式错误')
    return ret


def config_n(value_n):
    ret = {
        1700: value_n,
        2000: value_n,
        2300: value_n,
        2600: value_n}
    return ret


def config_row_data_20230426(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '无'

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['主串区段长度(m)']
    length2 = data['被串区段长度(m)'] = df_input['被串区段长度(m)']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = [1200, length2, 1200]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset - 1200

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = df_input['耦合系数(μH/km)']

    # 区段频率
    para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率(Hz)']
    para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率(Hz)']
    freq = freq1
    data['freq'] = para['freq'] = Freq(freq1)
    para['主串频率列表'] = [Freq(freq1)]
    para['被串频率列表'] = generate_frqs(Freq(freq2), 3, flip_flag=True)

    # 电容数量
    c_num1 = data['主串电容数(含TB)'] = df_input['主串电容数(含TB)']
    c_num2 = data['被串电容数(含TB)'] = df_input['被串电容数(含TB)']

    para['主串电容数'] = [c_num1]
    para['被串电容数'] = [12, c_num2, 12]

    # 电容容值
    data['主串电容值(μF)'] = df_input['主串电容值(μF)']
    data['被串电容值(μF)'] = df_input['被串电容值(μF)']

    para['主串容值列表'] = list(map(config_c_value_20230426, para['主串频率列表']))
    para['被串容值列表'] = list(map(config_c_value_20230426, para['被串频率列表']))

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
    data['分路起点'] = offset - 1200 - 14.5
    data['分路终点'] = offset + length2 + 1200 + 14.5


def config_row_data_0509_eerduosi(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '无'

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']

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
    data['线间距(m)'] = para['线间距'] = df_input['线间距(m)']
    k = round(-221.12 * np.log(1 - (1.505 / para['线间距']) ** 2), 1)
    data['耦合系数(μH/km)'] = para['耦合系数'] = k

    # 区段频率
    para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率(Hz)']
    para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率(Hz)']
    freq = freq1
    data['freq'] = para['freq'] = Freq(freq1)
    para['主串频率列表'] = [Freq(freq1)]
    para['被串频率列表'] = [Freq(freq2)]

    # 电容数量
    c_num1 = data['主串电容数(含TB)'] = df_input['主串电容数(含TB)']
    c_num2 = data['被串电容数(含TB)'] = df_input['被串电容数(含TB)']

    para['主串电容数'] = [c_num1]
    para['被串电容数'] = [c_num2]

    # 电容容值
    c_value1 = data['主串电容值(μF)'] = df_input['主串电容值(μF)']
    c_value2 = data['被串电容值(μF)'] = df_input['被串电容值(μF)']

    para['主串容值列表'] = [config_imp('rlc_s', 10e-3, None, c_value1*1e-6)]
    para['被串容值列表'] = [config_imp('rlc_s', 10e-3, None, c_value2*1e-6)]

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
    data['分路起点'] = offset
    data['分路终点'] = offset + length2

    # 电码化
    #################################################################################

    # FT1-U
    data['FT1-U二次侧输出电压(V)'] = value_t = df_input['FT1-U二次侧输出电压(V)']
    para['n_FT1u_25Hz_Coding'] = config_n(170 / value_t)

    #################################################################################

    # 调整电阻
    data['调整电阻(Ω)'] = value_r = df_input['调整电阻(Ω)']
    data['调整电感(H)'] = value_l = df_input['调整电感(H)']
    data['调整电容(F)'] = value_c = df_input['调整电容(F)']
    data['调整RLC模式'] = mode_rlc = df_input['调整RLC模式']

    if mode_rlc == '串联':
        para['Rt_25Hz_Coding'] = config_imp('rlc_s', value_r, value_l, value_c)
    elif mode_rlc == '并联':
        para['Rt_25Hz_Coding'] = config_imp('rlc_p', value_r, value_l, value_c)

    #################################################################################

    # 室内隔离盒
    data['NGL-C1(μF)'] = value_c = df_input['NGL-C1(μF)']
    value_c = value_c * 1e-6
    para['C1_NGL_25Hz_Coding'] = config_imp('rlc_s', None, None, value_c)

    #################################################################################

    # 室外隔离盒
    data['WGL-C1(μF)'] = value_c1 = df_input['WGL-C1(μF)']
    data['WGL-C2(μF)'] = value_c2 = df_input['WGL-C2(μF)']
    data['WGL-L1-R(Ω)'] = value_r1 = df_input['WGL-L1-R(Ω)']
    data['WGL-L1-L(H)'] = value_l1 = df_input['WGL-L1-L(H)']
    data['WGL-L2-R(Ω)'] = value_r2 = df_input['WGL-L2-R(Ω)']
    data['WGL-L2-L(mH)'] = value_l2 = df_input['WGL-L2-L(mH)']
    data['WGL-BPM变比'] = value_n = df_input['WGL-BPM变比']

    value_c1 = value_c1 * 1e-6
    value_c2 = value_c2 * 1e-6
    value_l2 = value_l2 * 1e-3

    para['C1_WGL_25Hz_Coding'] = config_imp('rlc_s', None, None, value_c1)
    para['C2_WGL_25Hz_Coding'] = config_imp('rlc_s', None, None, value_c2)
    para['L1_WGL_25Hz_Coding'] = config_imp('rlc_s', value_r1, value_l1, None)
    para['L1_WGL_25Hz_Coding'] = config_imp('rlc_s', value_r2, value_l2, None)
    para['n_WGL_25Hz_Coding'] = config_n(value_n)

    #################################################################################

    # 扼流变压器
    data['扼流变压器变比'] = value_n = df_input['扼流变压器变比']
    data['BE-Rm(Ω)'] = value_r = df_input['BE-Rm(Ω)']
    data['BE-Lm(H)'] = value_l = df_input['BE-Lm(H)']

    para['n_EL_25Hz_Coding'] = config_n(value_n)
    para['zm_EL_25Hz_Coding'] = config_imp('rlc_s', value_r, value_l, None)
