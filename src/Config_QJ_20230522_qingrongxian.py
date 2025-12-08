from src.ConstantType import Constant
from src.FrequencyType import Freq
from src.Method import generate_frqs
from src.ImpedanceParaType import ImpedanceMultiFreq

from src.Module.OutsideElement import CapC

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line
from src.Model.PreModel import PreModel


# 青荣线区间邻线干扰
def config_headlist_20230522_qingrongxian():
    head_list = [
        '序号',
        '备注',
        # '线路名称', '车站名称',
        '主串区段', '被串区段',

        # '线间距(m)',
        '耦合系数(μH/km)',
        # '并行长度(m)',
        # '被串相对位置(m)',

        '主串方向', '被串方向',
        # '线间距(m)',
        # '耦合系数(μH/km)',
        # '并行长度(m)',

        # '调谐区错位(m)',
        '被串相对位置(m)',
        '主串区段长度(m)', '被串区段长度(m)',
        # '主串左端坐标', '被串左端坐标',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '主串频率(Hz)', '被串频率(Hz)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        # '主串区段类型', '被串区段类型',
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


def config_row_data_20230522_qingrongxian(df_input, para, data):
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
    para['被串区段长度'] = [950, length2, 617]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset - 950

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
    para['被串电容数'] = [11, c_num2, 8]

    # 电容容值
    c_zhu_data = data['主串电容值(μF)'] = df_input['主串电容值(μF)']
    c_bei_data = data['被串电容值(μF)'] = df_input['被串电容值(μF)']

    c_tmp = ImpedanceMultiFreq()
    c_tmp.rlc_s = {
        1700: [10e-3, None, 25e-6],
        2000: [10e-3, None, 25e-6],
        2300: [10e-3, None, 25e-6],
        2600: [10e-3, None, 25e-6]}
    # para['主串容值列表'] = [c_tmp]
    # para['被串容值列表'] = [c_tmp, c_tmp, c_tmp]

    # 普铁高铁对比
    c_zhu = ImpedanceMultiFreq()
    c_zhu.rlc_s = {
        1700: [10e-3, None, c_zhu_data * 1e-6],
        2000: [10e-3, None, c_zhu_data * 1e-6],
        2300: [10e-3, None, c_zhu_data * 1e-6],
        2600: [10e-3, None, c_zhu_data * 1e-6]}
    c_bei = ImpedanceMultiFreq()
    c_bei.rlc_s = {
        1700: [10e-3, None, c_bei_data * 1e-6],
        2000: [10e-3, None, c_bei_data * 1e-6],
        2300: [10e-3, None, c_bei_data * 1e-6],
        2600: [10e-3, None, c_bei_data * 1e-6]}
    para['主串容值列表'] = [c_zhu]
    para['被串容值列表'] = [c_tmp, c_bei, c_tmp]

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
    data['分路起点'] = offset - 14.5
    data['分路终点'] = offset + length2 + 14.5


class PreModel_20230522_qingrongxian(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        self.train2['分路电阻1'].z = 1000000

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

        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=3,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[29] * 4,
                           m_typs=['2000A'] * 3,
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']] * 3,
                           send_lvs=[send_level] * 3,
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
