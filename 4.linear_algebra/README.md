# 线性回归项目
线性代数是很多机器学习算法的基础，在这个项目中，你将不借助任何库，用你之前所学来解决一个线性回归问题。

-----

# 项目内容
所有需要完成的任务都在 `linear_regression_project.ipynb` 中，其中包括编程题和证明题。

-----

# 单元测试
项目已经部署了自动化测试，你能在每个需要你完成的函数下面看到形如以下测试代码：
`%run -i -e test.py LinearRegressionTestCase.test_...`
Ctrl + Enter 运行即可。

如果你的实现有问题，会有断言错误`AssertionError`被抛出。
请重新检查你的实现，并且修正bug，直到通过测试为止。

以下是一些带有特定反馈的断言错误说明：

- AssertionError: Expected shape(M,N), but got shape(C,D)."
  + 返回的计算结果的形状不正确
- AssertionError: Matrix A shouldn't be modified.
  + 你在实现augmentMatrix时修改了矩阵A
- AssertionError: Matrix A is singular.
  + 你的gj_Solve实现在矩阵A是奇异矩阵时没有返回None
- AssertionError: Matrix A is not singular.
  + 你的gj_Solve实现会在矩阵A不是奇异矩阵时返回None
- AssertionError: Bad result.
  + 你的gj_Solve返回了不正确的计算结果
