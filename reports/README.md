# Original formatted case-study report

The portfolio build is based on the completed **Ad Click Prediction — CTR Modeling Submission** analysis and its polished formatted PDF:

`Ad_Click_Prediction_Submission_Formatted_Mohit_Bhatnagar.pdf`

The public repository keeps the analytical notebook and all validated benchmark facts in source control. The PDF is a presentation artifact and should be uploaded here unchanged once binary repository upload is available.

## Source-of-truth benchmark values

- 463,291 labeled impressions
- 31,331 clicks / 6.76% CTR
- selected model: CatBoost + personalization/interactions
- untouched temporal holdout ROC-AUC: 0.579538
- untouched temporal holdout PR-AUC: 0.078022

Do not replace these numbers with the synthetic public-demo model metrics.

## Binary upload checklist

Target repository path:

`reports/Ad_Click_Prediction_Submission_Formatted_Mohit_Bhatnagar.pdf`

When uploading through GitHub web or normal Git:

1. keep the exact filename above,
2. do not regenerate or alter the analytical content,
3. verify GitHub renders/downloads the PDF after commit,
4. update the README portfolio-assets section to link the PDF directly,
5. optionally attach the same PDF to the first tagged portfolio release.

The connected GitHub text-content tools used during this build can update source/Markdown but cannot safely attach the local binary PDF directly. That limitation does not affect the source notebook, benchmark evidence, or live application acceptance record.
