import random
import string
import json
import os
from datetime import datetime

class Leaderboard:
    def __init__(self, filename="leaderboard.json", top_k=10):
        self.filename = filename
        self.top_k = top_k
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load scores from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_scores(self):
        """Save scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
    
    def calculate_score(self, difficulty, attempts_used, word_length, is_one_shot=False):
        """Calculate score based on game parameters"""
        base_scores = {'easy': 10, 'medium': 20, 'hard': 30}
        base_score = base_scores.get(difficulty, 10)
        
        # Bonus for fewer attempts used
        attempt_bonus = (7 - attempts_used) * 5
        
        # Length bonus for longer words
        length_bonus = word_length * 2
        
        # One-shot bonus (massive bonus for guessing the whole word at once!)
        one_shot_bonus = 50 if is_one_shot else 0
        
        total_score = base_score + attempt_bonus + length_bonus + one_shot_bonus
        return max(total_score, 1)  # Minimum score of 1
    
    def add_score(self, player_name, difficulty, attempts_used, word_length, word, is_one_shot=False):
        """Add a new score to the leaderboard"""
        score = self.calculate_score(difficulty, attempts_used, word_length, is_one_shot)
        
        score_entry = {
            'player': player_name,
            'score': score,
            'difficulty': difficulty,
            'attempts_used': attempts_used,
            'word_length': word_length,
            'word': word,
            'is_one_shot': is_one_shot,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.scores.append(score_entry)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top K scores
        self.scores = self.scores[:self.top_k]
        
        self.save_scores()
        return score
    
    def display_leaderboard(self):
        """Display the top K leaderboard"""
        if not self.scores:
            print("\n🏆 No scores yet! Be the first to make the leaderboard!")
            return
        
        print(f"\n🏆 TOP {len(self.scores)} LEADERBOARD 🏆")
        print("=" * 70)
        print(f"{'Rank':<4} {'Player':<15} {'Score':<6} {'Diff':<6} {'Attempts':<8} {'Word':<12} {'Type':<8} {'Date':<12}")
        print("-" * 70)
        
        for i, entry in enumerate(self.scores, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            one_shot_indicator = "🎯" if entry.get('is_one_shot', False) else "  "
            print(f"{medal}{i:<3} {entry['player']:<15} {entry['score']:<6} "
                  f"{entry['difficulty']:<6} {entry['attempts_used']:<8} "
                  f"{entry['word']:<12} {one_shot_indicator:<8} {entry['date'][:10]:<12}")
        
        print("=" * 60)
    
    def get_player_rank(self, player_name):
        """Get player's current rank"""
        for i, entry in enumerate(self.scores, 1):
            if entry['player'].lower() == player_name.lower():
                return i
        return None

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
        self.is_one_shot_win = False
        self.leaderboard = Leaderboard()
        self.player_name = ''
    
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
    
    def make_one_shot_guess(self, word_guess):
        """Process a one-shot word guess"""
        if not word_guess.isalpha():
            return False, "Please enter a valid word (letters only)."
        
        word_guess = word_guess.lower().strip()
        
        if len(word_guess) != len(self.secret_word):
            return False, f"Word must be {len(self.secret_word)} letters long!"
        
        # Check if it's the correct word
        if word_guess == self.secret_word:
            # Mark all letters as guessed for display purposes
            self.guessed_letters.update(set(self.secret_word))
            self.won = True
            self.game_over = True
            self.is_one_shot_win = True
            return True, "🎯 BULLSEYE! One-shot win! 🎯"
        else:
            # Penalty for wrong one-shot guess
            self.attempts_left -= 2  # More penalty for wrong word guess
            return True, f"Wrong word! You lose 2 attempts. The word is not '{word_guess}'."
    
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
        self.is_one_shot_win = False
        self.select_word()
    
    def handle_game_end(self):
        """Handle end of game and update leaderboard"""
        if self.won and self.player_name:
            attempts_used = 6 - self.attempts_left
            score = self.leaderboard.add_score(
                self.player_name, 
                self.difficulty, 
                attempts_used, 
                len(self.secret_word), 
                self.secret_word,
                self.is_one_shot_win
            )
            
            print(f"\n🎉 Great job, {self.player_name}!")
            print(f"Your score: {score} points")
            
            if self.is_one_shot_win:
                print("🎯 One-shot bonus: +50 points!")
            
            # Check if player made it to leaderboard
            rank = self.leaderboard.get_player_rank(self.player_name)
            if rank:
                print(f"🏆 You're #{rank} on the leaderboard!")
            
            return True
        return False
    
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
    
    # Get player name
    while True:
        name = input("Enter your name: ").strip()
        if name:
            game.player_name = name
            break
        print("Please enter a valid name.")
    
    # Show leaderboard option
    show_leaderboard = input("\nWould you like to see the current leaderboard? (y/n): ").strip().lower()
    if show_leaderboard in ['y', 'yes']:
        game.leaderboard.display_leaderboard()
    
    # Difficulty selection
    while True:
        print("\nChoose difficulty:")
        print("1. Easy (3-4 letters) - Base Score: 10")
        print("2. Medium (6-8 letters) - Base Score: 20")
        print("3. Hard (9+ letters) - Base Score: 30")
        print("4. View Leaderboard")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            game.set_difficulty('easy')
            break
        elif choice == '2':
            game.set_difficulty('medium')
            break
        elif choice == '3':
            game.set_difficulty('hard')
            break
        elif choice == '4':
            game.leaderboard.display_leaderboard()
            continue
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    game.select_word()
    
    print(f"\n🎮 Game started! Difficulty: {game.difficulty.capitalize()}")
    print("Try to guess the word letter by letter!")
    print("Each wrong guess helps your flower grow! 🌸")
    print("You have 6 attempts to guess the word.")
    print("\n💡 Commands:")
    print("  - Enter a letter to guess")
    print("  - Enter a full word for one-shot guess (risky but high reward!)")
    print("  - Type 'hint' for a hint (after 2 guesses)")
    print("  - Type 'leaderboard' to view scores")
    print("  - Type 'quit' to exit")
    print("\n🎯 One-shot guessing: Guess the entire word at once!")
    print("   ✓ Correct: Instant win + 50 bonus points!")
    print("   ✗ Wrong: Lose 2 attempts!")
    
    while not game.game_over:
        print("\n" + "=" * 30)
        game.display_flower()
        print(f"\nWord: {game.display_word()}")
        print(f"Attempts left: {game.attempts_left}")
        
        if game.guessed_letters:
            print(f"Guessed letters: {', '.join(sorted(game.guessed_letters))}")
        
        guess = input("\nEnter a letter or full word: ").strip()
        
        if guess.lower() == 'quit':
            print("Thanks for playing! Goodbye!")
            return
        elif guess.lower() == 'leaderboard':
            game.leaderboard.display_leaderboard()
            continue
        elif len(guess) > 1 and guess.isalpha():
            # This is a word guess (one-shot)
            success, message = game.make_one_shot_guess(guess)
            print(f"\n{message}")
            
            if game.game_over:
                if game.won:
                    print("\n🎉 Congratulations! You won! 🎉")
                    print(f"The word was: {game.secret_word.upper()}")
                    print("🎯 ONE-SHOT CHAMPION! 🎯")
                    
                    # Handle leaderboard update
                    game.handle_game_end()
                    break
                else:
                    print("\n💀 Game Over! You lost! 💀")
                    print(f"The word was: {game.secret_word.upper()}")
                    print("Better luck next time!")
                    break
            continue
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
            
            # Handle leaderboard update
            game.handle_game_end()
            break
        elif status == "lost":
            print("\n💀 Game Over! You lost! 💀")
            print(f"The word was: {game.secret_word.upper()}")
            print("Better luck next time!")
            break
    
    # Show final leaderboard
    print("\n" + "=" * 50)
    game.leaderboard.display_leaderboard()
    
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









