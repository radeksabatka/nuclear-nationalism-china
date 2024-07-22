#This is a main python code used to an analysis on Nuclear Expansion using China as a case study

import os
import jieba
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# paths to local files
stopwords_path = '/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/nuclear-nationalism-china/stopwords.txt'
speeches_folder_path = '/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/nuclear-nationalism-china/data/texts'
# '/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/outputs/correlation_matrix.png

# Define keywords for each theme in Chinese
keywords = {
    "nationalism": ["国家", "爱国", "祖国", "民族自豪感"],
    "credible_deterrence": ["威慑", "威胁", "防御", "报复"],
    "prestige": ["声望", "地位", "名誉", "荣誉"],
    "military_complex": ["军事", "军队", "国防工业", "武器"]
}

# Load stopwords from file
def load_stopwords(filepath):
    stop_words = set()
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            stop_words.add(line.strip())
    return stop_words

# Load stopwords from the specified file
stop_words = load_stopwords(stopwords_path)

# Function to preprocess the text using jieba
def preprocess_text(text):
    # Tokenize text using jieba
    words = jieba.lcut(text)
    # Filter out stopwords, spaces, and punctuation
    filtered_words = [word for word in words if word not in stop_words and word.strip() and word not in "，。！？；：“”‘’（）【】《》、"]
    return ' '.join(filtered_words)

# Load texts from the folder
def load_texts(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                texts.append(file.read())
    return texts

# Load texts from the specified folder
texts = load_texts(speeches_folder_path)

# Convert to a DataFrame for convenience
df = pd.DataFrame(texts, columns=['text'])

# Apply preprocessing to all texts
df['preprocessed_text'] = df['text'].apply(preprocess_text)

# Calculate term frequencies
vectorizer = CountVectorizer(vocabulary=[word for sublist in keywords.values() for word in sublist])
X = vectorizer.fit_transform(df['preprocessed_text'])
frequencies = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Sum frequencies for each theme
theme_frequencies = {theme: frequencies[keywords].sum(axis=1) for theme, keywords in keywords.items()}
theme_frequencies_df = pd.DataFrame(theme_frequencies)

# Display the frequency table
print(theme_frequencies_df)

# Calculate the correlation matrix and p-values
correlation_matrix = theme_frequencies_df.corr()
p_values = pd.DataFrame(index=correlation_matrix.index, columns=correlation_matrix.columns)

for row in correlation_matrix.columns:
    for col in correlation_matrix.columns:
        corr, p_val = pearsonr(theme_frequencies_df[row], theme_frequencies_df[col])
        p_values.loc[row, col] = p_val

# Plot the heatmap of the correlation matrix and save it as a PNG file
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix of Themes')
plt.savefig('/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/outputs/correlation_matrix.png')  # Save the heatmap as a PNG file
plt.show()

# Display the correlation matrix and p-values
print("Correlation Matrix:")
print(correlation_matrix)
print("\nP-Values:")
print(p_values)

# Calculate basic statistics
basic_stats = theme_frequencies_df.describe().transpose()

# Save the correlation matrix, p-values, and basic statistics to an Excel file
excel_path = '/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/outputs/correlation_matrix.xlsx'

with pd.ExcelWriter(excel_path) as writer:
    correlation_matrix.to_excel(writer, sheet_name='Correlation Matrix')
    p_values.to_excel(writer, sheet_name='P-Values')
    basic_stats.to_excel(writer, sheet_name='Basic Stats')

print(f'Correlation matrix, p-values, and basic statistics saved to {excel_path}')