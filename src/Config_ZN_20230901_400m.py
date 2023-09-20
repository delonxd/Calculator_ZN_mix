from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq
from src.Model.PreModel import PreModel
import os
import time
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['font.sans-serif'] = ['consolas']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False


def config_input_20230901_400m(freq_zhu, freq_bei):

    columns = [
        '序号',
        '备注',
        '主串区段',
        '被串区段',
        '主串方向',
        '被串方向',
        '主串区段长度(m)',
        '被串区段长度(m)',
        '被串相对位置(m)',
        '耦合系数(μH/km)',
        '主串电平级',
        '主串频率(Hz)',
        '被串频率(Hz)',
        '主串电缆长度(km)',
        '被串电缆长度(km)',
        '主串电容数(含TB)',
        '被串电容数(含TB)',
        '主串道床电阻(Ω·km)',
        '被串道床电阻(Ω·km)',
        '分路间隔(m)',
        '分路电阻(Ω)',
        '主串TB模式',
        '被串TB模式',
    ]

    df = pd.DataFrame(index=columns, dtype='object')

    counter = 1
    for offset in range(-350, 400, 50):

        s0 = pd.Series(name=counter, index=columns)

        s0['序号'] = s0.name
        s0['备注'] = ''
        s0['主串区段'] = '测试1'
        s0['被串区段'] = '测试2'
        s0['主串方向'] = '右发'
        s0['被串方向'] = '右发'
        s0['主串区段长度(m)'] = 400
        s0['被串区段长度(m)'] = 400
        s0['被串相对位置(m)'] = offset
        s0['耦合系数(μH/km)'] = 20
        s0['主串电平级'] = 5
        s0['主串频率(Hz)'] = freq_zhu
        s0['被串频率(Hz)'] = freq_bei
        s0['主串电缆长度(km)'] = 10
        s0['被串电缆长度(km)'] = 10
        s0['主串电容数(含TB)'] = 4
        s0['被串电容数(含TB)'] = 4
        s0['主串道床电阻(Ω·km)'] = 10000
        s0['被串道床电阻(Ω·km)'] = 10000
        s0['分路间隔(m)'] = 1
        s0['分路电阻(Ω)'] = 1e-7
        s0['主串TB模式'] = '无TB'
        s0['被串TB模式'] = '无TB'

        print('generate row: %s --> %s' % (counter, s0.tolist()))

        df = pd.concat([df, s0], axis=1)
        counter += 1

    df = df.transpose()

    return df


# 配置表头
def config_headlist():
    head_list = [
        '序号',
        # '备注',
        # '线路名称', '车站名称',
        # '主串区段', '被串区段',

        # '线间距(m)',
        '耦合系数(μH/km)',
        # '并行长度(m)',
        # '被串相对位置(m)',

        '主串方向', '被串方向',
        # '线间距(m)',
        # '耦合系数(μH/km)',
        # '并行长度(m)',

        # '调谐区错位(m)',
        '被串相对位置(m)',
        '主串区段长度(m)', '被串区段长度(m)',
        # '主串左端坐标', '被串左端坐标',

        # '主串区段类型', '被串区段类型',
        '主串频率(Hz)', '被串频率(Hz)',

        # '主串电容数量列表', '被串电容数量列表',
        # '主串电容容值列表', '被串电容容值列表',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        '主串TB模式', '被串TB模式',

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


# def config_c_num_non_dead_zone(freq: Freq, length):
#     freq_value = freq.value
#
#     if 0 < length <= 300:
#         key = 0
#     elif length > 300:
#         key = int((length - 251) / 50)
#     else:
#         raise KeyboardInterrupt('config_c_num error: 区段长度错误')
#
#     table = {
#         0: [0, 0, 0, 0],
#         1: [5, 5, 4, 4],
#         2: [6, 6, 5, 5],
#         3: [7, 7, 5, 5],
#         4: [8, 8, 6, 6],
#         5: [9, 9, 7, 7],
#         6: [10, 10, 7, 7],
#         7: [10, 10, 8, 8],
#         8: [11, 11, 8, 8],
#         9: [12, 12, 9, 9],
#         10: [13, 13, 10, 10],
#         11: [14, 14, 10, 10],
#         12: [15, 15, 11, 11],
#         13: [15, 15, 12, 12],
#         14: [16, 16, 12, 12],
#         15: [17, 17, 13, 13],
#         16: [18, 18, 13, 13],
#         17: [19, 19, 14, 14],
#         18: [20, 20, 15, 15],
#         19: [20, 20, 15, 15],
#         20: [21, 21, 16, 16],
#         21: [22, 22, 17, 17],
#         22: [23, 23, 17, 17],
#     }
#     if key not in table.keys():
#         raise KeyboardInterrupt('config_c_num error: 区段长度超长')
#
#     index_dict = {
#         1700: 0,
#         2000: 1,
#         2300: 2,
#         2600: 3,
#     }
#
#     if freq_value not in index_dict.keys():
#         raise KeyboardInterrupt('config_c_num error: 区段频率错误')
#
#     c_num = table[key][index_dict[freq_value]]
#     return c_num


# def config_c_pack_20230801(freq_list, length_list, c_value_src):
#     if len(freq_list) != len(length_list):
#         raise KeyboardInterrupt('config_c_list_20230720_pusu error: 列表长度不等')
#
#     c_num_list = []
#     c_imp_list = []
#     c_val_list = []
#
#     for index in range(len(freq_list)):
#         freq = freq_list[index]
#         length = length_list[index]
#         c_val = c_value_src[index]
#
#         c_num = config_c_num_non_dead_zone(freq, length)
#
#         val_tmp = c_val * 1e-6
#         c_imp = ImpedanceMultiFreq()
#         c_imp.rlc_s = {
#             1700: [10e-3, None, val_tmp],
#             2000: [10e-3, None, val_tmp],
#             2300: [10e-3, None, val_tmp],
#             2600: [10e-3, None, val_tmp]}
#
#         c_num_list.append(c_num)
#         c_val_list.append(c_val)
#         c_imp_list.append(c_imp)
#
#     ret = {
#         '电容数量列表': c_num_list,
#         '电容容值列表': c_val_list,
#         '电容阻抗列表': c_imp_list,
#     }
#
#     return ret


# 配置行数据
def config_row_data(df_input, para, data):
    # 序号
    data['序号'] = para['序号'] = df_input['序号']

    # 备注
    data['备注'] = para['备注'] = df_input['备注']

    # 区段名
    data['主串区段'] = para['主串区段'] = df_input['主串区段']
    data['被串区段'] = para['被串区段'] = df_input['被串区段']

    # 区段长度
    length1 = data['主串区段长度(m)'] = df_input['主串区段长度(m)']
    length2 = data['被串区段长度(m)'] = df_input['被串区段长度(m)']
    para['主串区段长度'] = [length1]
    para['被串区段长度'] = [length2]

    # 相对位置
    data['被串相对位置(m)'] = offset = df_input['被串相对位置(m)']

    para['offset_zhu'] = 0
    para['offset_bei'] = offset

    # 耦合系数
    data['耦合系数(μH/km)'] = para['耦合系数'] = df_input['耦合系数(μH/km)']

    # 区段频率
    para['freq_主'] = freq1 = data['主串频率(Hz)'] = df_input['主串频率(Hz)']
    para['freq_被'] = freq2 = data['被串频率(Hz)'] = df_input['被串频率(Hz)']
    freq = freq1
    data['freq'] = para['freq'] = Freq(freq1)
    para['主串频率列表'] = [Freq(freq1)]
    para['被串频率列表'] = [Freq(freq2)]

    # 电容数量
    # data['主串电容数量列表'] = para['主串电容数'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = para['被串电容数'] = c_pack_bei['电容数量列表']

    c_num1 = df_input['主串电容数(含TB)']
    c_num2 = df_input['被串电容数(含TB)']

    data['主串电容数量列表'] = para['主串电容数'] = [c_num1]
    data['被串电容数量列表'] = para['被串电容数'] = [c_num2]

    data['主串电容数(含TB)'] = c_num1
    data['被串电容数(含TB)'] = c_num2

    # 电容容值
    data['主串电容值(μF)'] = 25
    data['被串电容值(μF)'] = 25

    # data['主串电容数量列表'] = c_pack_zhu['电容数量列表']
    # data['被串电容数量列表'] = c_pack_bei['电容数量列表']

    # data['主串电容容值列表'] = [25]
    # data['被串电容容值列表'] = [25]

    val_tmp = 25 * 1e-6
    c_imp = ImpedanceMultiFreq()
    c_imp.rlc_s = {
        1700: [10e-3, None, val_tmp],
        2000: [10e-3, None, val_tmp],
        2300: [10e-3, None, val_tmp],
        2600: [10e-3, None, val_tmp]}

    para['主串容值列表'] = [c_imp]
    para['被串容值列表'] = [c_imp]

    # 道床电阻
    data['主串道床电阻(Ω·km)'] = df_input['主串道床电阻(Ω·km)']
    data['被串道床电阻(Ω·km)'] = df_input['被串道床电阻(Ω·km)']

    para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
    para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])

    para['Rd'].value = df_input['主串道床电阻(Ω·km)']

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
    para['cab_len'] = 10
    data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)']
    data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)']

    # 分路电阻
    data['主串分路电阻(Ω)'] = para['主串分路电阻'] = df_input['分路电阻(Ω)']
    data['被串分路电阻(Ω)'] = para['被串分路电阻'] = df_input['分路电阻(Ω)']

    para['Rsht_z'] = df_input['分路电阻(Ω)']

    # 功出电源
    data['主串电平级'] = para['send_level'] = df_input['主串电平级']
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
    data['分路间隔(m)'] = df_input['分路间隔(m)']
    data['分路起点'] = offset
    data['分路终点'] = offset + length2

    # TB模式
    data['主串TB模式'] = para['主串TB模式'] = df_input['主串TB模式']
    data['被串TB模式'] = para['被串TB模式'] = df_input['被串TB模式']


class PreModel_20230901_ZN_400m(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=para['主串频率列表'],
                           m_lens=para['主串区段长度'],
                           j_lens=[0, 0],
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

        freq_tmp = Freq(para['freq_被'])
        freq_tmp.change_freq()

        m_num = len(para['被串区段长度'])
        j_num = m_num + 1
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=m_num,
                           m_frqs=para['被串频率列表'],
                           m_lens=para['被串区段长度'],
                           j_lens=[0] * j_num,
                           m_typs=['2000A'] * m_num,
                           c_nums=para['被串电容数'],
                           sr_mods=[para['sr_mod_被']] * m_num,
                           send_lvs=[send_level] * m_num,
                           parameter=parameter)

        sg3['区段1'].load_TB_mode(para['主串TB模式'])
        sg4['区段1'].load_TB_mode(para['被串TB模式'])
        sg3.refresh()
        sg4.refresh()

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()

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


def draw_image_20230901_400m():
    # plt.rcParams['font.size'] = 20

    # 根目录
    root = 'C:\\Users\\李继隆\\PycharmProjects\\Calculator_ZN_mix\\20230901_站内400m遍历\\'

    # 创建文件夹
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    res_dir = '%s图表汇总\\站内邻线干扰_%s' % (root, timestamp)

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    # 读取数据

    # file = '仿真输出_站内400m邻线干扰_主串1700_被串2300.xlsx'
    file = '仿真输出_站内400m邻线干扰_主串2600_被串2000.xlsx'

    path = '%s%s' % (root, file)
    df_input = pd.read_excel(path, '数据输出')
    df_data = pd.read_excel(path, '被串钢轨电流')

    for _ in range(1):

        # 数据处理
        df1 = df_input.copy()

        ###################################################################

        # 创建图表
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(hspace=1)
        ax = fig.add_subplot(1, 1, 1)

        # 图表标题
        title = file.split('.')[0]
        ax.set_title(title, x=0.5, y=1.04, fontsize=30)

        # fig.suptitle(title, fontsize=30)

        # 横纵坐标
        # 坐标名
        ax.set_xlabel('被串分路位置', fontsize=20)
        ax.set_ylabel('邻线干扰钢轨电流(A)', fontsize=20)

        # 纵坐标
        ax.yaxis.grid(True, which='major')
        # ax.yaxis.set_font(20)
        ax.set_ylim([0, 0.4])

        # 横坐标
        x_ticks = [0, 100, 200, 300, 400]
        x_label = ['接收', '100m', '200m', '300m', '发送']

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_label)

        # 坐标轴字体
        ax.tick_params(
            # axis='y',
            labelsize=14,       # y轴字体大小设置
            # color='r',        # y轴标签颜色设置
            # labelcolor='b',   # y轴字体颜色设置
            direction='in',     # y轴标签方向设置
            # pad=10,
        )

        ###################################################################

        # 画曲线
        size0 = df_data.index.size

        for i in range(size0):
            row = df_data.iloc[i, :].copy()

            row_output = df_input.iloc[i, :].copy()
            offset = row_output['被串相对位置(m)']

            label = '%sm' % offset

            xx = np.arange(row.size)
            yy = row.values

            ax.plot(
                xx,
                yy,
                linestyle='-',
                alpha=1,
                # color='r',
                color=cm.twilight(i / size0),
                label=label,
                # linewidth=width,
            )

        ###################################################################

        # 图例
        cb_pos = 0.11
        cax = fig.add_axes([cb_pos, 0.45, 0.01, 0.4])  # 四个参数分别是左、下、宽、长

        cmap = mpl.cm.twilight
        norm = mpl.colors.Normalize(vmin=-100, vmax=100)
        bounds = [tmp for tmp in np.linspace(-100, 100, size0 + 1)]
        cb = mpl.colorbar.ColorbarBase(
            ax=cax,
            cmap=cmap,
            norm=norm,
            # to use 'extend', you must specify two extra boundaries:
            # boundaries=[1.2] + bounds + [2.6],
            boundaries=bounds,
            # extend='both',
            # ticks=[1.3, 2.5],  # optional
            # ticks=[-100, 100],  # optional
            ticks=[],  # optional
            # spacing='proportional',
            orientation='vertical'
        )

        cb.set_ticks([-100, 0, 100])
        cb.set_ticklabels(['-350m', ' 0m', ' 350m'])

        cax.tick_params(labelsize=16)

        txt = '主\n被\n串\n错\n位'
        ax.text(
            -1.5, 0.5,
            txt,
            fontsize=16,
            color='black',
            va='center',
            ha='center',
            transform=cax.transAxes,
        )

        ax.legend(loc='upper right', fontsize=13)

        ###################################################################

        plt.tight_layout()

        filename1 = '%s\\%s.png' % (res_dir, title)
        fig.savefig(filename1)

        plt.show()


if __name__ == '__main__':
    draw_image_20230901_400m()