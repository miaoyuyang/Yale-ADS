#!/usr/bin/env python
# coding: utf-8
"""
@author: Miaoyu Yang
"""
# Readme<br>
# For this recommendation, the<br>
# beta<br>
# Current price<br>
# Target price<br>
# Total ESG score<br>
# Peer esg percentile<br>
# Dividend yield<br>
# is considered<br>
# For some stock, if some parameters are missing, the considering part involving those parameters will be ignored.<br>
# The beta is slightly considered (weight 1) since I want to give the target price more weight.<br>
# If the client is growth, the weight of the difference between target price and current price will be adjusted to 20 (default 10).<br>
# If the client is income, the weight of the dividend yield will be adjusted to 10 (default 1).<br>
# If the client is esg, the weight of the esg will be adjusted to 10 (default 1).<br>
# For final decision, the score ratio (total score / total weight) should be a valued centered by 1.0. A 1.0 score means the stock is neither good nor bad, you should HOLD.<br>
# If the score is above 1.1, means the stock is a good one, it is cheap and hava a good performance in client portfolio, you should BUY.<br>
# If the score is below 0.9, means the stock is a bad one, it is expensive and have a poor performance in client portfolio, you should SELL.<br>
# That is it, have fun!

import pandas as pd
import yfinance as yf
import numpy as np
from yahoofinancials import YahooFinancials



def invest(ticker, client=False):
    ticker = ticker.upper()
    #get the ticker form yfinance and yahoofinancials
    ticker_yf = yf.Ticker(ticker)
    #print(ticker_yf.info)
    ticker_yfal = YahooFinancials(ticker)
    """
    except:
        print("The input ticker \'"+ ticker+"\' is invalid, please try again. A \'Hold\' is returned as default.")
        return "Hold"
    """
    total_score = 0
    total_weight = 0
    esg_weight = 1
    income_weight = 1
    growth_weight = 10
    
    weight_table = {"beta":1,'target_current_diff':10}
    beta = ticker_yf.info['beta']
    currentPrice = ticker_yf.info['currentPrice']
    targetPrice = ticker_yf.info['targetMeanPrice']
    #peRatio = ticker_yf.info['trailingPE']
    industry = ticker_yf.info['industry']
    totalEsg = None
    esg_percentile = None
    dividend_yield = None
    peRatio = None
    
    print(f"Explanation of the stock {ticker}.\n")
    if beta is not None:
        total_score += (1.0-beta)*weight_table['beta']
        total_weight += weight_table['beta']
        
        if beta > 1.0:
            print(f'The beta of ticker {ticker} is {beta},which is higher than the beta of S & P 500. It is a relatively risky stock.')
        else:
            print(f'The beta of ticker {ticker} is {beta},which is lower than the beta of S & P 500. It is a relatively stable stock.')
        print(f'Since the beta is not strongly considered in this recommendation, it does not contribute much for the fina decision.')
    print()
    if (currentPrice is not None) and (targetPrice is not None):
        if client == "growth":
            growth_weight = 20
            print(f"Given the client using a {client} portfolio. the weight of the target price is higher in this recommendation.")
        else:
            print(f"The cliient is not highly considering growth, therefore the weight of the target price is mildly considered.")
        tc = ((targetPrice)/currentPrice ) * growth_weight
        
        total_score += tc
        total_weight += growth_weight
        tcp = 'higher' if targetPrice>currentPrice else 'lower'
        action = 'Buy' if targetPrice>currentPrice else 'Sell'
        print(f'To estimate the growth part, the current price and target price are considered.')
        print(f'The current price is ${currentPrice}.')
        print(f'The target price is ${targetPrice}, which is {tcp} than current price with a ratio {targetPrice/currentPrice}')
        print(f"Since the difference between target price and current price is strongly considered, a {tcp} target price will strongly drag the decision to {action}.")
        
    #if (peRatio is not None):
    try:
        sus = ticker_yf.sustainability
        #print(sus)
        for i,row in sus.iterrows():
            if i == "totalEsg":
                totalEsg = row.Value
            elif i == "percentile":
                esg_percentile = row.Value
    except:
        pass
    print()
    if totalEsg is not None:
        if client == "esg":
            esg_weight = 5
            print(f"Given the client using a {client} portfolio. the weight of the ESG is higher in this recommendation.")
        else:
            print(f"The cliient is not highly considering esg, therefore the weight of ESG is weakly considered.")
        total_score += (1+(50-totalEsg)/50)*esg_weight
        total_weight += esg_weight
        
        total_score += (1+(50-esg_percentile)/50)*esg_weight
        total_weight += esg_weight
        total_esg_p = 'lower' if totalEsg < 50 else 'higher'
        pp = 'lower' if esg_percentile < 50 else 'higher'
        action_t = "Buy" if  totalEsg < 50 else 'Sell'
        action_p = "Buy" if esg_percentile  < 50 else 'Sell'
        print(f'To estimate the esg part, the total esg score and peer esg percentile are considered.')
        print(f'The lower the total esg, the better the stock proform in sustainability.')
        print(f'The lower the peer esg percentile, the better the stock proform in sustainability.')
        print(f'The total esg is {totalEsg}, which is {total_esg_p} than 50, that will drag the decision to {action_t}.')
        print(f'The peer esg percentile is {esg_percentile}, which is {pp} than 50, that will drag the decision to {action_p}.')
        
    try:
        dividend_yield = ticker_yfal.get_dividend_yield()
    except:
        pass
    print()
    if dividend_yield is not None:
        if client == "income":
            income_ratio = 10
            print(f"Given the client using a {client} portfolio. the weight of the dividend and yield is higher in this recommendation.")
        else:
            print(f"The cliient is not highly considering income, therefore the weight of the dividend and yield is weakly considered.")
        total_score += (1+dividend_yield)*income_weight
        total_weight += income_weight
        
        print(f'To estimate the income part, the dividend and yield is considered.')
        print(f'The higher the dividend and yield, the better the stock proform in income.')
        print(f"The dividend and yield is {dividend_yield}. A higher dividend and yield will contribute more to the desision to Buy.")
    
    
    
    score = total_score/total_weight
    print(f"For the stcok {ticker}, the standard score is {total_weight}, while the total socre is {total_score}.")
    print(f"The score ratio = total score / standard score = {score}.")
    print(f"If the score ratio < 0.9, means the stock is expensive and underperformed, the recommendation is Sell.")
    print(f"If the score ratio between 0.9 and 1.1, means the stock is just normal valued, the recommendation is Hold.")
    print(f"If the score ratio > 1.1, means the stock is cheap and overperformed, the recommendation is Buy.")
    
    answer = None
    if score < 0.9:
        answer =  "Sell"
    elif score < 1.1:
        answer =  "Hold"
    else:
        answer =  "Buy"
        
    print(f"\nTherefore, the recommendation of stock {ticker} is {answer}.")
    return answer

print(invest("aapl",client='esg'))




