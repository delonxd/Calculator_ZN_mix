from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq
from src.Model.PreModel import PreModel


def get_guangzhan_info():
    info_line1 = [
        -36,
        ('0132AG', 2000, 475, 8),
        ('0132BG', 2600, 475, 6),
        ('0132CG', 2000, 500, 8),
        ('0148AG', 2600, 400, 5),
        ('0148BG', 2000, 600, 10),
        ('0148CG', 2600, 500, 6),
        ('0162AG', 2000, 551, 10),
        ('0162BG-1', 2600, 551, 7),
        ('0162BG-2', 2000, 400, 6),
        ('0178AG', 2600, 700, 8),
    ]

    info_line2 = [
        -294,
        ('NS1LQAG', 2000, 537, 9),
        ('5578CG', 2600, 470, 6),
        ('5578BG', 2000, 625, 10),
        ('5578AG', 2600, 745, 9),
        ('5560CG', 2000, 505, 9),
        ('5560BG', 2600, 625, 8),
        ('5560AG', 2000, 760, 13),
        ('5542CG', 2600, 490, 6),
        ('5542BG', 2000, 560, 10),
        ('5542AG', 2600, 800, 10),
    ]

    info_line3 = [
        -615,
        ('S1LQBG', 2600, 464, 6),
        ('S1LQAG', 2000, 464, 8),
        ('8420DG', 2600, 625, 8),
        ('8420CG', 2000, 745, 12),
        ('8420BG', 2600, 505, 7),
        ('8420AG', 2000, 625, 10),
        ('8394CG', 2600, 766, 10),
        ('8394BG', 2000, 490, 8),
        ('8394AG', 2600, 550, 7),
        ('8376CG', 2000, 810, 14),
    ]

    ret = []
    ret.extend(get_line_info(info_line1, info_line2))
    # ret.extend(get_line_info(info_line2, info_line1))
    # ret.extend(get_line_info(info_line2, info_line3))
    # ret.extend(get_line_info(info_line3, info_line2))

    return ret


def get_guangzhan_info_replace_c_with_TB():
    info_line1 = [
        150,
        ('广湛测试', 2600, 300, 0),
    ]

    info_line2 = [
        -470,
        ('5578CG', 2600, 470, 6),
        ('5578BG', 2000, 625, 10),
        ('5578AG', 2600, 745, 9),
    ]

    ret = []
    tmp = get_line_info(info_line1, info_line2)

    focus_ng = '5578BG'
    gz_freq = 2600
    mode = '广湛对南广'

    focus_zhu = '广湛测试'
    focus_bei = '5578BG'

    for scene in tmp:
        sec_zhu = scene[0][0]
        if sec_zhu == focus_zhu:
            bei_list = list(zip(*scene[1]))[0]

            if focus_bei in bei_list:
                tmp_scene = list(scene)
                tmp_scene.append(focus_bei)
                tmp_scene.append(focus_ng)
                tmp_scene.append(gz_freq)
                tmp_scene.append(mode)
                tmp_scene.append('换TB')
                # tmp_scene.append('不换TB')
                ret.append(tmp_scene)

    return ret


def get_guangzhan_info_no_cmp():
    ret = []

    # 1 南广重点
    focus_ng_list = ['5578BG', '5578AG']
    # focus_ng_list = ['5578AG']

    # 2 广湛频率
    gz_freq_list = [2600, 2000]
    # gz_freq_list = [2000]

    # 3 广湛区段长度
    gz_length_list = [300, 400, 500]

    # 4 主串被串线路
    mode_list = ['广湛对南广', '南广对广湛']
    # mode_list = ['广湛对南广']
    # mode_list = ['南广对广湛']

    for focus_ng in focus_ng_list:
        if focus_ng == '5578BG':
            info_line2 = [
                -470,
                ('5578CG', 2600, 470, 6),
                ('5578BG', 2000, 625, 10),
                ('5578AG', 2600, 745, 9),
            ]
            ng_length = 625

        elif focus_ng == '5578AG':
            info_line2 = [
                -625,
                ('5578BG', 2000, 625, 10),
                ('5578AG', 2600, 745, 9),
                ('5560CG', 2000, 505, 9),

            ]
            ng_length = 745
        else:
            raise KeyboardInterrupt('focus_bei error')

        for gz_freq in gz_freq_list:

            for mode in mode_list:

                for gz_length in gz_length_list:
                    offset_list = list(range(-gz_length-gz_length, ng_length-gz_length, 50))
                    offset_list.append(ng_length-gz_length)

                    for offset in offset_list:

                        freq_side = Freq(gz_freq).change_freq()

                        info_line1 = [
                            offset,
                            ('左端补充模型', freq_side, gz_length, 0),
                            ('广湛测试', gz_freq, gz_length, 0),
                            ('右端补充模型', freq_side, gz_length, 0),
                        ]

                        if mode == '广湛对南广':
                            tmp = get_line_info(info_line1, info_line2)
                            focus_zhu = '广湛测试'
                            focus_bei = focus_ng

                        elif mode == '南广对广湛':
                            tmp = get_line_info(info_line2, info_line1)
                            focus_zhu = focus_ng
                            focus_bei = '广湛测试'

                        else:
                            raise KeyboardInterrupt('mode error')

                        for scene in tmp:
                            sec_zhu = scene[0][0]
                            if sec_zhu == focus_zhu:
                                bei_list = list(zip(*scene[1]))[0]

                                if focus_bei in bei_list:
                                    tmp_scene = list(scene)
                                    tmp_scene.append(focus_bei)
                                    tmp_scene.append(focus_ng)
                                    tmp_scene.append(gz_freq)
                                    tmp_scene.append(mode)
                                    ret.append(tmp_scene)

    for index, ii in enumerate(ret):
        print(index, ii)

    # ret = ret[:15]
    return ret


def get_guangzhan_info_deduct_cmp():
    ret = []

    # 1 南广重点
    focus_ng_list = ['5578BG', '5578AG']
    # focus_ng_list = ['5578AG']

    # 2 广湛频率
    gz_freq_list = [2600, 2000]
    # gz_freq_list = [2000]

    # 3 广湛区段长度
    gz_length_list = [500, 600]

    # 4 主串被串线路
    mode_list = ['广湛对南广', '南广对广湛']
    # mode_list = ['广湛对南广']
    # mode_list = ['南广对广湛']

    # 5 广湛电容布置
    gz_cmp_list = ['电容数减1', '电容数减2']

    for gz_cmp in gz_cmp_list:

        for focus_ng in focus_ng_list:
            if focus_ng == '5578BG':
                info_line2 = [
                    -470,
                    ('5578CG', 2600, 470, 6),
                    ('5578BG', 2000, 625, 10),
                    ('5578AG', 2600, 745, 9),
                ]
                ng_length = 625

            elif focus_ng == '5578AG':
                info_line2 = [
                    -625,
                    ('5578BG', 2000, 625, 10),
                    ('5578AG', 2600, 745, 9),
                    ('5560CG', 2000, 505, 9),

                ]
                ng_length = 745
            else:
                raise KeyboardInterrupt('focus_bei error')

            for gz_freq in gz_freq_list:

                for mode in mode_list:

                    for gz_length in gz_length_list:
                        offset_list = list(range(-gz_length-gz_length, ng_length-gz_length, 50))
                        offset_list.append(ng_length-gz_length)

                        for offset in offset_list:

                            freq_side = Freq(gz_freq).change_freq()

                            info_line1 = [
                                offset,
                                ['左端补充模型', freq_side, gz_length, 0],
                                ['广湛测试', gz_freq, gz_length, 0],
                                ['右端补充模型', freq_side, gz_length, 0],
                            ]

                            if gz_cmp == '电容数减1':
                                deduct = 1
                            elif gz_cmp == '电容数减2':
                                deduct = 2
                            else:
                                raise KeyboardInterrupt('deduct error')

                            for i in [1, 2, 3]:
                                tmp_freq = info_line1[i][1]
                                tmp_len = info_line1[i][2]
                                info_line1[i][3] = config_c_num_high_speed(tmp_freq, tmp_len) - deduct

                            if mode == '广湛对南广':
                                tmp = get_line_info(info_line1, info_line2)
                                focus_zhu = '广湛测试'
                                focus_bei = focus_ng

                            elif mode == '南广对广湛':
                                tmp = get_line_info(info_line2, info_line1)
                                focus_zhu = focus_ng
                                focus_bei = '广湛测试'

                            else:
                                raise KeyboardInterrupt('mode error')

                            for scene in tmp:
                                sec_zhu = scene[0][0]
                                if sec_zhu == focus_zhu:
                                    bei_list = list(zip(*scene[1]))[0]

                                    if focus_bei in bei_list:
                                        tmp_scene = list(scene)
                                        tmp_scene.append(focus_bei)
                                        tmp_scene.append(focus_ng)
                                        tmp_scene.append(gz_freq)
                                        tmp_scene.append(mode)
                                        tmp_scene.append(gz_cmp)
                                        ret.append(tmp_scene)

    for index, ii in enumerate(ret):
        print(index, ii)

    # ret = ret[:15]
    return ret


def config_c_num_high_speed(freq_value, length):

    if 0 < length <= 300:
        key = 0
    elif length > 300:
        key = int((length - 251) / 50)
    else:
        raise KeyboardInterrupt('config_c_num error: 区段长度错误')

    table = {
        0: [0, 0, 0, 0],
        1: [5, 5, 4, 4],
        2: [6, 6, 5, 5],
        3: [7, 7, 5, 5],
        4: [8, 8, 6, 6],
        5: [9, 9, 7, 7],
        6: [10, 10, 7, 7],
        7: [10, 10, 8, 8],
        8: [11, 11, 8, 8],
        9: [12, 12, 9, 9],
        10: [13, 13, 10, 10],
        11: [14, 14, 10, 10],
        12: [15, 15, 11, 11],
        13: [15, 15, 12, 12],
        14: [16, 16, 12, 12],
        15: [17, 17, 13, 13],
        16: [18, 18, 13, 13],
        17: [19, 19, 14, 14],
        18: [20, 20, 15, 15],
        19: [20, 20, 15, 15],
        20: [21, 21, 16, 16],
        21: [22, 22, 17, 17],
        22: [23, 23, 17, 17],
    }
    if key not in table.keys():
        raise KeyboardInterrupt('config_c_num error: 区段长度超长')

    index_dict = {
        1700: 0,
        2000: 1,
        2300: 2,
        2600: 3,
    }

    if freq_value not in index_dict.keys():
        raise KeyboardInterrupt('config_c_num error: 区段频率错误')

    c_num = table[key][index_dict[freq_value]]
    return c_num


# 获得区段位置信息
def get_line_info(line1, line2):
    line1 = line1.copy()
    line2 = line2.copy()

    offset = line2[0] - line1[0]
    line1.pop(0)
    line2.pop(0)

    zhu_left = zhu_right = 0
    res = []
    for sec_zhu in line1:
        zhu_left = zhu_right
        zhu_right = zhu_left + sec_zhu[2]

        bei_list = []
        bei_offset = 0

        bei_left = bei_right = offset
        for sec_bei in line2:
            bei_left = bei_right
            bei_right = bei_left + sec_bei[2]

            if bei_right < (zhu_left - 60):
                continue

            if bei_left > (zhu_right + 60):
                continue

            if len(bei_list) == 0:
                bei_offset = bei_left - zhu_left

            bei_list.append(sec_bei)

        res.append((sec_zhu, bei_list, bei_offset))

    return res


# 配置输入
def config_input_20231217_guangzhan():

    columns = [
        '序号',
        '分路模式',
        '主串区段',
        '被串区段',
        '主串频率',
        '被串频率',
        '主串区段长度',
        '被串区段长度',
        '主串电容数',
        '被串电容数',
        '被串相对位置',
        '主串方向',
        '被串方向',
    ]

    direction_list = [
        # ('左发', '左发'),
        # ('左发', '右发'),
        # ('右发', '左发'),
        ('右发', '右发'),
    ]

    mode_list = [
        '主串调整被串分路',
        '主被串同时分路',
    ]

    # src = get_guangzhan_info()
    # src = get_guangzhan_info_no_cmp()
    src = get_guangzhan_info_replace_c_with_TB()
    # src = get_guangzhan_info_deduct_cmp()

    df = pd.DataFrame(index=columns, dtype='object')

    counter = 0
    for mode in mode_list:
        for val in src:

            for direction in direction_list:
                counter += 1

                s0 = pd.Series(name=counter, index=columns)

                s0['序号'] = s0.name
                s0['分路模式'] = mode

                zhu_info = val[0]
                bei_info = list(zip(*val[1]))

                s0['主串区段'] = zhu_info[0]
                s0['被串区段'] = list(bei_info[0])

                s0['主串频率'] = zhu_info[1]
                s0['被串频率'] = list(bei_info[1])

                s0['主串区段长度'] = zhu_info[2]
                s0['被串区段长度'] = list(bei_info[2])

                s0['主串电容数'] = zhu_info[3]
                s0['被串电容数'] = list(bei_info[3])

                s0['被串相对位置'] = val[2]

                s0['主串方向'] = direction[0]
                s0['被串方向'] = direction[1]

                s0['被串重点区段'] = val[3]

                s0['南广区段'] = val[4]
                s0['广湛频率'] = val[5]
                s0['主被串线路'] = val[6]
                s0['解决办法'] = val[7]
                print('generate row: %s --> %s' % (counter, s0.tolist()))

                df = pd.concat([df, s0], axis=1)

                # if counter == 4:
                #     return df.transpose()

    df = df.transpose()
    return df


# 配置表头
def config_headlist_20231217_guangzhan():
    head_list = [
        '序号',
        '备注',

        '南广区段',
        '广湛频率',
        '主被串线路',
        '解决办法',

        '分路模式',

        '耦合系数(μH/km)',

        # '线路名称', '车站名称',
        '主串区段', '被串区段',

        # '线间距(m)',
        # '并行长度(m)',
        # '被串相对位置(m)',

        '主串方向', '被串方向',
        # '线间距(m)',
        # '耦合系数(μH/km)',
        # '并行长度(m)',

        # '调谐区错位(m)',
        '主串区段长度(m)', '被串区段长度(m)',
        '被串相对位置(m)',

        # '主串左端坐标', '被串左端坐标',

        # '主串区段类型', '被串区段类型',
        '主串频率(Hz)', '被串频率(Hz)',

        # '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容数', '被串电容数',
        '主串电容值(μF)', '被串电容值(μF)',

        # '主串电容数量列表', '被串电容数量列表',
        # '主串电容容值列表', '被串电容容值列表',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串分路电阻(Ω)', '被串分路电阻(Ω)',

        '主串电缆长度(km)', '被串电缆长度(km)',

        '分路间隔(m)',

        '主串电平级',
        '电源电压',

        '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        # '故障位置', '故障类型',
        # '干扰值变化',
    ]

    return head_list


def config_c_pack_20231217_guangzhan(src):
    c_num_list = []
    c_imp_list = []
    c_val_list = []

    for c_num in src:
        c_val = 25
        val_tmp = c_val * 1e-6

        c_imp = ImpedanceMultiFreq()
        c_imp.rlc_s = {
            1700: [10e-3, None, val_tmp],
            2000: [10e-3, None, val_tmp],
            2300: [10e-3, None, val_tmp],
            2600: [10e-3, None, val_tmp]}

        c_num_list.append(c_num)
        c_val_list.append(c_val)
        c_imp_list.append(c_imp)

    ret = {
        '电容数量列表': c_num_list,
        '电容容值列表': c_val_list,
        '电容阻抗列表': c_imp_list,
    }

    return ret


# 配置行数据
def config_row_data_20231217_guangzhan(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = '广湛六线并行'
    data['分路模式'] = df_input['分路模式']

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['主串区段长度']
    length2 = data['被串区段长度(m)'] = df_input['被串区段长度']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = length2

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = 20

    # 区段频率
    para['freq_主'] = freq = df_input['主串频率']
    para['freq'] = Freq(freq)

    para['主串频率列表'] = [para['freq']]
    para['被串频率列表'] = list(map(lambda x: Freq(x), df_input['被串频率']))

    data['主串频率(Hz)'] = df_input['主串频率']
    data['被串频率(Hz)'] = df_input['被串频率']

    # data['主串区段类型'] = '高铁区间'
    # data['被串区段类型'] = '高铁区间'

    # 电容配置
    c_pack_zhu = config_c_pack_20231217_guangzhan([df_input['主串电容数']])
    c_pack_bei = config_c_pack_20231217_guangzhan(df_input['被串电容数'])

    # 电容模型参数
    para['主串电容数'] = c_pack_zhu['电容数量列表']
    para['被串电容数'] = c_pack_bei['电容数量列表']

    para['主串容值列表'] = c_pack_zhu['电容阻抗列表']
    para['被串容值列表'] = c_pack_bei['电容阻抗列表']

    # 电容参数输出
    data['主串电容数(含TB)'] = df_input['主串电容数']
    data['被串电容数(含TB)'] = df_input['被串电容数']

    data['主串电容数'] = df_input['主串电容数']
    data['被串电容数'] = df_input['被串电容数']

    data['主串电容值(μF)'] = c_pack_zhu['电容容值列表'][0]
    data['被串电容值(μF)'] = c_pack_bei['电容容值列表'][0]

    # data['主串电容数量列表'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = c_pack_bei['电容数量列表']

    # data['主串电容容值列表'] = c_pack_zhu['电容容值列表']
    # data['被串电容容值列表'] = c_pack_bei['电容容值列表']

    # 道床电阻
    rd = 10000
    data['主串道床电阻(Ω·km)'] = rd
    data['被串道床电阻(Ω·km)'] = rd

    para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
    para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])

    para['Rd'].value = rd

    # 钢轨阻抗
    data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
    data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)

    para['主串钢轨阻抗'] = para['Trk_z']
    para['被串钢轨阻抗'] = para['Trk_z']

    # 发码方向
    data['主串方向'] = para['sr_mod_主'] = df_input['主串方向']
    data['被串方向'] = para['sr_mod_被'] = df_input['被串方向']

    # 电缆参数
    data['电缆电阻最大(Ω/km)'] = 45
    data['电缆电阻最小(Ω/km)'] = 43
    data['电缆电容最大(F/km)'] = 28e-9
    data['电缆电容最小(F/km)'] = 28e-9

    para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
    para['Cable_C'].value = data['电缆电容最大(F/km)']

    # 电缆长度
    cab_len = 10
    para['cab_len'] = cab_len
    data['主串电缆长度(km)'] = para['主串电缆长度'] = cab_len
    data['被串电缆长度(km)'] = para['被串电缆长度'] = cab_len

    # 分路电阻

    mode = df_input['分路模式']

    r_sht = 1e-7
    if mode == '主串调整被串分路':
        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = 1e10
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
        data['主串分路电阻(Ω)'] = 'None'

    elif mode == '主被串同时分路':

        data['主串分路电阻(Ω)'] = para['主串分路电阻'] = r_sht
        data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_sht
    else:
        raise KeyboardInterrupt('分路模式错误')

    para['Rsht_z'] = r_sht

    # 功出电源
    data['主串电平级'] = para['send_level'] = 3
    data['电源电压'] = para['pwr_v_flg'] = '最大'

    # 特殊位置
    data['极性交叉位置'] = para['极性交叉位置'] = []
    data['特殊位置'] = para['special_point'] = data['极性交叉位置']
    data['节点选取模式'] = para['节点选取模式'] = '特殊'

    # 机车信号
    data['最小机车信号位置'] = '-'
    data['机车信号感应系数'] = \
        str(para['机车信号比例V']) + '/' + str(para['机车信号比例I'][freq])
    para['机车信号系数值'] = para['机车信号比例V'] / para['机车信号比例I'][freq]

    # 分路间隔
    data['分路间隔(m)'] = 1
    # data['分路起点'] = offset - 14.5
    # data['分路终点'] = offset + sum(length2) + 14.5

    focus_sec = df_input['被串重点区段']
    focus_index = data['被串区段'].index(focus_sec)

    l_point = sum(data['被串区段长度(m)'][:focus_index]) + offset - 14.5
    r_point = l_point + data['被串区段长度(m)'][focus_index] + 29

    data['分路起点'] = l_point
    data['分路终点'] = r_point

    data['南广区段'] = df_input['南广区段']
    data['广湛频率'] = df_input['广湛频率']
    data['主被串线路'] = df_input['主被串线路']
    para['解决办法'] = data['解决办法'] = df_input['解决办法']


class PreModel_QJ_20231217_guangzhan(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        self.train1['分路电阻1'].z = para['被串分路电阻']
        self.train2['分路电阻1'].z = para['主串分路电阻']

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=para['主串频率列表'],
                           m_lens=para['主串区段长度'],
                           j_lens=[29, 29],
                           m_typs=['2000A'],
                           c_nums=para['主串电容数'],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        # freq_tmp = Freq(para['freq_被'])
        # freq_tmp.change_freq()

        m_num = len(para['被串区段长度'])
        j_num = m_num + 1
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=m_num,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[29] * j_num,
                           m_typs=['2000A'] * m_num,
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']] * m_num,
                           send_lvs=[send_level] * m_num,
                           parameter=parameter)

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()

        if para['解决办法'] == '换TB':
            self.replace_c_with_TB()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['Trk_z'], rd=para['Trk_z'])
        self.set_rail_para(line=l4, z_trk=para['Trk_z'], rd=para['Trk_z'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for index, sec in enumerate(self.section_group3.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['主串容值列表'][index]

        for index, sec in enumerate(self.section_group4.element.values()):
            for ele in sec.element.values():
                if isinstance(ele, CapC):
                    ele.z = para['被串容值列表'][index]

    def replace_c_with_TB(self):
        para = self.parameter

        dict0 = {
            1700: 4,
            2000: 4,
            2300: 3,
            2600: 3,
        }

        for section_group in [self.section_group3, self.section_group4]:
            for sec in section_group.element.values():
                for ele in sec.element.values():
                    if isinstance(ele, CapC):
                        name = ele.name_base
                        freq = sec.m_freq.value

                        z_tb = para['TB'][freq]
                        z_tb = z_tb + para['TB_引接线_有砟']

                        num = int(name[1:])
                        divisor = dict0[freq]
                        if num % divisor == 0:
                            ele.z = z_tb

    def add_train(self):
        para = self.parameter
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train2])
        self.l3 = l3

        l4 = Line(name_base='线路4', sec_group=self.section_group4,
                  parameter=self.parameter, train=[self.train1])
        self.l4 = l4

        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()
