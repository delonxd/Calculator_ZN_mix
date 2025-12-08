from src.Method import columns_header
import pandas as pd
import itertools


def config_input_1128():

    # print(df_input)

    # ret = pd.DataFrame(columns=columns_header())
    # counter = 1
    # index = 1
    #
    # freq_zhu = [2600]
    # freq_bei = [2300]
    # freq_zhu = [1700]
    # freq_bei = [1700]

    # scene_list = [
    #    [[695, 8], [595, 6]]
    # ]

    scene_list = [
       # [[500, 6], [500, 6], '-', '-', 2600, 1700, '左发', '右发'],
       # [[500, 6], [500, 6], '-', '-', 2600, 1700, '左发', '左发'],
       [[500, 6], [500, 6], '-', '-', 2600, 2300, '左发', '右发'],
       [[500, 6], [500, 6], '-', '-', 2600, 2300, '左发', '左发'],
       # [[600, 8], [600, 8], '-', '-', 2600, 1700, '左发', '右发'],
       # [[600, 8], [600, 8], '-', '-', 2600, 1700, '左发', '左发'],
       [[600, 8], [600, 8], '-', '-', 2600, 2300, '左发', '右发'],
       [[600, 8], [600, 8], '-', '-', 2600, 2300, '左发', '左发'],
    ]

    # scene_list = [
    #    [[650, 8], [650, 8], '-', '-']
    # ]

    # scene_list = [
    #    [[690, 8], [615, 7], '-', '2973BG', -118],
    #    [[675, 8], [615, 7], '-', '2961BG', 2],
    # ]
    # sec_length = {
    #     '区间-普铁': [500],
    #     # '区间-普铁': [1400, 1000, 500],
    #     # '区间-高铁': [1400, 1000, 500],
    #     # '站内-有选频': [650, 500, 350],
    #     # '站内-无选频': [650, 500, 350],
    # }
    # sec_type = list(sec_length.keys())

    list0 = []

    index = 0

    for scene in scene_list:
        zhu_len = scene[0][0]
        bei_len = scene[1][0]
        zhu_cnum = scene[0][1]
        bei_cnum = scene[1][1]

        zhu_name = scene[2]
        bei_name = scene[3]

        zhu_freq = scene[4]
        bei_freq = scene[5]

        zhu_sr_mode = scene[6]
        bei_sr_mode = scene[7]

        # for offset in [0]:
        # for offset in [scene[4]]:
        for offset in range(-200, 201, 10):

            row = pd.Series(index=columns_header(), dtype='object')

            # row['故障位置'] = error
            # row['故障类型'] = e_type

            row['序号'] = int(index)
            # row['主串区段'] = '-'
            # row['被串区段'] = '-'

            row['主串区段'] = zhu_name
            row['被串区段'] = bei_name

            row['耦合系数'] = 24

            row['主串方向'] = zhu_sr_mode
            row['被串方向'] = bei_sr_mode

            row['主串区段长度(m)'] = zhu_len
            row['被串区段长度(m)'] = bei_len

            row['错位'] = offset
            row['被串相对位置(m)'] = offset - bei_len

            # row['分路起点'] = offset - 14.5
            # row['分路终点'] = offset + bei_len + 14.5

            if bei_sr_mode == '左发':
                row['分路起点'] = offset - 14.5
                row['分路终点'] = offset + 14.5 + bei_len * 2
            elif bei_sr_mode == '右发':
                row['分路起点'] = offset - 14.5 - bei_len
                row['分路终点'] = offset + 14.5 + bei_len
            else:
                raise KeyboardInterrupt('bei_sr_mode error')

            row['主串电平级'] = 4
            row['被串电平级'] = 4

            row['主串频率(Hz)'] = zhu_freq
            row['被串频率(Hz)'] = bei_freq

            row['主串电缆长度(km)'] = 10
            row['被串电缆长度(km)'] = 10

            row['主串电容数(含TB)'] = zhu_cnum
            row['被串电容数(含TB)'] = bei_cnum

            row['主串电容值(μF)'] = 50
            row['被串电容值(μF)'] = 50

            row['主串道床电阻(Ω·km)'] = 10000
            row['被串道床电阻(Ω·km)'] = 10000

            # row['主串TB模式'] = '无TB'
            # row['被串TB模式'] = '无TB'

            row['调谐区长度'] = 29

            row['分路电阻(Ω)'] = 1e-7
            row['分路间隔(m)'] = 1

            # print(ret.loc[index, '调谐区长度'])
            list0.append(row)

            index += 1
    ret = pd.DataFrame(list0)
    return ret


def config_input_20230720_pusu(sec_type, sec_length):

    columns = [
        '序号',
        '主串类型',
        '被串类型',
        '主串频率',
        '被串频率',
        '区段长度',
        '相对位置',
        # '主串方向',
        # '被串方向',
    ]

    # list0 = [1, 2]
    list1 = [1700, 2000, 2300, 2600]
    list2 = [1700, 2000, 2300, 2600]
    # list3 = [400, 500, 600, 700, 800, 1000, 1200]

    list0 = [sec_type]
    # list1 = [2600]
    # list2 = [2000]
    list3 = [sec_length]

    list4 = [0]

    total_list = list(itertools.product(
        list0, list1, list2, list3, list4))

    df = pd.DataFrame(index=columns, dtype='object')

    counter = 0
    for val in total_list:

        length = val[3]
        offset = -length
        while offset <= length:
            s0 = pd.Series(name=counter, index=columns)

            s0['序号'] = s0.name

            flag = val[0]
            if flag == 1:
                s0['主串类型'] = '高铁'
                s0['被串类型'] = '普速'
            else:
                s0['主串类型'] = '普速'
                s0['被串类型'] = '高铁'

            s0['主串频率'] = val[1]
            s0['被串频率'] = val[2]

            s0['区段长度'] = length
            s0['相对位置'] = offset

            print('generate row: %s --> %s' % (counter, s0.tolist()))

            df = pd.concat([df, s0], axis=1)

            offset += 50
            counter += 1

    df = df.transpose()

    return df


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 10000)

    # config_input_20230720_pusu()
