from multiprocessing import Process, Queue
import pyqtgraph.Qt as qt
import pyqtgraph as pg
import soundcard as sc
import numpy as np
import time
import sys
import scipy.signal as scipySignal

colorArray = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3',
              '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff',]

mics = sc.all_microphones(include_loopback=True)
print(mics)
# audioIn=mics[int(input("Choose input device: "))]
audioIn = mics[1]
RATE = 48000

CHUNK = 2048
BUFFER = 20000
LEN = BUFFER + CHUNK

channelsCNT = audioIn.channels
channels = range(0, audioIn.channels)

app = qt.QtWidgets.QApplication(sys.argv)

win = pg.GraphicsLayoutWidget(title="Buffered plot")  # creates a window
win.setGeometry(100, 100, 900, 300)

row = 0

curves=[]
for channel in channels:
    p = win.addPlot(row, channel, title="Channel " + str(channel))  # creates empty space for the plot in the window
    curve = p.plot(pen=colorArray[channel])  # create an empty "plot"
    p.setYRange(0, 1, padding=0)
    p.setXRange(0, CHUNK//2, padding=0)
    curve.setPos(0, 0)  # set x position in the graph to 0
    curves.append(curve)

if channelsCNT > 1:
    row += 1



def stream(q):
    with audioIn.recorder(samplerate=RATE) as mic:
        while 1:
            # start = time.time()
            data = mic.record(numframes=CHUNK)
            q.put(data)
            time.sleep(0.001)  # avoid overuse of resources
            # print("---->", time.time() - start)


def update(q: Queue):
    win.show()
    while True:
        while True:
            try:
                data = q.get_nowait()
                # print(q.qsize())
            except:
                app.processEvents()
                break
            # signal = np.sum(data, axis=1).real

            for channel in channels:
                signal = np.sum(data, axis=1).real
                if channel==0:
                    signal = scipySignal.detrend(signal)
                fft = np.abs(np.fft.fft(signal)) * 2 / (CHUNK // 2)
                fft = fft[:int(len(fft) / 2)]
                curves[channel].setData(fft)
            app.processEvents()
        time.sleep(0.001)


if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=update, args=(q,))
    p3 = Process(target=stream, args=(q,))
    p3.start()
    p1.start()
    p1.join()
    p3.join()
