from src.Method import write_to_excel
from src.logMethod import MainLog
from src.Data2Excel import SheetDataGroup
from src.Model.ModelParameter import ModelParameter
from src.ImpedanceParaType import ImpedanceMultiFreq

from src.Model.MainModel import MainModel
from src.Method import get_i_trk


from src.Config_ZN_20251027_digital_iterate import config_input_20251027_digital_iterate
from src.Config_ZN_20251027_digital_iterate import config_headlist_20251027_digital_iterate
from src.Config_ZN_20251027_digital_iterate import config_row_data_20251027_digital_iterate
from src.Config_ZN_20251027_digital_iterate import PreModel_20251027_digital_iterate

import pandas as pd
import numpy as np
import time
import os


def main_cal(output_path, work_path):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    #################################################################################

    # 参数输入

    # df_input = pd.read_excel(input_path, sheet_name='参数输入')
    # df_input = df_input.where(df_input.notnull(), None)

    df_input = config_input_20251027_digital_iterate()
    # df_input = config_input_20240814_digital_twin()

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
    # work_path = path3
    para = ModelParameter(workpath=work_path)

    para['MAX_CURRENT'] = {
        1700: 197,
        2000: 175,
        2300: 162,
        2600: 150,
    }

    para['Ccmp_z_change_zhu'] = ImpedanceMultiFreq()
    para['Ccmp_z_change_chuan'] = ImpedanceMultiFreq()

    para['TB_引接线_有砟'] = ImpedanceMultiFreq()
    para['TB_引接线_有砟'].z = {
        1700: (8.33 + 31.4j)*1e-3,
        2000: (10.11 + 35.2j)*1e-3,
        2300: (11.88 + 39.0j)*1e-3,
        2600: (13.60 + 42.6j)*1e-3}

    #################################################################################

    # 获取表头
    head_list = config_headlist_20251027_digital_iterate()

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
        config_row_data_20251027_digital_iterate(df_input_row, para, data)

        interval = data['分路间隔(m)']

        data2excel.add_new_row()

        len_posi = 0

        # 分路计算
        md = PreModel_20251027_digital_iterate(parameter=para)

        md.add_train()

        flag_l = data['分路起点']
        flag_r = data['分路终点']

        posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

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

            i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')
            i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu, direct='右')
            pwr_tcsr = '右调谐单元'

            v_rcv_bei = md.lg['线路4']['地面']['区段1']['中间接收']['1接收器']['U'].value_c
            v_rcv_zhu = md.lg['线路3']['地面']['区段1']['中间接收']['1接收器']['U'].value_c

            v_pwr_zhu = md.lg['线路3']['地面']['区段1'][pwr_tcsr]['1发送器']['2内阻']['U2'].value_c
            i_pwr_zhu = md.lg['线路3']['地面']['区段1'][pwr_tcsr]['1发送器']['2内阻']['I2'].value_c

            #################################################################################

            data2excel.add_data(sheet_name="主串功出电压", data1=v_pwr_zhu)
            data2excel.add_data(sheet_name="主串功出电流", data1=i_pwr_zhu)
            data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
            data2excel.add_data(sheet_name="主串分路电流", data1=i_sht_zhu)
            data2excel.add_data(sheet_name="主串轨入电压", data1=v_rcv_zhu)
            data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_bei)
            data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_bei)
            data2excel.add_data(sheet_name="被串轨入电压", data1=v_rcv_bei)

        # if (length+1) > columns_max:
        #     columns_max = length + 1
        if len_posi > columns_max:
            columns_max = len_posi

        i_trk_list = data2excel.data_dict["被串钢轨电流"][-1]
        # i_sht_list = data2excel.data_dict["被串分路电流"][-1]

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

    # posi_header = list(range(columns_max))
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
    filepath = output_path

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

    workbook = writer.book
    header_format = workbook.add_format({
        'bold': True,  # 字体加粗
        'text_wrap': True,  # 是否自动换行
        'valign': 'vcenter',  # 垂直对齐方式
        'align': 'center',  # 水平对齐方式
        'border': 1})

    write_to_excel(df=df_input, writer=writer, sheet_name="参数输入", hfmt=header_format)
    write_to_excel(df=df_data, writer=writer, sheet_name="数据输出", hfmt=header_format)

    names = [
        # "主串功出电压",
        # "主串功出电流",
        # "主串钢轨电流",
        "主串分路电流",
        # "主串轨入电压",
        "被串钢轨电流",
        "被串分路电流",
        # "被串轨入电压",
    ]

    # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
    # data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)
    data2excel.write2excel(sheet_names=names, writer=writer)

    writer.save()
    # return 1


if __name__ == '__main__':
    sub0 = '20251027_站内数字化两送一受遍历\\'
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())

    path1 = f'{sub0}\\仿真输出_站内数字化_两送一受_{timestamp}.xlsx'
    path2 = os.getcwd()

    main_cal(path1, path2)
