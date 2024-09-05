import numpy as np
import pandas as pd


# placeholder
def test():
    return "hello world"


# %% Copied from recent speed sensitivity work
def read_data(path="./data/SampleData.csv"):
    df = pd.read_csv(path, header=0)
    df.dropna(axis=0, inplace=True)
    return df


def power_law_exponent(Zo):
    return 0.24 + 0.096 * np.log10(Zo) + 0.016 * (np.log10(Zo) ** 2)


def power_law(z, z_ref, Zo):  #   u/Uref = (z/Zo)**n
    n = power_law_exponent(Zo)
    return (z / z_ref) ** n


def percent_turbulence(z, Zo):
    n = power_law_exponent(Zo)
    # operate on a series of z
    try:
        z = pd.Series(z)
        t1 = n * np.log(30 / Zo) / np.log(z[z < 100] / Zo)
        t2 = n * (np.log(30 / Zo)) / np.log(100 / Zo) + (z[z >= 100] - 100) / 500 * (
            0.01 - n * np.log(30 / Zo) / np.log(100 / Zo)
        )
        t = pd.concat([t1, t2])

    # operate on a single z
    except:
        if z < 100:
            t = n * np.log(30 / Zo) / np.log(z / Zo)
        else:
            t = n * (np.log(30 / Zo)) / np.log(100 / Zo) + (z - 100) / 500 * (
                0.01 - n * np.log(30 / Zo) / np.log(100 / Zo)
            )
    return t * 100
