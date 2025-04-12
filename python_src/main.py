import os
import json
import pandas as pd


def validate_folder(folder_path):
    """フォルダが存在するか確認"""
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        raise FileNotFoundError(f"指定されたフォルダが存在しません: {folder_path}")


def get_json_files(folder_path):
    """指定フォルダ内のJSONファイルを取得"""
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".json")
    ]


def load_json(file_name):
    """JSONファイルを読み込む"""
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSONファイルの読み込みに失敗しました: {file_name}, エラー: {e}")
        return None


def load_csv(file_path):
    """CSVファイルを読み込む"""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"データファイルが見つかりません: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"データファイルが空です: {e}")
    return None


def replace_columns(dataframe, json_values):
    """JSONの値に基づいて列名を置き換える"""
    try:
        new_columns = {
            col: json_values[i] if i < len(json_values) else col
            for i, col in enumerate(dataframe.columns[1:], start=0)
        }
        new_columns = {dataframe.columns[0]: dataframe.columns[0], **new_columns}
        dataframe.rename(columns=new_columns, inplace=True)
    except (KeyError, IndexError) as e:
        print(f"列名の置き換えに失敗しました: {e}")


def process_json_files(folder_path):
    """JSONファイルを処理してCSVを更新"""
    file_list = get_json_files(folder_path)
    for file_name in file_list:
        genotypes = load_json(file_name)
        if not genotypes:
            continue

        data_name = (
            os.path.basename(file_name).replace("genotype_", "").replace(".json", "")
        )
        Ddata_name = f"../data/{data_name}_Total_Distance.csv"
        Vdata_name = f"../data/{data_name}_Average_Velocity.csv"

        D = load_csv(Ddata_name)
        V = load_csv(Vdata_name)
        if D is None or V is None:
            continue

        replace_columns(D, list(genotypes.values()))
        replace_columns(V, list(genotypes.values()))

        try:
            D.to_csv(Ddata_name, index=False)
            V.to_csv(Vdata_name, index=False)
            print(f"CSVファイルを更新しました: {Ddata_name}, {Vdata_name}")
        except IOError as e:
            print(f"CSVファイルの書き込みに失敗しました: {e}")


def process_csv_files(data_folder, output_folder):
    """CSVファイルを処理してWT/PTZデータを保存"""
    os.makedirs(output_folder, exist_ok=True)
    csv_files = [
        f for f in os.listdir(data_folder) if f.endswith("Average_Velocity.csv")
    ]

    WT_data = pd.DataFrame()
    PTZ_data = pd.DataFrame()

    for csv_file in csv_files:
        file_path = os.path.join(data_folder, csv_file)
        try:
            df = pd.read_csv(file_path)
            WT_filtered = df[[col for col in df.columns if "WT" in col]]
            PTZ_filtered = df[[col for col in df.columns if "PTZ" in col]]

            WT_filtered.columns = [f"WT_{i + 1}" for i in range(WT_filtered.shape[1])]
            PTZ_filtered.columns = [
                f"PTZ_{i + 1}" for i in range(PTZ_filtered.shape[1])
            ]

            WT_data = (
                pd.concat([WT_data, WT_filtered], axis=1)
                if not WT_data.empty
                else WT_filtered
            )
            PTZ_data = (
                pd.concat([PTZ_data, PTZ_filtered], axis=1)
                if not PTZ_data.empty
                else PTZ_filtered
            )
        except Exception as e:
            print(
                f"CSVファイルの処理中にエラーが発生しました: {file_path}, エラー: {e}"
            )

    WT_data.to_csv(
        os.path.join(output_folder, "WT_data.csv"), index=False, encoding="utf-8"
    )
    PTZ_data.to_csv(
        os.path.join(output_folder, "PTZ_data.csv"), index=False, encoding="utf-8"
    )
    print(f"WT/PTZデータを保存しました: {output_folder}")


def main():
    """メイン処理"""
    folder_path = "../genotype"
    data_folder = "../data"
    output_folder = "../output"

    validate_folder(folder_path)
    process_json_files(folder_path)
    process_csv_files(data_folder, output_folder)
    print("処理が完了しました。")


if __name__ == "__main__":
    main()
