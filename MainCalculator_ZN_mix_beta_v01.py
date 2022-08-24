from src.Model.PreModel import *
from src.Method import *
from src.ConfigHeadList import *
from src.Data2Excel import *
from src.RowData import RowData

import pandas as pd
import time
import os

from functools import wraps


def try_calc(time0):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except BaseException as e:
                print(e)
            print("按任意键继续...")

        return wrapped_function
    return logging_decorator


def log_timestamp(val: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ret = timestamp + ' ' + val
    print(ret)
    return ret


@try_calc(None)
def main_cal(path1, path2, window):
    path3 = os.getcwd()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    #################################################################################

    calc_types = ["1对1", "2对1"]
    # calc_types = ["2对1"]

    input_dict = dict()

    for calc_type in calc_types:
        # 参数输入

        log_timestamp('检查%s表格数据 ...' % calc_type)

        df_input = pd.read_excel(path1, sheet_name=calc_type)
        df_input = df_input.where(df_input.notnull(), None)

        df_input = regular_input(df_input, calc_type)
        input_dict[calc_type] = df_input

        log_timestamp('检查完成')

        log_timestamp('计算%s干扰值 ...' % calc_type)

        df_input = input_dict[calc_type]
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
        trk_21 = ImpedanceMultiFreq()
        trk_21.rlc_s = {
            1700: [1.177, 1.314e-3, None],
            2000: [1.306, 1.304e-3, None],
            2300: [1.435, 1.297e-3, None],
            2600: [1.558, 1.291e-3, None]}

        para['Trk_z'].rlc_s = trk_21.rlc_s

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
        head_list = config_headlist_ZN_mix()

        # 初始化excel数据
        excel_data = []
        data2excel = SheetDataGroup(sheet_names=[])

        #################################################################################

        columns_max = 0
        counter = 1

        pd_read_flag = True
        # pd_read_flag = False

        arr1 = np.array([])
        arr2 = np.array([])

        for temp_temp in range(num_len):

            #################################################################################

            # # 封装程序显示
            # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # if getattr(sys, 'frozen', False):
            #     print(df_input[temp_temp:(temp_temp + 1)])
            # print(temp_temp)
            log_timestamp('计算第%s行数据 ...' % str(counter))

            #################################################################################

            # 数据表初始化
            data = dict()
            for key in head_list:
                data[key] = None

            # 打包行数据
            df_input_row = df_input.iloc[temp_temp]
            row_data = RowData(df_input_row, para, data, pd_read_flag)

            #################################################################################

            # 载入数据
            flag = pd_read_flag

            # 序号
            # row_data.config_number(counter, pd_read_flag=flag)
            row_data.config_number(counter, pd_read_flag=False)

            # 备注
            # row_data.config_remarks('主分路被调整', pd_read_flag=False)
            row_data.config_remarks('无', pd_read_flag=flag)

            row_data.config_sec_name('235G', 'XWG', pd_read_flag=flag)

            row_data.config_sec_length(1342, 665, pd_read_flag=flag)
            # row_data.config_offset(0, pd_read_flag=False)
            row_data.config_offset(0, pd_read_flag=True)

            row_data.config_mutual_coeff(24, pd_read_flag=flag)
            row_data.config_freq(2300, 2300, pd_read_flag=flag)
            # row_data.config_freq(cv1, cv2, pd_read_flag=flag)
            row_data.config_c_num(7, 7, pd_read_flag=flag)
            row_data.config_c_posi(None, None, pd_read_flag=False)
            # if temp_temp == 4:
            #     row_data.config_c_posi(None, [514/2], pd_read_flag=False)
            row_data.config_c2TB(False)

            row_data.config_c_value(25, 25, pd_read_flag=flag)
            # row_data.config_c_inhibitor(pd_read_flag=flag)

            # row_data.config_c_fault_mode('无', cv2, pd_read_flag=flag)
            # row_data.config_c_fault_num([], cv3, pd_read_flag=flag)

            # row_data.config_c_fault_mode(['无'], ['无'], pd_read_flag=flag)
            # row_data.config_c_fault_num([], [], pd_read_flag=flag)
            row_data.config_c_fault_mode(['无'], ['无'], pd_read_flag=False)
            row_data.config_c_fault_num([], [], pd_read_flag=False)

            row_data.config_rd(10000, 10000, pd_read_flag=flag, respectively=True)

            row_data.config_trk_z(pd_read_flag=False, respectively=False)

            # TB模式
            # row_data.config_TB_mode('无TB', pd_read_flag=False)
            row_data.config_TB_mode('双端TB', pd_read_flag=flag)
            # row_data.config_TB_mode('双端TB', pd_read_flag=False)

            # row_data.config_sr_mode('右发', '右发', pd_read_flag=False)
            # row_data.config_sr_mode('右发', '左发', pd_read_flag=False)
            row_data.config_sr_mode('', '', pd_read_flag=True)

            row_data.config_pop([], [], pd_read_flag=False)
            # if temp_temp == 1:
            #     row_data.config_pop([], [2,4,5], pd_read_flag=False)
            # elif temp_temp == 3:
            #     row_data.config_pop([2,4,5], [], pd_read_flag=False)

            row_data.config_cable_para()
            row_data.config_cable_length(10, 10, pd_read_flag=flag, respectively=True)
            # row_data.config_r_sht(1e-7, 1e-7, pd_read_flag=flag, respectively=True)
            row_data.config_r_sht(1e-7, 1e-7, pd_read_flag=False, respectively=True)
            row_data.config_power(5, '最大', pd_read_flag=flag)

            row_data.config_sp_posi()
            row_data.config_train_signal()
            row_data.config_error()

            # interval = row_data.config_interval(1, pd_read_flag=flag)
            interval = row_data.config_interval(1, pd_read_flag=False)

            if data['被串故障模式'] is None:
                print(para['freq_被'], para['被串故障模式'])
                continue
            data2excel.add_new_row()

            len_posi = 0
            #################################################################################

            # 分路计算

            md = PreModel_V001(parameter=para)

            md.add_train()
            # md.add_train_bei()

            # posi_list = np.arange(data['被串区段长度(m)']*3 + 14.5, -14.50001, -interval)

            flag_l = data['被串左端里程标']
            flag_r = data['被串左端里程标'] + data['被串区段长度(m)']

            # if data['被串方向'] == '正向':
            #     posi_list = np.arange(flag_r, flag_l - 0.0001, -interval)
            # else:
            #     posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

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

            for posi_bei in posi_list:

                if window is not None:
                    if window.event.is_set():
                        log_timestamp('计算中止')
                        # print('calculate stopped')
                        return

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
            data['被串最大干扰位置(m)'] = round(i_trk_list.index(max(i_trk_list))*interval)

            data_row = [data[key] for key in head_list]
            excel_data.append(data_row)

            if calc_type == '2对1':

                if counter % 5 == 1:
                    arr1 = np.array(i_trk_list)
                    arr2 = np.array(i_sht_list)
                elif counter % 5 == 2:
                    counter += 1

                    log_timestamp('计算第%s行数据 ...' % str(counter))

                    list1 = list(arr1 + np.array(i_trk_list))
                    list2 = list(arr2 + np.array(i_sht_list))
                    data2excel.data_dict['被串钢轨电流'].data_list.append(list1)
                    data2excel.data_dict['被串分路电流'].data_list.append(list2)
                    data2excel.data_dict['主串分路电流'].data_list.append([])

                    data_sum = dict()
                    for index, key in enumerate(head_list):
                        if key == '序号':
                            data_sum[key] = counter
                        elif key == '备注':
                            data_sum[key] = str('合并%s、%s' % (counter-2, counter-1))
                        elif key in [
                            '线间距(m)',
                            '耦合系数(μH/km)',
                            '并行长度(m)',
                            '被串相对位置(m)',
                            '主串区段',

                            '主串区段长度(m)',
                            '主串左端坐标',
                            '主串电容数(含TB)',

                            '主串区段类型',
                            '主串TB模式',
                            '主串电平级',
                        ]:
                            data_sum[key] = None
                        else:
                            data_sum[key] = data[key]

                    data_sum['被串最大干扰电流(A)'] = max(list1)
                    data_sum['被串最大干扰位置(m)'] = round(list1.index(max(list1)) * interval)

                    data_row = [data_sum[key] for key in head_list]
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
        # posi_header[0] = '被串接收端'

        data2excel.config_header()

        df_data = pd.DataFrame(excel_data, columns=head_list)

        #################################################################################

        # 保存到本地excel

        path = path2[:-5] + '_' + calc_type + '.xlsx'
        writer = pd.ExcelWriter(path, engine='xlsxwriter')

        workbook = writer.book
        header_format = workbook.add_format({
            'bold': True,  # 字体加粗
            'text_wrap': True,  # 是否自动换行
            'valign': 'vcenter',  # 垂直对齐方式
            'align': 'center',  # 水平对齐方式
            'border': 1})

        # if pd_read_flag:
        #     write_to_excel(df=df_input, writer=writer, sheet_name="参数设置", hfmt=header_format)
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

    log_timestamp('计算完成')


def main_test():
    path1 = '邻线干扰单独核算区段输入模板-V1.0.xlsx'
    path2 = '仿真输出_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx'

    main_cal(path1, path2, None)


if __name__ == '__main__':
    # import threading
    # main_cal('邻线干扰单独核算区段输入模板-V1.0.xlsx',
    #          '仿真输出' + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx',
    #          threading.Event())
    # main(sys.argv[1], sys.argv[2], sys.argv[3])

    main_test()
