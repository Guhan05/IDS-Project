import pandas as pd
import glob
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def load_data(folder_path):

    # 1. Load all parquet files
    files = glob.glob(os.path.join(folder_path, "*.parquet"))

    df_list = []
    for f in files:
        print("Loading:", f)
        df_list.append(pd.read_parquet(f))

    df = pd.concat(df_list, ignore_index=True)

    # 2. Clean column names (VERY IMPORTANT)
    df.columns = df.columns.str.strip()

    # 3. Remove nulls/duplicates
    df = df.dropna().drop_duplicates()

    # 4. Convert to binary labels
    df['Label'] = df['Label'].apply(
        lambda x: 0 if str(x).upper() == "BENIGN" else 1
    )

    # 5. Simple random sampling (FAST + SAFE)
    df = df.sample(frac=0.3, random_state=42)

    # 6. Split features/labels
    X = df.drop(columns=['Label'])
    y = df['Label']

    # 7. Normalize
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    # 8. Stratified train-test split (handles balance correctly)
    return train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
