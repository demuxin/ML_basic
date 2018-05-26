"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
import re

with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
任务3:
(080)是班加罗尔的固定电话区号。
固定电话号码包含括号，
所以班加罗尔地区的电话号码的格式为(080)xxxxxxx。

第一部分: 找出被班加罗尔地区的固定电话所拨打的所有电话的区号和移动前缀（代号）。
 - 固定电话以括号内的区号开始。区号的长度不定，但总是以 0 打头。
 - 移动电话没有括号，但数字中间添加了
   一个空格，以增加可读性。一个移动电话的移动前缀指的是他的前四个
   数字，并且以7,8或9开头。
 - 电话促销员的号码没有括号或空格 , 但以140开头。

输出信息:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
代号不能重复，每行打印一条，按字典顺序排序后输出。

第二部分: 由班加罗尔固话打往班加罗尔的电话所占比例是多少？
换句话说，所有由（080）开头的号码拨出的通话中，
打往由（080）开头的号码所占的比例是多少？

输出信息:
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
注意：百分比应包含2位小数。
"""


def tele_classify():
    fix_tele = []
    mob_tele = []

    for call in calls:
        if call[0][:5] == "(080)": # 主叫来自班加罗尔地区
            if call[1][:2] == "(0": # 被叫是固定电话
                last_index = re.search('\(.*\)', call[1]).end()
                if call[1][:last_index] not in fix_tele:
                    fix_tele.append(call[1][:last_index])

            # elif call[1][0] == "7" or call[1][0] == "8" or call[1][0] == "9":
            else: # 被叫是移动电话
                if call[1][:4] not in mob_tele:
                    mob_tele.append(call[1][:4])

    fix_tele = sorted(fix_tele, key = lambda x : x)
    mob_tele = sorted(mob_tele, key = lambda x : x)
    total_tele = fix_tele + mob_tele
    # for item in total_tele:
    #     print("The numbers called by people in Bangalore have codes: {}".format(item))
    print("The numbers called by people in Bangalore have codes: {}".format(total_tele))


def called_percentage():
    ban_calling = 0
    ban_called = 0
    for call in calls:
        if call[0][:5] == "(080)": # 主叫来自班加罗尔地区
            ban_calling += 1
            if call[1][:5] == "(080)": # 被叫来自班加罗尔地区
                ban_called +=1

    percentage = ban_called / ban_calling
    percentage = round(percentage, 4) * 100 # 百分比应包含2位小数
    ret_str = "{} percent of calls from fixed lines in Bangalore are calls to other " \
        "fixed lines in Bangalore.".format(percentage)
    return ret_str


tele_classify()
print(called_percentage())
