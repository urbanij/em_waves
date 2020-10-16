#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
#
# Created on:   Tue Nov 26 19:54:11 CET 2019
#
# Author(s):    Francesco Urbani <https://urbanij.github.io>
#
# File          waves.py
# Description:  
# 
# ==========================================================

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time

ε_0 = 8.854187817620389e-12
μ_0 = 4*np.pi*1e-7


class Medium:
    """docstring for Medium"""
    def __init__(self, ε_r, μ_r, σ):
        self._ε_r = ε_r
        self._μ_r = μ_r
        self._σ = σ

    def ε_eq(self, wave):
        """
        dielectric constant [F/m]
        """
        return ε_0 * self._ε_r * (1 + self._σ/(1j*wave._ω*ε_0 * self._ε_r)) 

    def μ_eq(self):
        """
        magnetic constant [H/m]
        """
        return μ_0 * self._μ_r

    def ζ_eq(self, wave):
        """
        characteristic impedance [Ω]
        epsilon_eq:   
        """
        return (self.μ_eq()/self.ε_eq(wave))**0.5

    def type(self, wave):
        U = self._σ / (wave._ω * self._ε_r)
        _type = 'Good conductor' if (U >= 1e2)              else \
                'Dielectric'     if (U < 1e2 and U >= 1e-2) else \
                'Insulator'
        return (U, _type)
    
    def __repr__(self):
        return f"<ε_r={self._ε_r}, μ_r={self._μ_r}, σ={self._σ}>"

class Wave:
    """docstring for Wave object"""
    def __init__(self, f=1.8e9, A=10):
        self._f = f             # [Hz]
        self._ω = 2*np.pi*f     # [rad/s]
        self._A = A             # [V/m]
        self._medium1 = Medium(ε_r=1, μ_r=1, σ=0) # vacuum is the default
        self._medium2 = self._medium1
        self._medium3 = self._medium2

    def add_mediums(self, medium1, medium2):
        self._medium1 = medium1
        self._medium2 = medium2
        
    def k(self, medium):
        """
        wavenumber [1/m]
        """
        return self._ω * np.sqrt(medium.μ_eq() * medium.ε_eq(self))

    def Γ(self, medium1, medium2):
        """
        reflection coefficient
        """
        return (medium2.ζ_eq(self)-medium1.ζ_eq(self))/(medium2.ζ_eq(self)+medium1.ζ_eq(self))

    def τ(self, medium1, medium2):
        """
        transmission coefficient
        """
        return 2*medium2.ζ_eq(self)/(medium2.ζ_eq(self)+medium1.ζ_eq(self))

    def δ(self, medium2):
        """
        skin depth
        """
        # return np.sqrt(2/(self._ω*medium2.μ_eq()*medium2._σ))
        
        α = self.k(medium2).imag
        return -1/α if α != 0 else np.inf

    def v(self, medium):
        """
        signal velocity [m/s]
        """
        return (1/np.sqrt(medium.ε_eq(self) * medium.μ_eq())).real

    def λ(self, medium):
        """
        wavelength [m]
        """
        return self.v(medium)/self._f

    def power_density_inc(self, medium):
        return 0.5 * 1/abs(medium.ζ_eq(self)) * abs(self._A)**2

    def power_density_trans(self, medium1, medium2):
        return self.power_density_inc(medium1) * (1-(abs(self.Γ(medium1, medium2)))**2)

    def __repr__(self):
        return f"Wave: f = {self._f} Hz; A = {self._A}"

    def print_data(self):
        print(f"U_1 := σ_1/(ω*ε_0*ε_r_1) = {self._medium1.type(self)[0]:.4g}  ==> medium 1 is a(n) \033[92m{self._medium1.type(self)[1]}\x1b[0m")
        print(f"U_2 := σ_2/(ω*ε_0*ε_r_2) = {self._medium2.type(self)[0]:.4g}  ==> medium 2 is a(n) \033[92m{self._medium2.type(self)[1]}\x1b[0m")
        print(f"μ_eq_1 = {self._medium1.μ_eq():.4g}")
        print(f"μ_eq_2 = {self._medium2.μ_eq():.4g}")
        print(f"ε_eq_1 = {self._medium1.ε_eq(self):.4g}")
        print(f"ε_eq_2 = {self._medium2.ε_eq(self):.4g}")
        print(f"ζ_eq_1 = {self._medium1.ζ_eq(self):.4g}")
        print(f"ζ_eq_2 = {self._medium2.ζ_eq(self):.4g}")
        print(f"k_1 = {self.k(self._medium1):.4g}")
        print(f"k_2 = {self.k(self._medium2):.4g}")
        print(f"Γ_e = {self.Γ(self._medium1,self._medium2):.4g} = {abs(self.Γ(self._medium1,self._medium2)):.4g} ∠ {np.angle(self.Γ(self._medium1,self._medium2)):.4g}")
        print(f"τ_e = {self.τ(self._medium1,self._medium2):.4g} = {abs(self.τ(self._medium1,self._medium2)):.4g} ∠ {np.angle(self.τ(self._medium1,self._medium2)):.4g}")
        print(f"δ = {self.δ(self._medium2):.4g}")        
        print(f"S_i = {self.power_density_inc(self._medium1):.4g}")
        print(f"S_t = {self.power_density_trans(self._medium1,self._medium2):.4g} = {100*self.power_density_trans(self._medium1,self._medium2)/self.power_density_inc(self._medium1):.4g}% S_i")

    def show(self, t, E1_i, ylim):
        fig, ax = plt.subplots(figsize=(10,8))
        fig.set_dpi(100)

        d_neg = -3*self.λ(self._medium1)
        d_pos = -d_neg

        z_medium1 = np.linspace(d_neg, 0, 300)
        z_medium2 = np.linspace(0, d_pos, 300)
        z     = z_medium1 + z_medium2

        k_1 = self.k(self._medium1)
        k_2 = self.k(self._medium2)

        Γ_e = self.Γ(self._medium1, self._medium2)
        τ_e = self.τ(self._medium1, self._medium2)

        
        e1_i   = lambda z, t: (      E1_i(k_1, -z, t)).real 
        e1_r   = lambda z, t: (Γ_e * E1_i(k_1, +z, t)).real
        e2_t   = lambda z, t: (τ_e * E1_i(k_2, -z, t)).real
        e1_tot = lambda z, t: e1_i(z,t) + e1_r(z, t)


        lines = []
        line1, = ax.plot(z_medium1, e1_i(z_medium1, t[0]),   "--", color='blue',   label='$e_1^i(z=z_0,t)$',     linewidth=1) 
        line2, = ax.plot(z_medium1, e1_r(z_medium1, t[0]),   "-.", color='red',    label='$e_1^r(z=z_0,t)$',     linewidth=1)
        line3, = ax.plot(z_medium1, e1_tot(z_medium1, t[0]), "-",  color='green',  label='$e_1^{tot}(z=z_0,t)$', linewidth=1.5) 
        line4, = ax.plot(z_medium2, e2_t(z_medium2, t[0]),   "-",  color='purple', label='$e_2^t(z=z_0,t)$',     linewidth=1.5)

        plt.title("Traveling wave" + \
                "\nmedium 1: z<0, $\epsilon_r$=" + str(self._medium1._ε_r) + ", $\mu_r$=" + str(self._medium1._μ_r) + ", $\sigma$ =" + str(self._medium1._σ) + \
                "\nmedium 2: z>0, $\epsilon_r$=" + str(self._medium2._ε_r) + ", $\mu_r$=" + str(self._medium2._μ_r) + ", $\sigma$ =" + str(self._medium2._σ)
            )
        plt.xlabel('space (z)')
        plt.ylabel('E [V/m]')
        plt.legend(loc='upper right')
        plt.ylim(ylim)
        plt.xlim([d_neg, d_pos])
        plt.grid(True)

        def animate(i):
            line1.set_data(z_medium1, e1_i(z_medium1, t[i]))
            line2.set_data(z_medium1, e1_r(z_medium1, t[i]))
            line3.set_data(z_medium1, e1_tot(z_medium1, t[i]))
            line4.set_data(z_medium2, e2_t(z_medium2, t[i]))
            return (line1,line2,line3,line4,)

        anim = animation.FuncAnimation(fig, animate, frames=len(t), interval=40, blit=True)
        
        plt.show()

    
    def save(self, t, E1_i, ylim):
        raise Exception("Unimplemented")
        self.show(t, E1_i, ylim)
        ### Save animation
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='fu'), bitrate=1800)
        anim.save(f'media/wave{time.time()}.mp4', writer=writer, dpi=200)



class Sine(Wave):
    """docstring for Sine"""
    def function(self, k, z, t):
        return self._A * np.exp(1j*k*z) * np.exp(1j*self._ω*t)

    def show(self, medium1=Medium(ε_r=1, μ_r=1, σ=0), medium2=Medium(ε_r=2, μ_r=1, σ=.81)):
        super().show(
            t=np.linspace(0, super().λ(medium1)/super().v(medium1), 45),
            E1_i=self.function,
            ylim=[-2*self._A, 2*self._A]
        )

class Gaussian(Wave):
    """docstring for Sine"""
    def __init__(self, f=1.8e9, A=10, rms=2.20):
        super().__init__(f, A)
        self._rms = rms

    def function(self, k, z, t):
        return self._A * 1/np.sqrt(2*np.pi*self._rms**2) * np.exp(-((self._ω*t + k.real*z)**2)/(2 * self._rms**2)) * np.exp(-k.imag*z)

    def show(self, medium1=Medium(ε_r=1, μ_r=1, σ=0), medium2=Medium(ε_r=1.5, μ_r=1, σ=.21)):
        peak=self._A/(self._rms*(2*np.pi)**0.5)
        super().show(
            t=np.linspace(-.8e-9, 1e-9, 160),
            E1_i=self.function,
            ylim=[-peak,1.2*peak]
        )

class Rect(Wave):
    """docstring for Sine"""
    def __init__(self, f=1.8e9, A=10, width=6.5):
        super().__init__(f, A)
        self._width = width

    def function(self, k, z, t):
        return self._A * (np.heaviside(self._ω*t + k.real*z+self._width,1e-6) - np.heaviside(self._ω*t + k.real*z-self._width, 1e-6)) * np.exp(-k.imag*z)

    def show(self, medium1=Medium(ε_r=1, μ_r=1, σ=0), medium2=Medium(ε_r=2, μ_r=1, σ=.81)):
        peak=self._A
        super().show(
            t=np.linspace(-.8e-9, 3e-9, 160),
            E1_i=self.function,
            ylim=[-peak,1.2*peak]
        )
