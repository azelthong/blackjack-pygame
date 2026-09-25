# Blackjack Game

A Blackjack game developed with Python and Pygame featuring multi-deck gameplay, automated dealer logic, hand scoring, natural Blackjack detection, and persistent win/loss tracking.

## Preview

![Blackjack Game](images/demo.png)

## Features

- Interactive Blackjack gameplay
- Four-deck card shoe
- Persistent shoe across multiple hands
- Automatic deck reshuffling when cards run low
- Hit and Stand controls
- Dealer automatically draws until reaching at least 17
- Hidden dealer card during the player's turn
- Natural Blackjack detection
- Dealer Blackjack detection
- Blackjack vs Blackjack push handling
- Dynamic Ace scoring as either 1 or 11
- Player bust detection
- Dealer bust detection
- Win, loss, and draw tracking
- New Hand functionality
- Graphical card display using Pygame

## Technologies

- Python
- Pygame

## How It Works

```text
Create 4-Deck Shoe
        ↓
Deal Two Cards to Player and Dealer
        ↓
Check for Natural Blackjack
        ↓
Player Chooses Hit or Stand
        ↓
Dealer Reveals Hidden Card
        ↓
Dealer Draws Until 17+
        ↓
Compare Scores
        ↓
Win / Loss / Push
        ↓
Start New Hand Using Remaining Shoe
```

## Blackjack Rules Implemented

### Card Values

Number cards use their displayed value.

```text
2–10 → Face value
J/Q/K → 10
A → 1 or 11
```

The value of an Ace is automatically adjusted when necessary to avoid exceeding 21.

### Natural Blackjack

A natural Blackjack requires exactly two cards with a total value of 21.

For example:

```text
Ace + King = Blackjack
```

while:

```text
7 + 7 + 7 = 21
```

is treated as a normal score of 21 rather than a natural Blackjack.

### Dealer Behaviour

After the player stands, the dealer automatically draws cards while the dealer's score is below 17.

### Four-Deck Shoe

The game uses four standard decks:

```text
52 cards × 4 decks = 208 cards
```

Unlike recreating the deck after every hand, cards remain removed from the shoe between rounds.

When the number of remaining cards becomes low, the game creates a fresh four-deck shoe.

## Installation

Clone the repository:

```bash
git clone https://github.com/azelthong/blackjack-pygame.git
```

Navigate into the project directory:

```bash
cd blackjack-pygame
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

## Running the Game

Run:

```bash
python main.py
```

## Project Structure

```text
blackjack-pygame/
│
├── images/
│   └── demo.png
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## What I Learned

Through this project, I gained experience with:

- Python game development
- Pygame
- Event-driven programming
- Game-state management
- Randomised card selection
- Multi-deck card management
- Conditional game logic
- User interaction through graphical controls
- Dynamic hand-value calculation
- Managing reusable state across multiple game rounds

## Future Improvements

Potential improvements include:

- Betting and chip management
- Split hands
- Double Down
- Insurance
- Blackjack payout rules
- Configurable number of decks
- Improved card graphics and animations
- Sound effects
- Game statistics and session history
- Unit testing for Blackjack scoring logic

## Author

**Azel Thong**

- GitHub: https://github.com/azelthong
- LinkedIn: https://www.linkedin.com/in/azel-thong-532084274/