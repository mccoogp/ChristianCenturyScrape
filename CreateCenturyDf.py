import pandas as pd

df = pd.DataFrame(columns=["Issue", "Date", "Article/Page Number", "Article Title", "Article Text", "Author"])
olddf = pd.read_csv("CenturyArts.csv")
for i in range(len(olddf)):
    df.loc[len(df)] = {"Issue" : "", "Date" : "", "Article/Page Number" : "", "Article Title" : "", "Article Text" : "", "Author" : ""}
df.to_csv("FinalCenturyArts.csv", index = False)