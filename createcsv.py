import pandas as pd

# Sample data for two random speeches
data = {
    "Speech ID": [1, 2],
    "Date": ["2023-01-01", "2023-02-01"],
    "Speaker": ["Speaker A", "Speaker B"],
    "Position": ["President", "Defense Minister"],
    "Title": ["Title A", "Title B"],
    "Location": ["Beijing", "Shanghai"],
    "Context": ["National Congress", "International Conference"],
    "Full Text": [
        "Today, we gather to celebrate the strength and unity of our nation. Our nuclear advancements are a testament to our commitment to national security and global peace.",
        "In the face of international challenges, our defense capabilities must remain robust. Our nuclear strategy is central to ensuring our sovereignty and protecting our interests."
    ],
    "Keywords": ["strength, unity, nuclear advancements", "defense capabilities, nuclear strategy, sovereignty"],
    "Sentiment Score": [0.8, 0.5],
    "Topic": ["Nationalism", "Nuclear Policy"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('speeches_dataset.csv', index=False)

print("CSV file 'speeches_dataset.csv' created successfully.")

