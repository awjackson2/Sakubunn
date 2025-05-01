# Japanese Sentence and Story Generator

This project helps Japanese language learners practice by generating natural sentences and short stories using vocabulary from their Anki flashcards. It uses the Claude 3 Haiku model to create contextually appropriate content.

## Prerequisites

- Python 3.x
- Anki (with Japanese vocabulary deck)
- Anthropic API key for Claude 3

## Setup

1. Install required Python packages:
```bash
pip install anthropic python-dotenv
```

2. Create a `.env` file in the project directory with your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

3. Update the Anki database path in `anki_db_connector.py`:
```python
# Update this path to match your Anki profile
anki_path = os.path.expanduser("~/.local/share/Anki2/aksel/collection.anki2")
```
Note: The path format varies by operating system:
- Windows: `C:\Users\YourUsername\AppData\Roaming\Anki2\YourProfile\collection.anki2`
- macOS: `~/Library/Application Support/Anki2/YourProfile/collection.anki2`
- Linux: `~/.local/share/Anki2/YourProfile/collection.anki2`

4. Update the deck name in `anki_db_connector.py` if needed:
```python
deck_name = "Genki"  # Change this to your deck name
```

## Usage

1. First, generate your vocabulary JSON file:
```bash
python anki_db_connector.py
```
This will create `japanese_vocabulary.json` containing your Anki vocabulary.

2. Run the sentence/story generator:
```bash
python sentence_generator.py
```

3. Choose between:
   - Single sentence generation
   - Short story generation (2-3 paragraphs)

The generated content will be saved to `generated_sentences.txt` with:
- Japanese text (with furigana)
- Romaji
- English translation
- Genki lesson references
- Timestamp

## Features

- Uses vocabulary from your Anki flashcards
- Generates natural, grammatically correct content
- Includes furigana for kanji
- Provides romaji and English translations
- References Genki textbook lessons
- Saves all generated content for later review

## Notes

- The script only uses vocabulary from cards that have been reviewed at least 3 times
- The model uses grammar patterns from the Genki textbook series
- Stories are designed to be 2-3 paragraphs long
- All content is generated using only vocabulary from your Anki deck 