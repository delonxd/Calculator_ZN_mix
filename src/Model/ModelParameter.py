import pickle
from src.ImpedanceParaType import ImpedanceMultiFreq
from src.ConstantType import Constant
import sys


# 模型参数
class ModelParameter:
    def __init__(self,
                 workpath,
                 name='原始参数'):
        self.name = name
        self.workpath = workpath

        if getattr(sys, 'frozen', False):
            workpath = sys._MEIPASS

        path = workpath + '/src/parameter_pkl/BasicParameter.pkl'
        self.parameter = dict()

        # with open('src/parameter_pkl/BasicParameter.pkl', 'rb') as pk_f:
        with open(path, 'rb') as pk_f:
            parameter = pickle.load(pk_f)

########################################################################################################################
        # 移频脉冲发送器
        parameter['z_pwr_yp'] = dict()
        parameter['z_pwr_yp'][1] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][1].rlc_s = {
            1700: [1.602, 0.165e-3, None],
            2000: [1.613, 0.165e-3, None],
            2300: [1.627, 0.165e-3, None],
            2600: [1.641, 0.165e-3, None]}

        parameter['z_pwr_yp'][2] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][2].rlc_s = {
            1700: [1.254, 0.126e-3, None],
            2000: [1.264, 0.126e-3, None],
            2300: [1.275, 0.126e-3, None],
            2600: [1.287, 0.126e-3, None]}

        parameter['z_pwr_yp'][3] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][3].rlc_s = {
            1700: [0.980, 0.091e-3, None],
            2000: [0.986, 0.091e-3, None],
            2300: [0.992, 0.091e-3, None],
            2600: [0.999, 0.091e-3, None]}

        parameter['z_pwr_yp'][4] = ImpedanceMultiFreq()
        parameter['z_pwr_yp'][4].rlc_s = {
            1700: [0.686, 0.058e-3, None],
            2000: [0.690, 0.058e-3, None],
            2300: [0.694, 0.058e-3, None],
            2600: [0.699, 0.058e-3, None]}

        # 移频脉冲发送器隔离
        parameter['z_pwr_ypmc_iso'] = ImpedanceMultiFreq()
        parameter['z_pwr_ypmc_iso'].rlc_s = {
            1700: [6.9, 2.62e-3, 2e-6],
            2000: [6.9, 2.62e-3, 2e-6],
            2300: [6.9, 2.62e-3, 2e-6],
            2600: [6.9, 2.62e-3, 2e-6]}

        # 移频脉冲防雷变压器
        parameter['z1_FL_ypmc'] = ImpedanceMultiFreq()
        parameter['z1_FL_ypmc'].rlc_s = {
            1700: [15.55, 6.90e-3, None],
            # 1700: [13.401, 6.683e-3, None],
            2000: [16.24, 6.86e-3, None],
            2300: [16.93, 6.84e-3, None],
            2600: [17.63, 6.81e-3, None]}

        parameter['z2_FL_ypmc'] = ImpedanceMultiFreq()
        parameter['z2_FL_ypmc'].rlc_s = {
            1700: [1883, 929e-3, None],
            # 1700: [1060, 663.437e-3, None],
            2000: [2611, 948e-3, None],
            2300: [3511, 972e-3, None],
            2600: [4643, 1003e-3, None]}

        # para1 = parameter['z1_FL_ypmc']
        # para2 = parameter['z2_FL_ypmc']
        # para3 = para1 * para2 / (para2 - para1)
        # parameter['z1_FL_ypmc'] = para3

        n_t = 1/1.095
        parameter['n_FL_ypmc'] = {
            1700: n_t,
            2000: n_t,
            2300: n_t,
            2600: n_t}

        # 移频脉冲扼流变压器
        parameter['z1_EL_ypmc'] = ImpedanceMultiFreq()
        parameter['z1_EL_ypmc'].rlc_s = {
            1700: [1.539, 502e-6, None],
            # 1700: [1.539, 502.818e-6, None],
            2000: [1.595, 500e-6, None],
            2300: [1.652, 498e-6, None],
            2600: [1.712, 496e-6, None]}

        parameter['z2_EL_ypmc'] = ImpedanceMultiFreq()
        parameter['z2_EL_ypmc'].rlc_s = {
            1700: [221, 44.2e-3, None],
            # 1700: [221.835, 44.169e-3, None],
            2000: [253, 40.9e-3, None],
            2300: [277, 38.3e-3, None],
            2600: [298, 36.1e-3, None]}

        para1 = parameter['z1_EL_ypmc']
        para2 = parameter['z2_EL_ypmc']
        para3 = para1 * para2 / (para2 - para1)
        parameter['z1_EL_ypmc'] = para3

        parameter['n_EL_ypmc'] = {
            1700: 5,
            2000: 5,
            2300: 5,
            2600: 5}

        # 移频脉冲接收端
        parameter['z_rcv_ypmc_iso'] = ImpedanceMultiFreq()
        parameter['z_rcv_ypmc_iso'].rlc_s = {
            1700: [25, 0.61e-3, 2e-6],
            2000: [25, 0.61e-3, 2e-6],
            2300: [25, 0.61e-3, 2e-6],
            2600: [25, 0.61e-3, 2e-6]}

        parameter['z_rcv_ypmc'] = ImpedanceMultiFreq()
        parameter['z_rcv_ypmc'].rlc_p = {
            1700: [400, 1.5e-3, None],
            2000: [400, 1.5e-3, None],
            2300: [400, 1.5e-3, None],
            2600: [400, 1.5e-3, None]}

        parameter['z_rcv_ypmc_iso2'] = ImpedanceMultiFreq()
        parameter['z_rcv_ypmc_iso2'].z = {
            1700: (143.36382516667515 - 25.410367118195474j),
            2000: (139.327150916492943 - 24.74158309793951j),
            2300: (136.09533295271993 - 23.70236776631829j),
            2600: (133.519251755064408 - 22.51025702855196j)}

########################################################################################################################
        # 白俄TAD
        parameter['TAD_z1_Belarus'] = ImpedanceMultiFreq()
        parameter['TAD_z1_Belarus'].rlc_s = {
            1700: (20.0739, 9.74608e-3, None),
            2000: (22.4710, 9.68749e-3, None),
            2300: (25.0969, 9.62455e-3, None),
            2600: (27.9120, 9.55859e-3, None)}

        parameter['TAD_z2_Belarus'] = ImpedanceMultiFreq()
        parameter['TAD_z2_Belarus'].rlc_s = {
            1700: (3.56163e3, 2.02889e-3, None),
            2000: (4.98841e3, 2.05249e-3, None),
            2300: (6.74819e3, 2.08324e-3, None),
            2600: (8.94749e3, 2.12174e-3, None)}

        n_bel = 630 / 62
        parameter['TAD_n_Belarus'] = {
            1700: n_bel,
            2000: n_bel,
            2300: n_bel,
            2600: n_bel}

########################################################################################################################

        # 白俄隔离盒Z1
        parameter['Z_iso1_Belarus'] = ImpedanceMultiFreq()
        parameter['Z_iso1_Belarus'].rlc_s = {
            1700: [6.9, 2.63e-3, 2e-6],
            2000: [6.9, 2.63e-3, 2e-6],
            2300: [6.9, 2.63e-3, 2e-6],
            2600: [6.9, 2.63e-3, 2e-6]}

        # 白俄隔离盒Z2
        parameter['Z_iso2_Belarus'] = ImpedanceMultiFreq()
        parameter['Z_iso2_Belarus'].rlc_s = {
            1700: [10, 200e-3, 2e-6],
            2000: [10, 200e-3, 2e-6],
            2300: [10, 200e-3, 2e-6],
            2600: [10, 200e-3, 2e-6]}

########################################################################################################################
        # 电容
        parameter['Ccmp_z'] = ImpedanceMultiFreq()
        parameter['Ccmp_z'].rlc_s = {
            1700: [10e-3, None, 25e-6],
            2000: [10e-3, None, 25e-6],
            2300: [10e-3, None, 25e-6],
            2600: [10e-3, None, 25e-6]}

        # # 电容
        # parameter['Ccmp_z'] = ImpedanceMultiFreq()
        # parameter['Ccmp_z'].rlc_s = {
        #     1700: [10e-3, None, 40e-6],
        #     2000: [10e-3, None, 40e-6],
        #     2300: [10e-3, None, 40e-6],
        #     2600: [10e-3, None, 40e-6]}

########################################################################################################################
        # 钢轨阻抗
        parameter['Trk_z'] = ImpedanceMultiFreq()
        parameter['Trk_z'].rlc_s = {
            1700: [1.177, 1.314e-3, None],
            # 1700: [1.84, 1.36e-3, None],
            2000: [1.306, 1.304e-3, None],
            2300: [1.435, 1.297e-3, None],
            2600: [1.558, 1.291e-3, None]}

        parameter['Cable_R'] = Constant(43)
        parameter['Cable_L'] = Constant(825e-6)
        parameter['Cable_C'] = Constant(28e-9)

        parameter['Rd'] = Constant(10000)
        parameter['Rsht_z'] = Constant(0.15)

        # # 钢轨阻抗21
        # parameter['Trk_z'] = ImpedanceMultiFreq()
        # parameter['Trk_z'].rlc_s = {
        #     # 1700: [1.177, 1.314e-3, None],
        #     1700: [1.349, 1.316e-3, None],
        #     2000: [1.306, 1.304e-3, None],
        #     2300: [1.435, 1.297e-3, None],
        #     2600: [1.558, 1.291e-3, None]}

########################################################################################################################

        # 标准开短路
        c_value = 25e-6
        parameter['Ccmp_z'].rlc_s = {
            1700: [10e-3, None, c_value],
            2000: [10e-3, None, c_value],
            2300: [10e-3, None, c_value],
            2600: [10e-3, None, c_value]}

        parameter['标准开路阻抗'] = ImpedanceMultiFreq()
        parameter['标准开路阻抗'].rlc_s = {
            1700: [1e10, None, None],
            2000: [1e10, None, None],
            2300: [1e10, None, None],
            2600: [1e10, None, None]}

        parameter['标准短路阻抗'] = ImpedanceMultiFreq()
        parameter['标准短路阻抗'].rlc_s = {
            1700: [1e-10, None, None],
            2000: [1e-10, None, None],
            2300: [1e-10, None, None],
            2600: [1e-10, None, None]}

        # 修正TAD_z3
        parameter['TAD_z3_发送端_区间'] = 2 * parameter['TAD_z3_发送端_区间']

########################################################################################################################

        # 钢轨阻抗
        parameter['z_be1'] = ImpedanceMultiFreq()
        parameter['z_be1'].rlc_s = {
            1700: [5.01, 0.506, 20e-6],
            2000: [5.01, 0.506, 20e-6],
            2300: [5.01, 0.506, 20e-6],
            2600: [5.01, 0.506, 20e-6]}

        parameter['z_be2'] = ImpedanceMultiFreq()
        parameter['z_be2'].rlc_s = {
            1700: [None, None, 2e-8],
            2000: [None, None, 2e-8],
            2300: [None, None, 1.2e-8],
            2600: [None, None, 1.2e-8]}

        parameter['z_be'] = (parameter['z_be1'] // parameter['z_be2']) / 24 / 24

########################################################################################################################

        # 机车信号比例
        parameter['机车信号比例I'] = {
            1700: 310 - 47,
            2000: 275 - 41,
            2300: 255 - 38,
            2600: 235 - 35}

        parameter['机车信号比例V'] = 115

########################################################################################################################

        parameter['z_pwr_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['z_pwr_25Hz_Coding'].rlc_s = {
            1700: [100, None, None],
            2000: [100, None, None],
            2300: [100, None, None],
            2600: [100, None, None]}

        parameter['z_FT1u'] = ImpedanceMultiFreq()
        parameter['z_FT1u'].rlc_s = {
            1700: [25.5, 1.5e-3, None],
            2000: [25.5, 1.5e-3, None],
            2300: [25.5, 1.5e-3, None],
            2600: [25.5, 1.5e-3, None]}

        # n_FT1u = 170 / 100
        n_FT1u = 170 / 40
        parameter['n_FT1u'] = {
            1700: n_FT1u,
            2000: n_FT1u,
            2300: n_FT1u,
            2600: n_FT1u}

        parameter['z_BPM'] = ImpedanceMultiFreq()
        # parameter['z_BPM'].rlc_s = {
        #     1700: [310, 1e-3, None],
        #     2000: [310, 1e-3, None],
        #     2300: [310, 1e-3, None],
        #     2600: [310, 1e-3, None]}

        # parameter['z_BPM'].rlc_s = {
        #     1700: [200, None, 0.286e-6],
        #     2000: [200, None, 0.286e-6],
        #     2300: [200, None, 0.286e-6],
        #     2600: [200, None, 0.286e-6]}

        parameter['z_BPM'].rlc_s = {
            1700: [300, None, None],
            2000: [300, None, None],
            2300: [300, None, None],
            2600: [300, None, None]}

        parameter['n_BPM'] = {
            1700: 4,
            2000: 4,
            2300: 4,
            2600: 4}

        parameter['n_EL_25Hz'] = {
            1700: 3,
            2000: 3,
            2300: 3,
            2600: 3}

        parameter['z_EL_25Hz'] = ImpedanceMultiFreq()
        parameter['z_EL_25Hz'].rlc_s = {
            1700: [3.47296, 0.001843964963, None],
            2000: [3.47296, 0.001843964963, None],
            2300: [3.47296, 0.001843964963, None],
            2600: [3.47296, 0.001843964963, None]}

########################################################################################################################
        # 电码化详细模型
        parameter['z_pwr_25Hz_Coding'] = dict()
        parameter['z_pwr_25Hz_Coding'][1] = ImpedanceMultiFreq()
        parameter['z_pwr_25Hz_Coding'][1].z = {
            1700: (22.30 + 29.00j),
            2000: (23.26 + 32.20j),
            2300: (23.93 + 36.77j),
            2600: (24.67 + 41.55j)}

        parameter['R1_FT1u_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['R1_FT1u_25Hz_Coding'].rlc_s = {
            1700: [100, None, None],
            2000: [100, None, None],
            2300: [100, None, None],
            2600: [100, None, None]}

        parameter['zs_FT1u_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['zs_FT1u_25Hz_Coding'].rlc_s = {
            1700: [54.86, 5.762e-3, None],
            2000: [58.15, 5.610e-3, None],
            2300: [61.47, 5.467e-3, None],
            2600: [64.79, 5.334e-3, None]}

        parameter['zm_FT1u_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['zm_FT1u_25Hz_Coding'].rlc_s = {
            1700: [9461, 0.3898, None],
            2000: [10410, 0.2796, None],
            2300: [11050, 0.2158, None],
            2600: [11590, 0.1647, None]}

        n_FT1u = 170 / 40
        parameter['n_FT1u_25Hz_Coding'] = {
            1700: n_FT1u,
            2000: n_FT1u,
            2300: n_FT1u,
            2600: n_FT1u}

        parameter['Rt_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['Rt_25Hz_Coding'].rlc_s = {
            1700: [50, None, None],
            2000: [50, None, None],
            2300: [50, None, None],
            2600: [50, None, None]}

########################################################################################################################

        parameter['z1_NGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['z1_NGL_25Hz_Coding'].rlc_s = {
            1700: [1400, 2.57, None],
            2000: [1800, 2.54, None],
            2300: [2800, 2.53, None],
            2600: [3500, 2.56, None]}

        parameter['C1_NGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['C1_NGL_25Hz_Coding'].rlc_s = {
            1700: [None, None, 1e-6],
            2000: [None, None, 1e-6],
            2300: [None, None, 1e-6],
            2600: [None, None, 1e-6]}

        parameter['L_NGL_25Hz_Coding'] = {}
        parameter['L_NGL_25Hz_Coding'][1700] = ImpedanceMultiFreq()
        parameter['L_NGL_25Hz_Coding'][1700].rlc_s = {
            1700: (67.3, 0.0698, None),
            2000: (82.1, 0.0690, None),
            2300: (97.0, 0.0680, None),
            2600: (111, 0.0675, None)}

        parameter['L_NGL_25Hz_Coding'][2000] = ImpedanceMultiFreq()
        parameter['L_NGL_25Hz_Coding'][2000].rlc_s = {
            1700: (50.2, 0.0510, None),
            2000: (61.2, 0.0500, None),
            2300: (72.5, 0.0494, None),
            2600: (83.8, 0.0489, None)}

        parameter['L_NGL_25Hz_Coding'][2300] = ImpedanceMultiFreq()
        parameter['L_NGL_25Hz_Coding'][2300].rlc_s = {
            1700: (38.90, 0.0386, None),
            2000: (47.20, 0.0380, None),
            2300: (56.10, 0.0376, None),
            2600: (64.72, 0.0372, None)}

        parameter['L_NGL_25Hz_Coding'][2600] = ImpedanceMultiFreq()
        parameter['L_NGL_25Hz_Coding'][2600].rlc_s = {
            1700: (30.5, 0.0300, None),
            2000: (37.5, 0.0298, None),
            2300: (44.6, 0.0295, None),
            2600: (51.6, 0.0292, None)}

        parameter['C3_NGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['C3_NGL_25Hz_Coding'].rlc_s = {
            1700: (None, None, 0.11e-6),
            2000: (None, None, 0.11e-6),
            2300: (None, None, 0.11e-6),
            2600: (None, None, 0.11e-6)}

        parameter['C4_NGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['C4_NGL_25Hz_Coding'].rlc_s = {
            1700: (None, None, 2e-6),
            2000: (None, None, 2e-6),
            2300: (None, None, 2e-6),
            2600: (None, None, 2e-6)}

########################################################################################################################

        parameter['L1_WGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['L1_WGL_25Hz_Coding'].rlc_s = {
            1700: (410, 0.344, None),
            2000: (480, 0.336, None),
            2300: (550, 0.331, None),
            2600: (600, 0.326, None)}

        parameter['L2_WGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['L2_WGL_25Hz_Coding'].rlc_s = {
            1700: (6.14, 0.00385, None),
            2000: (7.70, 0.00381, None),
            2300: (9.36, 0.00375, None),
            2600: (11.07, 0.0037, None)}

        parameter['C1_WGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['C1_WGL_25Hz_Coding'].rlc_s = {
            1700: (None, None, 1e-6),
            2000: (None, None, 1e-6),
            2300: (None, None, 1e-6),
            2600: (None, None, 1e-6)}

        parameter['C2_WGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['C2_WGL_25Hz_Coding'].rlc_s = {
            1700: (None, None, 20e-6),
            2000: (None, None, 20e-6),
            2300: (None, None, 20e-6),
            2600: (None, None, 20e-6)}

        parameter['zs_WGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['zs_WGL_25Hz_Coding'].rlc_s = {
            1700: (5.80, 1.30e-3, None),
            2000: (6.00, 1.30e-3, None),
            2300: (6.39, 1.30e-3, None),
            2600: (6.65, 1.29e-3, None)}

        parameter['zm_WGL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['zm_WGL_25Hz_Coding'].rlc_s = {
            1700: (1040, 0.192, None),
            2000: (1130, 0.170, None),
            2300: (1150, 0.153, None),
            2600: (1130, 0.141, None)}

        n_WGL_25Hz_Coding = 4
        parameter['n_WGL_25Hz_Coding'] = {
            1700: n_WGL_25Hz_Coding,
            2000: n_WGL_25Hz_Coding,
            2300: n_WGL_25Hz_Coding,
            2600: n_WGL_25Hz_Coding}

########################################################################################################################

        parameter['zs_EL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['zs_EL_25Hz_Coding'].rlc_s = {
            1700: (0.255, 0.120e-3, None),
            2000: (0.272, 0.119e-3, None),
            2300: (0.289, 0.118e-3, None),
            2600: (0.307, 0.117e-3, None)}


        parameter['zm_EL_25Hz_Coding'] = ImpedanceMultiFreq()
        parameter['zm_EL_25Hz_Coding'].rlc_s = {
            1700: (110, 0.024, None),
            2000: (123, 0.023, None),
            2300: (138, 0.021, None),
            2600: (154, 0.020, None)}

        n_EL_25Hz_Coding = 3
        parameter['n_EL_25Hz_Coding'] = {
            1700: n_EL_25Hz_Coding,
            2000: n_EL_25Hz_Coding,
            2300: n_EL_25Hz_Coding,
            2600: n_EL_25Hz_Coding}

########################################################################################################################

        parameter['inhibitor'] = {
            1700: (460.96e-6,   10.8e-6),
            2000: (399.54e-6,   9.7e-6),
            2300: (116.78e-6,   66e-6),
            2600: (79.73e-6,    72e-6)}

########################################################################################################################

        parameter['TB_电感短路'] = {
            1700: 11.42e-6,
            2000: 10.3e-6,
            2300: (55 + 93.75) * 1e-6,
            2600: (42 + 88.43) * 1e-6}

        parameter['TB_电感开路'] = {
            1700: None,
            2000: None,
            2300: 93.75e-6,
            2600: 88.43e-6}

########################################################################################################################

        # 无死区参数

        # 引接线
        parameter['Non_dead_zone_rca'] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_rca'].rlc_s = {
            1700: (6.46e-3, 2.90e-6, None),
            2000: (7.12e-3, 2.86e-6, None),
            2300: (7.74e-3, 2.82e-6, None),
            2600: (8.34e-3, 2.80e-6, None)}

        # L1、C1
        parameter['Non_dead_zone_z1'] = {}
        parameter['Non_dead_zone_z1'][1700] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z1'][1700].rlc_s = {
            1700: (8e-3, 54.16e-6, 84.15e-6),
            2000: (8e-3, 54.16e-6, 84.15e-6),
            2300: (8e-3, 54.16e-6, 84.15e-6),
            2600: (8e-3, 54.16e-6, 84.15e-6)}

        parameter['Non_dead_zone_z1'][2000] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z1'][2000].rlc_s = {
            1700: (8e-3, 65.84e-6, 54.67e-6),
            2000: (8e-3, 65.84e-6, 54.67e-6),
            2300: (8e-3, 65.84e-6, 54.67e-6),
            2600: (8e-3, 65.84e-6, 54.67e-6)}

        parameter['Non_dead_zone_z1'][2300] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z1'][2300].rlc_s = {
            1700: (17e-3, 130.00e-6, 65.91e-6),
            2000: (17e-3, 130.00e-6, 65.91e-6),
            2300: (17e-3, 130.00e-6, 65.91e-6),
            2600: (17e-3, 130.00e-6, 65.91e-6)}

        parameter['Non_dead_zone_z1'][2600] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z1'][2600].rlc_s = {
            1700: (17e-3, 130.00e-6, 47.63e-6),
            2000: (17e-3, 130.00e-6, 47.63e-6),
            2300: (17e-3, 130.00e-6, 47.63e-6),
            2600: (17e-3, 130.00e-6, 47.63e-6)}

        # L2、C2
        parameter['Non_dead_zone_z2'] = {}
        parameter['Non_dead_zone_z2'][1700] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z2'][1700].rlc_s = {
            1700: (22.000001e-3, 50e-6, None),
            2000: (25.000001e-3, 50e-6, None),
            2300: (28.000001e-3, 50e-6, None),
            2600: (31.000001e-3, 50e-6, None)}

        parameter['Non_dead_zone_z2'][2000] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z2'][2000].rlc_s = {
            1700: (22.000001e-3, 50e-6, None),
            2000: (25.000001e-3, 50e-6, None),
            2300: (28.000001e-3, 50e-6, None),
            2600: (31.000001e-3, 50e-6, None)}

        parameter['Non_dead_zone_z2'][2300] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z2'][2300].rlc_s = {
            1700: (22.000001e-3, None, 83.50e-6),
            2000: (25.000001e-3, None, 83.50e-6),
            2300: (28.000001e-3, None, 83.50e-6),
            2600: (31.000001e-3, None, 83.50e-6)}

        parameter['Non_dead_zone_z2'][2600] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_z2'][2600].rlc_s = {
            1700: (22.000001e-3, None, 73.01e-6),
            2000: (25.000001e-3, None, 73.01e-6),
            2300: (28.000001e-3, None, 73.01e-6),
            2600: (31.000001e-3, None, 73.01e-6)}

        # C5
        parameter['Non_dead_zone_c5'] = {}
        parameter['Non_dead_zone_c5'][1700] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_c5'][1700].rlc_s = {
            1700: (3e-3, None, 156.99e-6),
            2000: (3e-3, None, 156.99e-6),
            2300: (3e-3, None, 156.99e-6),
            2600: (3e-3, None, 156.99e-6)}

        parameter['Non_dead_zone_c5'][2000] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_c5'][2000].rlc_s = {
            1700: (3e-3, None, 113.89e-6),
            2000: (3e-3, None, 113.89e-6),
            2300: (3e-3, None, 113.89e-6),
            2600: (3e-3, None, 113.89e-6)}

        parameter['Non_dead_zone_c5'][2300] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_c5'][2300].rlc_s = {
            1700: (3e-3, None, 73.84e-6),
            2000: (3e-3, None, 73.84e-6),
            2300: (3e-3, None, 73.84e-6),
            2600: (3e-3, None, 73.84e-6)}

        parameter['Non_dead_zone_c5'][2600] = ImpedanceMultiFreq()
        parameter['Non_dead_zone_c5'][2600].rlc_s = {
            1700: (3e-3, None, 59.62e-6),
            2000: (3e-3, None, 59.62e-6),
            2300: (3e-3, None, 59.62e-6),
            2600: (3e-3, None, 59.62e-6)}

        # 内隔离
        parameter['non_dead_zone_z_inside_iso'] = {}
        p0 = parameter['Non_dead_zone_rca']
        p1 = parameter['Non_dead_zone_z1']
        p2 = parameter['Non_dead_zone_z2']
        parameter['non_dead_zone_z_inside_iso'][1700] = p0 + (p1[1700] // p2[1700])
        parameter['non_dead_zone_z_inside_iso'][2000] = p0 + (p1[2000] // p2[2000])
        parameter['non_dead_zone_z_inside_iso'][2300] = p0 + (p1[2300] // p2[2300])
        parameter['non_dead_zone_z_inside_iso'][2600] = p0 + (p1[2600] // p2[2600])


########################################################################################################################

        self.parameter = parameter

    def __len__(self):
        return len(self.parameter)

    def __getitem__(self, key):
        return self.parameter[key]

    def __setitem__(self, key, value):
        self.parameter[key] = value

    def values(self):
        return self.parameter.values()

    def keys(self):
        return self.parameter.keys()

    def items(self):
        return self.parameter.items()


if __name__ == '__main__':
    # print(time.asctime(time.localtime()))

    # 导入参数
    # para = ModelParameter()
    pass