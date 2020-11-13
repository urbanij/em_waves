"""
Demo [em_waves](https://pypi.org/project/em-waves)

Running:
after installing em_waves with:
    `pip3 install em_waves`
type:
    `python3 em_waves_demo1.py`
"""

import multiprocessing
from em_waves import Medium, Sine, Gaussian, Rect


SHOW_PLOT = True

def proc_func(wave):
    print (wave)
    wave.show()


def print_recap(*args):
    print(f"-"*20)
    print(f"f_0: {args[0]} GHz")
    print(f"-"*20)
    print(f"ε_r_1: {args[1]:<10} ε_r_2: {args[2]}")
    print(f"σ_1: {args[3]:<10}   σ_2: {args[4]}")
    print(f"-"*20)


def main():
    print("Insert data when prompted, if skipped default value will be used.")
    f_0 = float(input("Insert frequency in GHz: ") or 1.8)

    ε_r_1 = float(input("Insert ε_r_1: ") or 1.0)
    ε_r_2 = float(input("Insert ε_r_2: ") or 4.0)

    σ_1 = float(input("Insert σ_1: ") or 0)
    σ_2 = float(input("Insert σ_2: ") or 4e-10)

    print_recap(f_0, ε_r_1, ε_r_2, σ_1, σ_2)


    medium1 = Medium(ε_r=ε_r_1, μ_r=1, σ=σ_1)
    medium2 = Medium(ε_r=ε_r_2, μ_r=2.5, σ=σ_2)

    sine = Sine(f=f_0, A=10.0)
    gaussian = Gaussian(rms=1.3)
    rect = Rect(width=4) 

    sine.add_mediums(medium1=medium1, medium2=medium2)
    gaussian.add_mediums(medium1=medium1, medium2=medium2)
    rect.add_mediums(medium1=medium1, medium2=medium2)

    sine.print_data()
    

    if SHOW_PLOT:
        p1 = multiprocessing.Process(target=proc_func, args=(sine,))
        p2 = multiprocessing.Process(target=proc_func, args=(gaussian,))
        p3 = multiprocessing.Process(target=proc_func, args=(rect,))

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()


if __name__ == '__main__':
    main()
    