import numpy as np
from numpy.random import normal as randn
import tspy as ts
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)


def gen_ar(T, coeffs):
    c = np.flipud(coeffs)
    p = c.size
    x = np.zeros((T+p))
    for t in range(p, T):
        x[t] = np.dot(x[t-p:t], c) + randn()
    return x[p:]


def main():
    T = 500
    N = 2048
    e = np.zeros((T,))

    for t in range(T):
        e[t] = randn()

    a1 = 0.7
    b1, b2 = 0.3, -0.6
    x = gen_ar(T, [a1])
    y = gen_ar(T, [b1, b2])

    w, method = 201, 'hamming'

    settings0 = {'smooth': False}
    settings1 = {'smooth': True, 'smooth_window': w, 'smooth_method': method}

    se = ts.spectrum(e,  num=N, **settings0)
    sx = ts.spectrum(x,  num=N, **settings0)
    sy = ts.spectrum(y,  num=N, **settings0)
    sse = ts.spectrum(e, num=N, **settings1)
    ssx = ts.spectrum(x, num=N, **settings1)
    ssy = ts.spectrum(y, num=N, **settings1)

    freq = np.fft.rfftfreq(N, d=1/(2*np.pi))

    tse = (1 / (2 * np.pi)) * np.ones(freq.shape)
    tsx = (1 / (2 * np.pi)) * (1 / (1 + a1 ** 2 - 2 * a1 * np.cos(freq)))
    tsy = (1 / (2 * np.pi)) * (1 / (1 + b1 ** 2 + b2 ** 2
                                    - 2 * b1 * np.cos(freq)
                                    - 2 * b2 * np.cos(2 * freq)
                                    + 2 * b1 * b2 * np.cos(freq)))

    ticks = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
    tick_labels = ['0', r'$\frac{1}{4} \pi$', r'$\frac{2}{4} \pi$',
                   r'$\frac{3}{4} \pi$', r'$\pi$']

    tpl_conf = {'color': 'red', 'linestyle': 'dashed', 'linewidth': 2,
                'label': 'Theoretical'}
    pl_conf = {'color': 'black', 'alpha': 0.4, 'linewidth':0.5,
               'label': 'Estimated'}
    spl_conf = {'color': 'black', 'linewidth': 2,
                'label': 'Estimated (smooth)'}

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 7))

    ax[0, 0].plot(e, color='black', linewidth=0.5)
    ax[0, 0].grid(alpha=0.3)
    ax[0, 0].set_xlabel('Time')
    ax[0, 0].set_ylabel('Value')
    ax[0, 0].set_title('Gaussian white noise - sample realization')
    ax[0, 1].plot(x, color='black', linewidth=0.5)
    ax[0, 1].grid(alpha=0.3)
    ax[0, 1].set_xlabel('Time')
    ax[0, 1].set_ylabel('Value')
    ax[0, 1].set_title('AR(1) process - sample realization')
    ax[0, 2].plot(y, color='black', linewidth=0.5)
    ax[0, 2].grid(alpha=0.3)
    ax[0, 2].set_xlabel('Time')
    ax[0, 2].set_ylabel('Value')
    ax[0, 2].set_title('AR(2) process - sample realization')

    ax[1, 0].plot(freq, tse, **tpl_conf)
    ax[1, 0].plot(freq, se, **pl_conf)
    ax[1, 0].plot(freq, sse, **spl_conf)
    ax[1, 0].legend()
    ax[1, 0].grid(alpha=0.3)
    ax[1, 0].xaxis.set_ticks(ticks)
    ax[1, 0].xaxis.set_ticklabels(tick_labels)
    ax[1, 0].set_xlabel('Frequency')
    ax[1, 0].set_ylabel('Power density')
    ax[1, 0].set_title('Gaussian white noise - spectrum')
    ax[1, 1].plot(freq, tsx, **tpl_conf)
    ax[1, 1].plot(freq, sx, **pl_conf)
    ax[1, 1].plot(freq, ssx, **spl_conf)
    ax[1, 1].legend()
    ax[1, 1].grid(alpha=0.3)
    ax[1, 1].xaxis.set_ticks(ticks)
    ax[1, 1].xaxis.set_ticklabels(tick_labels)
    ax[1, 1].set_xlabel('Frequency')
    ax[1, 1].set_ylabel('Power density')
    ax[1, 1].set_title('AR(1) process - spectrum')
    ax[1, 2].plot(freq, tsy, **tpl_conf)
    ax[1, 2].plot(freq, sy, **pl_conf)
    ax[1, 2].plot(freq, ssy, **spl_conf)
    ax[1, 2].legend()
    ax[1, 2].grid(alpha=0.3)
    ax[1, 2].xaxis.set_ticks(ticks)
    ax[1, 2].xaxis.set_ticklabels(tick_labels)
    ax[1, 2].set_xlabel('Frequency')
    ax[1, 2].set_ylabel('Power density')
    ax[1, 2].set_title('AR(2) process - spectrum')

    plt.tight_layout()
    fig.savefig('../t_spectrum.pdf')
    fig.savefig('../t_spectrum.png')
    # plt.show()


if __name__ == '__main__':
    main()
