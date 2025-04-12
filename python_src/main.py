# 必要なライブラリをインポート
import os
import json
import pandas as pd

# フォルダパスの設定
folder_path = "../genotype"

# フォルダが存在するか確認
if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
    raise FileNotFoundError(f"指定されたフォルダが存在しません: {folder_path}")

# JSONファイルのリストを取得
file_list = [
    os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".json")
]

# ファイルごとに処理を実行
for file_name in file_list:
    try:
        # JSONファイルを読み込み
        with open(file_name, "r", encoding="utf-8") as f:
            genotypes = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSONファイルの読み込みに失敗しました: {file_name}, エラー: {e}")
        continue

    # データ名を抽出
    data_name = (
        os.path.basename(file_name).replace("genotype_", "").replace(".json", "")
    )
    Ddata_name = f"../data/{data_name}_Total_Distance.csv"
    Vdata_name = f"../data/{data_name}_Average_Velocity.csv"

    # データをロード（CSV形式を想定）
    try:
        D = pd.read_csv(Ddata_name)  # CSVファイルを読み込み
        V = pd.read_csv(Vdata_name)  # CSVファイルを読み込み
    except FileNotFoundError as e:
        print(f"データファイルが見つかりません: {e}")
        continue
    except pd.errors.EmptyDataError as e:
        print(f"データファイルが空です: {e}")
        continue

    # CSVの列名をJSONから抽出した値に置き換え
    try:
        new_columns = {
            col: genotypes[col] for col in D.columns if col in genotypes
        }  # JSONに一致する列名を置き換え
        D.rename(columns=new_columns, inplace=True)
        V.rename(columns=new_columns, inplace=True)
    except KeyError as e:
        print(f"列名の置き換えに失敗しました: {e}")
        continue

    # 更新されたCSVを保存
    try:
        D.to_csv(Ddata_name, index=False)  # 更新されたCSVを保存
        V.to_csv(Vdata_name, index=False)
        print(f"CSVファイルを更新しました: {Ddata_name}, {Vdata_name}")
    except IOError as e:
        print(f"CSVファイルの書き込みに失敗しました: {e}")

print("処理が完了しました。")
