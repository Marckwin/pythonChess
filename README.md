# pythonChess
 player vs ai chess game
## Description:
Pychess is a Player-Vs-AI chess engine implemented within pygame where a player is able to play chess against a computer that makes its own moves.
The game’s chess board and pieces was built using varying class based structures and polymorphism.

## Setup Instructions:
  * Ensure that python 3 is installed 
  * Ensure all listed files are within the main directory 
  * Install pygame and run chess.py:
  
  ### For Windows
    
    # Python and pip must be in your path for this to work
    
    pip install --user pygame
    python chess.py
 
 ### For Ubuntu
  ```
  sudo apt install python3-pip
  pip3 -m install --user pygame
  python3 chess.py
  ```
  * After running the main program, user will be prompted to select their color in the terminal
   enter “W” for white or “B” for black
  * Whoever plays as white makes the first move
  * In case of promotion, Terminal asks to pick one of “Q” - queen, “R”- rook, “B”- bishop, and “K” - knight.
  * if king is not safe, terminal displays “Check!
  * if in checkmate, terminal displays “CHECKMATE!”
