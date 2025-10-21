import random
import string
from tkinter import Y

class WordGuessGame:
    def __init__(self):
        self.word_list = {
            'easy': ['cat', 'dog', 'sun', 'moon', 'star', 'tree', 'bird', 'fish', 'book', 'hand'],
            'medium': ['python', 'computer', 'keyboard', 'elephant', 'mountain', 'butterfly', 'adventure', 'chocolate', 'rainbow', 'sunshine'],
            'hard': ['xylophone', 'rhinoceros', 'encyclopedia', 'magnificent', 'extraordinary', 'pharmaceutical', 'metamorphosis', 'psychology', 'bureaucracy', 'sophisticated']
        }
        self.difficulty = 'medium'
        self.secret_word = ''
        self.guessed_letters = set()
        self.correct_letters = set()
        self.attempts_left = 6
        self.game_over = False
        self.won = False
    
    def select_word(self):
        """Select a random word based on difficulty level"""
        self.secret_word = random.choice(self.word_list[self.difficulty]).lower()
        self.correct_letters = set(self.secret_word)
    
    def display_word(self):
        """Display the word with guessed letters revealed"""
        display = []
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append('_')
        return ' '.join(display)
    
    def display_flower(self):
        """Display flower drawing based on attempts left"""
        flower_parts = [
            "     🌱",      # Seed
            "     🌿",      # Small sprout
            "    🌿🌿",     # Growing stems
            "   🌿🌿🌿",    # More stems
            "  🌿🌿🌿🌿",   # Full stems
            " 🌸🌿🌿🌿🌿",  # One flower
            "🌸🌸🌿🌿🌿🌿", # Two flowers
            "🌸🌸🌸🌿🌿🌿🌿" # Full bloom
        ]
        
        parts_to_show = 8 - self.attempts_left
        print("  Your flower garden:")
        for i in range(min(parts_to_show, len(flower_parts))):
            print(flower_parts[i])
        
        # Show remaining potential growth
        if parts_to_show < len(flower_parts):
            print("  🌱🌱🌱🌱🌱🌱🌱🌱 (Keep guessing to help it grow!)")
        
        # Add soil line
        print("  ▓▓▓▓▓▓▓▓▓▓▓▓ (soil)")
    
    def make_guess(self, guess):
        """Process a letter guess"""
        if len(guess) != 1 or not guess.isalpha():
            return False, "Please enter a single letter."
        
        guess = guess.lower()
        
        if guess in self.guessed_letters:
            return False, "You've already guessed that letter!"
        
        self.guessed_letters.add(guess)
        
        if guess in self.correct_letters:
            return True, "Correct guess!"
        else:
            self.attempts_left -= 1
            return True, "Incorrect guess!"
    
    def check_game_status(self):
        """Check if game is won or lost"""
        if self.attempts_left <= 0:
            self.game_over = True
            self.won = False
            return "lost"
        
        if all(letter in self.guessed_letters for letter in self.secret_word):
            self.game_over = True
            self.won = True
            return "won"
        
        return "playing"
    
    def set_difficulty(self, difficulty):
        """Set game difficulty"""
        if difficulty in self.word_list:
            self.difficulty = difficulty
            return True
        return False
    
    def reset_game(self):
        """Reset game to initial state"""
        self.guessed_letters = set()
        self.correct_letters = set()
        self.attempts_left = 6
        self.game_over = False
        self.won = False
        self.select_word()
    
    def show_stats(self):
        """Display game statistics"""
        print(f"\n=== Game Statistics ===")
        print(f"Difficulty: {self.difficulty.capitalize()}")
        print(f"Word length: {len(self.secret_word)} letters")
        print(f"Attempts left: {self.attempts_left}")
        print(f"Letters guessed: {', '.join(sorted(self.guessed_letters)) if self.guessed_letters else 'None'}")
        print(f"Word: {self.display_word()}")

def main():
    game = WordGuessGame()
    
    print("🎯 Welcome to the Word Guessing Game! 🎯")
    print("=" * 50)
    
    # Difficulty selection
    while True:
        print("\nChoose difficulty:")
        print("1. Easy (3-4 letters)")
        print("2. Medium (6-8 letters)")
        print("3. Hard (9+ letters)")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            game.set_difficulty('easy')
            break
        elif choice == '2':
            game.set_difficulty('medium')
            break
        elif choice == '3':
            game.set_difficulty('hard')
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    game.select_word()
    
    print(f"\n🎮 Game started! Difficulty: {game.difficulty.capitalize()}")
    print("Try to guess the word letter by letter!")
    print("Each wrong guess helps your flower grow! 🌸")
    print("You have 6 attempts to guess the word.")
    
    while not game.game_over:
        print("\n" + "=" * 30)
        game.display_flower()
        print(f"\nWord: {game.display_word()}")
        print(f"Attempts left: {game.attempts_left}")
        
        if game.guessed_letters:
            print(f"Guessed letters: {', '.join(sorted(game.guessed_letters))}")
        
        guess = input("\nEnter a letter: ").strip()
        
        if guess.lower() == 'quit':
            print("Thanks for playing! Goodbye!")
            return
        elif guess.lower() == 'hint':
            # Give a hint (first letter)
            if len(game.guessed_letters) >= 2:  # Only after 2 guesses
                hint_letter = game.secret_word[0]
                if hint_letter not in game.guessed_letters:
                    game.guessed_letters.add(hint_letter)
                    print(f"💡 Hint: The word starts with '{hint_letter}'")
                else:
                    print("💡 You already know the first letter!")
            else:
                print("💡 You need to make at least 2 guesses before getting a hint!")
            continue
        
        success, message = game.make_guess(guess)
        print(f"\n{message}")
        
        status = game.check_game_status()
        
        if status == "won":
            print("\n🎉 Congratulations! You won! 🎉")
            print(f"The word was: {game.secret_word.upper()}")
            print("You're a word-guessing champion!")
            break
        elif status == "lost":
            print("\n💀 Game Over! You lost! 💀")
            print(f"The word was: {game.secret_word.upper()}")
            print("Better luck next time!")
            break
    
    # Ask if player wants to play again
    while True:
        play_again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if play_again in ['y', 'yes']:
            print("\n" + "=" * 50)
            main()  # Restart the game
            break
        elif play_again in ['n', 'no']:
            print("Thanks for playing! Goodbye! 👋")
            break
        else:
            print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()









