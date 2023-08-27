# Gold DofE Skills Section 

For my Gold section I wanted to build of the game development I started looking at towards the end of silver and try a few things that caught my interest. This included: Tetris, Wordle and solver, neural networks and a simple scrolling game.

## Chat Server

This project consists of 2 programs, a server which manages connections and the exchange of information and a client program which sends and recieves data from the server. The socket module and server IP to allow comunication and the threading module to run tasks simultaneously.

<img src="Chat_Server/login.png" alt="Login Window" width="400px">

First you run the server program, then run the client inputting a username and the IP of the server (0.0.0.0 if its the local machine). Then the chat window will open allowing you to connect, disconnect and send messages.

<img src="Chat_Server/multipleClients.png" alt="Login Window" width="400px">



## Dungeon Scroller

A very common part of games is scrolling, when the character appears stationary realtive to the screen and the world moves around them. I wanted to make a basic game to try this style. My approach was to code the game with reference to the world coordinates and convert them when drawing the images on screen using the screen position in the world. It helped me think of the screen as a window looking into the world.

<img src="Dungeon_Scroller/scrollerGame.png" alt="Dungeon Map" width="400px">



## Emails

I have previously looked at pulling information from websites and APIs, it seemed like a natural progression to send this data somewhere I could access it. This program is a basic case of automating an email using my email adress, which could be combined with other programs to send automated updates about a topic.



## Games and Neural Networks

### Flappy Bird

Flappy bird is another instance of a scrolling game with a simpler

