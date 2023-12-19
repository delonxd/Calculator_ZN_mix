from src.logMethod import *
from src.Data2Excel import *
from src.Config_QJ_20231128_huanganzhongji3 import *

import pandas as pd
import time
import os


def main_cal(_, path2, path3):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    #################################################################################

    # 参数输入
    df_input = config_input_20231128_huangan()

    df_input = df_input.where(df_input.notnull(), None)
    num_len = len(list(df_input['序号']))

    #################################################################################

    # 初始化变量
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

    # z_tb_2600_2000 = para['TB'][2600][2000].z

    #################################################################################

    # 获取表头
    head_list = config_headlist_20231128_huangan()

    #################################################################################

    # 初始化excel数据
    data_output = []
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

        MainLog.add_log_accurate('scene' + str(counter) + ' ...')

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
        config_row_data_20231128_huangan(df_input_row, para, data)

        interval = data['分路间隔(m)']

        data2excel.add_new_row()

        len_posi = 0

        # 分路计算

        md = PreModel_QJ_20231128_huangan(parameter=para)

        md.add_train()
        # md.add_train_bei()

        flag_l = data['分路起点']
        flag_r = data['分路终点']

        posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)

        MainLog.add_log_accurate('分路长度 --> %sm' % (flag_r - flag_l))

        # if data['被串方向'] == '左发':
        #     posi_list = np.arange(flag_r, flag_l - 0.0001, -interval)
        # elif data['被串方向'] == '右发':
        #     posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)
        # else:
        #     raise KeyboardInterrupt("被串方向应填写'左发'或'右发'")

        len_posi = max(len(posi_list), len_posi)

        tmp_posi = []

        for posi_bei in posi_list:
            para['分路位置'] = posi_bei

            md.train1.posi_rlt = posi_bei
            md.train1.set_posi_abs(0)

            posi_zhu = posi_bei
            md.train2.posi_rlt = posi_zhu
            md.train2.set_posi_abs(0)

            m1 = MainModel(md.lg, md=md)

            tmp_posi.append(posi_bei)
            if len(tmp_posi) == 100:
                MainLog.add_log_accurate('分路位置 --> %sm' % tmp_posi)
                tmp_posi = []

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

            if data['主串方向'] == '右发':
                i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu, direct='右')
            else:
                i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu, direct='左')

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

            i_trk_l = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='左')
            i_trk_r = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')

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

            data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
            data2excel.add_data(sheet_name="主串分路电流", data1=i_sht_zhu)
            data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_bei)
            data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_bei)
            # data2excel.add_data(sheet_name="被串分路点左侧钢轨电流", data1=i_trk_l)
            # data2excel.add_data(sheet_name="被串分路点右侧钢轨电流", data1=i_trk_r)
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

        MainLog.add_log_accurate('最大干扰电流 --> %.2fmA' % max_i)

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
        data_output.append(data_row)

        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # path_tmp = '20231128_黄庵中继3\\仿真输出_黄庵中继3_%s_%s_%s.xlsx' % (data['被串区段'], data['分路模式'], time_str)
        path_tmp = '20231128_黄庵中继3\\仿真输出_黄庵中继3_%s_%s_%s.xlsx' % (time_str, data['主串区段'], '分路电流')

        MainLog.add_log_accurate('save to excel complete.')

        # save2excel_20231128_huangan(
        #     path=path_tmp,
        #     data_output=data_output,
        #     head_list=head_list,
        #     data_detail=data2excel,
        # )

        save2excel_20231205_huangan(
            path=path_tmp,
            data_output=data_output,
            head_list=head_list,
            data_detail=data2excel,
        )

        data_output = []
        data2excel = SheetDataGroup(sheet_names=[])

        counter += 1

    # save2excel_20231128_huangan(
    #     path=path2,
    #     data_output=data_output,
    #     head_list=head_list,
    #     data_detail=data2excel,
    # )


if __name__ == '__main__':
    sub_name = '20231128_黄庵中继3'
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    main_cal(None,
             '%s\\仿真输出_黄庵中继3_%s.xlsx' % (sub_name, timestamp),
             os.getcwd())
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
