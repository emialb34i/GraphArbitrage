from data import *

if __name__ == '__main__':
    exchange_pairs()
    d = spot_rates_snapshot()
    df = create_adj_matrix(d)
