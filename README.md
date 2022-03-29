# CSCE-470-Project

## How to setup the environment to execute the code
1. Clone this repository
2. In your terminal, navigate to within this repository's folder. (e.g. with `cd ~/CSCE-470-Project`)
3. Execute the command `python3 python/test.py`. It will prompt you to enter a query statement that will be searched within our songs collection (data/azlyrics-csv).

## BM25 Equation
The following is the core algorithm that we decided to follow in order to implement docment ranking amongs our song collection.
![BM25 Equation](./imgs/BM25Equation.png)

### IDF Equation

![IDF Equation](./imgs/IDFEquation.png)

### IDF Equation (Accounts for negatives)
This IDF equation accounts for negative IDFs by adding 1 to all IDFs. \
![IDF Accounting for Negatives](./imgs/IDFEquation1.png)
