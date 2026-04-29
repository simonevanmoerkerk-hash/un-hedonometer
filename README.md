# Emotional Tone of UN General Debate Speeches: China (PRC) vs USA (1972–2025)
## Applying the labMT Hedonometer

---

## Research Question

How has the emotional tone of China's (PRC) UN General Debate speeches evolved since joining the United Nations in 1971, and how does that trajectory compare to the United States over the same period(1971-2025)?


## Relevance

The most interesting finding in this project is that China and the USA swap positions around 2000. before that, the USA scored higher, and after that, China does. This lines up with real world events: China joining the WTO, the Beijing Olympics, Xi Jinping coming to power, while the USA was dealing with 9/11, the Iraq War, and growing political divisions.

This matters for Digital Humanities because it raises a question: can we read shifts in global power through language scores? Especially, considering that the labMT tool was built from American English sources like Twitter and the New York Times. And China's speeches were not originally delivered in English. They were spoken in their native language and then translated into English by UN staff. So what we are actually measuring is a translator's English version of Chinese diplomacy, not the original words. That adds another layer of uncertainty: differences in scores between China and the USA might reflect genuine shifts in tone, the tool's Western bias, or simply differences in how UN translators render Chinese into English.

This question matters for Digital Humanities as it uses computational methods to trace how two global power present themselves through language. The UN General Debate is one of the few forums where every country speaks in a comparable format every year. Which makes it the ideal corpus for longitudinal comparison. By applying the labMT hedonometer to 54 years of diplomatic speech, this project asks whether shifts in global power are reflected in change in linguistic tone, and whether a sentiment tool built from American English captures those changes equally for both countries.


## Main Finding

---

## Corpus and Provenance


### Where the data came from
The data comes from the UN General Debate Corpus (UNGDC), created by Baturo, Dasandi, and Mikhaylov (2017) and hosted on Harvard Dataverse. The full corpus contains over 11,000 speeches from 193 countries, covering 1946 to 2025. For this project, only China (CHN) and the USA were kept, starting from 1972, leaving 108 speeches in total: 54 per country.

### UN General Debate Corpus
To test the research question, UN speeches were collected from the UN General Debate Corpus (UNGDC), created by Baturo, Dasandi, and Mikhaylov (2017) and hosted on Harvard Dataverse. The full corpus contains 11,141 speeches from 193 countries, covering 1946 to 2025. For this project, only China (CHN) and the USA were kept, starting from 1972, leaving 108 speeches in total: 54 per country.

### What metadata enables the comparison
The speeches are stored as plain text files, organised by year and country. Each filename follows the format `CHN_26_1971.txt` (country code, session number, year). The metadata that makes this comparison meaningful is the country code and year, which allows tracking each countries tone over the years.

### What the source leaves out
It is worth noting that speeches were originally delivered in the speaker's native language and then translated into English by UN staff. China's speeches were therefore originally in Mandarin. This means we are measuring a translated version of Chinese diplomacy, which is a limitation discussed further in the reflection section.

- Only one speech per country per year,  not all UN activity throughout the year
- Speeches were originally delivered in the speaker's native language and translated into English by UN staff. China's speeches were therefore originally in Mandarin
- The corpus does not include speeches from UN Security Council meetings, committee sessions, or other UN forums

**Source:** https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/0TJX8Y

**Date of access:** April 2026

**How this corpus differs from the first attempt:** The first project used artwork titles from the Metropolitan Museum of Art API. This project uses political UN speeches from a completely different source, domain, and institution. The comparison here is longitudinal (over time) rather than categorical (Eastern vs Western aesthetic concepts).

### Ethics
The corpus contains only official government statements delivered at a public international forum. No personal data or private information is involved. The corpus is publicly available and free to use for research purposes.

 The corpus only includes the annual General Debate speech. not all UN speeches a country makes throughout the year. It also does not capture tone in the original language, only in English translation.

---

## Measurement

### Tokenisation
Each speech was lowercased and split into words using a simple regex pattern (`re.findall(r"[a-z]+"`) that extracts only letter sequences. This removes punctuation, numbers, and special characters automatically. No stopwords were removed — words like "the", "and", "of" are kept because removing them would push scores toward extremes and make comparisons less fair.

### labMT Matching
Each word was looked up in the labMT 1.0 lexicon (Dodds et al., 2011), which contains 10,222 English words rated on a happiness scale from 1 to 9 by workers on Amazon Mechanical Turk. A score of 1 means very negative (like "terrorist" or "death"), 9 means very positive (like "laughter" or "love"), and 5 is neutral. Words that matched were averaged together to produce one happiness score per speech. Words that did not match were ignored.

### Scoring Choices
Each speech receives one happiness score, the average of all matched words. A separate filtered analysis (Figure 2) removes words scoring between 4.0 and 6.0 as a robustness check, keeping only emotionally charged words to see if the pattern holds.

### Coverage and OOV
Coverage measures the proportion of words in a speech that were successfully matched to the labMT lexicon. China's mean coverage is slightly lower than the USA's across all decades (see Figure 5), which suggests that the tool engages with China's diplomatic vocabulary slightly less well.

#### Figure 5 — labMT Coverage by Decade
![Coverage by decade](figures/coverage_by_decade.png)
China (red) consistently has lower coverage than the USA (blue) in every single decade. China's coverage drops in the 2020s to about 0.905, while the USA stays at 0.925. This means more of China's recent speeches contain words the labMT dictionary doesn't recognise.

Additionally, the OOV analysis (see figure 6) reveals something extremely important. China's most frequent missing words are "disarmament", "aggression", "hegemonism", "imperialism". These are not straightforwardly negative in all contexts "disarmament" for example could be framed positively as a peace goal. However, Without 
access to the surrounding context, we cannot be certain how they would score if 
they were in the labMT dictionary. The same applies to the USA where words such as "terrorists", "proliferation", "humanitarian", "democracies" are all missing too, and these would pull the score in different directions depending on how they were rated. The key point is that both countries' final scores are shaped not just by what the tool can read, but also by what it cannot. Any comparison between the two should be read with this in mind.

#### Figure 6 — Out-of-Vocabulary Words
![OOV words](figures/oov_words.png)
China's missing words are "disarmament" (250+ times), "aggression", "hegemonism", "imperialism". The USA's missing words are "terrorists", "proliferation", "humanitarian" and "democracies".


---

## Results and Figures

### Figure 1 — Emotional Tone Over Time
![China vs USA emotional tone](figures/china_vs_usa.png)

### Figure 2 — Emotional Tone with Neutral Words Removed
![China vs USA filtered](figures/china_vs_usa_filtered.png)

### Figure 3 — Bootstrap Statistical Test
![Bootstrap China vs USA](figures/bootstrap_china_usa.png)

### Figure 4 — Average Score by Leadership Era
![Leaders bar chart](figures/china_vs_usa_leaders.png)

---

## Critical Reflection and Limitations

---

## How to Run

---

## Credits and Citation

---

## AI Disclosure