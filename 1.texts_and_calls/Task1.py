"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
任务1：
短信和通话记录中一共有多少电话号码？每个号码只统计一次。
输出信息：
"There are <count> different telephone numbers in the records." """

'''
方法一：将所有号码保存到一个新的列表中，然后将列表转换为集合，用len()计算出集合中的个数。
方法二：将号码保存到一个新的列表中，如果列表中有该号码，则不保存，反之则保存，然后用len()函数。
我用方法二。
'''

# 方法一：
# total_numbers = set(sum([[x[0], x[1]] for x in texts], []) + sum([[x[0], x[1]] for x in calls], []))
# print("There are {} different telephone numbers in the records.".format(len(total_numbers)))

# 方法二：
def count_num():
    tele_num = []
    for text in texts:
        for x in range(2):
            if text[x] not in tele_num:
                tele_num.append(text[x])

    for call in calls:
        for x in range(2):
            if call[x] not in tele_num:
                tele_num.append(call[x])

    return len(tele_num)

print("There are {} different telephone numbers in the records.".format(count_num()))
