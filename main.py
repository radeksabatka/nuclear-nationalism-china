import os
import jieba
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import seaborn as sns
from wordcloud_generator import generate_wordcloud  # Import the wordcloud function

# Load stopwords from file
def load_stopwords(filepath):
    stop_words = set()
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            stop_words.add(line.strip())
    return stop_words

# Specify the path to your stopwords file
stopwords_path = '/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/nuclear-nationalism-china/stopwords.txt'

# Load stopwords from the specified file
stop_words = load_stopwords(stopwords_path)

# Function to preprocess the text using jieba
def preprocess_text(text):
    # Tokenize text using jieba
    words = jieba.lcut(text)
    # Filter out stopwords, spaces, and punctuation
    filtered_words = [word for word in words if word not in stop_words and word.strip() and word not in "，。！？；：“”‘’（）【】《》、"]
    return filtered_words

# Load texts from the folder
def load_texts(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                texts.append(file.read())
    return texts

# Specify the path to your speeches folder
speeches_folder_path = '/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/nuclear-nationalism-china/data/texts'

# Load texts from the specified folder
texts = load_texts(speeches_folder_path)

# Convert to a DataFrame for convenience
df = pd.DataFrame(texts, columns=['text'])

# Apply preprocessing to all texts
df['preprocessed_text'] = df['text'].apply(preprocess_text)

# Combine all preprocessed texts into one list
all_words = [word for text in df['preprocessed_text'] for word in text]

# Create a frequency distribution
word_counts = Counter(all_words)

# Remove empty strings from the word counts
if '' in word_counts:
    del word_counts['']

# Convert to DataFrame for easier handling
word_freq_df = pd.DataFrame(word_counts.items(), columns=['word', 'count']).sort_values(by='count', ascending=False)

# Display the top 30 most common words
print(word_freq_df.head(30))

# Set the font properties for matplotlib to display Chinese characters
font_path = '/Users/radeksabatka/Library/Fonts/simsun.ttf'  # Use the full absolute path

# Create a font properties object
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = ['SimSun']  # Use the name of the font
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is rendered correctly

# Plot the 30 most common words
plt.figure(figsize=(12, 8))
sns.barplot(x='count', y='word', data=word_freq_df.head(30))
plt.xlabel('Frequency', fontproperties=prop)
plt.ylabel('Words', fontproperties=prop)
plt.title('Top 30 Most Common Words', fontproperties=prop)
plt.xticks(fontproperties=prop)
plt.yticks(fontproperties=prop)
plt.show()

# Call the generate_wordcloud function
generate_wordcloud(word_counts, font_path, output_image_path='/Users/radeksabatka/Library/Mobile Documents/com~apple~CloudDocs/Academics/IR499 Dissertation/Python/outputs/wordcloud.png')