
## 高斯消元法

* vector.py：实现向量的加减乘除、积、量积等运算  
* line.py：求向量的交点  
* plane.py：判断平面是否平行、是否相交  
* linsys.py：使用高斯消元法对方程组进行化简并求解  

运行 `linsys.py`，得到如下结果：
```
------------------------测试用例---------------------------
Linear System:
Equation 1: 5.862x_1 + 1.178x_2 - 10.366x_3 = -8.150
Equation 2: 0 = -8.150
Linear System:
Equation 1: x_1 + 0.201x_2 - 1.768x_3 = -1.390
Equation 2: 0 = -8.150
No solutions
-------------------------
Linear System:
Equation 1: 8.631x_1 + 5.112x_2 - 1.816x_3 = -5.113
Equation 2: 8.576x_2 - 4.362x_3 = -4.219
Equation 3: 0 = 0
Linear System:
Equation 1: x_1 + 0.091x_3 = -0.301
Equation 2: x_2 - 0.509x_3 = -0.492
Equation 3: 0 = 0
Infinitely many solutions
-------------------------
Linear System:
Equation 1: 5.262x_1 + 2.739x_2 - 9.878x_3 = -3.441
Equation 2: 3.698x_2 + 17.233x_3 = 1.190
Equation 3: 53.559x_3 = -4.427
Equation 4: 0 = 0
Linear System:
Equation 1: x_1 = -1.177
Equation 2: x_2 = 0.707
Equation 3: x_3 = -0.083
Equation 4: 0 = 0
Vector: (Decimal('-1.177'), Decimal('0.707'), Decimal('-0.083'))
```