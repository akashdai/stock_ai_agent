from tools import stock_summary

def run_agent(query):

    query = query.upper().strip()

    return stock_summary(query)










