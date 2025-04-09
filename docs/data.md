# VisEval Dataset

## Introduction

VisEval dataset is a large-scale and high-quality dataset for Nature Language to Visualization (NL2VI) task. It contains 2,524 (NL, VIS) pairs, supports 7 common types of visualizations and covers 146 databases. 

- **VisEval.json** stores the JSON format of (NL, VIS) pairs. The natural language (NL) is a sentence that describes the desired visualization. The visualization (VIS) is represented in JSON format, including chart type, data for the x-axis, y-axis, and z-axis, as well as information such as sorting requirements.
- **VisEval_single.json** and **VisEval_multiple.json** store the visualizations that can be generated from a single data table and those that require processing multiple data tables, respectively.
- **databases** contains 146 databases, and each database has several data tables saved in CSV format.


## Important Notes / Caveats / FAQs
- The primary objective of this dataset is to serve as a benchmark for evaluating LLMs-based methods in natural language to visualization generation. This dataset is intended for research purposes only and should not be relied upon as the sole benchmark for production scenarios.
- How was the data collected? The dataset was constructed based on [nvBench](https://github.com/TsinghuaDatabaseGroup/nvBench). We selected high-quality queries from the original dataset, and we corrected and annotated the dataset ourselves. More details are provided in our paper's subsection 4.1.