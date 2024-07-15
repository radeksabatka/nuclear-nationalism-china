#This is a python script to create WordCloud for the main.py code
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def generate_wordcloud(word_counts, font_path, output_image_path=None):
    # Function to generate colors for word cloud
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl({}, 100%, 50%)".format(random_state.randint(0, 360))

    # Generate a word cloud
    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white', prefer_horizontal=1.0,
                          color_func=color_func, max_words=100).generate_from_frequencies(word_counts)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    if output_image_path:
        plt.savefig(output_image_path, format='png')
    else:
        plt.show()