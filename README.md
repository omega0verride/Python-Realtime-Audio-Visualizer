# Python-Realtime-Audio-Visualizer
An audio visualizer written using soundcard, scipy and pyqtgraph. Supports internal and microphone audio. Live waveform, buffered, hanning, FFT (frequency domain) etc.

Audio is captured on another process to not block the UI and pushes the data to a Queue to make sure we do not miss chunks of data while processing. 


![image](https://user-images.githubusercontent.com/64291401/178375127-96ed72b9-5c00-4a68-92d0-f4947d2cfed4.png)

