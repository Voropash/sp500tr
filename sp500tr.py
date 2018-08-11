import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from matplotlib.widgets import TextBox
import matplotlib.dates as mdates


returns = None
totalReturns = None
line1 = None
line2 = None
fig = None
ax = None
axbox1 = None
axbox2 = None
initial = None
years = None


def recalc(initial, years):
    global returns
    global totalReturns
    df = pd.read_csv('data.csv')
    df = df.tail(years*12)
    # Dividend
    sp500Initial = df.iloc[0].SP500
    ratio = initial/sp500Initial
    df['Date'] = df['Date'].astype('datetime64[D]')
    df.set_index('Date', inplace=True)
    shares = 1 + (df.Dividend / df.SP500).cumsum().shift(1).fillna(0)
    returns = ((df.SP500)*(1))*ratio
    totalReturns = ((df.SP500)*(shares))*ratio


def update():
    global line1
    global line2
    global fig
    global ax
    global initial
    global years
    line1.set_data(returns.index, returns)
    line2.set_data(totalReturns.index, totalReturns)
    ax.xaxis.set_tick_params(reset=True)
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_ylabel('Value of $%s initial investment over the course of %s year%s' % (initial, years, 's' if years > 1 else ''))
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()


def submit_initial(text):
    global initial
    initial = float(text)
    recalc(initial, years)
    update()


def submit_years(text):
    global years
    years = int(text)
    recalc(initial, years)
    update()


def _main(initial, years):
    global line1
    global line2
    global fig
    global ax
    recalc(initial, years)
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.3)
    axbox1 = plt.axes([0.1, 0.15, 0.8, 0.075])
    axbox2 = plt.axes([0.1, 0.05, 0.8, 0.075])
    initialText = TextBox(axbox1, 'Initial Investment', initial=str(initial))
    initialText.on_submit(submit_initial)
    yearsText = TextBox(axbox2, 'Years', initial=str(years))
    yearsText.on_submit(submit_years)
    line1, = ax.plot(returns.index, returns, label='SP500')
    line2, = ax.plot(totalReturns.index, totalReturns, label='SP500 (Total Returns)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value of $%s initial investment over the course of %s years' % (initial, years))
    ax.legend()
    plt.show()


if __name__ == '__main__':
    initial = 3000
    years = 5
    _main(initial, years)
