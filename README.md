# SensEmote-Emotion_Driven_Lights
Light (Lifx) colours respond to facial emotions using Microsoft Emotion API and Raspberry Pi

Raspberry Pi drives changes in colours to Lifx lights by capturing emotions and interpreting them using Microsoft Emotion API

Steps:
1. Burn the Raspberry Pi image file (location:) directly into an sdhc card and use it in your Raspberry Pi module. Alternatively, download the files but also ensure Pi is updated and CV2 is installed
2. Switch on the Pi and connect it via ethernet cable to computer
3. On an internet browser, go to 192.168.49.7 to access the configuration page
4. Enter wifi name, password to enable the Pi to connect to your network. Also update the Microsoft Emotion API subscription key and press submit
5. Switch on the Lifx light bulb (Configure the bulb to your network if you have not done so already)
6. Remove the ethernet cable and restart the Pi
7. Start making silly faces when the strobe light on the Pi goes red and watch as the Lifx light changes colours based on your facial emotions!

In its current setting, colour map for the emotions is:-
Anger/ Contempt - Red,
Disgust         - Green,
Fear            - Yellow,
Happiness       - Pink,
Neutral         - White,
Sadness         - Blue,
Surprise        - Orange

The above colour map can however be altered as needed by making changes to the database
