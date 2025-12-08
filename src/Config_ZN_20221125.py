from src.FrequencyType import Freq
from src.Method import generate_frqs
from src.Method import columns_header

from src.Module.OutsideElement import CapC

from src.TrackCircuitElement.SectionGroup import SectionGroup
from src.TrackCircuitElement.LineGroup import LineGroup
from src.TrackCircuitElement.Train import Train
from src.TrackCircuitElement.Line import Line
from src.Model.PreModel import PreModel

import itertools
import pandas as pd


def config_input_1125():

    # print(df_input)

    # ret = pd.DataFrame(columns=columns_header())
    # counter = 1
    # index = 1

    # freq_zhu = [1700, 2000, 2300, 2600]
    # freq_bei = [1700, 2000, 2300, 2600]

    freq_zhu = [2300]
    freq_bei = [2300]
    # freq_zhu = [1700]
    # freq_bei = [1700]
    sec_length = {
        '区间-普铁': [500],
        # '区间-普铁': [1400, 1000, 500],
        # '区间-高铁': [1400, 1000, 500],
        # '站内-有选频': [650, 500, 350],
        # '站内-无选频': [650, 500, 350],
    }
    sec_type = list(sec_length.keys())

    list0 = []

    index = 0
    for item in itertools.product(sec_type, freq_zhu, freq_bei):
        # print(item)
        for s_length in sec_length[item[0]]:

            cnum_zhu, cvalue_zhu, level = get_c_num_value_1125(item[0], s_length, item[1])
            cnum_bei, cvalue_bei, _ = get_c_num_value_1125(item[0], s_length, item[2])

            temp_zhu = list(map(lambda x: '主串-' + str(x+1), range(cnum_zhu)))
            temp_bei = list(map(lambda x: '被串-' + str(x+1), range(cnum_bei)))

            normal_flag = False
            e_list = ['无']
            e_list.extend(temp_zhu)
            e_list.extend(temp_bei)

            for error in e_list:
                for flag in ['断线', '减半']:
                    if error == '无':
                        e_type = '正常'
                    else:
                        e_type = flag

                    if normal_flag is True:
                        if error == '无':
                            continue

                    normal_flag = True
                    row = pd.Series(index=columns_header(), dtype='object')

                    row['故障位置'] = error
                    row['故障类型'] = e_type

                    row['序号'] = int(index)
                    row['线路名称'] = '-'
                    row['车站名称'] = '-'
                    row['主串区段'] = '-'
                    row['被串区段'] = '-'

                    row['线间距'] = '-'
                    row['耦合系数'] = 24
                    row['并行长度(m)'] = 0

                    row['主串方向'] = '右发'
                    row['被串方向'] = '右发'

                    row['主串区段类型'] = item[0]
                    row['被串区段类型'] = item[0]

                    row['主串区段长度(m)'] = s_length
                    row['被串区段长度(m)'] = s_length

                    row['主串坐标'] = 0
                    row['被串坐标'] = 0

                    row['主串坐标'] = 0
                    row['被串坐标'] = 0

                    row['主串电平级'] = level
                    row['被串电平级'] = level

                    row['主串频率(Hz)'] = item[1]
                    row['被串频率(Hz)'] = item[2]

                    row['主串电缆长度(km)'] = 10
                    row['被串电缆长度(km)'] = 10

                    row['主串电容数(含TB)'] = cnum_zhu
                    row['被串电容数(含TB)'] = cnum_bei

                    row['主串电容值(μF)'] = cvalue_zhu
                    row['被串电容值(μF)'] = cvalue_bei

                    row['主串道床电阻(Ω·km)'] = 10000
                    row['被串道床电阻(Ω·km)'] = 10000

                    row['主串TB模式'] = '无TB'
                    row['被串TB模式'] = '无TB'

                    d0 = {
                        '区间': 29,
                        '站内': 0,
                    }
                    row['调谐区长度'] = d0.get(item[0].split('-')[0])

                    # print(ret.loc[index, '调谐区长度'])
                    list0.append(row)

                    index += 1
    ret = pd.DataFrame(list0)
    return ret


def get_c_num_value_1125(sec_type, length, freq):
    cnum = None
    level = None
    if sec_type in ['站内-有选频', '站内-无选频']:
        cvalue = 25
        d_temp = {
            350: 3,
            500: 5,
            650: 7,
        }
        cnum = d_temp.get(length)
        if sec_type == '站内-无选频':
            level = 9
        if sec_type == '站内-有选频':
            if freq in [1700, 2000, 2300]:
                level = 7
            if freq in [2600]:
                level = 8

    elif sec_type == '区间-高铁':
        cvalue = 25
        if freq in [1700, 2000]:
            d_temp = {
                500: 8,
                1000: 16,
                1400: 23,
            }
            cnum = d_temp.get(length)

        if freq in [2300, 2600]:
            d_temp = {
                500: 6,
                1000: 12,
                1400: 17,
            }
            cnum = d_temp.get(length)

        d_temp = {
            500: 3,
            1000: 2,
            1400: 1,
        }
        level = d_temp.get(length)

    elif sec_type == '区间-普铁':
        d_temp = {
            1700: 55,
            2000: 50,
            2300: 46,
            2600: 40,
        }
        cvalue = d_temp.get(freq)

        if freq in [1700, 2000, 2300]:
            d_temp = {
                500: 6,
                1000: 10,
                1400: 18,
            }
            cnum = d_temp.get(length)

        if freq in [2600]:
            d_temp = {
                500: 6,
                1000: 10,
                1400: 20,
            }
            cnum = d_temp.get(length)

        d_temp = {
            500: 3,
            1000: 2,
            1400: 1,
        }
        level = d_temp.get(length)

    else:
        raise KeyboardInterrupt('sec_type error')

    return cnum, cvalue, level


def config_headlist_1125():
    head_list = [
        '序号',
        '备注',
        # '线路名称', '车站名称',
        # '主串区段', '被串区段',

        # '线间距(m)',
        '耦合系数(μH/km)',
        # '并行长度(m)',
        '被串相对位置(m)',

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

        '主串区段类型', '被串区段类型',
        # '主串TB模式', '被串TB模式',

        '主串分路电阻(Ω)', '被串分路电阻(Ω)',
        '主串电缆长度(km)', '被串电缆长度(km)',

        '分路间隔(m)',

        '主串电平级',
        '电源电压',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        '故障位置', '故障类型',
        '干扰值变化',
    ]

    return head_list


class PreModel_1125(PreModel):
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
        m_typs = self.get_m_typs_1125(para['主串区段类型'])
        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']],
                           j_lens=[para['调谐区长度'], para['调谐区长度']],
                           # m_typs=['2000A'],
                           m_typs=[m_typs],
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
        m_typs = self.get_m_typs_1125(para['被串区段类型'])
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']],
                           j_lens=[para['调谐区长度'], para['调谐区长度']],
                           # m_typs=['2000A'],
                           m_typs=[m_typs],
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        # sg3['区段1'].load_TB_mode(para['主串TB模式'])
        # sg4['区段1'].load_TB_mode(para['被串TB模式'])
        # sg3.refresh()
        # sg4.refresh()

        # m_frqs = generate_frqs(Freq(para['freq_被']), 2)
        # sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=2,
        #                    m_frqs=m_frqs,
        #                    m_lens=[560, 830],
        #                    j_lens=[29, 29, 29],
        #                    m_typs=['2000A']*2,
        #                    c_nums=[6, 9],
        #                    sr_mods=[para['sr_mod_被']]*2,
        #                    send_lvs=[send_level]*2,
        #                    parameter=parameter)

        # partent = sg3['区段1']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=para['主串区段长度'])
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.config_c_fault()

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

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_chuan']

    def config_c_fault(self):
        para = self.parameter

        error_pos = para['故障位置']
        error_typ = para['故障类型']

        if error_pos == '无':
            return

        split = error_pos.split('-')
        if split[0] == '主串':
            sec = self.section_group3['区段1']
            c_value = para['Ccmp_z_change_zhu'] * 2
        elif split[0] == '被串':
            sec = self.section_group4['区段1']
            c_value = para['Ccmp_z_change_chuan'] * 2
        else:
            raise KeyboardInterrupt('wrong section')

        c_pos = 'C' + split[1]

        if error_typ == '断线':
            sec.element.pop(c_pos)
        elif error_typ == '减半':
            sec.element[c_pos].z = c_value
        else:
            raise KeyboardInterrupt('wrong error_typ')


class PreModel_1125(PreModel):
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
        m_typs = self.get_m_typs_1125(para['主串区段类型'])
        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']],
                           j_lens=[para['调谐区长度'], para['调谐区长度']],
                           # m_typs=['2000A'],
                           m_typs=[m_typs],
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
        m_typs = self.get_m_typs_1125(para['被串区段类型'])
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']],
                           j_lens=[para['调谐区长度'], para['调谐区长度']],
                           # m_typs=['2000A'],
                           m_typs=[m_typs],
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        # m_frqs = generate_frqs(Freq(para['freq_被']), 2)
        # sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=2,
        #                    m_frqs=m_frqs,
        #                    m_lens=[560, 830],
        #                    j_lens=[29, 29, 29],
        #                    m_typs=['2000A']*2,
        #                    c_nums=[6, 9],
        #                    sr_mods=[para['sr_mod_被']]*2,
        #                    send_lvs=[send_level]*2,
        #                    parameter=parameter)

        # partent = sg3['区段1']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=para['主串区段长度'])
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.config_c_fault()

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

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_chuan']
