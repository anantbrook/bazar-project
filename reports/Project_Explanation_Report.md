# Paisabazaar Credit Health Analysis and Dashboard

**Detailed project explanation report**  
**Project type:** Exploratory data analysis, portfolio-level statistical analysis, score-label benchmark, and interactive business-intelligence dashboard  
**Prepared:** 23 October 2026

## 1. Executive summary

This project studies a monthly credit-profile dataset and presents its patterns in an interactive dashboard. Its business purpose is to help Paisabazaar monitor portfolio composition, investigate segment-level signals, and define evidence requirements for better operational decisions. The work is not a competition analysis and does not make decisions about any individual.

The source contains 100,000 monthly observations for 12,500 customers across eight snapshots. The available outcome is a three-category credit-score label: Poor, Standard, or Good. The largest group is Standard (53.2% of rows), followed by Poor (29.0%) and Good (17.8%).

The analysis finds descriptive differences between score groups. For example, median reported payment delay is 27 days in Poor-labelled records and 10 days in Good-labelled records. Profile-level hypothesis tests also find associations between score category and income, credit mix, and payment delay. These results help prioritize data-quality review, cohort investigation, and future outcome analysis; they do not show that a product or intervention caused a score change.

The notebook includes a Logistic Regression benchmark to classify the dataset's existing score label. On a profile-separated 20% test set, it achieves 0.668 accuracy, 0.710 balanced accuracy, and 0.662 macro F1. Hyperparameter tuning changes these values only slightly. This model predicts the existing label, not default, repayment, eligibility, approval, or business value. It is not used by the dashboard.

The Streamlit dashboard has five sections: Executive overview, Portfolio drivers, Portfolio movement, Decision brief, and Data & limits. It renders aggregate results only. A local launcher and cloud configuration are included. The public deployment uses a bundled synthetic dataset; authorized private analysis can use an approved de-identified source through `PAISABAZAAR_DATA`.

## 2. Business context and project objective

Paisabazaar operates in banking and credit-product discovery. Understanding portfolio-level credit profiles can help the business define stronger monitoring, review, and measurement practices. The project explores the data with the following objectives:

- Describe the distribution of the supplied credit-score categories.
- Compare payment, debt, credit-mix, and inquiry patterns across those categories.
- Summarize how portfolio score labels differ between the first and last selected snapshots.
- Convert descriptive signals into explicit business-decision hypotheses that can be tested with verified outcomes.
- Provide an interactive, readable interface for exploring aggregate patterns.

The business goals of reducing defaults, improving approvals, increasing customer understanding, or improving revenue cannot be measured with this dataset. It does not contain verified repayment/default outcomes, application or approval records, campaign exposure, customer conversions, or revenue. The report therefore treats these as future measurement goals rather than achieved project results.

## 3. Project scope and workflow

The project combines a Jupyter notebook for analysis and a Streamlit web dashboard for interaction. The workflow is:

| Stage | Work performed |
|---|---|
| Data review | Loaded the monthly credit-profile file and checked its shape, data types, missing values, duplicate rows, and category distributions. |
| Preparation | Trimmed text, normalized score-label spelling, converted numeric-looking fields safely, and preserved meaningful categories such as NM. |
| Exploration | Compared aggregate score composition and related payment, debt, credit-mix, income, and inquiry indicators. |
| Statistical analysis | Built one record per customer for three hypothesis tests so repeated monthly rows did not count as independent customers. |
| Benchmark model | Used a group-aware train/test split and a Logistic Regression classifier to predict the supplied score label for analysis practice. |
| Dashboard | Added interactive filters, aggregate charts, score-transition summaries, and a business decision brief. |
| Deployment preparation | Added a one-click Windows launcher, cloud start configuration, and a bundled synthetic public demo dataset. |

## 4. Dataset overview

### 4.1 Size and observation unit

The CSV has 100,000 rows and 28 columns. Each row is a customer-month observation. There are 12,500 distinct Customer_ID values and eight month values, with one snapshot per customer per month in this file. For the dashboard, ID, Name, and SSN are excluded while reading the CSV, leaving 25 analysis fields including Customer_ID for internal aggregation. The customer ID is never shown in charts or downloads.

The repeated monthly rows are important. A chart over rows describes customer-month observations, not 100,000 different people. Customer-level transitions and statistical tests aggregate repeated observations by Customer_ID before comparing customers.

### 4.2 Main variable groups

| Variable group | Examples | How the project uses them |
|---|---|---|
| Snapshot and grouping | Month, Customer_ID | Select time windows and calculate aggregate customer-level transitions. |
| Target label | Credit_Score | Group observations into Poor, Standard, and Good. |
| Payment behavior | Delay_from_due_date, Num_of_Delayed_Payment, Payment_of_Min_Amount, Payment_Behaviour | Describe payment-related patterns across labels. |
| Credit profile | Credit_Mix, Num_Credit_Card, Num_Bank_Accounts, Num_of_Loan, Credit_History_Age | Compare reported credit mix and profile characteristics. |
| Financial amounts | Annual_Income, Monthly_Inhand_Salary, Outstanding_Debt, Total_EMI_per_month, Monthly_Balance | Compare medians and test customer-level income differences. Units and currency are not verified. |
| Utilization and inquiries | Credit_Utilization_Ratio, Num_Credit_Inquiries | Explore association with the score label. Utilization is kept on the source scale; it is not assumed to be a percentage. |
| Sensitive fields | ID, Name, SSN | Present in the original source. The dashboard excludes these fields at CSV read time. |

### 4.3 Data quality and preparation

The notebook reports 100,000 rows by 28 columns, zero exact duplicate rows, and zero missing cells after its type-conversion and cleaning pass. The cleaned file contains three score labels. Numeric-looking columns are converted using safe numeric parsing; unexpected values become missing rather than being silently interpreted as valid numbers. Score spelling is normalized to title case, and NM is retained as a minimum-payment response category.

The dashboard independently loads the CSV and excludes ID, Name, and SSN in the CSV reader. It parses its numeric fields safely and uses cached loading for responsive interaction. It does not show customer-level rows. The aggregate download contains month-level score shares only.

The notebook and dashboard have different privacy behavior: the notebook performs broad exploratory work on the full source dataframe, while the dashboard excludes direct identifiers during loading. Before sharing the notebook, review its saved cell outputs and clear any raw-row display that could contain personal fields.

## 5. Exploratory findings

### 5.1 Overall score-label mix

| Credit-score label | Monthly records | Share of records |
|---|---:|---:|
| Standard | 53,174 | 53.2% |
| Poor | 28,998 | 29.0% |
| Good | 17,828 | 17.8% |
| **Total** | **100,000** | **100.0%** |

These percentages describe rows in the supplied dataset. They should not be interpreted as the percentage of all Paisabazaar customers or as the current customer portfolio unless the dataset's sampling and date coverage are verified.

### 5.2 Score-label share across snapshots

The Good-label share is 15.8% in month 1 and 19.3% in month 8. Over the same snapshots, the Poor-label share is 28.7% and 28.8%; the Standard-label share is 55.5% and 51.9%. This is a descriptive change in the data. It does not identify why labels changed or imply that a Paisabazaar action caused the change.

### 5.3 Median profile indicators by score label

| Indicator | Poor | Standard | Good | Interpretation note |
|---|---:|---:|---:|---|
| Reported delay from due date | 27 | 18 | 10 | Field name suggests days; confirm units with the data owner. |
| Outstanding debt | 1,945.35 | 1,001.61 | 736.47 | Dataset units; currency is unverified. |
| Credit utilization | 32.01 | 32.33 | 32.74 | Values are close across groups; source scale is unverified. |
| Credit inquiries | 8 | 5 | 3 | Median count in monthly rows. |
| Credit-history age | 161 months | 227 months | 288 months | Approximate conversion from the supplied numeric field. |

These are row-level medians by label, except where noted otherwise. They show association, not causation. In particular, the similarity in the utilization medians means this dataset alone does not support a simple claim that utilization separates the three categories.

### 5.4 First-to-last customer label transition

Across the full eight-month window, each of the 12,500 customers is represented once by their first and last score label. By the ordinal ordering Poor < Standard < Good:

| Movement from first to last selected month | Customers | Share |
|---|---:|---:|
| Improved label | 2,129 | 17.0% |
| Same label | 8,656 | 69.2% |
| Declined label | 1,715 | 13.7% |

The calculation compares only the first and last labels and does not count the path between them. A customer could improve and later decline while ending at the same category. The result is not a change in a numeric credit score or evidence of an intervention effect.

## 6. Customer-level hypothesis tests

To reduce the dependence problem caused by repeated monthly rows, the notebook forms one customer summary: modal score label, median annual income, modal credit mix, and mean payment delay. The three tests use this 12,500-customer summary. The p-values are very small in a large sample; effect sizes and practical relevance matter alongside statistical significance.

| Question | Test and result | Effect size | Responsible interpretation |
|---|---|---|---|
| Is income higher for Good than Poor score groups? | One-sided Mann-Whitney U; Good median income 45,800.93, Poor median 31,607.29; p = 3.16e-143. | Rank-biserial correlation = 0.372. | Income distributions differ in this sample. Units and currency are unverified, and this does not establish that income causes a score label. |
| Are credit mix and score label associated? | Chi-square test of independence; chi-square(4) = 6,633.64; p < 1e-300 due to numerical underflow. | Cramer's V = 0.515. | The customer-level categories are associated in this dataset. Do not turn this association into a product-eligibility rule. |
| Do mean payment delays differ among score groups? | Kruskal-Wallis test; H = 3,004.35; p < 1e-300 due to numerical underflow. | Epsilon-squared = 0.240. | Mean customer delay was 30.00 for Poor, 19.19 for Standard, and 10.66 for Good. Group distributions differ, but the test does not identify cause. |

The notebook does not document a multiple-testing correction. The results should be treated as exploratory. Follow-up work should pre-register a small set of questions, report confidence intervals, check assumptions and data definitions, and validate results on an independent time period.

## 7. Notebook model benchmark

### 7.1 Target and split

The model target is Credit_Score, the label already present in the dataset. Predictors exclude ID, Customer_ID, Month, Name, SSN, Occupation, Type_of_Loan, and Credit_Score. Credit_Mix is included in the current feature set, so confirm it is available at the intended prediction time and is not derived from the target process before treating this benchmark as operationally meaningful.

A StratifiedGroupKFold split assigns all rows for a customer to either training or testing, not both. The split is approximately 80% training (80,000 rows, 10,000 customers) and 20% test (20,000 rows, 2,500 customers). This avoids leakage from a customer's other monthly snapshots across the train/test boundary.

### 7.2 Preprocessing and model

The notebook's benchmark is Logistic Regression with class_weight set to balanced. Numeric features use median imputation and RobustScaler. Categorical features use most-frequent imputation and one-hot encoding with unknown categories ignored. Annual income and outstanding debt receive log1p transforms; their raw columns are removed. Monthly in-hand salary is omitted from the model features because it is highly correlated with annual income.

A RandomizedSearchCV search uses three StratifiedGroupKFold splits and macro F1 scoring. The selected settings are C = 0.1 and balanced class weights. The best cross-validation macro F1 is 0.658.

### 7.3 Test performance

| Metric | Baseline | Tuned |
|---|---:|---:|
| Accuracy | 0.668 | 0.668 |
| Balanced accuracy | 0.710 | 0.711 |
| Macro F1 | 0.662 | 0.662 |
| Weighted F1 | 0.671 | 0.671 |

Rounded class results for the tuned run are:

| Label | Precision | Recall | F1 |
|---|---:|---:|---:|
| Good | 0.51 | 0.84 | 0.63 |
| Poor | 0.63 | 0.70 | 0.66 |
| Standard | 0.82 | 0.59 | 0.69 |

Tuning provides a negligible change at the reported precision and does not materially improve macro F1. Standard has the largest support, while the balanced model has much higher recall for Good than precision. For a descriptive class-label benchmark, balanced accuracy and macro F1 are more informative than accuracy alone. These scores do not measure default detection or business value. The model is not loaded or called by the Streamlit dashboard.

## 8. Interactive dashboard guide

| Section | Purpose and controls |
|---|---|
| Executive overview | Shows filtered row and profile counts, Good-label share, median reported delay, monthly score-label trend, overall composition, and an aggregate monthly CSV download. |
| Portfolio drivers | Compares credit mix, payment behaviour, minimum-payment responses, and selectable median indicators across score labels. |
| Portfolio movement | Builds a first-to-last label transition heatmap and higher/stable/lower label shares for profiles with at least two selected snapshots. |
| Decision brief | Lets the analyst choose a business lens such as delays, utilization, debt, inquiries, or history; displays aggregate medians and specifies the next evidence-gathering step. It uses all score groups and mixes within the selected months. |
| Data & limits | Explains data preparation, privacy behavior, model scope, and decision-use limitations. |

The sidebar provides a month-range slider and filters for score groups and credit mix. The portfolio-movement page intentionally uses all score groups and credit mixes within the selected months so that selecting one score category does not erase the start-to-end movement.

The UI is designed for aggregate business analysis and decision support. It has no individual lookup, row-level display, automated eligibility decision, default prediction, or personalized credit recommendation.

## 9. Business recommendations and measurement plan

The dashboard can prioritize analysis and decision design, but it cannot prove a positive impact. The following are recommended business-analysis workstreams:

1. **Portfolio monitoring:** track score-label mix, payment-delay distribution, debt exposure, and inquiry volume over time. Set materiality thresholds and review owners before treating a change as an operational signal.
2. **Driver validation:** test whether credit mix, payment indicators, debt, inquiries, and history are available at decision time, stable across periods, and incremental to a defined outcome.
3. **Outcome linkage:** join governed repayment, delinquency, application, approval, and revenue data to measure actual business impact rather than label association.
4. **Decision experiment:** where a process, workflow, or offer is changed, use a time-separated comparison or controlled test with a pre-specified success metric.
5. **Model governance:** retain human review for consequential decisions; document input lineage, threshold rationale, monitoring, and segment performance before operational deployment.

For every operating change, define a decision owner, baseline period, comparison group, primary outcome, follow-up window, and escalation procedure before launch. Prefer a randomized holdout or time-separated backtest when appropriate. Do not substitute dashboard engagement for verified repayment, approval, or revenue outcomes. Evaluate stability, missingness, segment performance, and unintended consequences alongside any business metric.

A future measurement dataset needs verified outcome fields such as repayment status, delinquency timing, product application and approval events, policy decisions, conversion, revenue, and post-decision performance. Governance review is needed before adding or joining such data.

## 10. Limitations and responsible use

- The outcome is a supplied score category, not a numeric bureau score or observed default.
- The dataset has repeated monthly observations; row-level charts can overstate the number of independent people.
- The data's sampling method, time period, representativeness, and field definitions are not documented here.
- Currency and precise units are unverified. The dashboard retains source units and labels them as such.
- Credit utilization is not assumed to be a percent.
- Hypothesis tests are exploratory and no multiple-testing adjustment is documented.
- A predictive score-label model is not a credit-risk model and must not determine eligibility, pricing, or approval.
- Correlation and group differences do not show that changing one attribute will improve a customer's label.
- The original CSV includes direct identifiers. Keep it out of public repositories, public hosting, and public report attachments.
- Inspect notebook outputs before sharing because exploratory notebook cells may contain source rows.

## 11. Local use and deployment status

### Run locally on Windows

1. Keep the authorized local dataset next to app.py as dataset-2.csv.
2. Double-click run_dashboard.bat. It creates the virtual environment if needed, installs requirements when imports are unavailable, starts Streamlit, and opens the browser.
3. If the browser does not open automatically, visit http://127.0.0.1:8501.
4. Docker is not required.

### Cloud preparation

The public deployment uses the bundled synthetic `data/credit_health_demo.csv`; it is safe for demonstration but does not represent real customers or Paisabazaar operations. For authorized private analysis, use an approved de-identified source in private storage and set `PAISABAZAAR_DATA` to its path. Do not upload the source CSV to a public repository or public demo.

## 12. Project files

| File | Role |
|---|---|
| app.py | Streamlit dashboard code. |
| Sample_ML_Submission_Templatedone_.ipynb | Analysis notebook, chart experiments, profile-level statistical tests, and score-label model benchmark. |
| dataset-2.csv | Local source data. Contains direct identifiers; excluded from Git and should remain private. |
| data/credit_health_demo.csv | Synthetic public dataset used by the deployed dashboard. |
| requirements.txt | Python dependencies for notebook and dashboard. |
| run_dashboard.bat | One-click Windows launcher for local use. |
| render.yaml | Render service configuration; does not deploy or provide the dataset by itself. |
| README.md | Short setup, privacy, and scope notes. |

## 13. Conclusion

The project provides an interactive, aggregate-level view of credit-profile patterns and a foundation for data-backed business decision design. In this dataset, reported payment delays, debt, credit mix, income, and inquiries vary across the supplied score categories. Most profiles retain the same first-to-last category across the eight snapshots, while smaller groups move up or down.

The business opportunity is to turn these patterns into governed portfolio monitoring, hypothesis testing, and outcome measurement. This analysis does not demonstrate that Paisabazaar has reduced defaults, improved approvals, or increased revenue. It is a decision-support dashboard and portfolio-analysis demonstration, not a production credit-decision platform.

## 14. Project artifacts and source basis

This report is based on the local project artifacts: the supplied dataset-2.csv, the Jupyter notebook Sample_ML_Submission_Templatedone .ipynb, and the Streamlit dashboard code in app.py. Figures and metrics are summarized from the project's saved analysis and are subject to the data-definition and sampling limitations described above. No external portfolio, bureau, repayment, or campaign data was used.

## 15. Suggested next steps

1. Confirm data provenance, sampling, date coverage, units, and the business meaning of each field with the data owner.
2. Review the notebook's saved outputs and remove any displayed customer-level data before sharing the notebook.
3. Agree on privacy, consent, retention, and access controls before using any customer data outside the local environment.
4. Define a priority business decision, owner, comparison strategy, and pre-specified primary outcome.
5. Add verified repayment, delinquency, application, approval, policy-decision, conversion, and revenue outcomes only under appropriate governance.
6. Evaluate each decision rule or process change with confidence intervals, stability checks, segment performance, and a documented decision rule.
7. Revisit the predictive benchmark only if there is a valid operational target, reliable time-available predictors, an independent temporal validation set, and a clear human-review process.

---
