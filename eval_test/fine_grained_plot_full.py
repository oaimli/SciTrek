import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    with open("fine_grained_filtering_128k_em_full.json") as f:
        results = json.load(f)

    all_1 = list(results["qwen3_4b_thinking_2507"].values())
    all_2 = list(results["qwen3_30b_a3b_thinking_2507"].values())
    all_3 = list(results["deepseek_r1_distill_llama_70b_instruct"].values())
    all_4 = list(results["gemini25_pro"].values())
    all_5 = list(results["gpt41_20250414"].values())
    all_6 = list(results["o4mini_20250416"].values())

    fig, (ax_1, ax_2, ax_3) = plt.subplots(3, 1, figsize=(25, 10))

    # question focus
    model_1 = [float(tmp)*100 for tmp in all_1[0:7]]
    model_2 = [float(tmp)*100 for tmp in all_2[0:7]]
    model_3 = [float(tmp)*100 for tmp in all_3[0:7]]
    model_4 = [float(tmp)*100 for tmp in all_4[0:7]]
    model_5 = [float(tmp)*100 for tmp in all_5[0:7]]
    model_6 = [float(tmp)*100 for tmp in all_6[0:7]]
    print(model_1)
    print(model_2)
    print(model_3)
    print(model_4)
    print(model_5)
    print(model_6)
    xs = range(1, 8)
    xs_psv1 = (np.array(xs) - 0.25).tolist()
    xs_psv2 = (np.array(xs) - 0.15).tolist()
    xs_psv3 = (np.array(xs) - 0.05).tolist()
    xs_psv4 = (np.array(xs) + 0.05).tolist()
    xs_psv5 = (np.array(xs) + 0.15).tolist()
    xs_psv6 = (np.array(xs) + 0.25).tolist()
    bar_width = 0.1
    ks = ["Author Count", "Author List", "Author Relation", "Citation Relation", "Reference Count", "Title List", "Title Word Count"]
    ax_1.bar(xs_psv1, height=model_1, width=bar_width, color='deepskyblue')
    ax_1.bar(xs_psv2, height=model_2, width=bar_width, color='darkcyan')
    ax_1.bar(xs_psv3, height=model_3, width=bar_width, color="mediumturquoise")
    ax_1.bar(xs_psv4, height=model_4, width=bar_width, color="darkmagenta")
    ax_1.bar(xs_psv5, height=model_5, width=bar_width, color="lightgray")
    ax_1.bar(xs_psv6, height=model_6, width=bar_width, color="lightcoral")
    ax_1.set_xticks(xs)
    ax_1.set_xlim(0.5, 7.5)
    ax_1.set_xticklabels(ks, fontproperties='Times New Roman', fontsize=32)
    ax_1.tick_params(axis='y', labelsize=32)
    ax_1.set_ylim(0, 70)
    ax_1.set_ylabel(r"EM (%)", fontsize=32, family='Times New Roman')

    # sql type
    # original label: multi_graph_filtering", "multi_ran_aggregating", "multi_ran_filtering_foa", "multi_ran_filtering_foo", "multi_ran_filtering_ofo", "multi_ran_organizing"
    # original order: "Graph Filtering", "Aggregating", "Filtering+Aggregating", "Filtering+Sorting", "Filtering", "Sorting"
    # new order: "Aggregating", "Sorting", "Filtering", "Filtering+Aggregating", "Filtering+Sorting", "Graph Filtering"
    st_1 = [-1] * 6
    st_1[0] = all_1[7:13][1]
    st_1[1] = all_1[7:13][5]
    st_1[2] = all_1[7:13][4]
    st_1[3] = all_1[7:13][2]
    st_1[4] = all_1[7:13][3]
    st_1[5] = all_1[7:13][0]
    st_2 = [-1] * 6
    st_2[0] = all_2[7:13][1]
    st_2[1] = all_2[7:13][5]
    st_2[2] = all_2[7:13][4]
    st_2[3] = all_2[7:13][2]
    st_2[4] = all_2[7:13][3]
    st_2[5] = all_2[7:13][0]
    st_3 = [-1] * 6
    st_3[0] = all_3[7:13][1]
    st_3[1] = all_3[7:13][5]
    st_3[2] = all_3[7:13][4]
    st_3[3] = all_3[7:13][2]
    st_3[4] = all_3[7:13][3]
    st_3[5] = all_3[7:13][0]
    st_4 = [-1] * 6
    st_4[0] = all_4[7:13][1]
    st_4[1] = all_4[7:13][5]
    st_4[2] = all_4[7:13][4]
    st_4[3] = all_4[7:13][2]
    st_4[4] = all_4[7:13][3]
    st_4[5] = all_4[7:13][0]
    st_5 = [-1] * 6
    st_5[0] = all_5[7:13][1]
    st_5[1] = all_5[7:13][5]
    st_5[2] = all_5[7:13][4]
    st_5[3] = all_5[7:13][2]
    st_5[4] = all_5[7:13][3]
    st_5[5] = all_5[7:13][0]
    st_6 = [-1] * 6
    st_6[0] = all_6[7:13][1]
    st_6[1] = all_6[7:13][5]
    st_6[2] = all_6[7:13][4]
    st_6[3] = all_6[7:13][2]
    st_6[4] = all_6[7:13][3]
    st_6[5] = all_6[7:13][0]

    model_1 = [float(tmp)*100 for tmp in st_1]
    model_2 = [float(tmp)*100 for tmp in st_2]
    model_3 = [float(tmp)*100 for tmp in st_3]
    model_4 = [float(tmp)*100 for tmp in st_4]
    model_5 = [float(tmp)*100 for tmp in st_5]
    model_6 = [float(tmp)*100 for tmp in st_6]
    xs = range(1, 7)
    xs_psv1 = (np.array(xs) - 0.25).tolist()
    xs_psv2 = (np.array(xs) - 0.15).tolist()
    xs_psv3 = (np.array(xs) - 0.05).tolist()
    xs_psv4 = (np.array(xs) + 0.05).tolist()
    xs_psv5 = (np.array(xs) + 0.15).tolist()
    xs_psv6 = (np.array(xs) + 0.25).tolist()
    bar_width = 0.1
    ks = ["Aggregating", "Sorting", "Filtering", "Filtering+Aggregating", "Filtering+Sorting", "Relational Filtering"]
    ax_2.bar(xs_psv1, height=model_1, width=bar_width, color='deepskyblue')
    ax_2.bar(xs_psv2, height=model_2, width=bar_width, color='darkcyan')
    ax_2.bar(xs_psv3, height=model_3, width=bar_width, color="mediumturquoise")
    ax_2.bar(xs_psv4, height=model_4, width=bar_width, color="darkmagenta")
    ax_2.bar(xs_psv5, height=model_5, width=bar_width, color="lightgray")
    ax_2.bar(xs_psv6, height=model_6, width=bar_width, color="lightcoral")
    ax_2.set_xticks(xs)
    ax_2.set_xlim(0.5, 6.5)
    ax_2.set_xticklabels(ks, fontproperties='Times New Roman', fontsize=32)
    ax_2.tick_params(axis='y', labelsize=32)
    ax_2.set_ylim(0, 70)
    ax_2.set_ylabel(r"EM (%)", fontsize=32, family='Times New Roman')

    # domain
    model_1 = [float(tmp)*100 for tmp in all_1[13:]]
    model_2 = [float(tmp)*100 for tmp in all_2[13:]]
    model_3 = [float(tmp)*100 for tmp in all_3[13:]]
    model_4 = [float(tmp)*100 for tmp in all_4[13:]]
    model_5 = [float(tmp)*100 for tmp in all_5[13:]]
    model_6 = [float(tmp)*100 for tmp in all_6[13:]]
    xs = range(1, 9)
    xs_psv1 = (np.array(xs) - 0.25).tolist()
    xs_psv2 = (np.array(xs) - 0.15).tolist()
    xs_psv3 = (np.array(xs) - 0.05).tolist()
    xs_psv4 = (np.array(xs) + 0.05).tolist()
    xs_psv5 = (np.array(xs) + 0.15).tolist()
    xs_psv6 = (np.array(xs) + 0.25).tolist()
    bar_width = 0.1
    ks = ["CS", "Economics", "EE", "Math", "Physics",
          "Biology", "Finance", "Statistics"]
    ax_3.bar(xs_psv1, height=model_1, width=bar_width, color='deepskyblue', label="Qwen3-4B-Thinking-2507")
    # for xs_psv1_item, model_1_item in zip(xs_psv1, model_1):
    #     ax_3.text(xs_psv1_item, model_1_item, model_1_item, ha='center', va='bottom', fontsize=28)
    ax_3.bar(xs_psv2, height=model_2, width=bar_width, color='darkcyan', label="Qwen3-30B-A3B-Thinking-2507")
    ax_3.bar(xs_psv3, height=model_3, width=bar_width, color="mediumturquoise", label="DeepSeek-R1-Distill-Llama-70B")
    ax_3.bar(xs_psv4, height=model_4, width=bar_width, color="darkmagenta", label="Gemini 2.5 Pro")
    ax_3.bar(xs_psv5, height=model_5, width=bar_width, color="lightgray", label="GPT-4.1")
    ax_3.bar(xs_psv6, height=model_6, width=bar_width, color="lightcoral", label="o4-mini")
    ax_3.set_xticks(xs)
    ax_3.set_xlim(0.5, 8.5)
    ax_3.set_xticklabels(ks, fontproperties='Times New Roman', fontsize=32)
    ax_3.tick_params(axis='y', labelsize=32)
    ax_3.set_ylim(0, 70)
    ax_3.set_ylabel(r"EM (%)", fontsize=32, family='Times New Roman')

    ax_3.legend(
        bbox_to_anchor=(0.90, -0.25),
        ncol=3,
        prop={"family": 'Times New Roman', "size": 32}
        )

    plt.subplots_adjust(top=0.97, bottom=0.30, right=0.98, left=0.05, hspace=0.4)
    # plt.show(dpi=600)
    plt.savefig("fine_grained_plot_full.png", dpi=600)