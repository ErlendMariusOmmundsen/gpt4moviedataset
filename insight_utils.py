from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def print_prediction(df, index: int = None):
    if index:
        print(df.iloc[index]["prediction"])
    print(df.sample(1)["prediction"])


def line_plot_column(
    dataframes: List[pd.DataFrame], shared_column: str, dataframe_names: List[str]
):
    """
    Plot lines of a shared column for multiple DataFrames with identical columns.

    Parameters:
        dataframes (list): A list of DataFrames.
        shared_column (str): The name of the shared column.
    """
    # Plot lines of the shared column for each DataFrame
    for i, df in enumerate(dataframes):
        plt.plot(df[shared_column], label=f"{dataframe_names[i]}")

    # Add labels and title
    plt.xlabel("Row index")
    plt.ylabel(shared_column)
    plt.title(shared_column)

    # Add a legend
    plt.legend()

    # Display the plot
    plt.show()


calculations = ["mean", "median", "max", "min", "std"]


def bar_groups_chart(
    dataframes: List[pd.DataFrame],
    dataframe_names: List[str],
    metric: str,
    calculations: List[str] = calculations,
    row_range_start: int = 0,
    row_range_end: int = -1,
    y_start: int = 0,
    y_end: int = 1,
):
    for i, df in enumerate(dataframes):
        df["approach"] = [dataframe_names[i] for j in range(len(df))]
        df = df.iloc[row_range_start:row_range_end]

    df = pd.concat(dataframes)
    data = {}

    for i, df in enumerate(dataframes):
        values = []
        for calc in calculations:
            values.append(df[metric].agg(calc))
        data.update({dataframe_names[i]: values})

    x = np.arange(len(calculations))  # the label locations
    width = 0.15  # the width of the bars
    multiplier = -1

    fig, ax = plt.subplots(layout="constrained")

    for attribute, measurement in data.items():
        print(attribute, measurement)
        offset = width * multiplier
        rects = ax.bar(
            x + offset, [round(m, 2) for m in measurement], width, label=attribute
        )
        ax.bar_label(rects, padding=10)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(metric)
    ax.set_title(f"{metric.capitalize()} Aggregate Comparison")
    ax.set_xticks(x + width, calculations)
    ax.legend(loc="upper left", ncols=1)
    ax.set_ylim(y_start, y_end)

    plt.show()


def box_plot(dataframes: List[pd.DataFrame], dataframe_names: List[str], metric: str):
    metric_values = [df[metric] for df in dataframes]

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid", palette="pastel")

    ax = sns.boxplot(
        data=metric_values,
        width=0.4,
        fliersize=5,
        flierprops={
            "markerfacecolor": "lightgray",
            "markeredgecolor": "black",
            "marker": "o",
        },
    )

    ax.set_xticklabels(dataframe_names, rotation=45, ha="right", fontsize=12)
    ax.set_xlabel("Dataframe", fontsize=14)
    ax.set_ylabel(metric, fontsize=14)
    ax.set_title(metric + " Distribution", fontsize=18)

    sns.despine()

    plt.tight_layout()
    plt.show()