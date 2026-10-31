# Predictive Modeling and Risk Scoring for Bank Customer Churn

## Abstract

This project develops an educational churn-risk workflow for a 10,000-customer bank dataset. The outcome is `Exited`, where 1 denotes a customer who exited. The dataset has 2,037 churned customers (20.37%) and 7,963 retained customers (79.63%). The workflow compares Logistic Regression and Random Forest using a stratified holdout, reports threshold-dependent classification measures and ROC-AUC, and provides customer-level probability estimates in a Streamlit interface. Exploratory differences by geography, activity, age, gender, and product count motivate further investigation; they are associations in this dataset and do not establish causes of churn. Final model metrics must be copied from the app after training and are intentionally not invented here.

## 1. Background and objective

Customer attrition can reduce customer lifetime value, revenue stability, and opportunities to serve customers with additional products. A predictive score can help prioritize review and retention outreach before a customer leaves. This project aims to estimate the probability of `Exited = 1`, identify patterns associated with the model's predictions, and let an analyst inspect how a hypothetical profile changes its score.

The system is a decision-support prototype. A score alone does not establish that a customer intends to leave or that a specific offer will prevent it. Human review and measured intervention outcomes are required before operational use.

## 2. Dataset and preparation

The supplied file, `European_Bank.csv`, was shared through the project Google Drive link. It contains 10,000 rows and 14 columns: `Year`, `CustomerId`, `Surname`, `CreditScore`, `Geography`, `Gender`, `Age`, `Tenure`, `Balance`, `NumOfProducts`, `HasCrCard`, `IsActiveMember`, `EstimatedSalary`, and `Exited`.

There are no missing values, no exact duplicate rows, and no duplicate customer IDs in the inspected file. `Exited` contains 7,963 zeros and 2,037 ones. Every record has `Year = 2025`; this constant field has no discriminatory information and is excluded. `CustomerId` and `Surname` are excluded because they are identifiers rather than useful generalizable predictors. The remaining categorical fields are one-hot encoded. Numeric missing values are median-imputed and scaled within the model pipeline (the supplied data has none missing). Unknown categories are safely ignored at prediction time.

The pipeline also derives balance-to-salary ratio, product density (`NumOfProducts / (Tenure + 1)`), engagement-product interaction, and age-tenure interaction. These engineered variables are hypotheses for model comparison, not established business drivers.

## 3. Exploratory findings

The overall churn rate is 20.37%. The following rates are raw subgroup summaries, not adjusted estimates:

| Group | Customers | Churn rate |
|---|---:|---:|
| France | 5,014 | 16.15% |
| Germany | 2,509 | 32.44% |
| Spain | 2,477 | 16.67% |
| Female | 4,543 | 25.07% |
| Male | 5,457 | 16.46% |
| Inactive | 4,849 | 26.85% |
| Active | 5,151 | 14.27% |

Churn varies by product count: 27.71% for one product (5,084 customers), 7.58% for two products (4,590), 82.71% for three products (266), and 100% for four products (60). The last two groups are small, especially the four-product group, so these rates are uncertain and should not be treated as stable population effects.

Age-band churn rates are 7.56% below age 30 (n=1,641), 10.88% at 30–39 (n=4,346), 30.79% at 40–49 (n=2,618), 56.04% at 50–59 (n=869), and 27.95% at 60 or above (n=526). Mean age is 44.84 among churners and 37.41 among retained customers. Mean balance is 91,108.54 for churners and 72,745.30 for retained customers. Mean tenure is similar (4.93 versus 5.03 years), as are mean product counts (1.48 versus 1.54).

These comparisons are descriptive. Differences can reflect confounding among variables, data collection choices, or subgroup sizes. Demographic attributes such as age, gender, and geography require careful fairness review; the app's feature importance is a model explanation, not a causal explanation.

## 4. Modeling and evaluation plan

The target is `Exited`; positive class 1 means churn. A fixed random seed and stratified 80/20 train-test split preserve the class ratio. Preprocessing is fitted on the training portion through a scikit-learn pipeline to prevent information leakage. The app offers:

1. Logistic Regression with class weighting as an interpretable baseline.
2. Random Forest with class weighting as a nonlinear tree-based comparison.

The dashboard reports accuracy, precision, recall, F1, ROC-AUC, a confusion matrix, ROC curve, and the distribution of holdout probabilities. Accuracy is shown alongside class-sensitive measures because a majority-class prediction would already be correct for 79.63% of this imbalanced dataset. Precision reflects the share of flagged customers who churned; recall reflects the share of churners detected. The threshold is adjustable, so precision and recall will change with it. Threshold choice should reflect outreach capacity and the relative cost of missed churn versus unnecessary contact.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | Fill from app | Fill from app | Fill from app | Fill from app | Fill from app |
| Random Forest (threshold 0.50) | 0.853 | 0.659 | 0.575 | 0.614 | 0.862 |

Use the same holdout split and threshold when comparing models. Select a model based on the business objective, not accuracy alone. Before relying on probabilities, assess calibration and subgroup performance on a separate evaluation process. The selected model is then refit on all labeled rows for the app's illustrative risk calculator; holdout metrics remain the reported evaluation results.

## 5. Application

The Streamlit application provides dataset preview and missing-value counts, model selection, a threshold control, holdout metrics and plots, feature-importance visualization, and a customer-profile risk calculator. It excludes identifiers and constant fields. The feature-importance chart uses absolute Logistic Regression coefficients or Random Forest impurity importance. Neither proves causation. The what-if calculator returns model estimates for the entered profile and should be used to explore sensitivity, not to claim a real intervention's effect.

## 6. Recommendations and limitations

The raw summaries suggest examining whether German-market customer experience, inactivity, age-related needs, and product utilization merit deeper research. For the unusual three- and four-product churn rates, first validate the records and investigate customer journeys before designing actions. A bank should test targeted, non-coercive service improvements through controlled experiments and measure retention, customer outcomes, and costs.

Important limitations include the single 2025 snapshot, lack of observed event timing and outreach history, class imbalance, no evidence of representativeness, potential proxy effects in demographic features, and no causal identification. The dataset may be synthetic or educational; do not assume it represents a real bank's current customers. There is no calibration study or external validation in this project. Model scores can become stale as customer behavior and products change.

## 7. Conclusion

The project turns a customer-level churn dataset into an explainable, interactive modeling workflow. The data show meaningful descriptive differences across several groups, but only a controlled holdout evaluation can establish predictive performance, and neither predictive importance nor a high score proves why a customer will leave. Complete the results table from the app, record the limitations, and keep any real retention decision under human review.

## Reproducibility

Install `requirements.txt`, then run `streamlit run app.py`. The app automatically loads `data/European_Bank.csv`, which is deliberately excluded from version control. Record the model, threshold, holdout metrics, and date in the final submission.
