import pandas as pd
from translate import trans_to_en

# Prepare data for the model by translating data and removing noises in data Step 1-4

# 1.Data selection
df = pd.read_csv("AppGallery.csv")

# convert the dtype object to unicode string
df['Interaction content'] = df['Interaction content'].values.astype('U')
df['Ticket Summary'] = df['Ticket Summary'].values.astype('U')
# Optional: rename variable names for remebering easily
df["y1"] = df["Type 1"]
df["y2"] = df["Type 2"]
df["y3"] = df["Type 3"]
df["y4"] = df["Type 4"]
df["x"] = df['Interaction content']
df["y"] = df["y2"]
# remove empty y
df = df.loc[(df["y"] != '') & (~df["y"].isna()),]
# 2.Data grouping

# 3.Translation
df["ts_en"] = trans_to_en(df["Ticket Summary"].to_list())

# 4.Deal with noises in data
temp = df
noise = "(sv\s*:)|(wg\s*:)|(ynt\s*:)|(fw(d)?\s*:)|(r\s*:)|(re\s*:)|(\[|\])|(aspiegel support issue submit)|(null)|(nan)|((bonus place my )?support.pt 自动回复:)"
temp["ts"] = temp["Ticket Summary"].str.lower().replace(noise, " ", regex=True).replace(r'\s+', ' ',
                                                                                        regex=True).str.strip()
temp_debug = temp.loc[:, ["Ticket Summary", "ts", "y"]]

temp["ic"] = temp["Interaction content"].str.lower()
noise_1 = [
    "(from :)|(subject :)|(sent :)|(r\s*:)|(re\s*:)",
    "(january|february|march|april|may|june|july|august|september|october|november|december)",
    "(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
    "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    "\d{2}(:|.)\d{2}",
    "(xxxxx@xxxx\.com)|(\*{5}\([a-z]+\))",
    "dear ((customer)|(user))",
    "dear",
    "(hello)|(hallo)|(hi )|(hi there)",
    "good morning",
    "thank you for your patience ((during (our)? investigation)|(and cooperation))?",
    "thank you for contacting us",
    "thank you for your availability",
    "thank you for providing us this information",
    "thank you for contacting",
    "thank you for reaching us (back)?",
    "thank you for patience",
    "thank you for (your)? reply",
    "thank you for (your)? response",
    "thank you for (your)? cooperation",
    "thank you for providing us with more information",
    "thank you very kindly",
    "thank you( very much)?",
    "i would like to follow up on the case you raised on the date",
    "i will do my very best to assist you"
    "in order to give you the best solution",
    "could you please clarify your request with following information:"
    "in this matter",
    "we hope you(( are)|('re)) doing ((fine)|(well))",
    "i would like to follow up on the case you raised on",
    "we apologize for the inconvenience",
    "sent from my huawei (cell )?phone",
    "original message",
    "customer support team",
    "(aspiegel )?se is a company incorporated under the laws of ireland with its headquarters in dublin, ireland.",
    "(aspiegel )?se is the provider of huawei mobile services to huawei and honor device owners in",
    "canada, australia, new zealand and other countries",
    "\d+",
    "[^0-9a-zA-Z]+",
    "(\s|^).(\s|$)"]
for noise in noise_1:
    print(noise)
    temp["ic"] = temp["ic"].replace(noise, " ", regex=True)
temp["ic"] = temp["ic"].replace(r'\s+', ' ', regex=True).str.strip()
temp_debug = temp.loc[:, ["Interaction content", "ic", "y"]]

print(temp.y1.value_counts())
good_y1 = temp.y1.value_counts()[temp.y1.value_counts() > 10].index
temp = temp.loc[temp.y1.isin(good_y1)]

# Save to csv
temp.to_csv("AppGallery_done.csv", index=False)