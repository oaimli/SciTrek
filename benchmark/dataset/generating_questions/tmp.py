# import json
#
# output = '{ "name":"age", "age"d:30, "city":"New York"}'
# try:
#     output_json = json.loads(output)
#     print(output_json)
# except json.JSONDecodeError as err:
#     print("JSON parsing error,", err)
#
# print(output.find("age"))

import matplotlib.pyplot as plt
# plot
x = range(0, 5)
y1 = [1, 1, 1, 1, 2]
y2 = [2, 2, 2, 2, 2]
y3 = [3, 3, 3, 3, 3]

plt.figure(figsize=(9, 5))
plt.plot(x, y1, color='deepskyblue', label="Question Length")
plt.plot(x, y2, color='darkcyan', label="SQL Length")
plt.plot(x, y3, color="orange", label="Number of SQL Clauses")
plt.yticks(fontproperties='Times New Roman', fontsize=22)
plt.xticks(list(x), fontproperties='Times New Roman', fontsize=22)
plt.xlabel("Question index", fontdict={"size":22, "family": 'Times New Roman'})
plt.legend(prop={"family": 'Times New Roman', "size": 17})
plt.show()
# plt.savefig('grouping.png', dpi=1024)