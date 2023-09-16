### Wordle Game Client Version

The World Game Client Version is written in Python to design to interact with a given Wordle game server. The client play the Wordle game, with quiet a twist where they guess a secret word within a limited amount chances.

## Prerequisites
Before using this Wordle Game Client, ensure that you have the following:

- Python 3.8 or higher installed on your system
- A text file named "wordlist.txt" containing the list of valid words that would be used for guessing. (The file is provided in this zip)
- Access to the Wordle game server used

## Getting Started
1. Download this Wordle Game Client script to your local machine
2. Download the "wordlist.txt" to your local machine so that the code can run 
3. Open a terminal and navigate to the directory where the python script and text file can be found
4. Run the script with this command: python WordleGameClient.py <proj1.3700.network> <username> [--tls]
    - Your hostname is provided and your username is your Northeastern University username without your full @northeastern.edu 
5. The client will connect to the server and start the Wordle game.

## Game Rules
- The Wordle Game Client will connect to the server and attempt to guess the chosen seceret word for that round
- It will make guesses based the text file provided
- If the guess was not right, they would be able to guess again, once requested and a new guess would be created
- The client can not make guesses outside of the word list 
- The game continues until the client reaches the maximum number of guesses or the server sends a "bye" message.

## Configuration
You can configure the client by using command line arguments:
- <hostname>: Provide the hostname of the Wordle game server.(most likely given to you)
- <username>: Provide your Northeastern University username
- '-p', '--port': You would be able to specify the TCP port number
- '-s', '--tls': This flag to enable TLS encryption for the connection

## Output
1) The client will display information about the game progress and connection in your local terminal
2) Once the game has ended, it will save the secret flags both normal and TLS to a file callled "secretFlags.txt"

Author
- Alyssa Mckenzie Griffith 