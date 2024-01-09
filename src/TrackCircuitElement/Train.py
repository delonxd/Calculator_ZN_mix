from src.AbstractClass.ElePack import *
from src.Module.OutsideElement import ROutside


# 列车
class Train(ElePack):
    def __init__(self, name_base, posi, parameter):
        parent_ins = None
        super().__init__(parent_ins, name_base)
        self.init_position(posi)
        self.parameter = parameter
        self.element['分路电阻1'] = ROutside(parent_ins=self, name_base='分路电阻1',
                                         posi=0, z=self.parameter['Rsht_z'])
        self.set_ele_name(prefix='')
        self.set_posi_abs(0)


# 多轮对列车
class TrainMulti(ElePack):
    def __init__(self, name_base, posi, parameter, wheel_list):
        parent_ins = None
        super().__init__(parent_ins, name_base)
        self.init_position(posi)
        self.parameter = parameter

        self.wheel_list = wheel_list

        for i, wheel_posi in enumerate(wheel_list):

            ele_name = '轮对%s' % (i+1)
            ele = ROutside(
                parent_ins=self,
                name_base=ele_name,
                posi=wheel_posi,
                z=self.parameter['Rsht_z']
            )

            self.element[ele_name] =ele

        self.set_ele_name(prefix='')
        self.set_posi_abs(0)

    # def head_wheel(self, head):
    #     return self

    def set_r_sht(self, z):
        for ele in self.element.values():
            ele.z = z

    def set_head_posi(self, posi_rlt, head):
        if head == '右':
            length = self.wheel_list[-1]
            self.posi_rlt = posi_rlt - length
        elif head == '左':
            self.posi_rlt = posi_rlt
        else:
            raise KeyboardInterrupt('车头方向错误')

        self.set_posi_abs(0)
