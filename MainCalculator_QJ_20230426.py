from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.Model.PreModel import *
from src.FrequencyType import Freq
from src.ConstantType import *
from src.Method import *
from src.logMethod import *
from src.ConfigHeadList import *
from src.Data2Excel import *
from src.RowData import RowData
from src.ConfigRowData import *

import pandas as pd
import time
import itertools
import os
import sys


def main_cal(path1, path2):
    # path1 = '邻线干扰计算_站内混合_配置输入_v1.0.xlsx'
    # path2 = '仿真输出' + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx'
    path3 = os.getcwd()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    #################################################################################

    # 参数输入
    # df_input = pd.read_excel('邻线干扰参数输入_v0.3.1.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_拆电容.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_电码化.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_v0.4.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_移频脉冲_v0.2.xlsx')
    # df_input = pd.read_excel('ZPW-2000A一体化邻线干扰参数输入表格_v0.4.0.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_2000A一体化_v0.4.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_韩家岭.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_20200730.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_20200806.xlsx')
    # df_input = pd.read_excel('邻线干扰参数输入_BPLN.xlsx')

    df_input = pd.read_excel(path1)
    df_input = df_input.where(df_input.notnull(), None)

    # df_input = regular_input(df_input)

    # MainLog.add_log_accurate('init input')
    # df_input = init_input_1128()
    # print(df_input)
    # print(list(df_input['序号']))
    num_len = len(list(df_input['序号']))

    # 检查输入格式
    # check_input(df_input)

    #################################################################################

    # # 获取时间戳
    # localtime = time.localtime()
    # timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    #################################################################################

    # 初始化变量
    # work_path = os.getcwd()
    work_path = path3
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

    # trk_2000A_21 = ImpedanceMultiFreq()
    # trk_2000A_21.rlc_s = {
    #     1700: [1.71, 1.36e-3, None],
    #     2000: [1.90, 1.35e-3, None],
    #     2300: [2.04, 1.34e-3, None],
    #     2600: [2.24, 1.33e-3, None]}

    # trk_2000A_21.rlc_s = {
    #     1700: [1.59, 1.34e-3, None],
    #     2000: [1.72, 1.33e-3, None],
    #     2300: [1.86, 1.32e-3, None],
    #     2600: [2.00, 1.31e-3, None]}

    # trk_2000A_21.rlc_s = {
    #     1700: [1.80, 1.18e-3, None],
    #     2000: [1.98, 1.17e-3, None],
    #     2300: [2.16, 1.16e-3, None],
    #     2600: [2.33, 1.15e-3, None]}

    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['Ccmp_z_change_zhu'] = ImpedanceMultiFreq()
    para['Ccmp_z_change_chuan'] = ImpedanceMultiFreq()

    para['TB_引接线_有砟'] = ImpedanceMultiFreq()
    para['TB_引接线_有砟'].z = {
        1700: (8.33 + 31.4j)*1e-3,
        2000: (10.11 + 35.2j)*1e-3,
        2300: (11.88 + 39.0j)*1e-3,
        2600: (13.60 + 42.6j)*1e-3}

    # z_tb_2600_2000 = para['TB'][2600][2000].z

    #################################################################################

    # 获取表头
    # head_list = config_headlist_ypmc()
    # head_list = config_headlist_2000A_inte()
    # head_list = config_headlist_2000A_QJ()
    # head_list = config_headlist_inhibitor_c()
    # head_list = config_headlist_hanjialing()
    # head_list = config_headlist_20200730()
    # head_list = config_headlist_V001()
    # head_list = config_headlist_ZN_mix()
    # head_list = config_headlist_1125()
    # head_list = config_headlist_1128()
    head_list = config_headlist_20230426()

    #################################################################################

    # 初始化excel数据
    excel_data = []
    # data2excel = Data2Excel(sheet_names=[])
    data2excel = SheetDataGroup(sheet_names=[])

    #################################################################################

    # 获取循环变量

    clist1 = clist2 = clist3 = clist4 = clist5 = clist6 = [[]]

    clist = list(itertools.product(
        clist1, clist2, clist3, clist4, clist5, clist6))

    #################################################################################

    columns_max = 0
    counter = 1

    # temp_temp = 0
    # cv1, cv2, cv3, cv4, cv5, cv6 = [0] * 6

    pd_read_flag = True
    # pd_read_flag = False

    # num_len = 1

    MainLog.add_log_accurate('start calculate')
    MainLog.add_log_accurate('total: ' + str(num_len))

    max_i_normal = 0

    # for cv1, cv2, cv3, cv4, cv5, cv6 in clist:
    for temp_temp in range(num_len):

        #################################################################################

        # # 封装程序显示
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # if getattr(sys, 'frozen', False):
        #     print(df_input[temp_temp:(temp_temp + 1)])
        # print(temp_temp)
        # print('calculating line ' + str(counter) + ' ...')

        MainLog.add_log_accurate('line' + str(counter) + ' ...')

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
        config_row_data_20230426(df_input_row, para, data)

        interval = data['分路间隔(m)']

        data2excel.add_new_row()

        len_posi = 0

        # 分路计算

        # md = PreModel(parameter=para)
        # md = PreModel_2000A_QJ(parameter=para)
        # md = PreModel_YPMC(parameter=para)
        # md = PreModel_EeMe(parameter=para)
        # md = PreModel_25Hz_coding(parameter=para)
        # md = PreModel_QJ_25Hz_coding(parameter=para)
        # md = PreModel_20200730(parameter=para)
        # md = PreModel_V001(parameter=para)
        # md = PreModel_1128(parameter=para)
        md = PreModel_20230426(parameter=para)

        md.add_train()
        # md.add_train_bei()

        flag_l = data['分路起点']
        flag_r = data['分路终点']

        if data['被串方向'] == '左发':
            posi_list = np.arange(flag_r, flag_l - 0.0001, -interval)
        elif data['被串方向'] == '右发':
            posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)
        else:
            raise KeyboardInterrupt("被串方向应填写'左发'或'右发'")

        # if data['被串方向'] == '正向':
        #     posi_list = np.arange((data['被串左端里程标'] + data['被串区段长度(m)'])+14.5,
        #                           (data['被串左端里程标'] - 0.0001) - 14.5,
        #                           -interval)
        # else:
        #     posi_list = np.arange(data['被串左端里程标'] - 14.5,
        #                           (data['被串左端里程标']  + data['被串区段长度(m)'] + 0.0001)+14.5,
        #                           interval)

        # if data['被串方向'] == '正向':
        #     posi_list = np.arange((data['被串左端里程标'] + 560 + 830) + 14.5,
        #                           (data['被串左端里程标'] - 0.0001) - 14.5,
        #                           -interval)

        len_posi = max(len(posi_list), len_posi)

        tmp_counter = 0
        for posi_bei in posi_list:
            # tmp_counter += 1
            # print(posi_bei)
            # if tmp_counter == 100:
            #     tmp_counter = 0
            #     print('*'*100)
            # if event.is_set():
            #     print('calculate stopped')
            #     return

            para['分路位置'] = posi_bei

            md.train1.posi_rlt = posi_bei
            md.train1.set_posi_abs(0)

            posi_zhu = posi_bei
            md.train2.posi_rlt = posi_zhu
            md.train2.set_posi_abs(0)

            m1 = MainModel(md.lg, md=md)

            # zm_sva = 2 * np.pi * freq * data["SVA'互感"] * 1e-6 * 1j
            #
            # # list_sva1_mutual = [(3, 4, '右'), (3, 4, '左') ,(4, 3, '右') ,(4, 3, '左')]
            # list_sva1_mutual = [(3, 4, '右')]
            # for sva1_mutual in list_sva1_mutual:
            #     config_sva1_mutual(m1, sva1_mutual, zm_sva)
            #
            # m1.equs.creat_matrix()
            # m1.equs.solve_matrix()

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

            #################################################################################

            # data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
            data2excel.add_data(sheet_name="主串分路电流", data1=i_sht_zhu)
            data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_bei)
            data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_bei)
            # data2excel.add_data(sheet_name="被串轨入电压", data1=v_rcv_bei)
            # data2excel.add_data(sheet_name="主串SVA'电流", data1=i_sva1)
            # data2excel.add_data(sheet_name="被串钢轨电流折算后", data1=i_trk_bei_temp)
            # data2excel.add_data(sheet_name="实测阻抗", data1=z_mm)
            # data2excel.add_data(sheet_name="阻抗模值", data1=z_mm_abs)
            # data2excel.add_data(sheet_name="耦合系数", data1=co_mutal)

        # if (length+1) > columns_max:
        #     columns_max = length + 1
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
        MAX_I = para['MAX_CURRENT'][data['主串频率(Hz)']]

        # if data['故障位置'] == '无':
        #     max_i_normal = max_i
        #
        # data['干扰值变化'] = max_i / max_i_normal - 1
        #
        # print('%.2fmA, %.2f%%' % (max_i, data['干扰值变化'] * 100))

        print('%.2fmA' % max_i)

        # if max_i > MAX_I:
        #     text = '干扰频率：' + str(data['主串频率(Hz)']) + 'Hz，'\
        #            + '干扰电流上限' + str(MAX_I) + 'mA；第' \
        #            + str(counter) \
        #            + '行数据干扰电流超上限：最大干扰电流为' \
        #            + str(round(max_i, 1)) \
        #            + 'mA，位于距离被串发送端' \
        #            + str(round(data['被串最大干扰位置(m)'], 0)) \
        #            + 'm处'
        #     for key in head_list:
        #         data[key] = None
        #
        #     data2excel.refresh_row()
        #
        #     # data['备注'] = text
        #     raise KeyboardInterrupt(text)

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
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    posi_header = list(range(columns_max))
    # posi_header[0] = '发送端'
    # posi_header[0] = '主串发送端'
    # posi_header = None

    data2excel.config_header()
    # data2excel["被串钢轨电流"].header[0] = '被串发送端'
    # data2excel["被串分路电流"].header[0] = '被串发送端'
    # data2excel["主串钢轨电流"].header[0] = '被串发送端'
    # data2excel["主串分路电流"].header[0] = '被串发送端'
    # data2excel["主串轨面电压"].header[0] = '主串发送端'

    df_data = pd.DataFrame(excel_data, columns=head_list)

    #################################################################################

    # 保存到本地excel
    # filename = '仿真输出'
    # filepath = 'src/Output/'+ filename + timestamp + '.xlsx'
    # filepath = ''+ filename + '_' + timestamp + '.xlsx'
    filepath = path2

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

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
        "被串钢轨电流",
        "被串分路电流",
        # "主串钢轨电流",
        # "主串分路电流",
        # "主串轨面电压",
        # "主串SVA'电流",
        # "被串钢轨电流折算后",
        # "被串轨入电压",
        # "主串TB电流",
        # "被串TB电流",
        # "主串TB电压",
        # "被串TB电压",
    ]

    # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
    # data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)
    data2excel.write2excel(sheet_names=names, writer=writer)

    writer.save()
    # return 1
    #
    #
    #
    #
    #
    # # main(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main_cal('邻线干扰参数输入_QJ_V003.xlsx',
             '仿真输出' + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx',
             )
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
