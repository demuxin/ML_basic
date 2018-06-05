from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'no unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'no unique orthogonal component'

    # init():用于初始化对象，在创建新对象时调用
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            # Decimal()确保所有坐标都是小数，而不是浮点数或整数
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates) # 向量维度

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)


    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)


    def time_scalar(self, c): # 数乘
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)


    def magnitude(self): # 计算向量的长度
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))


    def normalized(self): # 单位向量
        try:
            magnitude = self.magnitude()
            return self.time_scalar(1./magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)


    def dot(self, v): # 计算点积
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])


    def angle_with(self, v, in_degrees=False): # 计算向量角度
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            # The value of input for acos range from -1 <= x <= 1
            dot_value = 1 if (abs(u1.dot(u2) - Decimal('1.'))) <= 1e-10 else u1.dot(u2)
            angle_in_radians = acos(dot_value) # 将点积传入反余弦函数中
            ''' 方法二：
            vector_dot = self.dot(v) # decimal
            multi_magni = Decimal(self.magnitude() * v.magnitude())
            angle_in_radians = acos(vector_dot / multi_magni)
            '''
            if in_degrees: # 角度
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else: # 弧度
                return angle_in_radians

        except Exception as e: # 检查是否为零向量
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e


    def is_zero_vector(self, tolerance=1e-10): # 零向量
        # 由于精度问题，确保点积的值非常小就行
        return self.magnitude() < tolerance


    def is_parallel(self, v): # 平行
        return (self.is_zero_vector() or v.is_zero_vector() or
                self.angle_with(v) == 0 or self.angle_with(v) == pi)


    def is_orthogonal(self, v, tolerance=1e-10): # 垂直
        return (abs(self.dot(v)) < tolerance)


    def component_parallel_to(self, basis): # 平行分量
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.time_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e


    def component_orthogonal_to(self, basis): # 垂直分量
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e


    def cross(self, v): # 向量积
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
            new_coordinates = [  y1*z2 - y2*z1 ,
                               -(x1*z2 - x2*z1),
                                 x1*y2 - x2*y1  ]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            # 如果是二维向量，就向每个向量中添加为0的z轴坐标
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or 
                  msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e


    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()


    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')


    # str():在使用print语句时被调用
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    # eq():判断self对象是否等于对象v
    def __eq__(self, v):
        return self.coordinates == v.coordinates
