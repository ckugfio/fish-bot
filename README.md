# fish-bot
A simple fishing bot for games

<h1 align="center"> ⚙️ Step-by-Step Configuration </h1>

1. Configure the 2 keys
  CAST: Key to start the action (e.g., click or "1")
  REEL: Key to finish (e.g., "2" or "E")
  TOGGLE: Key to turn bot on/off (F9 by default)

2. Select detection zone
  Click "Select Region"
  Drag a box around the icon/indicator that appears when it bites
  Smaller zone = faster detection

3. Capture the indicator color
  Screen Mode: Click the button, then click the icon color when it bites
  Palette Mode: Choose color manually if you know it

4. Adjust tolerance
  Not detecting? → Increase tolerance (+10-30)
  False positives? → Decrease tolerance (-5-10)

5. Activate the bot! Press F9 (or your configured key) and the bot does the work (You need to be in the game window for it to work correctly).

<h1 align="center"> How It Works </h1>

The bot runs this loop automatically:

1. Press CAST key (starts fishing)
   
      ↓
3. Monitor selected zone 30 times/second
   
      ↓
5. Did the indicator color appear? (e.g., ! or "BITE")
   
      ↓
7. Press REEL key immediatel
   
      ↓
9. Wait 2-3 seconds and repeat from step 1

<h1 align="center"> Tips for Your Game </h1> 

Small zone = better: Select only the icon area, not whole screen

Unique color: If the icon has a specific color (e.g., bright red), use it

Test tolerance: Start at 20 and adjust based on results

Windowed vs Fullscreen: Works in both modes

Background: You can minimize the bot while playing

<h1 align="center"> ⚠️ Disclaimer </h1> 

Use at your own risk. Some games (especially online/MMO) may consider bot usage a violation of their terms of service. This bot is designed primarily for single-player games or mechanics that don't provide competitive advantage.

