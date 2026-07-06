import pandas as pd


if __name__ == "__main__":
    data = pd.read_excel("analysis_2602.xlsx")
    # target_values = ["NULLL"]
    # target_values = ["FORMAT"]
    target_values = ["LESS"]
    # target_values = ["MORE"]

    for i in range(1, 16):
        print(data[i][0])
        values = data[i][1:]

        values_aggregating = values[0:10]
        tmp = 0
        for value in values_aggregating:
            # print(value)
            if value in target_values:
                tmp += 1
        print("values_aggregating", tmp/len(values_aggregating))

        values_sorting = values[10:20]
        tmp = 0
        for value in values_sorting:
            # print(value)
            if value in target_values:
                tmp += 1
        print("values_sorting", tmp / len(values_sorting))

        values_filtering = values[20:30]
        tmp = 0
        for value in values_filtering:
            # print(value)
            if value in target_values:
                tmp += 1
        print("values_filtering", tmp / len(values_filtering))

        values_filtering_aggregating = values[30:40]
        tmp = 0
        for value in values_filtering_aggregating:
            # print(value)
            if value in target_values:
                tmp += 1
        print("values_filtering_aggregating", tmp / len(values_filtering_aggregating))

        values_filtering_sorting = values[40:50]
        tmp = 0
        for value in values_filtering_sorting:
            # print(value)
            if value in target_values:
                tmp += 1
        print("values_filtering_sorting", tmp / len(values_filtering_sorting))

        values_rational_filtering = values[50:60]
        tmp = 0
        for value in values_rational_filtering:
            # print(value)
            if value in target_values:
                tmp += 1
        print("values_rational_filtering", tmp / len(values_rational_filtering))

