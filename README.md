# Musical STAR
A python game that serves as a fun and easy way to get music recommendations!


It uses the Last FM API to search similar artists and their top tracks and albums.
Made using the pygame library.
Requires: Python version 3.8+

# My Inspiration
My love for listening to a wide variety of music inspired me to create this game. It can get
boring to listen to the same artist over and over again, no matter how much you love them.
The usual way to get new artists to listen to is through reccomendations, human or otherwise,
and Musical-Star adds a little twist.

With Musical-STAR you can get reccomendations for brand new artists similar to the ones you
like in a fun, unique way. Also, claw machines are just fun.

For the hackathon, I am submitting to the Make Anything, But Make it YOU (Beginner-Friendly Track)

### HOW TO PLAY THE GAME

1. First, get your API Key here: https://www.last.fm/api/account/create

You will have to create an API account with an email.
Write anything you want for application name or description.
For callback URL you can just put in something like: http://localhost/ or https //127.0.0.1

2. Once you have an API, go to api.py and paste it into the API KEY variable.

3. Install dependencies from requirements.txt

4. Once everything is set-up, you can simply run main.py to play the game!
   
## Game Instructions

- Contrals are WASD, or Arrow keys. Q to drop prizes. E to open one. Space for picking up prizes.
- The game pulls artist/song data from LastFM using your API key.
- A GUI window will open (built with pygame).
- Once you click play, you will enter an Input Screen. Write any artist that you like
on the gray boxes and the game will generate artists similar to them. You can also
adjust the number of prizes generated at the bottom right corner.
- In the game loop, you control the claw and you get prizeballs with different artists inside.
