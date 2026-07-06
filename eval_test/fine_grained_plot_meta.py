import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    with open("fine_grained_filtering_128k_em_meta.json") as f:
        results = json.load(f)
    # with open("fine_grained_filtering_128k_rouge_l_full.json") as f:
    #     results = json.load(f)
    # with open("fine_grained_filtering_128k_f1_full.json") as f:
    #     results = json.load(f)

    all_1 = list(results["gemini25_pro"].values())
    all_2 = list(results["gemma3_27b_it"].values())
    all_3 = list(results["gpt41_20250414"].values())
    all_4 = list(results["llama33_70b_instruct"].values())
    all_5 = list(results["llama4_scout_17b_16e_instruct"].values())
    all_6 = list(results["o4mini_20250416"].values())
    all_7 = list(results["qwen25_14b_instruct_1m"].values())
    all_8 = list(results["qwen25_7b_instruct_1m"].values())

    fig, (ax_1, ax_2, ax_3) = plt.subplots(3, 1, figsize=(25, 10))

    # question focus
    model_1 = [float(tmp)*100 for tmp in all_1[0:7]]
    model_2 = [float(tmp)*100 for tmp in all_2[0:7]]
    model_3 = [float(tmp)*100 for tmp in all_3[0:7]]
    model_4 = [float(tmp)*100 for tmp in all_4[0:7]]
    model_5 = [float(tmp)*100 for tmp in all_5[0:7]]
    model_6 = [float(tmp)*100 for tmp in all_6[0:7]]
    model_7 = [float(tmp)*100 for tmp in all_7[0:7]]
    model_8 = [float(tmp)*100 for tmp in all_8[0:7]]
    xs = range(1, 8)
    xs_psv1 = (np.array(xs) - 0.35).tolist()
    xs_psv2 = (np.array(xs) - 0.25).tolist()
    xs_psv3 = (np.array(xs) - 0.15).tolist()
    xs_psv4 = (np.array(xs) - 0.05).tolist()
    xs_psv5 = (np.array(xs) + 0.05).tolist()
    xs_psv6 = (np.array(xs) + 0.15).tolist()
    xs_psv7 = (np.array(xs) + 0.25).tolist()
    xs_psv8 = (np.array(xs) + 0.35).tolist()
    bar_width = 0.1
    ks = ["Author Count", "Author List", "Author Relation", "Citation Relation", "Reference Count", "Title List", "Title Word Count"]
    ax_1.bar(xs_psv1, height=model_1, width=bar_width, color='deepskyblue', label="Gemini 2.5 Pro")
    ax_1.bar(xs_psv2, height=model_2, width=bar_width, color='darkcyan', label="Gemma3-27B-IT")
    ax_1.bar(xs_psv3, height=model_3, width=bar_width, color="orange", label="GPT4.1")
    ax_1.bar(xs_psv4, height=model_4, width=bar_width, color="darkmagenta", label="Llama3.3-70B-Instruct")
    ax_1.bar(xs_psv5, height=model_5, width=bar_width, color="khaki", label="Llama4-Scout-Instruct")
    ax_1.bar(xs_psv6, height=model_6, width=bar_width, color="mediumturquoise", label="o4mini")
    ax_1.bar(xs_psv7, height=model_7, width=bar_width, color="lavender", label="Qwen2.5-14B-Instruct-1M")
    ax_1.bar(xs_psv8, height=model_8, width=bar_width, color="crimson", label="Qwen2.5-7b-Instruct-1M")
    ax_1.set_xticks(xs)
    ax_1.set_xlim(0.5, 7.5)
    ax_1.set_xticklabels(ks, fontproperties='Times New Roman', fontsize=26)
    ax_1.tick_params(axis='y', labelsize=26)
    ax_1.set_ylim(0, 100)
    ax_1.set_ylabel(r"EM (%)", fontsize=26, family='Times New Roman')

    # sql type
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
    st_7 = [-1] * 6
    st_7[0] = all_7[7:13][1]
    st_7[1] = all_7[7:13][5]
    st_7[2] = all_7[7:13][4]
    st_7[3] = all_7[7:13][2]
    st_7[4] = all_7[7:13][3]
    st_7[5] = all_7[7:13][0]
    st_8 = [-1] * 6
    st_8[0] = all_8[7:13][1]
    st_8[1] = all_8[7:13][5]
    st_8[2] = all_8[7:13][4]
    st_8[3] = all_8[7:13][2]
    st_8[4] = all_8[7:13][3]
    st_8[5] = all_8[7:13][0]

    model_1 = [float(tmp)*100 for tmp in st_1]
    model_2 = [float(tmp)*100 for tmp in st_2]
    model_3 = [float(tmp)*100 for tmp in st_3]
    model_4 = [float(tmp)*100 for tmp in st_4]
    model_5 = [float(tmp)*100 for tmp in st_5]
    model_6 = [float(tmp)*100 for tmp in st_6]
    model_7 = [float(tmp)*100 for tmp in st_7]
    model_8 = [float(tmp)*100 for tmp in st_8]
    xs = range(1, 7)
    xs_psv1 = (np.array(xs) - 0.35).tolist()
    xs_psv2 = (np.array(xs) - 0.25).tolist()
    xs_psv3 = (np.array(xs) - 0.15).tolist()
    xs_psv4 = (np.array(xs) - 0.05).tolist()
    xs_psv5 = (np.array(xs) + 0.05).tolist()
    xs_psv6 = (np.array(xs) + 0.15).tolist()
    xs_psv7 = (np.array(xs) + 0.25).tolist()
    xs_psv8 = (np.array(xs) + 0.35).tolist()
    bar_width = 0.1
    ks = ["Aggregating", "Sorting", "Filtering", "Filtering+Aggregating", "Filtering+Sorting", "Relational Filtering"]
    ax_2.bar(xs_psv1, height=model_1, width=bar_width, color='deepskyblue', label="Gemini 2.5 Pro")
    ax_2.bar(xs_psv2, height=model_2, width=bar_width, color='darkcyan', label="Gemma3-27B-IT")
    ax_2.bar(xs_psv3, height=model_3, width=bar_width, color="orange", label="GPT4.1")
    ax_2.bar(xs_psv4, height=model_4, width=bar_width, color="darkmagenta", label="Llama3.3-70B-Instruct")
    ax_2.bar(xs_psv5, height=model_5, width=bar_width, color="khaki", label="Llama4-Scout-Instruct")
    ax_2.bar(xs_psv6, height=model_6, width=bar_width, color="mediumturquoise", label="o4mini")
    ax_2.bar(xs_psv7, height=model_7, width=bar_width, color="lavender", label="Qwen2.5-14B-Instruct-1M")
    ax_2.bar(xs_psv8, height=model_8, width=bar_width, color="crimson", label="Qwen2.5-7b-Instruct-1M")
    ax_2.set_xticks(xs)
    ax_2.set_xlim(0.5, 6.5)
    ax_2.set_xticklabels(ks, fontproperties='Times New Roman', fontsize=26)
    ax_2.tick_params(axis='y', labelsize=26)
    ax_2.set_ylim(0, 100)
    ax_2.set_ylabel(r"EM (%)", fontsize=26, family='Times New Roman')

    # domain
    model_1 = [float(tmp)*100 for tmp in all_1[13:]]
    model_2 = [float(tmp)*100 for tmp in all_2[13:]]
    model_3 = [float(tmp)*100 for tmp in all_3[13:]]
    model_4 = [float(tmp)*100 for tmp in all_4[13:]]
    model_5 = [float(tmp)*100 for tmp in all_5[13:]]
    model_6 = [float(tmp)*100 for tmp in all_6[13:]]
    model_7 = [float(tmp)*100 for tmp in all_7[13:]]
    model_8 = [float(tmp)*100 for tmp in all_8[13:]]
    xs = range(1, 9)
    xs_psv1 = (np.array(xs) - 0.35).tolist()
    xs_psv2 = (np.array(xs) - 0.25).tolist()
    xs_psv3 = (np.array(xs) - 0.15).tolist()
    xs_psv4 = (np.array(xs) - 0.05).tolist()
    xs_psv5 = (np.array(xs) + 0.05).tolist()
    xs_psv6 = (np.array(xs) + 0.15).tolist()
    xs_psv7 = (np.array(xs) + 0.25).tolist()
    xs_psv8 = (np.array(xs) + 0.35).tolist()
    bar_width = 0.1
    ks = ["Computer Science", "Economics", "Electronic Engineering", "Math", "Physics",
          "Biology", "Finance", "Statistics"]
    ax_3.bar(xs_psv1, height=model_1, width=bar_width, color='deepskyblue', label="Gemini 2.5 Pro")
    ax_3.bar(xs_psv2, height=model_2, width=bar_width, color='darkcyan', label="Gemma3-27B-IT")
    ax_3.bar(xs_psv3, height=model_3, width=bar_width, color="orange", label="GPT4.1")
    ax_3.bar(xs_psv4, height=model_4, width=bar_width, color="darkmagenta", label="Llama3.3-70B-Instruct")
    ax_3.bar(xs_psv5, height=model_5, width=bar_width, color="khaki", label="Llama4-Scout-Instruct")
    ax_3.bar(xs_psv6, height=model_6, width=bar_width, color="mediumturquoise", label="o4mini")
    ax_3.bar(xs_psv7, height=model_7, width=bar_width, color="lavender", label="Qwen2.5-14B-Instruct-1M")
    ax_3.bar(xs_psv8, height=model_8, width=bar_width, color="crimson", label="Qwen2.5-7b-Instruct-1M")
    ax_3.set_xticks(xs)
    ax_3.set_xlim(0.5, 8.5)
    ax_3.set_xticklabels(ks, fontproperties='Times New Roman', fontsize=26)
    ax_3.tick_params(axis='y', labelsize=26)
    ax_3.set_ylim(0, 100)
    ax_3.set_ylabel(r"EM (%)", fontsize=26, family='Times New Roman')

    ax_3.legend(
        bbox_to_anchor=(0.91, -0.25),
        ncol=4,
        prop={"family": 'Times New Roman', "size": 26}
        )

    plt.subplots_adjust(top=0.97, bottom=0.20, right=0.98, left=0.05, hspace=0.4)
    # plt.show(dpi=600)
    plt.savefig("fine_grained_plot_meta.png", dpi=600)