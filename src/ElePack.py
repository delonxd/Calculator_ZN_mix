# 元素包
class ElePack:
    prop_table = {
        '父对象': 'parent_ins',
        '基础名称': 'name_base',
        '名称': 'name',
        '元素字典': 'element',
        '元素列表': 'ele_list',
        '室外元素标识': 'flag_outside',
        '元素列表标识': 'flag_ele_list',
        '单位元素标识': 'flag_ele_unit',
        '相对位置': 'posi_rlt',
        '绝对位置': 'posi_abs',
    }

    def __init__(self, parent_ins, name_base):
        self.parent_ins = parent_ins
        self.name_base = name_base
        self.name = str()
        self.element = dict()
        self.ele_list = list()
        self.flag_outside = False
        self._posi_rlt = None
        self.posi_abs = None
        self.flag_ele_list = False
        self.flag_ele_unit = False

    @property
    def posi_rlt(self):
        return self._posi_rlt

    @posi_rlt.setter
    def posi_rlt(self, value):
        self._posi_rlt = value

    def init_position(self, posi):
        self.flag_outside = True
        self._posi_rlt = posi
        self.posi_abs = 0

    def add_element(self, name, instance):
        if self.flag_ele_list:
            self.element[name] = instance
            self.ele_list.append(instance)

    def __len__(self):
        return len(self.element)

    def __getitem__(self, key):
        return self.element[key]

    def __setitem__(self, key, value):
        self.element[key] = value

    def values(self):
        return self.element.values()

    def keys(self):
        return self.element.keys()

    def items(self):
        return self.element.items()

    def set_property(self, key, value):
        prop_name = self.prop_table[key]
        exec('self.' + prop_name + ' = value')
        pass

    def get_property(self, key):
        value = None
        try:
            prop_name = self.prop_table[key]
            value = eval('self.' + prop_name)
        except KeyError:
            pass
        return value

    # 获得元器件连接顺序的列表
    def get_md_list(self, md_list):
        if self.flag_ele_list is True:
            for ele in self.ele_list:
                md_list = ele.get_md_list(md_list)
        else:
            md_list.append(self)
        return md_list

    # 设置绝对位置
    def set_posi_abs(self, abs_posi):
        if self.flag_outside is True:
            if self.parent_ins is None:
                self.posi_abs = self.posi_rlt + abs_posi
            else:
                self.posi_abs = self.parent_ins.posi_abs + self.posi_rlt
            if self.flag_ele_unit is False:
                for ele in self.element.values():
                    ele.set_posi_abs(abs_posi)

    # 获取元器件绝对位置
    def get_posi_abs(self, posi_list):
        posi_list = posi_list.copy()
        if self.flag_ele_unit is False:
            for ele in self.element.values():
                posi_list = ele.get_posi_abs(posi_list)
        else:
            posi_list.append(self.posi_abs)
            posi_list = self.sort_posi_list(posi_list)
        return posi_list

    # 快速获取绝对位置
    def get_posi_fast(self, ele_set):
        posi_all = list()
        for ele in ele_set:
            posi_all.append(ele.posi_abs)
        posi_all = self.sort_posi_list(posi_all)
        return posi_all

    # 配置元器件的名称
    def set_ele_name(self, prefix=''):
        if self.parent_ins is None:
            self.name = prefix + self.name_base
        else:
            self.name = self.parent_ins.name + '_' + self.name_base
        for ele in self.element.values():
            ele.set_ele_name(prefix=prefix)

    # 获得所有元器件的字典
    def get_element(self, ele_set, flag_ele_unit=True):
        if not (flag_ele_unit * self.flag_ele_unit):
            for ele in self.element.values():
                ele_set = ele.get_element(ele_set=ele_set, flag_ele_unit=flag_ele_unit)
        else:
            ele_set.add(self)
        return ele_set

    # # 获得所有变量
    # def get_varb(self, varb_set):
    #     if hasattr(self, 'varb_dict'):
    #         for ele in self.varb_dict.values():
    #             varb_set.add(ele)
    #     else:
    #         for ele in self.element.values():
    #             varb_set = ele.get_varb(varb_set)
    #     return varb_set.copy()

    # 使两个模块的变量映射到同一个变量对象
    @staticmethod
    def equal_varb(pack1, pack2):
        module1 = pack1[0]
        module2 = pack2[0]
        num1 = pack1[1]
        num2 = pack2[1]
        name1 = module1.varb_name[num1]
        name2 = module2.varb_name[num2]
        module1.varb_dict[name1] = module2.varb_dict[name2]

    # 节点排序
    @staticmethod
    def sort_posi_list(posi_list):
        new_list = list(set(posi_list))
        new_list.sort()
        return new_list

    # 变换频率
    @staticmethod
    def change_freq(freq):
        new = None
        if freq == 1700:
            new = 2300
        elif freq == 2000:
            new = 2600
        elif freq == 2300:
            new = 1700
        elif freq == 2600:
            new = 2000
        return new
