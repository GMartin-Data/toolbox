from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import f_oneway, probplot
import seaborn as sns


def bar_chart(df: pd.DataFrame, var: str, out: bool = False) -> None:
    """
    Draw bar chart for nominal variables
    `out` set to True allows to export the graph in png format in the graphs folder.
    """
    total = len(df)
    ax = sns.countplot(x=var, data=df, hue=var)

    for p in ax.patches:
        # Display modalities' percentages
        height = p.get_height()
        percentage = "{:.0f}%".format(100 * height / total)
        ax.text(p.get_x() + p.get_width() / 2.0, height + 3, percentage, ha="center")

        # Customize title
        ax.set_title(f"{var}'s bar chart", size="x-large", weight="bold", color="blue")

        # Set vertical xticks
        plt.xticks(rotation=90)

        # Customize labels on x and y axis
        plt.xlabel(var, fontsize=11, fontweight="bold")
        plt.ylabel("count", fontsize=11, fontweight="bold")

    # Export
    if out:
        plt.savefig(f"graphs/{var}_bar_chart.png", dpi=300)

    plt.show()


def catplot(x: str, y: str, df: pd.DataFrame, out: bool = True) -> None:
    """
    Draw a boxplot crossing informations between:
    - the continuous variable y
    - the nominal variable x
    `out` set to True allows to export the output in .csv format in csvs folder.
    """
    sns.catplot(x=x, y=y, hue=x, data=df, legend=False, kind="box")

    plt.title(f"Boxplot of {y} vs {x}", size="x-large", weight="bold", c="b")
    plt.xticks(rotation=90)

    if out:
        plt.savefig(f"graphs/boxplot_{y}_vs_{x}.png", dpi=300)

    plt.show()


def contingency_table(
    df: pd.DataFrame, var1: str, var2: str, out: bool = True
) -> pd.DataFrame:
    """
    Get the contingency table for two nominal features of a DataFrame.
    `out` set to True allows to export the output in .csv format in csvs folder.
    """
    ct = pd.crosstab(df[var1], df[var2])
    if out:
        ct.to_csv(f"csvs/{var1}_{var2}_ct.csv", index=True)
    return ct


def correlation_heatmap(df: pd.DataFrame, out: bool = True) -> None:
    """
    Displays correlations between numerical features of a DataFrame.
    `out` set to True allows to export the graph in png format in the graphs folder.
    """
    corr = df.select_dtypes(include="number").corr()
    # Create a matrix full of zeros similar to corr
    mask = np.zeros_like(corr)
    # Set the upper triangle of the mask to True
    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax = sns.heatmap(
            corr,
            # MASK
            mask=mask,
            # Div palette, suffix _r to reverse
            cmap="RdBu_r",  # coolwarm, vlag, icefire
            # Text in heatmap
            annot=True,  # Allowing annotations.
            fmt=".2f",  # Formatting annotations.
            annot_kws=dict(fontsize=9, fontweight="bold"),  # Other formatting
            # Values on vertical colorbar
            vmax=1,
            center=0,
            vmin=-1,
        )
    plt.title("Correlations Heatmap", size="x-large", weight="bold", c="b")

    if out:
        plt.savefig("graphs/correlations_heatmap.png", dpi=300)

    plt.show()


def cramers_v(ct: pd.DataFrame, chi2: float) -> float:
    """
    Perform Cramer's V test to measure correlation between two nominal variables,
    Params
    ------
        ct: the observed contingency table,
        chi2: the chi2 result of scipy.stats.contingency function on ct.
    """
    n = ct.sum().sum()  # Retrieve the number of observations
    n_rows, n_cols = ct.shape
    phi2 = chi2 / n
    phi2corr = max(0, phi2 - (n_rows - 1) * (n_cols - 1) / (n - 1))
    row_corr = n_rows - ((n_rows - 1) ** 2) / (n - 1)
    col_corr = n_cols - ((n_cols - 1) ** 2) / (n - 1)
    cramer_v = np.sqrt(phi2corr / min(row_corr - 1, col_corr - 1))
    return cramer_v


def draw_probplot(df: pd.DataFrame, var: str, out: bool = False) -> None:
    """
    Draw a qqplot of the variable to check its normality.
    `out` set to True allows to export the graph in .png format in the graphs folder.
    """
    probplot(df[var], dist="norm", plot=plt)
    plt.title(f"QQ Plot for {var}", size="x-large", weight="bold", color="blue")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Ordered Values")

    if out:
        plt.savefig(f"graphs/{var}_qqplot.png", dpi=300)

    plt.show()


def extract_var_outliers(df: pd.DataFrame, var: str, out: bool = False) -> pd.DataFrame:
    """
    Spots outliers (according to how they're defined on a boxplot)
    from the feature `feat` of the DataFrame `df`
    `out` set to True allows to export the output in .csv format in csvs folder.
    """
    q1, q3 = df[var].quantile([0.25, 0.75])
    iqr = q3 - q1
    outliers = df[df[var] > q3 + 1.5 * iqr]
    if out:
        outliers.to_csv(f"csvs/{var}_outliers.csv", index=False)
    return outliers


def hist_box_plot(col: str, df: pd.DataFrame, out: bool = False) -> None:
    """
    Display an histogram and a boxplot of df[col],
    col being a continuous numerical variable.
    `out` set to True allows to export the graph in .png format.
    """
    f, (ax_box, ax_hist) = plt.subplots(
        2, sharex=True, gridspec_kw={"height_ratios": (0.2, 1)}
    )
    mean = df[col].mean()
    median = df[col].median()
    mode = df[col].mode().values[0]

    sns.boxplot(data=df, x=col, ax=ax_box)
    ax_box.axvline(mean, color="r", linestyle="--")
    ax_box.axvline(median, color="g", linestyle="-")
    ax_box.axvline(mode, color="b", linestyle="-")

    sns.histplot(data=df, x=col, ax=ax_hist, kde=True)
    ax_hist.axvline(mean, color="r", linestyle="--", label="Mean")
    ax_hist.axvline(median, color="g", linestyle="-", label="Median")
    ax_hist.axvline(mode, color="b", linestyle="-", label="Mode")

    ax_hist.legend(loc="best")

    # Set x-axis label
    ax_hist.set_xlabel(col, fontsize=11, fontweight="bold")

    # Set y-axis label for the histogram
    ax_hist.set_ylabel("Count", fontsize=11, fontweight="bold")

    # Clear the x-axis label for the boxplot (as they share the same x-axis)
    ax_box.set(xlabel="")


def lineplot(
    x: str,
    y: str,
    df: pd.DataFrame,
    cat: Optional[str] = None,
    estimator: str = "mean",
    out: bool = False,
) -> None:
    """
    Draw a lineplot between two numerical variables x and y.
    `cat` set to a nominal variable's name allows to color the graph and draw multiples.
    `estimator` allows to specify the estimator used for bootstrapping.
    `out` set to True allows to export the graph in .png format in the graphs folder.
    """
    sns.relplot(
        x=x,
        y=y,
        data=df,
        kind="line",
        estimator=estimator,
        hue=cat,
        col=cat,
        col_wrap=df[cat].nunique() // 2 if cat else None,
    )
    graph_title = f"Line plot of {estimator} {y} by {x}"
    file_name = f"line_plot_{estimator}_{y}_by_{x}"

    if cat:
        graph_title += f" and {cat}"
        file_name += f"_and_{cat}"

    plt.suptitle(graph_title, size="x-large", weight="bold", color="blue", y=1.05)
    plt.ylabel(f"{estimator} {y}")
    if out:
        plt.savefig(f"graphs/{file_name}.png", dpi=300)

    plt.show()

    # Customize suptitle
    plt.suptitle(
        f"Distribution of {y} variable", size="x-large", weight="bold", color="blue"
    )

    # Export
    if out:
        plt.savefig(f"graphs/{y}_hist_box.png", dpi=300)

    plt.show()


def kdeplots(df: pd.DataFrame, cat: str, x: str = "charges", out: bool = True) -> None:
    """
    Draw kdeplots of charges according to modalities of `cat`
    `out` set to True allows to export the graph in png format in the graphs folder.
    """
    sns.kdeplot(x=x, hue=cat, data=df)

    plt.title(f"Kdeplots of {x} by {cat}", size="x-large", weight="bold", c="b")

    if out:
        plt.savefig(f"graphs/kdeplots_{x}_by_{cat}.png", dpi=300)

    plt.show()


def one_way_anova(df: pd.DataFrame, nom_var: str, num_var: str) -> Tuple[float, float]:
    """
    Perform one way ANOVA between a nominal variable and a numerical one,
    using `f_oneway` function from `scipy.stats`
    `num_var` is set by default to the target: `charges` of
    `cleaned_df`, which is the default `df`.
    """
    grouped_data = [group[num_var].values for name, group in df.groupby(nom_var)]
    f_statistic, p_value = f_oneway(*grouped_data)
    return f_statistic, p_value


def pairplot(df: pd.DataFrame, cat: Optional[str] = None, out: bool = False) -> None:
    """
    Draw a pairplot of the `df` DataFrame
    `hue` allows to color scatterplots according to a nominal variable
    `out` set to True allows to export the graph in .png format in the graphs folder.
    """
    sns.pairplot(data=df, hue=cat, corner=True)
    title = "Pair Plot"
    if cat:
        title += f" Colored by {cat}"

    plt.suptitle(title, size="x-large", weight="bold", color="blue", y=1)

    if out:
        file_name = "pairplot"
        if cat:
            file_name += f"_hue_{cat}"
        plt.savefig(f"graphs/{file_name}.png", dpi=300)

    plt.show()
