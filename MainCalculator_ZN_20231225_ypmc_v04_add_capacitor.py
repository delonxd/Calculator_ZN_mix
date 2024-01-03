from src.Model.PreModel import PreModel
from src.Model.ModelParameter import ModelParameter
from src.Model.MainModel import MainModel
from src.Method import *
from src.logMethod import *
from src.Data2Excel import *

from src.Config_ZN_20231225_ypmc_v04_add_capacitor import *

import pandas as pd
import time
import os
import sys


def main_cal():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    #################################################################################

    input_path = '20231225_移频脉冲BZE加电容\\邻线干扰参数输入_移频脉冲_BZE加电容.xlsx'

    # 参数输入
    df_input = pd.read_excel(input_path)
    df_input = df_input.where(df_input.notnull(), None)
    num_len = len(list(df_input['序号']))

    #################################################################################

    # 获取时间戳
    localtime = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))
    output_path = '20231225_移频脉冲BZE加电容\\仿真输出_移频脉冲_%s.xlsx' % timestamp

    #################################################################################

    # 初始化变量
    work_path = os.getcwd()
    para = ModelParameter(workpath=work_path)

    para['MAX_CURRENT'] = {
        1700: 197,
        2000: 175,
        2300: 162,
        2600: 150,
    }

    # 钢轨阻抗
    trk_2000A_21 = ImpedanceMultiFreq()
    trk_2000A_21.rlc_s = {
        1700: [1.177, 1.314e-3, None],
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}

    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['Ccmp_z_change_zhu'] = ImpedanceMultiFreq()
    para['Ccmp_z_change_chuan'] = ImpedanceMultiFreq()

    para['TB_引接线_有砟'] = ImpedanceMultiFreq()
    para['TB_引接线_有砟'].z = {
        1700: (8.33 + 31.4j)*1e-3,
        2000: (10.11 + 35.2j)*1e-3,
        2300: (11.88 + 39.0j)*1e-3,
        2600: (13.60 + 42.6j)*1e-3}

    # # 第一组参数
    # para['YPMC_BZE'] = ImpedanceMultiFreq()
    # para['YPMC_BZE'].rlc_s = {
    #     1700: [202.734, 429.237e-3, None],
    #     2000: [260.239, 430.666e-3, None],
    #     2300: [335.495, 432.703e-3, None],
    #     2600: [435.161, 435.658e-3, None]}
    #
    # c_bze_cap = {
    #     1700: 23.61e-6,
    #     2000: 17.21e-6,
    #     2300: 13.12e-6,
    #     2600: 10.35e-6,
    # }

    # 第二组参数

    para['YPMC_BZE'] = ImpedanceMultiFreq()
    para['YPMC_BZE'].rlc_s = {
        1700: [129.25, 58.07e-3, None],
        2000: [150.56, 56.50e-3, None],
        2300: [176.77, 55.03e-3, None],
        2600: [211.86, 53.62e-3, None]}

    c_bze_cap = {
        1700: 0.145e-6,
        2000: 0.107e-6,
        2300: 0.083e-6,
        2600: 0.066e-6,
    }

    para['YPMC_BZE_c'] = dict()
    para['YPMC_BZE_add_cap'] = dict()

    for key, value in c_bze_cap.items():
        para['YPMC_BZE_c'][key] = ImpedanceMultiFreq()

        para['YPMC_BZE_c'][key].rlc_s = {
            1700: (None, None, value),
            2000: (None, None, value),
            2300: (None, None, value),
            2600: (None, None, value)}

        # # 只安装BZE
        # para['YPMC_BZE_add_cap'][key] = para['YPMC_BZE'] / 49
        # para['bze_condition'] = '只安装BZE'

        # 加装BZE并联电容
        para['YPMC_BZE_add_cap'][key] = (para['YPMC_BZE_c'][key] // para['YPMC_BZE']) / 49
        para['bze_condition'] = 'BZE并联电容'

    output_path = '20231225_移频脉冲BZE加电容\\仿真输出_移频脉冲_%s_%s.xlsx' % (timestamp, para['bze_condition'])

    # para['YPMC_BZE_add_cap'][1700] = para['YPMC_BZE_c'][1700] // para['YPMC_BZE']
    # para['YPMC_BZE_add_cap'][2000] = para['YPMC_BZE_c'][2000] // para['YPMC_BZE']
    # para['YPMC_BZE_add_cap'][2300] = para['YPMC_BZE_c'][2300] // para['YPMC_BZE']
    # para['YPMC_BZE_add_cap'][2600] = para['YPMC_BZE_c'][2600] // para['YPMC_BZE']
    #
    # para['YPMC_BZE_add_cap'][1700] = para['YPMC_BZE_add_cap'][1700] / 49
    # para['YPMC_BZE_add_cap'][2000] = para['YPMC_BZE_add_cap'][2000] / 49
    # para['YPMC_BZE_add_cap'][2300] = para['YPMC_BZE_add_cap'][2300] / 49
    # para['YPMC_BZE_add_cap'][2600] = para['YPMC_BZE_add_cap'][2600] / 49

    # para['YPMC_BZE_add_cap'][1700] = para['YPMC_BZE'] / 49
    # para['YPMC_BZE_add_cap'][2000] = para['YPMC_BZE'] / 49
    # para['YPMC_BZE_add_cap'][2300] = para['YPMC_BZE'] / 49
    # para['YPMC_BZE_add_cap'][2600] = para['YPMC_BZE'] / 49

    #################################################################################

    # 获取表头
    head_list = config_headlist_20231225_add_capacitor()

    #################################################################################

    # 初始化excel数据
    excel_data = []
    # data2excel = Data2Excel(sheet_names=[])
    data2excel = SheetDataGroup(sheet_names=[])

    #################################################################################

    columns_max = 0
    counter = 1

    MainLog.add_log_accurate('start calculate')
    MainLog.add_log_accurate('total: ' + str(num_len))

    for temp_temp in range(num_len):

        #################################################################################

        # # 封装程序显示
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # if getattr(sys, 'frozen', False):
        #     print(df_input[temp_temp:(temp_temp + 1)])
        # print(temp_temp)
        # print('calculating line ' + str(counter) + ' ...')

        MainLog.add_log_accurate('-' * 50)
        MainLog.add_log_accurate('scene: ' + str(counter) + ' ...')

        #################################################################################

        # 数据表初始化
        data = dict()
        for key in head_list:
            data[key] = None

        # 添加数据行
        # data2excel.add_row()
        # data2excel.add_new_row()

        # 打包行数据
        df_input_row = df_input.iloc[temp_temp]

        # 配置数据
        config_row_data_20231225_add_capacitor(df_input_row, para, data)

        interval = data['分路间隔(m)']

        data2excel.add_new_row()

        len_posi = 0

        # 分路计算
        md = PreModel_20231225_ZN_ypmc_v04_add_capacitor(parameter=para)

        md.add_train()

        flag_l = data['分路起点']
        # flag_r = data['分路起点']
        flag_r = data['分路终点']

        if data['被串方向'] == '右发':
            posi_list = np.arange(flag_r, flag_l - 0.0001, -interval)
        elif data['被串方向'] == '左发':
            posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)
        else:
            raise KeyboardInterrupt("被串方向应填写'左发'或'右发'")

        len_posi = max(len(posi_list), len_posi)

        for posi_bei in posi_list:
            para['分路位置'] = posi_bei

            md.train1.posi_rlt = posi_bei
            md.train1.set_posi_abs(0)

            posi_zhu = posi_bei
            md.train2.posi_rlt = posi_zhu
            md.train2.set_posi_abs(0)

            m1 = MainModel(md.lg, md=md)

            i_sht_zhu = md.lg['线路3']['列车2']['分路电阻1']['I'].value_c
            i_sht_bei = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c

            # i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu, direct='右')
            # i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')
            # if data['被串方向'] == '正向':
            #     i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')
            #     v_rcv_bei = md.lg['线路4']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
            #
            # else:
            #     i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='左')
            #     v_rcv_bei = md.lg['线路4']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

            if data['被串方向'] == '右发':
                i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')
            else:
                i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='左')

            # i1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['6SVA1']['I1'].value
            # i2 = md.lg['线路3']['地面']['区段1']['右调谐单元']['6SVA1']['I2'].value
            #
            # i_sva1 = abs(i1 - i2)
            #
            # i_trk_bei_temp = i_trk_bei / i_sva1

            # i_source_fs = m1['线路3'].node_dict[length].l_track['I2'].value
            # i_source_fs = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value
            # v_load_fs = m1['线路4'].node_dict[length].l_track['U2'].value

            # z_mm = np.inf if i_source_fs == 0 else v_load_fs / i_source_fs
            # z_mm = v_load_fs / i_source_fs
            # z_mm_abs = abs(z_mm)
            # co_mutal = z_mm_abs / 2 / np.pi / para['freq_主'] / (length-posi_tr)*1000 * 1e6 * 2
            # co_mutal = round(co_mutal, 2)

            # i_TB = md.lg['线路4']['地面']['区段1']['TB2']['I'].value_c
            # i_ca = md.lg['线路4']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value_c
            # i_C1 = md.lg['线路4']['地面']['区段1']['C5']['I'].value_c
            # i_C2 = md.lg['线路4']['地面']['区段1']['C4']['I'].value_c
            # i_C3 = md.lg['线路4']['地面 ']['区段1']['C3']['I'].value_c
            # i_C4 = md.lg['线路4']['地面']['区段1']['C2']['I'].value_c
            # i_C5 = md.lg['线路4']['地面']['区段1']['C1']['I'].value_c

            # v_rcv_bei = md.lg['线路4']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
            # v_rcv_bei = md.lg['线路4']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

            # v_rcv_zhu1 = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
            # v_rcv_zhu2 = md.lg['线路3']['地面']['区段1']['右绝缘节']['相邻调谐单元']['1接收器']['U'].value_c

            #################################################################################

            # data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
            data2excel.add_data(sheet_name="主串分路电流", data1=i_sht_zhu)
            data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_bei)
            data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_bei)

        if len_posi > columns_max:
            columns_max = len_posi

        i_trk_list = data2excel.data_dict["被串钢轨电流"][-1]
        i_sht_list = data2excel.data_dict["被串分路电流"][-1]

        # i_sht_list_zhu = data2excel.data_dict["主串分路电流"][-1]

        data['被串最大干扰电流(A)'] = max(i_trk_list)
        # data['主串出口电流(A)'] = i_sht_list_zhu[0]
        # data['主串入口电流(A)'] = i_sht_list_zhu[-1]
        data['被串最大干扰位置(m)'] = round(i_trk_list.index(max(i_trk_list))*interval)
        max_i = data['被串最大干扰电流(A)'] * 1000
        # MAX_I = para['MAX_CURRENT'][data['主串频率(Hz)']]

        # if data['故障位置'] == '无':
        #     max_i_normal = max_i
        #
        # data['干扰值变化'] = max_i / max_i_normal - 1
        #
        # print('%.2fmA, %.2f%%' % (max_i, data['干扰值变化'] * 100))
        MainLog.add_log_accurate('max_i --> %.2fmA' % max_i)

        # v_rcv_bei_list = data2excel.data_dict["被串轨入电压"][-1]
        # data['被串最大轨入电压(主被串同时分路状态)'] = max(v_rcv_bei_list)

        # v_rcv_bei_list = data2excel.data_dict["被串轨入电压"][-1]
        # data['被串最大轨入电压(主调整被调整)'] = max(v_rcv_bei_list)

        data_row = [data[key] for key in head_list]
        excel_data.append(data_row)
        counter += 1

        #################################################################################

        # if not getattr(sys, 'frozen', False):
        #     print(data.keys())
        #     print(data.values())
        #     print(i_sht_list)
        #
    #################################################################################

    # 修正表头
    data2excel.config_header()
    data2excel["被串钢轨电流"].header[0] = '被串发送端'
    data2excel["被串分路电流"].header[0] = '被串发送端'
    # data2excel["主串钢轨电流"].header[0] = '被串发送端'
    # data2excel["主串分路电流"].header[0] = '被串发送端'
    # data2excel["主串轨面电压"].header[0] = '主串发送端'

    df_data = pd.DataFrame(excel_data, columns=head_list)

    #################################################################################

    # 保存到本地excel
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

    workbook = writer.book
    header_format = workbook.add_format({
        'bold': True,  # 字体加粗
        'text_wrap': True,  # 是否自动换行
        'valign': 'vcenter',  # 垂直对齐方式
        'align': 'center',  # 水平对齐方式
        'border': 1})

    write_to_excel(df=df_input, writer=writer, sheet_name="参数设置", hfmt=header_format)
    write_to_excel(df=df_data, writer=writer, sheet_name="数据输出", hfmt=header_format)

    names = [
        "被串钢轨电流",
        "被串分路电流",
        # "主串钢轨电流",
        "主串分路电流",
    ]

    # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
    # data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)
    data2excel.write2excel(sheet_names=names, writer=writer)

    writer.save()
    # return 1


if __name__ == '__main__':
    main_cal()
