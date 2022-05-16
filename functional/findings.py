import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from . import map_color


def analyze_most_different(most_different, male_unique, feature=False):
    x = list(most_different.keys())

    if feature:
        x[x.index('are  be')] = 'are & be'
        x[x.index('zomerhits 20102020')] = 'zomerhits 2010-2020'

    y = list(most_different.values())

    # Map colors according to which user received the playlist
    c = map_color(male_unique, most_different)

    plt.figure(figsize=[12.0, 10.0])

    plt.ylim(-0.5, 19.5)

    plt.barh(x, y, height=0.8, color=c, label=['blue','red'])
    plt.grid()

    plt.gca().invert_yaxis()

    plt.title('Top 20 playlists only one user received in recommendations')
    plt.xlabel('Count')
    plt.ylabel('Playlist Name')

    plt.legend(['male', 'female'])
    plt.tight_layout()

    plt.savefig('data/topuniqueplaylist.jpg')