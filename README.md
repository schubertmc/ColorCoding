# 🎨 ColorCoding 🌈
ColorCoding - Anki Add-on 

Improve your learning strategy with the ColorCoding add-on. This tool allows you to set specific font colors for different terms and automatically colors these preset words when editing cards. Consistently color-coding your Anki cards can effectively enhance memory retention.

<img src="https://raw.githubusercontent.com/schubertmc/ColorCoding/main/src/example/example_3.gif" width="800" />

## Installation
Please follow the instructions on the [anki web page](https://ankiweb.net/shared/info/2113325087). 

## How to use ColorCoding

### 1. Settings 
Within Anki, open “Tools” -> “Color Coding…” to set up word-color pairs.


<img src="https://raw.githubusercontent.com/schubertmc/ColorCoding/main/src/example/example_4.gif" width="400" />
Make sure there are no empty spaces in your word definitions.

Alternatively, you can manually provide data in JSON format, e.g., 
```
[{"word": "penicillin", "group": "", "color": "red"}, 
{"word": "doxycycline", "group": "", "color": "green"},
...
].
```
via “Tools” -> “Color Coding…” -> "Modify Manually".

### 2. Coloring
Once you want to color your words, press the ColorCoding button. This automatically colors all defined words in the field that is currently being edited.

All available HTML color names and HEX color codes can be used. One color can be set for as many words as you want, allowing specific font colors to be used for either a single term or an entire group of words.

Preset words will automatically be colored while typing within the Add window.

## Updates
- 2024-08-24 Improved functionality, with great support from [FelixKohlhas](https://github.com/FelixKohlhas).
- 2022-02-02 Initial Release Color Coding

## Datasets 
Preset datasets for color group word pairs are currently available for German and English medication lists.

### Accessing the Preset Datasets
1. **English Medication List**: [here](https://github.com/schubertmc/ColorCoding/blob/main/src/example/medication_list_english_v2.json)
2. **German Medication List**: [here](https://github.com/schubertmc/ColorCoding/blob/main/src/example/medication_list_german_v2.json)

These can then be manually inserted into the addon via “Tools” -> “Color Coding…” -> "Modify Manually". 

## Help and Support
This add-on is still under development.
Please report any bug reports or feature requests.


## Contact
[schubertmc](https://github.com/schubertmc) 

<br>
2022 - 2024
