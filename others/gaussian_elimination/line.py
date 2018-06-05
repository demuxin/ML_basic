from decimal import Decimal, getcontext
from vector import Vector

getcontext().prec = 30 # 控制小数个数

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    #直线法向量和直线等式的常量，法向量给出了标准直线形式的系数。(Ax + By = k)
    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            #n = self.normal_vector
            n = self.normal_vector.coordinates
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    @staticmethod
    def first_nonzero_index(iterable): # 找到等式的第一个非零系数
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


    def is_parallel_to(self, ell):
        n1 = self.normal_vector
        n2 = ell.normal_vector

        return n1.is_parallel(n2)


    def __str__(self): # 使用变量x1和x2输出直线等式的标准形式，很容易类推到多维空间。

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector.coordinates

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    def __eq__(self, ell):

        # 如果直线的法向量为零向量，即直线定义等式的左侧为0，则判断两直线的常量系数是否相等
        if self.normal_vector.is_zero_vector():
            if not ell.normal_vector.is_zero_vector():
                print('there is a zero vector')
                return False
            else:
                print('both lines are zero vector')
                diff = self.constant_term - ell.constant_term
                return MyDecimal(diff).is_near_zero()
        elif ell.normal_vector.is_zero_vector():
            print('there is a zero vector')
            return False

        if not self.is_parallel_to(ell):
            return False

        print('parallel lines')
        x0 = self.basepoint
        y0 = ell.basepoint
        basepoint_diff = x0.minus(y0)

        n = self.normal_vector
        # 两点构成的向量与法向量是否垂直,点积是否为零
        # MyDecimal(basepoint_diff.dot(n)).is_near_zero()
        return basepoint_diff.is_orthogonal(n)

    def intersection_with(self, ell): # 求交点

        if self == ell: # 直线重合，则交点为整个直线
            return self
        elif self.is_parallel_to(ell): # 直线平行不重合，无交点
            return None

        A, B = self.normal_vector.coordinates
        C, D = ell.normal_vector.coordinates
        k1 = self.constant_term
        k2 = ell.constant_term

        x_numerator = D*k1 - B*k2
        y_numerator = -C*k1 + A*k2
        one_over_denom = Decimal('1')/(A*D - B*C)

        getcontext().prec = 3 # 控制小数个数
        return Vector([x_numerator, y_numerator]).time_scalar(one_over_denom)


# 扩展Decimal类，检测小数对象是否在误差范围内
class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

# ell1 = Line(normal_vector=Vector([4.046, 2.836]), constant_term=1.21)
# ell2 = Line(normal_vector=Vector([10.115, 7.09]), constant_term=3.025)
# print('intersection 1: {}'.format(ell1.intersection_with(ell2)))

# ell1 = Line(normal_vector=Vector([7.204, 3.182]), constant_term=8.68)
# ell2 = Line(normal_vector=Vector([8.172, 4.114]), constant_term=9.883)
# print('intersection 2: {}'.format(ell1.intersection_with(ell2)))

# ell1 = Line(normal_vector=Vector([1.182, 5.562]), constant_term=6.744)
# ell2 = Line(normal_vector=Vector([1.773, 8.343]), constant_term=9.525)
# print('intersection 3: {}'.format(ell1.intersection_with(ell2)))
