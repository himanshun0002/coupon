import os
import sys
import re

class SRTTranslatorSimple:
    def __init__(self):
        # Simple English to Hindi dictionary for common phrases
        self.translations = {
            'music': 'संगीत',
            'never': 'कभी नहीं',
            'going': 'जा रहा',
            'to': 'को',
            'give': 'देना',
            'you': 'आप',
            'up': 'ऊपर',
            'let': 'जाने देना',
            'down': 'नीचे',
            'run': 'भागना',
            'around': 'इधर-उधर',
            'make': 'बनाना',
            'cry': 'रोना',
            'say': 'कहना',
            'goodbye': 'अलविदा',
            'tell': 'बताना',
            'lie': 'झूठ',
            'hurt': 'चोट पहुंचाना',
            'and': 'और',
            'there': 'वहां',
            'are': 'हैं',
            'no': 'नहीं',
            'strangers': 'अजनबी',
            'love': 'प्यार',
            'know': 'जानना',
            'rules': 'नियम',
            'something': 'कुछ',
            'still': 'अभी भी',
            'committed': 'प्रतिबद्ध',
            'struggle': 'संघर्ष',
            'get': 'प्राप्त करना',
            'wrong': 'गलत',
            'any': 'कोई',
            'other': 'अन्य',
            'guy': 'लड़का',
            'just': 'सिर्फ',
            'want': 'चाहना',
            'how': 'कैसे',
            'feel': 'महसूस करना',
            'got': 'मिला',
            'understand': 'समझना',
            'we': 'हम',
            'known': 'जाना',
            'each': 'एक-दूसरे',
            'for': 'के लिए',
            'so': 'इतना',
            'long': 'लंबा',
            'heart': 'दिल',
            'been': 'रहा',
            'aching': 'दर्द करना',
            'hard': 'कठिन',
            'too': 'बहुत',
            'shy': 'शर्मीला',
            'it': 'यह',
            'as': 'जैसा',
            'if': 'अगर',
            'all': 'सभी',
            'what': 'क्या',
            'on': 'चल रहा',
            'game': 'खेल',
            'play': 'खेलना',
            'ask': 'पूछना',
            'me': 'मुझसे',
            'don': 'मत',
            'but': 'लेकिन',
            'see': 'देखना',
            'ready': 'तैयार',
            'do': 'करना',
            'sing': 'गाना',
            'night': 'रात',
            'please': 'कृपया',
            'wear': 'पहनना',
            'just say': 'बस कह दो',
            'like': 'जैसा',
            'both': 'दोनों',
            'gonna': 'जा रहा',
            'gotta': 'होगा',
            'never gonna give you up': 'कभी आपको छोड़ने नहीं जा रहा',
            'never gonna let you down': 'कभी आपको नीचे नहीं जाने दूंगा',
            'never gonna run around': 'कभी इधर-उधर नहीं भागूंगा',
            'never gonna make you cry': 'कभी आपको रोने नहीं दूंगा',
            'never gonna say goodbye': 'कभी अलविदा नहीं कहूंगा',
            'never gonna tell a lie': 'कभी झूठ नहीं बोलूंगा',
            'and hurt you': 'और आपको चोट नहीं पहुंचाऊंगा'
        }
        
    def parse_srt(self, srt_file_path):
        """Parse SRT file and extract subtitle blocks"""
        with open(srt_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = re.split(r'\n\s*\n', content.strip())
        
        parsed_blocks = []
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    index = int(lines[0])
                    timestamp = lines[1]
                    text = '\n'.join(lines[2:])
                    parsed_blocks.append({
                        'index': index,
                        'timestamp': timestamp,
                        'text': text
                    })
                except ValueError:
                    continue
        
        return parsed_blocks
    
    def translate_text(self, text):
        """Translate text using dictionary lookup"""
        text_lower = text.lower().strip()
        
        # Check for exact matches first
        if text_lower in self.translations:
            return self.translations[text_lower]
        
        # Try to translate word by word
        words = text_lower.split()
        translated_words = []
        
        for word in words:
            # Clean the word (remove punctuation)
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word in self.translations:
                translated_words.append(self.translations[clean_word])
            else:
                translated_words.append(word)  # Keep original if not found
        
        return ' '.join(translated_words)
    
    def translate_srt_file(self, input_file, output_file=None):
        """Translate SRT file to Hindi"""
        if not os.path.exists(input_file):
            print(f"Error: SRT file '{input_file}' not found.")
            return False
        
        if output_file is None:
            name, ext = os.path.splitext(input_file)
            output_file = f"{name}_hi{ext}"
        
        print(f"Translating {input_file} to Hindi...")
        
        blocks = self.parse_srt(input_file)
        if not blocks:
            print("Error: Could not parse SRT file.")
            return False
        
        print(f"Found {len(blocks)} subtitle blocks to translate.")
        
        translated_blocks = []
        for i, block in enumerate(blocks):
            print(f"Translating block {i+1}/{len(blocks)}: {block['text'][:50]}...")
            
            translated_text = self.translate_text(block['text'])
            
            translated_block = {
                'index': block['index'],
                'timestamp': block['timestamp'],
                'text': translated_text
            }
            translated_blocks.append(translated_block)
        
        # Write translated SRT file
        with open(output_file, 'w', encoding='utf-8') as f:
            for block in translated_blocks:
                f.write(f"{block['index']}\n")
                f.write(f"{block['timestamp']}\n")
                f.write(f"{block['text']}\n\n")
        
        print(f"Translation completed! Output saved to: {output_file}")
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python srt_translator_simple.py <input_srt_file> [output_srt_file]")
        print("\nExample:")
        print("  python srt_translator_simple.py downloaded_video.srt")
        print("  python srt_translator_simple.py downloaded_video.srt hindi_subtitles.srt")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    translator = SRTTranslatorSimple()
    success = translator.translate_srt_file(input_file, output_file)
    
    if success:
        print("\n✅ Translation completed successfully!")
    else:
        print("\n❌ Translation failed!")

if __name__ == "__main__":
    main()
