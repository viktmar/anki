
from googletrans import Translator

# list of all available languages here:
# https://cloud.google.com/translate/docs/languages

# language = "vi"
language = "ja"
# language = "th"

# load words from file
lines = []
with open("important_words.md", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if len(line) > 0:
            lines.append(line)

# translate
translator = Translator()
translated = translator.translate(lines, src="en", dest=language)

# extract translations, pronunciation information if available, and put them together
translated_text = []
for t in translated:
    if t.pronunciation is None or t.pronunciation == t.origin:
        tt = t.text
    else:
        tt = t.text + "   [ " + t.pronunciation + " ]"
    translated_text.append([t.origin, tt])

# create a string
str = "\n".join([" -> ".join(i) for i in translated_text])

# save the string to a file
with open(language + ".md", "w") as f:
    f.write(str)

