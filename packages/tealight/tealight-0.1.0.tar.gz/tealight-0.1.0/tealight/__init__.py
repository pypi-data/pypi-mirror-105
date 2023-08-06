from matplotlib.collections import PatchCollection
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd


def candlestick_plot(df, date, low, high, open, close, volume):
    df = df.copy()

    # Intervals will proably be consistent, but take median in case of gaps
    # Scaled by .9 to leave a gap between entries
    interval = (df[date] - df[date].shift(1)).median() * .9

    # Work out the left and right of each rect
    df['left'] = (df[date] - interval/2).apply(mdates.date2num)
    df['right'] = (df[date] + interval/2).apply(mdates.date2num)

    # Specify overall up or down
    df['change'] = np.where(
        df[close].ge(df[open]),
        'Up', 'Down'
    )

    df['change'] = pd.Categorical(
        df['change'], categories=('Up', 'Down'), ordered=True
    )

    # Draw fig and axes, with ratios
    fig, axes = plt.subplots(
        figsize=(10, 5), nrows=2, 
        gridspec_kw={'height_ratios': [5, 2]},
        sharex=True
    )

    for i, (desc, data) in enumerate(df.groupby('change')):
        # Draw on our lines
        axes[0].vlines(
            x=data[date], ymin=data[low], ymax=data[high], color=f'C{i}',
            label=desc, zorder=3
        )

        # Draw the candle rectangles
        candle_rects = data.apply(
            lambda r: Rectangle(
                xy=(r['left'], min(r[close], r[open])), 
                width=r['right'] - r['left'], 
                height=abs(r[close] - r[open]), 
            ), axis=1
        )

        # Draw the volume rectangles
        volume_rects = data.apply(
            lambda r: Rectangle(
                xy=(r['left'], 0), 
                width=r['right'] - r['left'], 
                height=r[volume], 
            ), axis=1
        )

        # Add our rectangles to the axes
        axes[0].add_collection(
            PatchCollection(
                candle_rects.to_list(), fc=f'C{i}', ec=f'C{i}', zorder=2
            )
        )
        axes[1].add_collection(
            PatchCollection(
                volume_rects.to_list(), fc=f'C{i}', ec=f'C{i}', zorder=2
            )
        )

    axes[0].legend()
    axes[0].set_ylabel('Value')
    axes[0].set_xlim(df['left'].min(), df['right'].max())

    axes[1].set_ylim(0, df[volume].max()*1.05)
    axes[1].set_ylabel(volume)
    axes[1].set_ylabel('Volume')

    for ax in axes:
        ax.grid(axis='both', zorder=1, alpha=.5, ls=':')
        for side in ax.spines.keys():
            ax.spines[side].set_visible(False)
        ax.tick_params(axis='y', length=0)

    axes[0].tick_params(axis='x', length=0)

    return fig, axes
