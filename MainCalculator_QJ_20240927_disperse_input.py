from MainCalculator_QJ_20240904_disperse import main_cal

import os
import time
import pandas as pd


def cycle_cal():
    input_path = '邻线干扰参数输入_区间分散式_v0.1.xlsx'
    df_input = pd.read_excel(input_path)

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    file_path = '仿真输出_分散式轨道电路_%s.xlsx' % timestamp

    main_cal(file_path, os.getcwd(), None, df_input)


if __name__ == '__main__':
    cycle_cal()
