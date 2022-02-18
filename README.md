# Affirm Upward Project
This project is to create an endpoint to allow existing merchant to setup configurations for pre-approval of loan application. This endpoint accepts three input parameters which are **minimum loan amount, maximum loan amount, and pre-qualification enabled** and returns the **merchant id** of the merchant if successful. 

Each parameter is described as follows: 
- Minimum loan amount: the minimum amount a user can get a loan for (in cents)
- Maximum_loan_amount: the maximum amount a user can get a loan for (in cents)
- Prequal_enabled: a boolean indicating if the Prequal feature will be enabled for that merchant

# Design Decisions
Design decisions when creating this endpoint are as follows:
- Both the minimum loan amount and maximum loan amount must be **non-negative** float values.
- The maximum loan amount must be **greater than minimum loan amount**. It is assumed that it is impractical for a merchant to have the same max and min loan amount. 
- True and False booleans are treated as 1 and 0 respectively. **A validator is created to handle these cases**
- Loan amount with **leading zero** (ex: 0100) is automatically handled by python and an TypeErorr will be thrown

# Future Improvements
One future improvement is to use a database such as SQL to manage the stored data instead of in-memory storage. 

# Special Notes
It was discovered that the instructions provided in "README" for Python was written for Mac/Linux OS only. Additionally, the instructions are slightly outdated. A README(WINDOWS) is provided for future references.
