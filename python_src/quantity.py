import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# データの読み込み
data_files = {
    "WT": "../TotalDistance_WT.csv",
    "aKO": "../TotalDistance_scn1laa_KO.csv",
    "bKO": "../TotalDistance_scn1lab.sa16474_KO.csv",
    "DKO": "../TotalDistance_scn1laa_scn1lab.sa16474_DKO.csv",
}
data = {key: pd.read_csv(file) for key, file in data_files.items()}


# 平均値算出関数
def compute_average(data, col_range):
    # 指定された列範囲の平均を計算
    ave_data = data.iloc[:, col_range].mean(axis=1)
    return pd.DataFrame({"time": data["time"], "ave_data": ave_data})


# 列名変更関数
def change_rowname(data):
    # 列名を変更し、データを縦持ちに変換
    data.columns = ["time"] + [f"V{i}" for i in range(1, data.shape[1])]
    return pd.melt(data, id_vars="time", var_name="variable", value_name="value")


# 平均値と列名変更の適用
averages = {}
for key, df in data.items():
    col_range = slice(1, df.shape[1])  # 列範囲を動的に設定
    averages[key] = compute_average(df, col_range)
    data[key] = change_rowname(df)


# グラフ化関数
def plot_distance(dis_data, ave_data, output_file):
    # 移動距離のグラフを作成
    plt.figure(figsize=(6, 4))
    sns.lineplot(
        data=dis_data, x="time", y="value", hue="variable", palette="gray", legend=False
    )
    sns.lineplot(data=ave_data, x="time", y="ave_data", color="red", label="Average")
    plt.axvline(x=120, color="gray", linestyle="--")
    plt.axvline(x=300, color="gray", linestyle="--")
    plt.fill_betweenx(y=[0, 2000], x1=120, x2=300, color="red", alpha=0.1)
    plt.ylim(0, 2000)
    plt.xlabel("時間 [s]")
    plt.ylabel("移動距離 [mm]")
    plt.legend()
    plt.savefig(output_file)
    plt.close()


# グラフの作成と保存
for key in data.keys():
    plot_distance(data[key], averages[key], f"TotalDistance_{key}.png")


# t検定関数
def perform_t_tests(data_dict):
    # 各データ間でt検定を実施
    keys = list(data_dict.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            t_stat, p_value = ttest_ind(
                data_dict[keys[i]]["value"], data_dict[keys[j]]["value"]
            )
            print(f"{keys[i]} vs {keys[j]}: t-stat={t_stat:.4f}, p-value={p_value:.4e}")


# t検定の実行
perform_t_tests(data)
