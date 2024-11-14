
import os
from gtts import gTTS

# set the language code of the desired language
# list of all available languages here:
# https://cloud.google.com/translate/docs/languages
language = "vi"

path = language + "_audio"

# Sample list of lists with front and back for each card
lines = []
with open(language + ".md", "r") as f:
    for line in f.readlines():
        lines.append(line.strip().split(" -> "))

assert all(len(l) == 2 for l in lines), "number of fields must be 2 for each word"

# if folder does not exists, create it
if not os.path.exists(path):
    os.makedirs(path)

# if audio file does not exists, generate it
for line in lines:
    file_path = os.path.join(path, line[0] + '.mp3')
    if not os.path.exists(file_path):
        tt = line[1].split(" [")[0]
        tts = gTTS(tt, lang=language)
        tts.save(file_path)
