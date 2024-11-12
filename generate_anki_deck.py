
import genanki
import random
import os

language = "vi"

path = language + "_audio"

# Sample list of lists with front and back for each card
lines = []
with open(language + ".md", "r") as f:
    for line in f.readlines():
        lines.append(line.strip().split(" -> "))

assert all(len(l) == 2 for l in lines), "number of fields must be 2 for each word"

# ==================================================================================================
# generate audio
# ==================================================================================================
from gtts import gTTS

if not os.path.exists(path):
    os.makedirs(path)

for line in lines:
    file_path = os.path.join(path, line[0] + '.mp3')
    if not os.path.exists(file_path):
        tt = line[1].split(" [")[0]
        tts = gTTS(tt, lang=language)
        tts.save(file_path)

# ==================================================================================================
# generate deck with audio
# ==================================================================================================
# unique model and deck ID generation (ensure IDs are consistent across script runs)
model_id = random.randrange(1 << 30, 1 << 31)
deck_id  = random.randrange(1 << 30, 1 << 31)

# create the model
model = genanki.Model(
    model_id,
    'Language Learning with Audio',
    fields=[
        {'name': 'English'},
        {'name': 'Foreign'},
        {'name': 'Audio'},
    ],
    templates=[
        {
            'name': 'English -> Foreign',
            'qfmt': '{{English}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Foreign}}<br>{{Audio}}',
        },
        {
            'name': 'Foreign -> English',
            'qfmt': '{{Foreign}}<br>{{Audio}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{English}}',
        },
    ],
    css="""
    .card {
      font-family: arial;
      font-size: 20px;
      text-align: center;
      color: black;
      background-color: white;
    }
    """
)

# create the deck
deck = genanki.Deck(deck_id, language)

for line in lines:
    line[1] = line[1].replace(" [", "<br>[")

# add cards to the deck
for english, foreign in lines:
    note = genanki.Note(
        model=model,
        fields=[english, foreign, f"[sound:{english}.mp3]"]
    )
    deck.add_note(note)

# create a package
package = genanki.Package(deck)

# add media files (audio files) to the package
media_files = [os.path.join(path, english) + ".mp3" for english, _ in lines]
package.media_files = media_files

# save the deck
package.write_to_file(language + '.apkg')

