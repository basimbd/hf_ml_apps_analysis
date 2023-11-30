# hf_ml_apps_analysis
This app analyzes the ease and maintainability of Text Classification and Text Generation applications in Hugging Face by analyzing their respective project size (Lines of Code).

# How To Run
At first, run the following command to install the required dependencies used in
this project.

`pip install -r requirements.txt`

Then use this command to start the application.

`python -m src.run.py`

To execute the tests, run the following command.

`python -m unittest`

# Tools Used
- **huggingface_hub** package with **HfApi Client** is used to communicate with 
Hugging Face and fetch the models and spaces.
- **Lizard** was used as the static code analyzer to get the code size of the 
projects. The reason **Lizard** was used because it is a very mature analyzer 
(Created over 11 years ago) and still maintained. Also, it has 1.7k stars on 
GitHub and is used for static analysis in other papers as well.

# Methodology
The approach to this analysis can be divided in three parts: data collection, 
analysis, and making inference.
### Data Collection
- For data collection, the top 20 most popular models for each of
`text-classification` and `text-generation` was fetched. Then for each of these
40 models, the spaces were fetched that were using these models.
- The popularity of the models was determined by the `downloads` count of a model. 
The `likes` count was not used because a large number of users do not give 
ratings. And also, even if one does not like the model, it is still used.
### Analysis
- Once the information about the spaces was fetched, each space was cloned.
Then lizard was run inside the project to get the code size i.e., lines of code 
without comments (NLOC). After running lizard, the project directory is removed
so as not to bloat the disk space.
- Certain files and directories (e.g., `data/`, `dataset/`, `test/`, etc.) were
excluded from the analysis. Since tests and datasets are different from the
development effort of an application, they were excluded. Also, Lizard itself
ignores large files like `images`, `.pickle`, `.txt`, `.csv`, etc. file types.
- Some of the spaces was discarded and not analyzed because they were
duplicates. By manually checking 50 random spaces, it was found that duplicate
spaces usually have only a single commit during the duplication. Also, spaces 
that have some level of activity has more than 1 commit. So, spaces that had 
only 1 commit was discarded.
- The analysis results were stored in the `output/` directory as `.csv` files
for the inference stage. Also, the summary is printed in the terminal.

### Inference
- For the inference process, the analysis step was run 3 times. Then data was
noted from the analysis output. These data consist of total number of spaces, 
analyzed number of spaces, Non-comment Lines of Code (NLOC) for all the spaces,
and average NLOC size for each space. All these data are separately collected
for both Text Classification and Text Generation.
- Also, a couple of charts were used for better understanding of the data.

# Results
|                     | Text Classification | Text Generation |
|---------------------|---------------------|-----------------|
| Number of Spaces    | 693                 | 2810            |
| Analyzed Spaces     | 513                 | 1664            |
| Avg. NLOC per Space | 729.42              | 30616.43        |

Table 1: Analysis Data

- These data can slightly change while running on different days depending on the
availability of spaces in Hugging Face at that time. This can result in +-5
spaces for Text Classification and +-100 spaces for Text Generation.
- The reason why a large number of Text Generation spaces were not analyzed is
because a lot of them are clones. For example, only the `microsoft/HuggingGPT`
space has almost 50 duplicates.

The average NLOC size of the Text Generation spaces is extremely high. To
understand if this is the overall trend, a bar-chart is generated (as shown below). It shows
the range of NLOC in X-axis, and the percentage of spaces that fall in that
range. This chart reveals that over 50% of the spaces actually have NLOC in the
0-100 range. The average is skewed by some spaces 
(`OFA-Sys/OFA-vqa`, `yizhangliu/Grounded-Segment-Anything`) that have an NLOC 
of around 100k-400k.
![percent_of_spaces_by_nloc.png](/readme_files/percent_of_spaces_by_nloc.png)

From the standpoint of code size, developing applications using 
"Text Classification" models is easier than using "Text Generation" models.

# Challenges
- A big hurdle in the analysis was the git cloning of spaces. A lot of the
spaces have datasets or other large files in their repository. Because of that,
downloading those repos during git clone was taking a lot of time. This was
slowing down the overall study. To mitigate this, `git-lfs` along with 
filtering was used. GIT-LFS handles large files better and the filter option 
was used to fetch files larger than 1M only when needed. This way the git 
cloning was working faster and the overall process was expedited.

# Future Directions
- The Lizard analyzer provides several other metrics alongside NLOC. Among 
those, Cyclomatic Complexity Number (CCN) can be very useful for this study.
Cyclomatic Complexity uses flow-graph-construction to determine the number of
linearly-independent paths in the program flow. Therefore, combining NLOC and
CCN can give a better understanding about how easy to develop and maintain are
these ML apps.
- Although the models are primarily for Text Classification and Text 
Generation, they are used in a variety of domains. It could be useful to 
characterize the domains these models are affecting. However, the approach may
need some NLP techniques to mine the space card texts as domain info is not
directly associated with spaces by Hugging Face.
