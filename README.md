# YocketProfilesExtractor

**WHAT**:

This is a small Python utility to extract historical data of filtered profiles from [Yocket](https://yocket.com/) and push it to the Google Sheets spreadsheet.

---

**WHY**:

While shortlisting universities for my MS applications, I wanted historical data to have an understanding of the profiles of applicants each university has admitted in recent years. While searching for the sources of this data, I came across Yocket, which contains a great deal of it. Yocket offers several filters on the [Yocket Connect](https://yocket.com/connect) listing page, but analysing this information is difficult because of:
* Listing page does not mention the GPA details of candidates
* Profile detail page cannot be opened in new tab
* When navigating to the profile detail page and then returning to the listing page, the user is always redirected to the top of the listing page rather than the point from which they originally navigated. Therefore, we must scroll back till the previous results.

I felt compelled to develop this simple utility to address these issues. This has greatly aided me in analysing the thousands of records, and I believe it could do the same for other people.

----

**HOW**:

Following are the files that need changes before running this application:
* **_google_service_account_creds.json_**: Download the Google credentials json from Google Cloud Platform and paste its content to this file. For the unversed, follow the steps [here](https://www.plus2net.com/python/pygsheets.php).
* **_credentials_config.properties_**: Add values for these properties from your Yocket account. Below is the screenshot for reference:
![alt text](https://github.com/gkamboj/YocketProfilesExtractor/blob/main/raw/Yocket_Token_UUID.png "Yocket account credentials")
* **_app_config.properties_**: This file is used to get the filtering parameters on the basis of which Yocket Connect data is fetched and then added to Google sheet. Change the properties such as MAX_GRE_SCORE (maximum GRE score to consider), MIN_GRE_SCORE (minimum GRE score to consider), MAX_CGPA (maximum GPA to consider), MIN_CGPA (minimum CGPA to consider), PLP_UNIVERSITY_ID (Yocket id of the university you want data of, you will get this through ways such as URL of the university page: for eg., [Stony Brook University](https://yocket.com/universities/state-university-of-new-york-at-stony-brook-735) id is 735), APPLICATION_STATUSES_TO_CHECK (to set the application statused to consider), GOOGLE_SHEET_NAME (name of the spreadsheet in which you want to store the data), GOOGLE_SHEET_WORKSHEET (worksheet number within the spreadsheet), etc.
* Give edit access of your Google Sheet spreadhseet to the _client_email_ value from the Google credentials json.

---

**OUTPUT**:

Following columns are populated in the spreadsheet:

| UniqueId | Name | University | Country | Expenses | Degree | MastersCourse | CGPA | Percentage | Backlogs | UG College | GRE | AWA | TOEFL | IELTS | WorkEx | Papers | Projects | Year | Term | Status | AppliedDate | DecisionDate |
| -------- | ---- | ---------- | ------- | -------- | ------ | ------------- | ---- | ---------- | -------- | ---------- | --- | --- | ----- | ----- | ------ | ------ | -------- | ---- | ---- | ------ | ----------- | ------------ |

