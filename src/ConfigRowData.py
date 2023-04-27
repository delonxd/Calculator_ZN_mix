from src.FrequencyType import Freq
from src.ConstantType import *
from src.ImpedanceParaType import *


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
