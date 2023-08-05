# SciScripts  
Scripts for controlling devices/running experiments/analyzing data  


## Installation
```bash
$ pip install --user sciscripts
```

Or if you plan to contribute to the code / want to change the code and see the results on the fly / want the most up-to-date version:
```bash
$ git clone https://gitlab.com/malfatti/SciScripts/
$ cd SciScripts/
$ pip install --user asdf h5py matplotlib numpy pandas pyserial rpy2 scipy sounddevice
$ pip install --user -e .
```


## Dependencies

1. OS:
    - Linux
2. Python:
    - asdf
    - h5py
    - matplotlib
    - numpy
    - pandas
    - pyserial
    - rpy2
    - scipy
    - sounddevice
3. Optional
    - xdpyinfo
    - xrandr

Also, some environment variables are expected to be set. You can add it to `~/.bashrc`, or `~/.profile`, or wherever your desktop environment searches for exported variables:
```bash
export DATAPATH=~/Data
export ANALYSISPATH=~/Analysis
```
changing the path to where you find appropriate.


## Examples

Here is a walkthrough for the `Examples/FilteringAndPlotting.py` script.

Load data from an open-ephys recording folder:
```python
In [1]: import numpy as np

In [2]: from sciscripts.IO import IO

In [3]: from sciscripts.Analysis import Analysis

In [4]: from sciscripts.Analysis.Plot import Plot

In [5]: Data, Rate = IO.DataLoader('DataSet/2018-08-13_13-25-45_1416')
Loading recording1 ...
Loading recording2 ...
Loading recording3 ...
Loading recording4 ...
Loading recording5 ...
Loading recording6 ...
Loading recording7 ...
Loading recording8 ...
Converting to uV...

In [6]: Data.keys()                     # Get open-ephys recording processors
Out[6]: dict_keys(['100'])
```

Select a recording and filter it:
```python
In [7]: Rec0 = Data['100']['0']['0'][:,:16]  # Work with the 1st rec, 1st experiment and 1st 16ch

In [8]: Rate0 = Rate['100']['0']  # Rate for the 1st experiment

In [9]: Time0 = np.arange(Rec0.shape[0])/Rate0

In [10]: Rec0Theta = Analysis.FilterSignal(Rec0, Rate0, Frequency=[4,12], FilterOrder=2)
Filtering channel 1 ...
Filtering channel 2 ...
Filtering channel 3 ...
Filtering channel 4 ...
Filtering channel 5 ...
Filtering channel 6 ...
Filtering channel 7 ...
Filtering channel 8 ...
Filtering channel 9 ...
Filtering channel 10 ...
Filtering channel 11 ...
Filtering channel 12 ...
Filtering channel 13 ...
Filtering channel 14 ...
Filtering channel 15 ...
Filtering channel 16 ...

In [11]: Rec0Gamma = Analysis.FilterSignal(Rec0, Rate0, Frequency=[30,100], FilterOrder=3)
Filtering channel 1 ...
Filtering channel 2 ...
Filtering channel 3 ...
Filtering channel 4 ...
Filtering channel 5 ...
Filtering channel 6 ...
Filtering channel 7 ...
Filtering channel 8 ...
Filtering channel 9 ...
Filtering channel 10 ...
Filtering channel 11 ...
Filtering channel 12 ...
Filtering channel 13 ...
Filtering channel 14 ...
Filtering channel 15 ...
Filtering channel 16 ...
```

Plot all channels from raw and filtered data:
```python
In [12]: Plot.AllCh(Rec0[:int(Rate0*0.05),:], Save=True, File='Plot1', Ext=['png'])
```
![](Plot1.png)
```python
In [13]: # Set plot window for each band
    ...: Window = int(Rate0)
    ...: 
    ...: # Plot
    ...: plt = Plot.Return('plt')
    ...: Fig, Axes = plt.subplots(1,3)
    ...: Axes[0] = Plot.AllCh(Rec0[:Window,:], Time0[:Window], Ax=Axes[0], lw=0.7)
    ...: Axes[1] = Plot.AllCh(Rec0Theta[:Window,:], Time0[:Window], Ax=Axes[1], lw=0.7)
    ...: Axes[2] = Plot.AllCh(Rec0Gamma[:Window,:], Time0[:Window], Ax=Axes[2], lw=0.7)
    ...: 
    ...: # Set labels
    ...: AxArgs = {'xlabel': 'Time [s]'}
    ...: for Ax in Axes: 
    ...:    Plot.Set(Ax=Ax, AxArgs=AxArgs)
    ...: 
    ...: Axes[0].set_ylabel('Voltage [µv]')
    ...: Axes[0].set_title('Raw signal')
    ...: Axes[1].set_title('Theta [4-12Hz]')
    ...: Axes[2].set_title('Gamma [30-100Hz]')
    ...:
    ...: Plot.Set(Fig=Fig)
    ...: Fig.savefig('Plot2.png')
    ...: plt.show()
```
![](Plot2.png)

Scripts using this package for real experiments and analysis can be found at `Examples/`, [here](https://gitlab.com/malfatti/LabScripts/-/tree/master/Python3/Exps) and [here](https://gitlab.com/malfatti/LabScripts/-/tree/master/Python3/Analysis).

