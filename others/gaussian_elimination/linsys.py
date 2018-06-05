# 构建高斯消去法进行运算
from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30

class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes): # 提供平面对象列表，初始化线性方程组对象
        try:
            d = planes[0].dimension
            for p in planes: # 确保所有平面都位于同一维度
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    # 将方程组变成三角型并返回
    def compute_triangular_form(self):
        system = deepcopy(self)
        mum_equations = len(system)
        num_variables = system.dimension
        j = 0 # current variable is x

        for i in range(mum_equations): # 遍历方程
            while j < num_variables:
                # 获取第i个方程变量j的系数
                c = MyDecimal(system[i].normal_vector.coordinates[j])
                if c.is_near_zero():
                    # 将行i与其下面的变量j的系数不为零的行交换
                    swap_succeeded = system.swap_with_row_below_for_nonzero_coefficient(i, j)
                    if not swap_succeeded:
                        j += 1
                        continue

                system.clear_coefficients_below(i, j) # 清除行i下面的所有方程中变量j的系数
                j += 1
                break

        return system


    def swap_with_row_below_for_nonzero_coefficient(self, row, col):
        num_equations = len(self)

        for k in range(col+1, num_equations):
            coeff = MyDecimal(self[k].normal_vector.coordinates[col])
            if not coeff.is_near_zero():
                self.swap_rows(row, k)
                return True

        return False


    def clear_coefficients_below(self, row, col):
        num_equations = len(self)
        beta = self[row].normal_vector.coordinates[col]

        for k in range(row+1, num_equations):
            gamma = self[k].normal_vector.coordinates[col]
            alpha = -gamma/beta
            self.add_multiple_times_row_to_row(alpha, row, k)


    # 将三角型化为最简梯阵型方程组
    def compute_rref(self):
        tf = self.compute_triangular_form()
        num_equations = len(tf)
        pivot_indices = tf.indices_of_first_nonzero_terms_in_each_row() # 每行首项变量的索引列表

        for i in range(num_equations)[::-1]:
            j = pivot_indices[i] # 第i个方程的首个非零系数的变量
            if j < 0:
                continue
            tf.scale_row_to_make_coefficient_equal_one(i, j)
            tf.clear_coefficients_above(i, j)

        return tf


    def scale_row_to_make_coefficient_equal_one(self, row, col):
        coeff = MyDecimal(self[row].normal_vector.coordinates[col])
        beta = Decimal('1.') / coeff
        self.multiply_coefficient_and_row(beta, row)


    def clear_coefficients_above(self, row, col):
        for k in range(row)[::-1]:
            alpha = -self[k].normal_vector.coordinates[col]
            self.add_multiple_times_row_to_row(alpha, row, k)


    # 得出方程组的结果
    def compute_solution(self):
        try:
            return self.do_gaussian_elimination_and_extract_solution()

        except Exception as e: # 无解或无数解时抛出异常
            if (str(e) == self.NO_SOLUTIONS_MSG or
                str(e) == self.INF_SOLUTIONS_MSG):
                return str(e)
            # else:        #Exception: No nonzero elements found
            #     raise e  #这里抛出异常，被Python解释器捕获，打印错误信息堆栈，然后程序退出


    def do_gaussian_elimination_and_extract_solution(self):
        rref = self.compute_rref()

        rref.raise_exception_if_contradictory_equation() # 0=k
        rref.raise_exception_if_too_few_pivots() # 主变量太少

        num_variables = rref.dimension
        solution_coordinates = [rref.planes[i].constant_term for i in
                                range(num_variables)] # 方程的常数项

        # 保留三位小数
        solu_coord = [i.quantize(Decimal('0.000')) for i in solution_coordinates]
        return Vector(solu_coord)


    def raise_exception_if_contradictory_equation(self):
        for p in self.planes:
            try:
                p.first_nonzero_index(p.normal_vector.coordinates)

            except Exception as e:
                # 如果plane的法向量的坐标全为0
                if str(e) == 'No nonzero elements found':
                    constant_term = MyDecimal(p.constant_term)
                    # 检查常量项是否为零
                    if not constant_term.is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                    # else:    # 这里抛出异常的话，上个函数的剩余部分都不会执行
                    #     raise e


    def raise_exception_if_too_few_pivots(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        # 计算非负索引的数量
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension

        if num_pivots < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)


    # 交换两个等式
    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]


    # 将等式乘以非零数字
    def multiply_coefficient_and_row(self, coefficient, row):
        normal_vector = self[row].normal_vector
        new_normal_vector = normal_vector.time_scalar(coefficient)
        new_constant_term = self[row].constant_term * coefficient
        self[row] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)


    # 将多倍的等式加到另一个等式上
    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        new_normal_vector = n1.time_scalar(coefficient).plus(n2)

        k1 = self[row_to_add].constant_term
        k2 = self[row_to_be_added_to].constant_term
        new_constant_term = (coefficient * k1) + k2
        self[row_to_be_added_to] = Plane(normal_vector=new_normal_vector,
                                         constant_term=new_constant_term)


    # 负责找出每个等式的第一个非零项位置，有助于寻找每个等式里的主变量
    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    # 返回方程组里平面的数量
    def __len__(self):
        return len(self.planes)


    # 使用下标标记法访问方程组中特定平面或方程
    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    # 输出简洁的方程组
    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


'''
p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

s = LinearSystem([p0,p1,p2,p3])

print(s.indices_of_first_nonzero_terms_in_each_row())
print('{},\n{},\n{},\n{}'.format(s[0],s[1],s[2],s[3]))
print(s)

# s.swap_rows(0, 1) # 第0行和第1行进行交换
# s.multiply_coefficient_and_row(2, 0) # 第0行乘以系数2
# s.add_multiple_times_row_to_row(2, 0, 1) # 将第0行乘以2，加到第1行
print(s.compute_triangular_form())

print(MyDecimal('1e-9').is_near_zero())
print(MyDecimal('1e-11').is_near_zero())
'''


print('------------------------测试用例---------------------------')
# 应该为无解
p0 = Plane(normal_vector=Vector(['5.862','1.178','-10.366']), constant_term='-8.15')
p1 = Plane(normal_vector=Vector(['-2.931','-0.589','5.183']), constant_term='-4.075')
ss = LinearSystem([p0, p1])
print(ss.compute_triangular_form())
print(ss.compute_rref())
print(ss.compute_solution())

print('-'*25)

# 应该为无数解
p0 = Plane(normal_vector=Vector(['8.631','5.112','-1.816']), constant_term='-5.113')
p1 = Plane(normal_vector=Vector(['4.315','11.132','-5.27']), constant_term='-6.775')
p2 = Plane(normal_vector=Vector(['-2.158','3.01','-1.727']), constant_term='-0.831')
ss = LinearSystem([p0, p1, p2])
print(ss.compute_triangular_form())
print(ss.compute_rref())
print(ss.compute_solution())

print('-'*25)

# # 唯一解[-1.177, 0.707, -0.083]
p0 = Plane(normal_vector=Vector(['5.262','2.739','-9.878']), constant_term='-3.441')
p1 = Plane(normal_vector=Vector(['5.111','6.358','7.638']), constant_term='-2.152')
p2 = Plane(normal_vector=Vector(['2.016','-9.924','-1.367']), constant_term='-9.278')
p3 = Plane(normal_vector=Vector(['2.167','-13.543','-18.883']), constant_term='-10.567')
ss = LinearSystem([p0, p1, p2, p3])
print(ss.compute_triangular_form())
print(ss.compute_rref())
print(ss.compute_solution())
