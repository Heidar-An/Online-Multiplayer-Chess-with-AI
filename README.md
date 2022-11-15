# Online Multiplayer Chess with AI

## Summary
Created in python library, Pygame. Allows user to choose between AI or play on the same computer/with others online.
This was created for my NEA - Non Exam Assessment for A-Level Computer Science. I received full marks for it (and thus got the highest in the class)

![image](https://user-images.githubusercontent.com/74025356/202046043-fbd0f8c8-8056-42f4-8982-321b06ac02e2.png)

## How does it work?
The AI uses the Minimax algorithm, with alpha beta pruning to help speed it up. 
The socket library was used to connect users online together.




## What other features are there?
There is also a colour picker to customise your board to be any RGB colour (integer values only) from 0-255 using custom made sliders.
Furthermore, the game also has a timed feature. I have made it so that users have 10 minutes each (with 0 increment time). When this time runs out, the game is over.

