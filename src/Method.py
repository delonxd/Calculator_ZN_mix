from src.AbstractClass.ElePack import *
from src.Module.JumperWire import *
from src.Model.SingleLineModel import *
import numpy as np
import pandas as pd
import itertools


#################################################################################

# 显示元素
def show_ele(vessel, para=''):
    if isinstance(vessel, (list, set)):
        list_t = list()
        for ele in vessel:
            if para == '':
                list_t.append(ele.__repr__())
            else:
                list_t.append(ele.__dict__[para].__repr__())
        list_t.sort()
        for ele in list_t:
            print(ele)
    elif isinstance(vessel, (dict, ElePack)):
        keys = sorted(list(vessel.keys()))
        for key in keys:
            if para == '':
                print(key, ':', vessel[key])
            else:
                print(vessel[key].__dict__[para])


#################################################################################

# 获取频率
def generate_frqs(freq1, m_num, flip_flag=False):
    frqs = list()
    if flip_flag:
        freq1.change_freq()
    for _ in range(m_num):
        frqs.append(freq1)
        freq1 = freq1.copy()
        freq1.change_freq()
    return frqs


#################################################################################

# 获取电容数
def get_c_nums(m_frqs, m_lens):
    c_nums = list()
    for num in range(len(m_frqs)):
        freq = m_frqs[num]
        length = m_lens[num]
        c_num = get_c_num(freq, length)
        c_nums.append(c_num)
    return c_nums


#################################################################################

# 获取电容数
def get_c_num(freq, length):
    if 0 < length < 300:
        index = 0
    elif length == 300:
        index = 1
    elif length > 300:
        index = int((length - 251) / 50)
    else:
        index  = 0

    CcmpTable1 = [0, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 15, 15, 16, 17, 18, 19, 20, 20, 21, 22, 23, 24, 25]
    CcmpTable2 = [0, 4, 5, 5, 6, 7,  7,  8,  8,  9, 10, 10, 11, 12, 12, 13, 13, 14, 15, 15, 16, 17, 17, 18, 18]

    freq = freq.value
    if freq == 1700 or freq == 2000:
        table = CcmpTable1
    elif freq == 2300 or freq == 2600:
        table = CcmpTable2
    else:
        table = []

    c_num = table[index]

    return c_num


#################################################################################

# 获取钢轨电流
def get_i_trk(line, posi, direct='右'):
    i_trk = None
    if direct == '右':
        if line.node_dict[posi].r_track is not None:
            i_trk = line.node_dict[posi].r_track['I1'].value_c
        else:
            i_trk = 0.0
    elif direct == '左':
        if line.node_dict[posi].l_track is not None:
            i_trk = line.node_dict[posi].l_track['I2'].value_c
        else:
            i_trk = 0.0

    return i_trk


#################################################################################

# 获取耦合系数
def get_mutual(distance):
    l1 = 6
    d = 1.435
    k1 = 13

    k_mutual = k1 / np.log((l1 * l1 - d * d) / l1 / l1)
    l2 = distance
    k2 = k_mutual * np.log((l2 * l2 - d * d) / l2 / l2)
    return k2


#################################################################################

# 配置SVA'互感
def config_sva1_mutual(model, temp, zm_sva):
    # zm_sva = 2 * np.pi * 1700 * 1 * 1e-6 * 1j
    m1 = model

    # temp_list = [(3, 4, '右'), (3, 4, '左') ,(4, 3, '左') ,(4, 3, '左')]
    # for temp in temp_list:
    line_zhu = '线路' + str(temp[0])
    line_bei = '线路' + str(temp[1])
    str_t = '线路组_' + line_bei + '_地面_区段1_' + temp[2] + '调谐单元_6SVA1_方程1'
    equ_t = m1.equs.equ_dict[str_t]
    str_t = '线路组_' + line_zhu + '_地面_区段1_' + temp[2] + '调谐单元'
    varb1 = m1[line_zhu]['元件'][str_t]['6SVA1']['I1']
    varb2 = m1[line_zhu]['元件'][str_t]['6SVA1']['I2']
    equ_t.varb_list.append(varb1)
    equ_t.varb_list.append(varb2)
    equ_t.coeff_list = np.append(equ_t.coeff_list, zm_sva)
    equ_t.coeff_list = np.append(equ_t.coeff_list, -zm_sva)


#################################################################################

# 配置跳线组
def config_jumpergroup(*jumpers):
    for jumper in jumpers:
        if not isinstance(jumper, JumperWire):
            raise KeyboardInterrupt('类型错误：参数需要为跳线类型')
        else:
            jumper.jumpergroup = list(jumpers)


#################################################################################

# 合并节点
def combine_node(nodes):
    if len(nodes) < 1:
        raise KeyboardInterrupt('数量错误：合并node至少需要1个参数')

    posi = nodes[0].posi
    node_new = Node(posi)
    node_new.node_type = 'combined'
    node_new.l_track = list()
    node_new.r_track = list()
    for node in nodes:
        if not isinstance(node, Node):
            raise KeyboardInterrupt('类型错误：合并node参数需要为节点类型')
        elif not node.posi == posi:
            raise KeyboardInterrupt('位置错误：合并node需要节点在相同水平位置')
        else:
            if node.l_track is not None:
                node_new.l_track.append(node.l_track)
            if node.r_track is not None:
                node_new.r_track.append(node.r_track)
            for key, value in node.element.items():
                node_new.element[key] = value
            node_new.equs.add_equations(node.equs)
    node_new.group_type = 'combined'
    return node_new


#################################################################################

# 合并节点组
def combine_node_group(lines):
    groups = NodeGroup()
    posi_set = set()
    for line in lines:
        posi_set.update(line.node_dict.posi_set)

    posi_list = list(posi_set)
    posi_list.sort()

    for posi in posi_list:
        nodes_list = list()
        for line in lines:
            if posi in line.node_dict.keys():
                nodes_list.append(line.node_dict[posi])
        nodes = tuple(nodes_list)
        node_new = combine_node(nodes)
        groups.node_dict[posi] = node_new

    return groups


#################################################################################

# 检查输入
def check_input(df):
    para = dict()
    para['FREQ'] = [1700, 2000, 2300, 2600]
    para['SEND_LEVEL'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    para['CABLE_LENGTH'] = [7.5, 10]
    para['C_NUM'] = [0, 1, 2, 3, 4, 5, 6, 7]
    para['TB_MODE'] = ['双端TB', '左端单TB', '右端单TB', '无TB']


    num_len = len(list(df['序号']))
    for temp_temp in range(num_len):
        df_input = df.iloc[temp_temp]

        # 检查主串名称格式
        name = str(df_input['主串区段'])
        if len(name) <= 8:
            pass
        else:
            raise KeyboardInterrupt("主串区段应填写长度小于等于8位的字符串")

        # 检查被串名称格式
        name = str(df_input['被串区段'])
        if len(name) <= 8:
            pass
        else:
            raise KeyboardInterrupt("被串区段应填写长度小于等于8位的字符串")

        # 检查主串方向格式
        if df_input['主串方向'] == '左发' or df_input['主串方向'] == '右发':
            pass
        else:
            raise KeyboardInterrupt("主串方向应填写'左发'或'右发'")

        # 检查被串方向格式
        if df_input['被串方向'] == '左发' or df_input['被串方向'] == '右发':
            pass
        else:
            raise KeyboardInterrupt("被串方向应填写'左发'或'右发'")

        # 检查主串区段长度格式
        if 0 <= df_input['主串区段长度(m)'] <= 650:
            pass
        else:
            raise KeyboardInterrupt("'主串区段长度(m)'应填写0~650的实数")

        # 检查被串区段长度格式
        if 0 <= df_input['被串区段长度(m)'] <= 650:
            pass
        else:
            raise KeyboardInterrupt("'被串区段长度(m)'应填写0~650的实数")

        # 检查被串相对位置格式
        if -650 <= df_input['被串相对位置(m)'] <= 650:
            pass
        else:
            raise KeyboardInterrupt("'被串相对位置(m)'应填写-650~650的实数")

        # 检查耦合系数格式
        if 0 < df_input['耦合系数'] <= 40:
            pass
        else:
            raise KeyboardInterrupt("'耦合系数'应填写大于0小于等于40的实数")

        # 检查主串电平级格式
        if df_input['主串电平级'] in para['SEND_LEVEL']:
            pass
        else:
            raise KeyboardInterrupt("'主串电平级'应填写1~9的整数")

        # 检查主串频率格式
        if df_input['主串频率(Hz)'] in para['FREQ']:
            pass
        else:
            raise KeyboardInterrupt("'主串频率(Hz)'应填写四种标准载频之一")

        # 检查被串频率格式
        if df_input['被串频率(Hz)'] in para['FREQ']:
            pass
        else:
            raise KeyboardInterrupt("'被串频率(Hz)'应填写四种标准载频之一")

        # 检查主串电缆长度格式
        if df_input['主串电缆长度(km)'] in para['CABLE_LENGTH']:
            pass
        else:
            raise KeyboardInterrupt("'主串电缆长度(km)'应填写7.5或10")

        # 检查被串电缆长度格式
        if df_input['被串电缆长度(km)'] in para['CABLE_LENGTH']:
            pass
        else:
            raise KeyboardInterrupt("'被串电缆长度(km)'应填写7.5或10")

        # 检查主串电容数格式
        if df_input['主串电容数(含TB)'] in para['C_NUM']:
            pass
        else:
            raise KeyboardInterrupt("'主串电容数(含TB)'应填写0~7之间的整数")

        # 检查被串电容数格式
        if df_input['被串电容数(含TB)'] in para['C_NUM']:
            pass
        else:
            raise KeyboardInterrupt("'被串电容数(含TB)'应填写0~7之间的整数")

        # 检查主串电容值格式
        if 25 <= df_input['主串电容值(μF)'] <= 80:
            pass
        else:
            raise KeyboardInterrupt("'主串电容值(μF)'应填写25~80的实数")

        # 检查被串电容值格式
        if 25 <= df_input['被串电容值(μF)'] <= 80:
            pass
        else:
            raise KeyboardInterrupt("'被串电容值(μF)'应填写25~80的实数")

        # 检查主串道床电阻格式
        if 0 < df_input['主串道床电阻(Ω·km)'] <= 10000:
            pass
        else:
            raise KeyboardInterrupt("'主串道床电阻(Ω·km)'应填写0~10000的正实数")

        # 检查被串道床电阻格式
        if 0 < df_input['被串道床电阻(Ω·km)'] <= 10000:
            pass
        else:
            raise KeyboardInterrupt("'被串道床电阻(Ω·km)'应填写0~10000的正实数")

        # 检查TB模式格式
        if df_input['TB模式'] in para['TB_MODE']:
            pass
        else:
            raise KeyboardInterrupt("'TB模式'应填写标准格式")


def get_section_length():

    import itertools
    param = list()
    zhu_list = range(50, 601, 50)

    for offset in range(50, 301, 50):
        for len1 in zhu_list:
            l_list = [-offset, offset]
            r_list = [len1 - offset, len1 + offset]

            for l_pos, r_pos in itertools.product(l_list, r_list):

                tmp = Param20201307(
                    len_zhu=len1,
                    l_pos=l_pos,
                    r_pos=r_pos,
                )
                if tmp.flg is True:
                    param.append(tmp)
                    print(tmp.lens_zhu, tmp.lens_bei, tmp.offset, tmp.index_bei)
    return param


class LengthParam:
    def __init__(self):
        self.zhu_length = list()
        self.bei_length = list()
        self.offset = 0


class Param20201307:

    def __init__(self, len_zhu, l_pos, r_pos):
        offset = abs(l_pos)
        self.flg = True
        self.l_pos = l_pos
        self.r_pos = r_pos

        self.lens_zhu = [len_zhu]

        tmp = r_pos - l_pos
        self.lens_bei = [len_zhu, tmp, len_zhu]

        # print(self.lens_bei)
        self.offset = None
        self.index_bei = None

        if abs(r_pos) < offset:
            self.flg = False

        if abs(len_zhu - l_pos) < offset:
            self.flg = False

        if r_pos <= l_pos:
            self.flg = False

        if r_pos - l_pos > 600:
            self.flg = False

        if l_pos < 0:
            self.offset = l_pos
            self.lens_bei.pop(0)
            self.index_bei = 0

            if r_pos >= len_zhu:
                self.lens_bei.pop(-1)

        elif l_pos > 0:
            self.offset = l_pos - len_zhu
            self.index_bei = 1

            if r_pos >= len_zhu:
                self.lens_bei.pop(-1)


def parallel(z1, z2):
    return (z1 * z2) / (z1 + z2)


def cal_zl(zpt, zin):
    zj = (0.037931222832602786+0.3334597710765984j)
    zca = (0.006459333+0.030996667j)
    z1 = (zpt * zin) / (zpt + zin) + zca
    return (z1 * zj) / (z1 + zj)


def regular_input(df_input, calc_type):
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
            ret.loc[index, '主串电容值(μF)'] = 25
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
            ret.loc[index, '被串电容值(μF)'] = 25
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

    for _, row in ret.copy().iterrows():
        ret.loc[index] = row
        ret.loc[index, '序号'] = index
        ret.loc[index, '主串方向'] = '右发'
        ret.loc[index, '被串方向'] = '右发'
        index += 1

    return ret


def get_tb_mode(val1, val2):
    if val1 == '有':
        val1 = True
    elif val1 == '无':
        val1 = False

    if val2 == '有':
        val2 = True
    elif val2 == '无':
        val2 = False

    if val1 is True and val2 is False:
        return '左端单TB'

    elif val1 is False and val2 is True:
        return '右端单TB'

    elif val1 is True and val2 is True:
        return '双端TB'

    elif val1 is False and val2 is False:
        return '无TB'


def check_input_v01(df_input, group):
    counter = 1
    data1 = [0] * 3

    mutual_dict = {
        4.5: 26.2,
        5: 21.0,
        5.5: 17.2,
        6: 14.4,
        6.5: 12.2,
        7: 10.5,
        7.5: 9.1,
        8: 8.0,
        8.5: 7.0,
        9: 6.3,
        9.5: 5.6,
        10: 5.1,
    }

    for _, row in df_input.iterrows():
        if row['频率'] is None:
            break

        check_data(
            read=row['区段长度'],
            calc=row['右端坐标'] - row['左端坐标'],
            error_type='区段长度错误',
        )

        if counter % group != 1:
            if not pd.isnull(row['线路名称']):
                raise KeyboardInterrupt('线路名称错误: 表格应合并')

            if not pd.isnull(row['车站名称']):
                raise KeyboardInterrupt('车站名称错误: 表格应合并')

        if counter % 2 == 0:

            if not pd.isnull(row['线间距']):
                raise KeyboardInterrupt('线间距错误: 表格应合并')

            if not pd.isnull(row['耦合系数']):
                raise KeyboardInterrupt('耦合系数错误: 表格应合并')

            data2 = [row['并行长度'], row['左端坐标'], row['右端坐标']]

            if data2[0] != data1[0]:
                raise KeyboardInterrupt('并行长度错误: 主被串并行长度不相等')

            length = min(data1[2], data2[2]) - max(data1[1], data2[1])

            check_data(
                read=data1[0],
                calc=length,
                error_type='并行长度错误',
            )

        else:
            data1 = [row['并行长度'], row['左端坐标'], row['右端坐标']]

            d0 = row['线间距']

            if d0 < 4.5:
                raise KeyboardInterrupt('线间距错误: 线间距应不小于4.5m')

            m1 = 0
            for key, value in mutual_dict.items():
                if d0 < key:
                    break
                m1 = value

            row['耦合系数'] = round(row['耦合系数'], 1)
            check_data(
                read=row['耦合系数'],
                calc=m1,
                error_type='耦合系数错误',
            )

        counter += 1

    row0 = pd.Series()
    freq = 0
    if group == 4:
        counter = 1

        for _, row in df_input.iterrows():
            if row['频率'] is None:
                break

            if counter % 4 == 2:
                row0 = row.copy().drop('并行长度')
            elif counter % 4 == 0:
                row1 = row.copy().drop('并行长度')

                row0 = row0.dropna()
                row1 = row1.dropna()

                if not row1.eq(row0).all():
                    raise KeyboardInterrupt('2对1数据错误: 被串区段数据不符')

            elif counter % 4 == 1:
                freq = row['频率']
            elif counter % 4 == 3:
                if freq != row['频率']:
                    raise KeyboardInterrupt('2对1数据错误: 主串区段频率不符')

            counter += 1


def check_data(read, calc, error_type):
    if read != calc:
        raise KeyboardInterrupt(
            '%s: 读取的数据为%s；应填写%.1f' %
            (error_type, read, calc)
        )


def get_c_num_mix(length):
    return -(-length // 100)


def columns_header():

    index = [
        '序号',
        '线路名称',
        '车站名称',

        '主串区段',
        '被串区段',

        '线间距',
        '耦合系数',
        '并行长度(m)',
        # '被串相对位置(m)',

        '主串方向',
        '被串方向',
        '主串区段类型',
        '被串区段类型',
        '主串区段长度(m)',
        '被串区段长度(m)',
        '主串坐标',
        '被串坐标',

        '主串电平级',
        '被串电平级',
        '主串频率(Hz)',
        '被串频率(Hz)',
        '主串电缆长度(km)',
        '被串电缆长度(km)',
        '主串电容数(含TB)',
        '被串电容数(含TB)',
        '主串电容值(μF)',
        '被串电容值(μF)',
        '主串道床电阻(Ω·km)',
        '被串道床电阻(Ω·km)',
        '主串TB模式',
        '被串TB模式',
    ]

    return index


def write_to_excel(df, writer, sheet_name, hfmt):
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, hfmt)


def init_input_1125():

    # print(df_input)

    ret = pd.DataFrame(columns=columns_header())
    counter = 1
    index = 1

    # freq_zhu = [1700, 2000, 2300, 2600]
    # freq_bei = [1700, 2000, 2300, 2600]


    freq_zhu = [2300]
    freq_bei = [2300]
    # freq_zhu = [1700]
    # freq_bei = [1700]
    sec_length = {
        '区间-普铁': [500],
        # '区间-普铁': [1400, 1000, 500],
        # '区间-高铁': [1400, 1000, 500],
        # '站内-有选频': [650, 500, 350],
        # '站内-无选频': [650, 500, 350],
    }
    sec_type = list(sec_length.keys())

    list0 = []

    index = 0
    for item in itertools.product(sec_type, freq_zhu, freq_bei):
        # print(item)
        for s_length in sec_length[item[0]]:

            cnum_zhu, cvalue_zhu, level = get_cnum_value_1125(item[0], s_length, item[1])
            cnum_bei, cvalue_bei, _ = get_cnum_value_1125(item[0], s_length, item[2])

            temp_zhu = list(map(lambda x: '主串-' + str(x+1), range(cnum_zhu)))
            temp_bei = list(map(lambda x: '被串-' + str(x+1), range(cnum_bei)))

            normal_flag = False
            e_list = ['无']
            e_list.extend(temp_zhu)
            e_list.extend(temp_bei)

            for error in e_list:
                for flag in ['断线', '减半']:
                    if error == '无':
                        e_type = '正常'
                    else:
                        e_type = flag

                    if normal_flag is True:
                        if error == '无':
                            continue

                    normal_flag = True
                    row = pd.Series(index=columns_header(), dtype='object')

                    row['故障位置'] = error
                    row['故障类型'] = e_type

                    row['序号'] = int(index)
                    row['线路名称'] = '-'
                    row['车站名称'] = '-'
                    row['主串区段'] = '-'
                    row['被串区段'] = '-'

                    row['线间距'] = '-'
                    row['耦合系数'] = 24
                    row['并行长度(m)'] = 0

                    row['主串方向'] = '右发'
                    row['被串方向'] = '右发'

                    row['主串区段类型'] = item[0]
                    row['被串区段类型'] = item[0]

                    row['主串区段长度(m)'] = s_length
                    row['被串区段长度(m)'] = s_length

                    row['主串坐标'] = 0
                    row['被串坐标'] = 0

                    row['主串坐标'] = 0
                    row['被串坐标'] = 0

                    row['主串电平级'] = level
                    row['被串电平级'] = level

                    row['主串频率(Hz)'] = item[1]
                    row['被串频率(Hz)'] = item[2]

                    row['主串电缆长度(km)'] = 10
                    row['被串电缆长度(km)'] = 10


                    row['主串电容数(含TB)'] = cnum_zhu
                    row['被串电容数(含TB)'] = cnum_bei

                    row['主串电容值(μF)'] = cvalue_zhu
                    row['被串电容值(μF)'] = cvalue_bei

                    row['主串道床电阻(Ω·km)'] = 10000
                    row['被串道床电阻(Ω·km)'] = 10000

                    row['主串TB模式'] = '无TB'
                    row['被串TB模式'] = '无TB'

                    d0 = {
                        '区间': 29,
                        '站内': 0,
                    }
                    row['调谐区长度'] = d0.get(item[0].split('-')[0])

                    # print(ret.loc[index, '调谐区长度'])
                    list0.append(row)

                    index += 1
    ret = pd.DataFrame(list0)
    return ret


def get_cnum_value_1125(sec_type, length, freq):
    cnum = None
    cvalue = None
    level = None
    if sec_type in ['站内-有选频', '站内-无选频']:
        cvalue = 25
        d_temp = {
            350: 3,
            500: 5,
            650: 7,
        }
        cnum = d_temp.get(length)
        if sec_type == '站内-无选频':
            level = 9
        if sec_type == '站内-有选频':
            if freq in [1700, 2000, 2300]:
                level = 7
            if freq in [2600]:
                level = 8

    elif sec_type == '区间-高铁':
        cvalue = 25
        if freq in [1700, 2000]:
            d_temp = {
                500: 8,
                1000: 16,
                1400: 23,
            }
            cnum = d_temp.get(length)

        if freq in [2300, 2600]:
            d_temp = {
                500: 6,
                1000: 12,
                1400: 17,
            }
            cnum = d_temp.get(length)

        d_temp = {
            500: 3,
            1000: 2,
            1400: 1,
        }
        level = d_temp.get(length)

    elif sec_type == '区间-普铁':
        d_temp = {
            1700: 55,
            2000: 50,
            2300: 46,
            2600: 40,
        }
        cvalue = d_temp.get(freq)

        if freq in [1700, 2000, 2300]:
            d_temp = {
                500: 6,
                1000: 10,
                1400: 18,
            }
            cnum = d_temp.get(length)

        if freq in [2600]:
            d_temp = {
                500: 6,
                1000: 10,
                1400: 20,
            }
            cnum = d_temp.get(length)

        d_temp = {
            500: 3,
            1000: 2,
            1400: 1,
        }
        level = d_temp.get(length)

    else:
        raise KeyboardInterrupt('sec_type error')

    return cnum, cvalue, level


def init_input_1128():

    # print(df_input)

    ret = pd.DataFrame(columns=columns_header())
    counter = 1
    index = 1

    freq_zhu = [2600]
    freq_bei = [2300]
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

        for offset in range(-200, 201, 10):
        # for offset in [0]:
        # for offset in [scene[4]]:

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



if __name__ == '__main__':
    # m_lens = [700, 700, 700]
    # m_frqs = generate_frqs(Freq(2600), 3)
    # c_nums = get_c_nums(m_frqs, m_lens)
    init_input_1125()
    pass