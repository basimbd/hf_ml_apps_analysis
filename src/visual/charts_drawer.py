import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
from src.utils.common_utils import PROJECT_DIR


def draw_space_comparison_box():
    try:
        # These files should be available if the fetching of the spaces was successful.
        tc_spaces_df = pd.read_csv(f"{PROJECT_DIR}/output/text-classification-spaces.csv")
        tg_spaces_df = pd.read_csv(f"{PROJECT_DIR}/output/text-generation-spaces.csv")
    except FileNotFoundError as err:
        logging.exception(f"File {err.filename} not found.")
        return

    # Find the spaces that are common in both Text Classification and Text Generation
    common_spaces_df = tc_spaces_df.loc[tc_spaces_df['id'].isin(tg_spaces_df['id']), :]

    # Get the number of spaces of each type
    tc_spaces = tc_spaces_df.shape[0]
    tg_spaces = tg_spaces_df.shape[0]
    overlap_spaces = common_spaces_df.shape[0]

    rect_a = patches.Rectangle((0, 0), tc_spaces, 1, linewidth=1, color='blue', alpha=0.5, label='Text Classification')
    rect_b = patches.Rectangle((tc_spaces - overlap_spaces, 0), tg_spaces, 1, color='orange',
                               alpha=0.5, label='Text Generation')

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.add_patch(rect_a)
    ax.add_patch(rect_b)

    ax.set_xlim(0, max(tc_spaces, tg_spaces) + overlap_spaces)
    ax.set_ylim(0, 2)
    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

    ax.legend()
    ax.set_xlabel("Number of Hugging Face Spaces (Overlapping area denotes projects available in both)")

    plt.xticks(range(0, tg_spaces, 300))
    plt.savefig(f'{PROJECT_DIR}/output/number_of_hugging_face_spaces.png', bbox_inches='tight')
    plt.show()


def draw_nloc_comparison_bar_chart():
    try:
        # These files should be available if the lizard analysis of the spaces was successful.
        tc_size_df = pd.read_csv(f"{PROJECT_DIR}/output/text-classification-space-sizes.csv")
        tg_size_df = pd.read_csv(f"{PROJECT_DIR}/output/text-generation-space-sizes.csv")
    except FileNotFoundError as err:
        logging.exception(f"File {err.filename} not found.")
        return

    # a key-value result,
    # key: space size (NLOC count) range (for example 0-100).
    # value: percent of spaces falling in that range.
    space_size_percentage_chart_df = get_space_size_percentage_by_nloc_range(tc_size_df, tg_size_df)

    ranges = list(space_size_percentage_chart_df["nloc_range"])
    tc_space_counts = list(space_size_percentage_chart_df["space_percents_tc"])
    tg_space_counts = list(space_size_percentage_chart_df["space_percents_tg"])

    plt.figure(figsize=(12, 6))

    x_axis = np.arange(len(ranges))

    plt.bar(x_axis - 0.4, tc_space_counts, label='Text Classification', align='edge', width=0.4)
    plt.bar(x_axis, tg_space_counts, label='Text Generation', align='edge', width=0.4)

    plt.xticks(x_axis, ranges, rotation=90)
    plt.xlabel("Ranges of Lines of Codes")
    plt.ylabel("% of Spaces in Each Range")
    plt.title("Project percentages of Hugging Face Spaces by Lines of Codes")
    plt.legend()
    plt.savefig(f'{PROJECT_DIR}/output/percent_of_spaces_by_nloc.png', bbox_inches='tight')
    plt.show()


def get_space_size_percentage_by_nloc_range(tc_size_df: pd.DataFrame, tg_size_df: pd.DataFrame):
    tc_line_chart, tg_line_chart = find_space_counts_per_nloc_range(tc_size_df, tg_size_df)

    tc_chart_percents = percent_of_each_item_in_list(tc_line_chart.values())
    tg_chart_percents = percent_of_each_item_in_list(tg_line_chart.values())

    tc_percent_chart_df = pd.DataFrame(data={"nloc_range": tc_line_chart.keys(), "space_percents": tc_chart_percents})
    tg_percent_chart_df = pd.DataFrame(data={"nloc_range": tg_line_chart.keys(), "space_percents": tg_chart_percents})

    space_size_percent_chart_df = tg_percent_chart_df.merge(tc_percent_chart_df, on=["nloc_range"], how="outer", suffixes=("_tg", "_tc")).fillna(0)
    # a bug in pandas merge changes the dtype of the dataframe. So changing it back to int.
    space_size_percent_chart_df['space_percents_tc'] = space_size_percent_chart_df['space_percents_tc'].astype(int)

    # The query drops the rows if neither TC nor TG have any project in tha NLOC count range.
    return space_size_percent_chart_df.query("(space_percents_tc != 0) and (space_percents_tg != 0)")


def find_space_counts_per_nloc_range(tc_size_df: pd.DataFrame, tg_size_df: pd.DataFrame):
    INTERVAL_STEP = 100
    tc_line_chart = {}
    tg_line_chart = {}

    max_size = find_max(tc_size_df, tg_size_df)

    interval_start = 0
    while interval_start < (max_size+1):
        # until 1000 line count, interval is 100. After 1000 line count, interval is 1000
        # because very few have more than 1000 lines.
        if interval_start >= 1000:
            INTERVAL_STEP = 1000
        interval_end = interval_start + INTERVAL_STEP

        tc_space_count = 0
        tg_space_count = 0

        for tc_space in tc_size_df.values:
            if interval_start <= tc_space[1] < interval_end:
                tc_space_count += 1

        for tg_space in tg_size_df.values:
            if interval_start <= tg_space[1] < interval_end:
                tg_space_count += 1

        # exclude from chart if there is 0 project in this lines of code interval
        if not (tc_space_count == 0):
            tc_line_chart[(interval_start, interval_end)] = tc_space_count
        if not (tg_space_count == 0):
            tg_line_chart[(interval_start, interval_end)] = tg_space_count
        interval_start += INTERVAL_STEP
    return tc_line_chart, tg_line_chart


def find_max(tc_size_df: pd.DataFrame, tg_size_df: pd.DataFrame):
    # Find the 95th Percentile NLOC count and treat it as max. Actual maximum is not used to avoid using outliers.
    tc_size_df = tc_size_df[tc_size_df['size'] != 0]
    tg_size_df = tg_size_df[tg_size_df['size'] != 0]

    tc_max = int(np.percentile(tc_size_df['size'], 95))
    tg_max = int(np.percentile(tg_size_df['size'], 95))

    return max(tc_max, tg_max)


def percent_of_each_item_in_list(my_list):
    sum_of_list = sum(my_list)
    return [round((val/sum_of_list)*100) for val in my_list]
