import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.python.keras import models, layers, regularizers, callbacks
from tensorflow.python.keras.models import model_from_json

def mean_and_std():
    """学習用のデータから平均値と標準偏差を抽出"""
    names = ["Place", "Number", "Name", "Age", "Live", "Weight", "Rank", "A_1st", 
                     "A_2nd", "B_1st", "B_2nd", "Moter_No", "Moter_2nd", "Bote_No", "Bote_2nd"]
    df = pd.read_csv('program_no_shinki.csv', names = names).drop(["Name", "Live", "Number"], axis=1).fillna(0)
    
    df_dummies = pd.get_dummies(df["Rank"])
    df_dummies.astype("float32")
    
    df = df.drop('Rank', axis=1)
    df.astype("float32")
    
    df = pd.merge(df, df_dummies, how="left", left_index=True, right_index=True)
    
    X = df.values.astype("float32")
    
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    
    return mean, std


def model_weight():
    #　データ40000件（新規抜き）
    model_1st = model_from_json(open("weights/suminoe_no_shinki.json", "r").read())
    model_1st.load_weights("weights/suminoe_no_shinki.h5")
    
    model_2nd = model_from_json(open("weights/suminoe_2nd_40000.json", "r").read())
    model_2nd.load_weights("weights/suminoe_2nd_40000.h5")
    
    model_3rd = model_from_json(open("weights/suminoe_3rd_40000.json", "r").read())
    model_3rd.load_weights("weights/suminoe_3rd_40000.h5")
    
    return model_1st, model_2nd, model_3rd


def create_df(date):
    filename = f"edited_data/{date}.csv"
    
    names = ["Place", "Number", "Name", "Age", "Live", "Weight", "Rank", "A_1st",
                           "A_2nd", "B_1st", "B_2nd", "Moter_No", "Moter_2nd", "Bote_No", "Bote_2nd"]
    df_test = pd.read_csv(filename, names = names)
    
    data_list = []
    for num in range(1, 73):
        if num % 6 == 0 and num <= 6:
            data_list.append(df_test[:num])
            previous_num = num
        elif num % 6 == 0:
            data_list.append(df_test[previous_num: num])
            previous_num = num
    
    return data_list


def edit_and_prediction(date, mean, std, data_list model):
    for num, df_test in enumerate(data_list, start=1):
        names = ["Place", "Number", "Name", "Age", "Live", "Weight", "Rank", "A_1st",
                 "A_2nd", "B_1st", "B_2nd", "Moter_No", "Moter_2nd", "Bote_No", "Bote_2nd"]
        df_rank = pd.DataFrame([[None, None, None, None, None, None, "A1", None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, "A2", None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, "B1", None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, "B2", None, None, None, None, None, None, None, None]], columns=names)
        df_test = df_test.append(df_rank, ignore_index=True)
        df_test = df_test.drop(["Name", "Number", "Live"], axis=1)
        df_dummies2 = pd.get_dummies(df_test["Rank"]).astype("float32")


        df_test_merge = pd.merge(df_test, df_dummies2, how="left", left_index=True, right_index=True)
        df_test_merge = df_test_merge.dropna().drop("Rank", axis=1)

        df_test = df_test_merge.astype('float32')
        df_test -= mean
        df_test /= std
        
        pre = model.predict(df_test)


        with open("race_predict.txt", "a", encoding="utf-8") as f:
            f.write("""\
{} : {}Rの予想結果
------------------------""".format(date, num))
            f.write("\n1st Predict(10000)<br>")
            for i, predict_1st_1 in enumerate(pre_1st_1, start=1):
                f.write("\n {} :   {:6.1f}%<br>".format(i, float(predict_1st_1)*100))
            
            f.write("\n\n")

            f.write("\n1st Predict(44000)<br>")
            for i, predict_1st_2 in enumerate(pre_1st_2, start=1):
                f.write("\n {} :   {:6.1f}%<br>".format(i, float(predict_1st_2)*100))
            
            f.write("\n\n")
            
            f.write("\n1st Predict(no bias)<br>")
            for i, predict_1st_3 in enumerate(pre_1st_3, start=1):
                f.write("\n {} :   {:6.1f}%<br>".format(i, float(predict_1st_3)*100))

            f.write("\n\n")