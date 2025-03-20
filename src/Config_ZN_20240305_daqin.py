import pandas as pd
import numpy as np
from src.Method import check_input_v01, columns_header, get_tb_mode


def regular_input_20240305_daqin(df_input, calc_type):
    df_input = df_input.replace(r'^\s*$', np.nan, regex=True)
    df_input = df_input.dropna(how='all', axis=0)

    if calc_type == '1对1':
        group = 2
    elif calc_type == '2对1':
        group = 4
    else:
        raise KeyboardInterrupt('calc_type错误')

    df_input.columns = map(lambda x: x.split('\n')[0], df_input.columns)
    check_input_v01(df_input, group)

    # print(df_input)

    ret = pd.DataFrame(columns=columns_header())
    counter = 1
    index = 1

    name1 = ''
    name2 = ''

    for _, row in df_input.iterrows():
        if row['频率'] is None:
            break

        if counter % group == 1:
            name1 = row['线路名称']
            name2 = row['车站名称']

        if counter % 2 == 1:
            ret.loc[index, '序号'] = index
            ret.loc[index, '线路名称'] = name1
            ret.loc[index, '车站名称'] = name2

            ret.loc[index, '线间距'] = row['线间距']
            ret.loc[index, '耦合系数'] = row['耦合系数']
            ret.loc[index, '并行长度(m)'] = row['并行长度']

            ret.loc[index, '主串区段'] = row['区段名称']
            ret.loc[index, '主串区段类型'] = row['配置']
            ret.loc[index, '主串区段长度(m)'] = row['区段长度']
            ret.loc[index, '主串坐标'] = row['左端坐标']

            ret.loc[index, '主串频率(Hz)'] = row['频率']
            ret.loc[index, '主串电平级'] = int(row['发送电平级'])
            ret.loc[index, '主串电缆长度(km)'] = 10
            ret.loc[index, '主串电容值(μF)'] = 50
            ret.loc[index, '主串道床电阻(Ω·km)'] = 10000
            # ret.loc[index, '被串相对位置(m)'] = row['区段长度'] - row['并行长度']
            # ret.loc[index, '主串电容数(含TB)'] = int(-(-row['区段长度'] // 100))
            ret.loc[index, '主串电容数(含TB)'] = int(row['电容个数（包含TB）'])
            ret.loc[index, '主串TB模式'] = get_tb_mode(row['左端是否有TB'], row['右端是否有TB'])
            ret.loc[index, '主串方向'] = '左发'

        else:
            ret.loc[index, '被串区段'] = row['区段名称']
            ret.loc[index, '被串区段类型'] = row['配置']
            ret.loc[index, '被串区段长度(m)'] = row['区段长度']
            ret.loc[index, '被串坐标'] = row['左端坐标']

            ret.loc[index, '被串频率(Hz)'] = row['频率']
            ret.loc[index, '被串电平级'] = int(row['发送电平级'])
            ret.loc[index, '被串电缆长度(km)'] = 10
            ret.loc[index, '被串电容值(μF)'] = 50
            ret.loc[index, '被串道床电阻(Ω·km)'] = 10000
            ret.loc[index, '被串电容数(含TB)'] = int(row['电容个数（包含TB）'])
            ret.loc[index, '被串TB模式'] = get_tb_mode(row['左端是否有TB'], row['右端是否有TB'])
            ret.loc[index, '被串方向'] = '左发'

            index += 1

        counter += 1

    for _, row in ret.copy().iterrows():

        ret.loc[index] = row
        ret.loc[index, '序号'] = index
        ret.loc[index, '主串区段'] = row['被串区段']
        ret.loc[index, '被串区段'] = row['主串区段']
        ret.loc[index, '主串区段类型'] = row['被串区段类型']
        ret.loc[index, '被串区段类型'] = row['主串区段类型']
        ret.loc[index, '主串区段长度(m)'] = row['被串区段长度(m)']
        ret.loc[index, '被串区段长度(m)'] = row['主串区段长度(m)']
        # ret.loc[index, '被串相对位置(m)'] = -row['被串相对位置(m)']

        ret.loc[index, '主串坐标'] = row['被串坐标']
        ret.loc[index, '被串坐标'] = row['主串坐标']

        ret.loc[index, '主串电平级'] = row['被串电平级']
        ret.loc[index, '被串电平级'] = row['主串电平级']
        ret.loc[index, '主串频率(Hz)'] = row['被串频率(Hz)']
        ret.loc[index, '被串频率(Hz)'] = row['主串频率(Hz)']
        ret.loc[index, '主串电容数(含TB)'] = row['被串电容数(含TB)']
        ret.loc[index, '被串电容数(含TB)'] = row['主串电容数(含TB)']
        ret.loc[index, '主串TB模式'] = row['被串TB模式']
        ret.loc[index, '被串TB模式'] = row['主串TB模式']

        index += 1

    if calc_type == '2对1':
        ret2 = ret.copy()
        ret = pd.DataFrame(columns=columns_header())

        length = index - 1
        for i in range(length):

            t1 = i // 4
            t2 = (i % 4) // 2
            t3 = (i % 4) % 2

            i2 = int(t2 * length / 2 + t1 * 2 + t3)

            ret.loc[i+1, :] = ret2.iloc[i2, :]
            ret.loc[i+1, '序号'] = i+1

    for _, row in ret.copy().iterrows():
        ret.loc[index] = row
        ret.loc[index, '序号'] = index
        ret.loc[index, '主串方向'] = '右发'
        ret.loc[index, '被串方向'] = '右发'
        index += 1

    return ret
