import pandas as pd

# Load the CSV file
df = pd.read_csv('speeches_dataset.csv')

# Function to generate bibliography entry in Chicago style
def generate_bibliography(row):
    speaker = row['Speaker']
    title_chinese = row['Title (Chinese)']
    title_english = row['Title (English)']
    date = row['Date']
    location = row['Location']
    context = row['Context']
    source = row['Source']
    bibliography_entry = f"{speaker}. \"{title_chinese}\" [{title_english}]. Speech delivered at the {context}, {location}, {date}. {source}."
    return bibliography_entry

# Apply the function to each row and store the results
df['Bibliography Entry'] = df.apply(generate_bibliography, axis=1)

# Display the bibliography entries
for entry in df['Bibliography Entry']:
    print(entry)

# Save the bibliography entries to a text file
with open('bibliography.txt', 'w', encoding='utf-8') as f:
    for entry in df['Bibliography Entry']:
        f.write(entry + '\n')

print("Bibliography saved to 'bibliography.txt'.")