import json
import random
import os
import sys
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_api_key():
    """Get the API key from environment variables or exit if not found."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key like this:")
        print("ANTHROPIC_API_KEY=your_api_key_here")
        sys.exit(1)
    return api_key

def load_vocabulary():
    """Load the vocabulary from the JSON file."""
    try:
        with open('japanese_vocabulary.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: japanese_vocabulary.json not found.")
        print("Please run anki_db_connector.py first to generate the vocabulary file.")
        sys.exit(1)

def save_content(content, content_type, filename="generated_sentences.txt"):
    """Save the generated content to a file with nice formatting."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the entry
    entry = f"""
{'='*80}
Generated on: {timestamp}
Type: {content_type}

Generated content:
{'-'*40}
{content}
{'='*80}
"""
    
    # Append to file
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    return filename

def generate_sentence(vocabulary):
    """Generate a sentence using Claude API."""
    try:
        # Initialize Claude client with explicit API key
        client = Anthropic(api_key=get_api_key())
        
        # Create a prompt that describes the task
        word_list = "\n".join([f"- {word['kanji']} ({word['reading']}): {word['meaning']}" + (f" [{word['particle']}]" if word.get('particle') else "") for word in vocabulary])
        
        prompt = f"""You are a Japanese language expert. Create a natural Japanese sentence using words from the following vocabulary list.
The sentence should be:
1. Grammatically correct
2. Natural and commonly used
3. Use 2-3 words from the provided vocabulary
4. Be at an appropriate level for someone learning Japanese
5. ONLY use words from the provided vocabulary list

Available vocabulary:
{word_list}

Please provide:
1. The sentence in Japanese (with furigana)
2. The sentence in romaji
3. The English translation
4. A brief explanation of the grammar points used
5. A list of which words from the vocabulary were used

Format your response like this:
Japanese: [sentence with furigana]
Romaji: [romaji version]
English: [translation]
Grammar: [explanation]
Words used: [list of words used]"""

        # Get response from Claude using Haiku model
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.7,
            system="You are a helpful Japanese language teacher who creates natural, grammatically correct sentences using only the provided vocabulary.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.content[0].text
    except Exception as e:
        print(f"Error generating sentence: {str(e)}")
        sys.exit(1)

def generate_story(vocabulary):
    """Generate a short story using Claude API."""
    try:
        # Initialize Claude client with explicit API key
        client = Anthropic(api_key=get_api_key())
        
        # Create a prompt that describes the task
        word_list = "\n".join([f"- {word['kanji']} ({word['reading']}): {word['meaning']}" + (f" [{word['particle']}]" if word.get('particle') else "") for word in vocabulary])
        
        prompt = f"""You are a Japanese language expert. Create a short story (2-3 paragraphs) using words from the following vocabulary list.
The story should be:
1. Grammatically correct
2. Natural and commonly used
3. Be around 2-3 paragraphs
4. Be at an appropriate level for someone learning Japanese
5. Have a clear beginning, middle, and end
6. Be interesting and engaging
7. Use a variety of grammar structures
8. Include dialogue when appropriate
9. ONLY use words from the provided vocabulary list

Available vocabulary:
{word_list}

Please provide:
1. The story in Japanese (with furigana)
2. The story in romaji
3. The English translation
4. A brief explanation of the grammar points used
5. A list of which words from the vocabulary were used

Format your response like this:
Japanese: [story with furigana]
Romaji: [romaji version]
English: [translation]
Genki Lesson: [lesson numbers from Genki Japanese textbook]
"""

        # Get response from Claude using Haiku model
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=3000,
            temperature=0.8,
            system="You are a helpful Japanese language teacher who creates natural, grammatically correct stories using only the provided vocabulary. And using grammer patterns founnd in the Genki Japanese learning textbookss.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.content[0].text
    except Exception as e:
        print(f"Error generating story: {str(e)}")
        sys.exit(1)

def main():
    # Load vocabulary
    vocabulary = load_vocabulary()
    print(f"Loaded {len(vocabulary)} vocabulary items")
    
    # Get user input for content type
    print("\nChoose content type:")
    print("1. Single sentence")
    print("2. Short story")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        # Generate sentence
        print("\nGenerating sentence...")
        content = generate_sentence(vocabulary)
        content_type = "Sentence"
    elif choice == "2":
        # Generate story
        print("\nGenerating story...")
        content = generate_story(vocabulary)
        content_type = "Story"
    else:
        print("Invalid choice. Please run the script again and choose 1 or 2.")
        sys.exit(1)
    
    print(f"\nGenerated {content_type.lower()}:")
    print(content)
    
    # Save to file
    filename = save_content(content, content_type)
    print(f"\nContent saved to {filename}")

if __name__ == "__main__":
    main() 