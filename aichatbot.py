import pandas as pd
from translate import trans_to_en
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import joblib

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
df["ts"] = df['Ticket Summary']

df["y"] = df["y2"]

# remove empty y
df = df.loc[(df["y"] != '') & (~df["y"].isna()),]

# 2.Data grouping


# 3.Translation
df["ts_en"] = trans_to_en(df["Ticket Summary"].to_list())

# 4.Deal with noises in data
temp = df
# remove re:
# remove extrac white space
# remove
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
print(temp.shape)
    
#5 Dealing with multi level data
y = temp["y"].to_numpy()
#6 Textual data representation

tfidfconverter = TfidfVectorizer(max_features=2000, min_df=4, max_df=0.90)
x1 = tfidfconverter.fit_transform(temp["Interaction content"]).toarray()
x2 = tfidfconverter.fit_transform(temp["ts_en"]).toarray()
X = np.concatenate((x1, x2), axis=1)

#7 Dealing imbalanced data

# remove bad test cases from test dataset
Test_size = 0.20
y_series = pd.Series(y)
good_y_value = y_series.value_counts()[y_series.value_counts() >= 3].index
y_good = y[y_series.isin(good_y_value)]
X_good = X[y_series.isin(good_y_value)]
y_bad = y[y_series.isin(good_y_value) == False]
X_bad = X[y_series.isin(good_y_value) == False]
test_size = X.shape[0] * 0.2 / X_good.shape[0]
#print(f"new_test_size: {new_test_size}")
X_train, X_test, y_train, y_test = train_test_split(X_good, y_good,     test_size=test_size, random_state=0)
X_train = np.concatenate((X_train, X_bad), axis=0)
y_train = np.concatenate((y_train, y_bad), axis=0)

#8 Decide on whether we want supervised or un-supervised learning: Brainstorming activity
# Thinking: supervised since we want to seperate data into categories (classification)

#9 Data preparation for modelling
y = temp.y.to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#10 Model selection for email classification
classifier = RandomForestClassifier(n_estimators=1000, random_state=0)

#11 Model training, and testing for email classification
forest = classifier.fit(X_train, y_train)

# Save the trained model to a file

''''''
joblib.dump(classifier, "random_forest_model.pkl")

print(forest)

print(classifier.score(X_test, y_test))
print('X_test:', X_test)
# Make predictions
y_pred = classifier.predict(X_test)
print("Predictions: ",  y_pred)
# Print Accuracy
train_accuracy = accuracy_score(y_train, classifier.predict(X_train))
test_accuracy = accuracy_score(y_test, y_pred)
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Feature Importances
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]  # Sorting in descending order

# Print the feature ranking
print("Feature ranking:")
for i in range(X.shape[1]):
    print(f"{i + 1}. Feature {indices[i]} ({importances[indices[i]]:.4f})")

# Visualizing feature importance
plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), indices)
plt.show()
''''''
# Display testing and result

y_pred = classifier.predict(X_test)
p_result = pd.DataFrame(classifier.predict_proba(X_test))
p_result.columns = classifier.classes_
print(p_result)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))