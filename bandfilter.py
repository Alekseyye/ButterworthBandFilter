from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

np.seterr(over='raise') # в случае переполнения выбрасывается исключение

# Характеристики полосового фильтра

w01 = 10    # нижняя граница диапазона пропускания, Гц
w02 = 20    # верхняя граница диапазона пропускания, Гц
N = 5    # порядок фильтра
f = 1000   # частота дискретизации, Гц

'''
# задание исходного сигнала из внешнего файла данных

name = 'имя_файла_с_данными'
data = np.loadtxt('name.txt')
t = data[:, 0]     # предполагается, что значения времени считываются 
sig = data[:, 1]   # из 1ого столбца, а сигнал - 2из ого
'''

#'''
# модель исходного сигнала

t0 = 1    # длительность исходного сигнала, с
w1 = 15    # частоты синусоидальных колебаний, состовляющих сигнал, Гц
w2 = 50
U = 10    # амплитуда исходного сигнала, В

t = np.arange(0, t0, 1/f)    # равномерный массив моментов времени t
sig = U * np.sin(2 * np.pi * w1 * t) + U * np.sin(2 * np.pi * w2 * t)
#'''

# вычисление коэффициентов фильтра
b, a = signal.butter(N, [w01, w02], 'band', analog = True)

# получение и построение ЛАЧХ и ЛФЧХ фильтра
w, h = signal.freqs(b, a)    # получение функции h(w) для фильтра

fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)

# ЛАЧХ фильтра
ax1.semilogx(w, np.log10(abs(h)))   # график с логарифмическим масштабированием по оси абсцисс
ax1.set_title('ЛАЧХ фильтра Баттерворта')    # название графика
#ax1.set_xlabel('Частота, Гц')    # названия осей на графике
ax1.set_ylabel('Понижение амплитуды, дБ')
ax1.margins(0, 0.1)    # создание отступов от границ графика
ax1.grid(True)    # добавление сетки
ax1.axvline(w01, color = 'red')    # диапазон пропускания
ax1.axvline(w02, color = 'red')

# ЛФЧХ фильтра
ax2.semilogx(w, np.unwrap(np.angle(h))) 
ax2.set_title('ЛФЧХ фильтра Баттерворта')
ax2.set_xlabel('Частота, Гц')
ax2.set_ylabel('Фаза, рад')
ax2.margins(0, 0.1)    
ax2.grid(True)    
ax2.axvline(w01, color = 'red')    
ax2.axvline(w02, color = 'red')

plt.tight_layout()
plt.show()

# прохождение сигнала через идеальный фильтр
filtsigideal = signal.lfilter(b, a, sig)

# прохождение сигнала через реальный фильтр
sos = signal.butter(N, [w01, w02], 'band', fs = f, output = 'sos')
filtsigreal = signal.sosfilt(sos, sig)

# графическое отображение исходного и фильтрованного сигнала
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex = False)

ax1.plot(t, sig)    # задание графика sig(t)
ax1.set_title('Исходный сигнал')    # название графика
ax1.axis([0, t0, -2*U, 2*U])    # установление пределов осей абсцисс и ординат
#ax1.set_xlabel('Частота, Гц')
ax1.set_ylabel('Амплитуда, В')
ax1.grid(True)

ax2.plot(t, filtsigreal)
ax2.set_title('Сигнал после идеального фильтра')
ax2.axis([0, t0, -2*U, 2*U])
#ax2.set_xlabel('Время, с')
ax2.set_ylabel('Амплитуда, В')
ax2.grid(True)

ax3.plot(t, filtsigreal)
ax3.set_title('Сигнал после реального фильтра')
ax3.axis([0, t0, -2*U, 2*U])
ax3.set_xlabel('Время, с')
ax3.set_ylabel('Амплитуда, В')
ax3.grid(True)

plt.tight_layout()
plt.show()