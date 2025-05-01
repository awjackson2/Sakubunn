import sqlite3
import os
import json
import pandas as pd
import re

# Path to your Anki collection - update with your actual path
# Windows: C:\Users\YourUsername\AppData\Roaming\Anki2\YourProfile\collection.anki2
# macOS: ~/Library/Application Support/Anki2/YourProfile/collection.anki2
# Linux: ~/.local/share/Anki2/YourProfile/collection.anki2
anki_path = os.path.expanduser("~/.local/share/Anki2/aksel/collection.anki2")

def clean_text(text):
    """Clean text by removing HTML tags and normalizing whitespace."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def process_meaning(meaning):
    """Process the meaning field to separate main meaning and particle information."""
    # Split on <small> to separate main meaning from particle info
    parts = meaning.split('<small>')
    main_meaning = clean_text(parts[0])
    
    particle = None
    if len(parts) > 1:
        # Extract particle information if present
        particle_match = re.search(r'\((.*?)\)', parts[1])
        if particle_match:
            particle = clean_text(particle_match.group(1))
    
    return main_meaning, particle

try:
    # Connect to the database
    conn = sqlite3.connect(anki_path)
    cursor = conn.cursor()

    # List all available tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Query to extract notes from a specific Japanese deck
    deck_name = "Genki"  

    # Get the deck ID
    cursor.execute("SELECT id, name FROM decks")
    deck_id = None
    for deck in cursor.fetchall():
        if deck[1].lower() == deck_name.lower():
            deck_id = deck[0]
            break

    if deck_id:
        print(f"\nFound deck '{deck_name}' with ID: {deck_id}")
        
        # Get card IDs from this deck that have been reviewed at least 3 times
        cursor.execute("SELECT id FROM cards WHERE did = ? AND reps >= 3", (deck_id,))
        card_ids = [row[0] for row in cursor.fetchall()]
        
        # Get notes for these cards
        vocabulary_data = []
        for card_id in card_ids:
            cursor.execute("SELECT nid FROM cards WHERE id = ?", (card_id,))
            note_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT flds FROM notes WHERE id = ?", (note_id,))
            fields = cursor.fetchone()[0].split('\x1f')  # Fields are separated by \x1f character
            
            if len(fields) >= 2:
                # Extract kanji and reading from the ruby format
                ruby_text = fields[0]
                meaning = fields[1]
                
                # Extract kanji and reading using regex
                kanji_match = re.search(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>', ruby_text)
                if kanji_match:
                    kanji = clean_text(kanji_match.group(1))
                    reading = clean_text(kanji_match.group(2))
                    
                    # Process the meaning field
                    main_meaning, particle = process_meaning(meaning)
                    
                    vocabulary_data.append({
                        'kanji': kanji,
                        'reading': reading,
                        'meaning': main_meaning,
                        'particle': particle
                    })

        # Save as JSON for later use with AI sentence generation
        with open('japanese_vocabulary.json', 'w', encoding='utf-8') as f:
            json.dump(vocabulary_data, f, ensure_ascii=False, indent=4)
        
        print(f"Extracted {len(vocabulary_data)} vocabulary items (cards reviewed 3+ times)")
    else:
        print(f"\nDeck '{deck_name}' not found. Please check the list of available decks above and update the deck_name variable with the correct name.")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
