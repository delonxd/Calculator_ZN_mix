import pandas as pd
import itertools


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
