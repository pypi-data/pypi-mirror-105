Financedata allows you to extract daily financial data from yahoo.

Other sources will be added in the future.
===========================================================

Quick Start

Fetching FX data

from DataFinder import data
df = data.financeFXData(
                    "USDTRY", ##Symbol
                    "2021-01-01", ##Start Date
                    "2021-05-11") ##End Date


Fetching Stock data

df = data.financeData(
                    "TSLA",         ##Symbol
                    "NASDAQ",       ##Stock Market
                    "2021-01-01",   ##Start Date
                    "2021-05-11")   ##End Date
                    
                    
*For BIST companies

df = data.financeData(
                    "CCOLA",         ##Symbol
                    "Bist",       ##Stock Market
                    "2021-01-01",   ##Start Date
                    "2021-05-11")   ##End Date
                    
                    