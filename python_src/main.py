# 必要なライブラリをインポート
import os
import json
import pandas as pd

# フォルダパスの設定
folder_path = "../genotype"
file_list = [
    os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".json")
]

# 初期化
MV_WT, MV_aKO, MV_bKO, MV_DKO, MV_PTZ, MV_Lam = None, None, None, None, None, None
TD_WT, TD_aKO, TD_bKO, TD_DKO, TD_PTZ, TD_Lam = None, None, None, None, None, None

# ファイルごとに処理を実行
for file_name in file_list:
    # JSONファイルを読み込み
    with open(file_name, "r", encoding="utf-8") as f:
        genotypes = json.load(f)

    # データ名を抽出
    data_name = (
        os.path.basename(file_name).replace("genotype_", "").replace(".json", "")
    )
    Ddata_name = f"{data_name}_Total_Distance"
    Vdata_name = f"{data_name}_Average_Velocity"

    # データをロード（pickle形式を想定）
    D = pd.read_pickle(Ddata_name)
    V = pd.read_pickle(Vdata_name)

    # サンプル名とジェノタイプの対応表を作成
    genotype_df = pd.DataFrame(
        {
            "sample_col": [
                f"sample-{int(name.replace('Genotype', ''))}"
                for name in genotypes.keys()
            ],
            "genotype": list(genotypes.values()),
        }
    )

    # 各ジェノタイプに対応する列を抽出
    def get_columns_by_genotype(df, genotype_df, genotype):
        cols = genotype_df.loc[genotype_df["genotype"] == genotype, "sample_col"]
        return [col for col in cols if col in df.columns]

    wt_cols = get_columns_by_genotype(D, genotype_df, "WT")
    aKO_cols = get_columns_by_genotype(D, genotype_df, "kcc2aKO")
    bKO_cols = get_columns_by_genotype(D, genotype_df, "kcc2bKO")
    DKO_cols = get_columns_by_genotype(D, genotype_df, "kcc2DKO")
    PTZ_cols = get_columns_by_genotype(D, genotype_df, "PTZ")
    Lam_cols = get_columns_by_genotype(D, genotype_df, "Lam")

    # 各ジェノタイプのデータを結合
    MV_WT = pd.concat([MV_WT, V[wt_cols]], axis=1) if MV_WT is not None else V[wt_cols]
    MV_aKO = (
        pd.concat([MV_aKO, V[aKO_cols]], axis=1) if MV_aKO is not None else V[aKO_cols]
    )
    MV_bKO = (
        pd.concat([MV_bKO, V[bKO_cols]], axis=1) if MV_bKO is not None else V[bKO_cols]
    )
    MV_DKO = (
        pd.concat([MV_DKO, V[DKO_cols]], axis=1) if MV_DKO is not None else V[DKO_cols]
    )
    MV_PTZ = (
        pd.concat([MV_PTZ, V[PTZ_cols]], axis=1) if MV_PTZ is not None else V[PTZ_cols]
    )
    MV_Lam = (
        pd.concat([MV_Lam, V[Lam_cols]], axis=1) if MV_Lam is not None else V[Lam_cols]
    )

    TD_WT = pd.concat([TD_WT, D[wt_cols]], axis=1) if TD_WT is not None else D[wt_cols]
    TD_aKO = (
        pd.concat([TD_aKO, D[aKO_cols]], axis=1) if TD_aKO is not None else D[aKO_cols]
    )
    TD_bKO = (
        pd.concat([TD_bKO, D[bKO_cols]], axis=1) if TD_bKO is not None else D[bKO_cols]
    )
    TD_DKO = (
        pd.concat([TD_DKO, D[DKO_cols]], axis=1) if TD_DKO is not None else D[DKO_cols]
    )
    TD_PTZ = (
        pd.concat([TD_PTZ, D[PTZ_cols]], axis=1) if TD_PTZ is not None else D[PTZ_cols]
    )
    TD_Lam = (
        pd.concat([TD_Lam, D[Lam_cols]], axis=1) if TD_Lam is not None else D[Lam_cols]
    )

# 結果の確認（必要に応じて保存や出力を追加）
print("処理が完了しました。")
