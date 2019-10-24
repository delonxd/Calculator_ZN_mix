from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *

import pandas as pd
import time


class TestModel:
    # def __init__(self, freq, length, c_num, level, rd, r_cable, cab_len, turnout_list):
    def __init__(self, turnout_list, parameter):
        # 导入参数
        # parameter = ModelParameter()
        # parameter['freq'] = freq
        # parameter['length'] = length
        # parameter['c_num'] = c_num
        # parameter['Cable_R'] = r_cable
        # parameter['cab_len'] = cab_len
        # parameter['Rd'] = rd
        # parameter['level'] = level

        self.parameter = parameter
        self.train = Train(name_base='列车1', posi=0, parameter=parameter)

        # 轨道电路初始化
        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1, freq1=parameter['freq'],
                           m_length=[parameter['length']],
                           j_length=[22, 22],
                           m_type=['2000A_Belarus'],
                           c_num=[parameter['c_num']],
                           parameter=parameter)
        self.section_group3 = sg3

        l3 = Line(name_base='线路3', sec_group=sg3,
                  parameter=parameter)
        self.l3 = l3

        self.lg = LineGroup(l3, name_base='线路组')
        self.lg.refresh()

    def add_train(self):
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=self.train)
        self.l3 = l3

        self.lg = LineGroup(l3, name_base='线路组')
        self.lg.refresh()


def get_output(lg):
    output = 13 * [0]
    output[0] = lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['2内阻']['U2'].value_c
    output[1] = lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['3隔离元件']['U2'].value_c
    output[2] = lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['3隔离元件']['I2'].value_c
    output[3] = lg['线路3']['地面']['区段1']['左调谐单元']['2防雷']['1开路阻抗']['U1'].value_c
    output[4] = lg['线路3']['地面']['区段1']['左调谐单元']['2防雷']['3变压器']['U2'].value_c
    output[5] = lg['线路3']['地面']['区段1']['左调谐单元']['3Cab']['U2'].value_c
    output[6] = lg['线路3']['地面']['区段1']['左调谐单元']['6CA']['U2'].value_c
    output[7] = lg['线路3']['地面']['区段1']['右调谐单元']['6CA']['U2'].value_c
    output[8] = lg['线路3']['地面']['区段1']['右调谐单元']['3Cab']['U2'].value_c
    output[9] = lg['线路3']['地面']['区段1']['右调谐单元']['2防雷']['3变压器']['U2'].value_c
    output[10] = lg['线路3']['地面']['区段1']['右调谐单元']['2防雷']['1开路阻抗']['U1'].value_c
    output[11] = lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['1隔离元件']['U2'].value_c
    output[12] = lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['0接收器']['U'].value_c
    return output


if __name__ == '__main__':
    # df = pd.read_excel('../Input/白俄验证输入参数.xlsx', header=None)

    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    fq_list = [1700, 2000, 2300, 2600]
    len_list = [num for num in range(100, 1600, 100)]
    len_list.insert(3, 300)
    c_interval = 50
    c_num_list = [int(len_list[num] / c_interval) for num in range(len(len_list))]
    c_num_list[0] = 0
    c_num_list[1] = 0
    c_num_list[2] = 0

    level = 3
    cab_len = 10
    turnout_list = []

    # freq = fq_list[0]
    # length = len_list[0]
    # c_num = c_num_list[0]

    para = ModelParameter()

    # 电容白俄
    c_value = 40e-6
    para['Ccmp_z'].rlc_s = {
        1700: [10e-3, None, c_value],
        2000: [10e-3, None, c_value],
        2300: [10e-3, None, c_value],
        2600: [10e-3, None, c_value]}

    # 白俄钢轨阻抗25
    trk_Belarus_25 = ImpedanceMultiFreq()
    trk_Belarus_25.rlc_s = {
        1700: [1.500, 1.370e-3, None],
        2000: [1.600, 1.360e-3, None],
        2300: [1.740, 1.350e-3, None],
        2600: [1.930, 1.340e-3, None]}

    # 白俄钢轨阻抗800
    trk_Belarus_800 = ImpedanceMultiFreq()
    trk_Belarus_800.rlc_s = {
        1700: [1.380, 1.360e-3, None],
        2000: [1.530, 1.350e-3, None],
        2300: [1.680, 1.350e-3, None],
        2600: [1.790, 1.340e-3, None]}

    trk_Belarus_list = [trk_Belarus_25, trk_Belarus_800]

    para['cab_len'] = cab_len
    para['level'] = level

    head_list = ['区段长度', '电容间隔', '电容值', '电容数', '钢轨电阻', '钢轨电感',
                 '区段频率', '分路电阻', '道床电阻',
                 '调整轨入最大值', '调整轨入最小值',
                 '分路残压最大值', '最大分路残压位置',
                 '机车信号最小值', '最小机车信号位置']
    excel_list = []

    interval_list = list(range(100, 10, -10))
    c_value_list = list(range(10, 85, 5))
    c_value_list = [round(c_v*1e-6, 10) for c_v in c_value_list]

    length = 1500
    for trk_Belarus in trk_Belarus_list:
        para['Trk_z'] = trk_Belarus
        for freq in fq_list:
            for c_interval in interval_list:
                c_num = int((length - 22) / c_interval + 0.5)
                for c_value in c_value_list:
                    para['Ccmp_z'].rlc_s = {
                        1700: [10e-3, None, c_value],
                        2000: [10e-3, None, c_value],
                        2300: [10e-3, None, c_value],
                        2600: [10e-3, None, c_value]}


    # for freq in fq_list:
    #     for length, c_num in zip(len_list, c_num_list):
                    data = dict()
                    data['区段长度'] = length
                    data['电容间隔'] = c_interval
                    data['电容值'] = c_value
                    data['电容数'] = c_num
                    data['钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                    data['钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                    data['区段频率'] = freq
                    data['道床电阻'] = rd = 2
                    data['分路电阻'] = r_sht = 0.15

                    para['freq'] = freq
                    para['length'] = length
                    para['c_num'] = c_num

                    #####################################################################################
                    # 调整最有利状态
                    para['Cable_R'] = 43
                    para['Rd'] = 10000
                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    m1 = MainModel(md.lg, md=md)

                    m1.change_coefficient(m1.module_set)


                    print(len(m1.cons))
                    data['调整轨入最大值'] \
                        = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

                    #####################################################################################
                    # 调整最不利状态
                    para['Cable_R'] = 47
                    para['Rd'] = rd
                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    m1 = MainModel(md.lg, md=md)
                    data['调整轨入最小值'] \
                        = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

                    #####################################################################################
                    # 分路最不利状态
                    para['Cable_R'] = 43
                    para['Rd'] = 10000
                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    md.add_train()
                    md.parameter['Rsht_z'] = r_sht
                    posi_list = range(11, (length - 11), 100)
                    v_rcv_list = []

                    # v_rcv_max = 0
                    # v_rcv_max_posi = posi_list[0]

                    count = 0
                    for posi_tr in posi_list:
                        md.train.posi_rlt = posi_tr
                        md.train.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)

                        v_rcv = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c
                        v_rcv_list.append(v_rcv)

                        # if v_rcv > v_rcv_max:
                        #     v_rcv_max = v_rcv
                        #     v_rcv_max_posi = posi_tr

                    data['分路残压最大值'] = max(v_rcv_list)
                    index_p = posi_list[v_rcv_list.index(data['分路残压最大值'])]
                    data['最大分路残压位置'] = index_p

                    # data['分路残压最大值'] = v_rcv_max
                    # data['最大分路残压位置'] = v_rcv_max_posi

                    #####################################################################################
                    # 机车信号最不利状态
                    para['Cable_R'] = 47
                    para['Rd'] = rd
                    md = TestModel(turnout_list=turnout_list, parameter=para)
                    md.add_train()
                    md.parameter['Rsht_z'] = r_sht
                    i_trk_list = []
                    for posi_tr in posi_list:
                        md.train.posi_rlt = posi_tr
                        md.train.set_posi_abs(0)
                        m1 = MainModel(md.lg, md=md)
                        if m1['线路3'].node_dict[posi_tr].l_track is not None:
                            i_trk = m1['线路3'].node_dict[posi_tr].l_track['I2'].value_c
                        else:
                            i_trk = None
                        i_trk_list.append(i_trk)
                    data['机车信号最小值'] = min(i_trk_list)
                    index_p = posi_list[i_trk_list.index(data['机车信号最小值'])]
                    data['最小机车信号位置'] = index_p

                    #####################################################################################

                    row_list = [data[key] for key in head_list]
                    excel_list.append(row_list)
                    print(row_list)

    df = pd.DataFrame(excel_list, columns=head_list)

    # 保存到本地excel
    filename = '../Output/白俄区段长度遍历' + timestamp + '.xlsx'
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="调整表", index=False)
        pass