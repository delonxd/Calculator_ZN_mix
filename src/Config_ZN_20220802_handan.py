from src.FrequencyType import Freq
from src.Method import generate_frqs

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line
from src.Model.PreModel import PreModel

from src.Module.TcsrLib import ZPW2000A_ZN_PTSVA1
from src.Module.TcsrLib import ZPW2000A_ZN_25Hz_Coding


# 邯郸25Hz邻线干扰表头
def config_headlist_handan():
    head_list = [
        '序号',
        '备注',
        '主串区段', '被串区段',

        '耦合系数',
        '被串相对位置(m)',
        '主串分路位置(m)',

        '主串方向', '被串方向',
        # '线间距(m)',
        # '耦合系数(μH/km)',
        # '并行长度(m)',

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
    ]

    return head_list


class PreModel_0802_handan(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 1)
        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']],
                           j_lens=[0, 0],
                           m_typs=['2000A'],
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        m_frqs = generate_frqs(Freq(para['freq_被']), 1)
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']],
                           j_lens=[0, 0],
                           m_typs=['2000A_25Hz_Coding'],
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        # sg3['区段1'].load_TB_mode(para['主串TB模式'])
        # sg4['区段1'].load_TB_mode(para['被串TB模式'])
        # sg3.refresh()
        # sg4.refresh()

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.change_cable_length()
        # self.pop_c()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['Trk_z'], rd=para['Trk_z'])
        self.set_rail_para(line=l4, z_trk=para['Trk_z'], rd=para['Trk_z'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_cable_length(self):
        para = self.parameter

        sec_class = (
            ZPW2000A_ZN_25Hz_Coding,
            ZPW2000A_ZN_PTSVA1,
        )

        if para['主串电缆长度'] is not None:
            for ele in self.section_group3['区段1'].element.values():
                if isinstance(ele, sec_class):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['主串电缆长度']

        # print(para['主串电缆长度'])
        # print(para['被串电缆长度'])

        if para['被串电缆长度'] is not None:
            for ele in self.section_group4['区段1'].element.values():
                if isinstance(ele, sec_class):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['被串电缆长度']
