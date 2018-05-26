"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
texts和calls是一个二维列表，一维列表的元素都是字符串。
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
任务0:
短信记录的第一条记录是什么？通话记录最后一条记录是什么？
输出信息:
"First record of texts, <incoming number> texts <answering number> at time <time>"
"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"
"""

def print_info():
    # first_text = texts[0]
    # print_text = "First record of texts, {} texts {} at time {}". \
        # format(first_text[0], first_text[1], first_text[2])
    # print(print_text)
    print("First record of texts, {} texts {} at time {}".format(*texts[0]))

    # last_call = calls[-1]
    # print_call = "Last record of calls, {} calls {} at time {}, lasting {} seconds". \
    #     format(last_call[0], last_call[1], last_call[2], last_call[3])
    # print(print_call)
    print("Last record of calls, {} calls {} at time {}, lasting {} seconds".format(*calls[-1]))

print_info()
