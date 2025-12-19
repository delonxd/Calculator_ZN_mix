from src.Method import write_to_excel
from src.logMethod import MainLog
from src.Data2Excel import SheetDataGroup
from src.Model.ModelParameter import ModelParameter

from src.Config_ZN_20250818_digital_adj import config_input_20250818_digital
from src.Config_ZN_20250818_digital_adj import config_headlist_20250818_digital
from src.Config_ZN_20250818_digital_adj import calculate_row_data_adj

import pandas as pd
import time
import os
# import itertools
# import sys


def main_cal_20250818_digital_adj(mode, input_path, output_path):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    MainLog.add_log_accurate(f'       mode --> {mode}')
    MainLog.add_log_accurate(f' input path --> {input_path}')
    MainLog.add_log_accurate(f'output path --> {output_path}')

    #################################################################################

    # 参数输入

    df_input = config_input_20250818_digital(mode, input_path)
    size = len(list(df_input['序号']))

    # 检查输入格式
    # check_input(df_input)

    #################################################################################

    # # 获取时间戳
    # localtime = time.localtime()
    # timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    #################################################################################

    # 初始化变量
    work_path = os.getcwd()
    # work_path = path3
    para = ModelParameter(workpath=work_path)

    #################################################################################

    # 获取表头
    head_list = config_headlist_20250818_digital(mode)

    #################################################################################

    # 初始化excel数据
    excel_data = []
    data2excel = SheetDataGroup(sheet_names=[])

    #################################################################################

    counter = 1

    MainLog.add_log_accurate('start calculate')
    MainLog.add_log_accurate(f'total scenes: {size}')

    for row_num in range(size):

        #################################################################################

        # # 封装程序显示
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # if getattr(sys, 'frozen', False):
        #     print(df_input[temp_temp:(temp_temp + 1)])
        # print(temp_temp)
        # print('calculating line ' + str(counter) + ' ...')

        MainLog.add_log_accurate('-' * 50)
        MainLog.add_log_accurate(f'scene: {counter} / {size} ...')

        #################################################################################

        # 数据表初始化
        data = dict()
        for key in head_list:
            data[key] = None

        # 打包行数据
        df_input_row = df_input.iloc[row_num]

        # 配置数据
        calculate_row_data_adj(
            df_input=df_input_row,
            para=para,
            data=data,
            data2excel=data2excel,
            mode=mode,
        )

        #################################################################################
        data_row = [data[key] for key in head_list]
        excel_data.append(data_row)
        counter += 1

        #################################################################################

        # if not getattr(sys, 'frozen', False):
        #     print(data.keys())
        #     print(data.values())
        #     print(i_sht_list)

    #################################################################################

    # 修正表头
    data2excel.config_header()
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

    # write_to_excel(df=df_input, writer=writer, sheet_name="参数设置", hfmt=header_format)
    write_to_excel(df=df_data, writer=writer, sheet_name="数据输出", hfmt=header_format)

    names = [
        "钢轨电流",
        "分路电流",
    ]

    # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
    # data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)
    data2excel.write2excel(sheet_names=names, writer=writer)

    writer.save()
    # return 1
    MainLog.add_log_accurate(f'complete.')


if __name__ == '__main__':

    # timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # # path1 = ''
    # # # path1 = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——一送一受.xlsx'
    # # # path1 = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——两送一受.xlsx'
    # path1 = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——一送两受.xlsx'
    # path2 = f'20250530_车站数字化调整表\\仿真输出_{timestamp}.xlsx'
    #
    # # main_cal('一送一受', path1, path2)
    # # main_cal('两送一受', path1, path2)
    # main_cal_20250818_digital_adj('一送两受', path1, path2)

    # path_dict = {
    #     '一送一受': 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——一送一受.xlsx',
    #     '两送一受': 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——两送一受.xlsx',
    #     '一送两受': 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\车站数字化调整表——一送两受.xlsx',
    # }
    #
    # for cnd, path1 in path_dict.items():
    #     timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    #     path2 = f'20250530_车站数字化调整表\\仿真输出_{timestamp}_{cnd}.xlsx'
    #     main_cal_20250818_digital_adj(cnd, path1, path2)

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    cnd = '两送一受'
    # cnd = '一送一受'
    # path1 = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\参数输入_蒙元_一送一受.xlsx'
    # path2 = f'20250530_车站数字化调整表\\仿真输出_{timestamp}_蒙元_{cnd}.xlsx'
    # path1 = 'C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\参数输入_一送一受_核对.xlsx'
    # path2 = f'20250530_车站数字化调整表\\仿真输出_{timestamp}_核对_{cnd}.xlsx'

    dir1 = "C:\\Users\\李继隆\\Desktop\\车站数字化调整表\\蒙元站"
    path1 = f"{dir1}\\蒙元点石沟装车站_{cnd}_核对.xlsx"
    path2 = f"{dir1}\\仿真输出_蒙元点石沟装车站_{cnd}_核对_{timestamp}.xlsx"

    main_cal_20250818_digital_adj(cnd, path1, path2)
