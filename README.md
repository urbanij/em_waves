## em-waves

[![Downloads](https://pepy.tech/badge/em-waves)](https://pepy.tech/project/em-waves)


### Installation
`pip install em_waves`


### Usage
```python
from em_waves import Medium, Sine, Gaussian, Rect

f_0     = 1.8e9 # [Hz]
E_0     = 10.0  # [V/m]

free_space = Medium(ε_r=1, μ_r=1, σ=0)
medium2 =    Medium(ε_r=5, μ_r=3, σ=.04)

wave = Sine(f=f_0, A=E_0)
# wave = Gaussian(rms=1.3)
# wave = Rect(width=4)

wave.add_mediums(medium1=free_space, medium2=medium2)
wave.print_data()
wave.show()
```


![Alt Text](https://raw.githubusercontent.com/urbanij/misc-scripts/master/ef/1_waves/media/cosine.gif)

![Alt Text](https://raw.githubusercontent.com/urbanij/misc-scripts/master/ef/1_waves/media/gaussian.gif)

![Alt Text](https://raw.githubusercontent.com/urbanij/misc-scripts/master/ef/1_waves/media/rect.gif)


### Demo installation and usage
[![asciicast](https://asciinema.org/a/0nIiOrAbAfusd1GOhGW1ZSTuO.svg)](https://asciinema.org/a/0nIiOrAbAfusd1GOhGW1ZSTuO)