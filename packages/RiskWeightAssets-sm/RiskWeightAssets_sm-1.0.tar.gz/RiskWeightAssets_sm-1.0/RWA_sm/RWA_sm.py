import numpy as np
from scipy.stats import norm


def expected_loss_as_percentage(df):
    """Represents the Expected Loss (EL) as a percentile value."""
    df["Expected Loss (%)"] = df["masterpdtal"] * df["LGDtal"]
    return df["Expected Loss (%)"].astype(float)


def asset_correlation(df):
    """Calculates the Asset Correlation (rho)"""
    df["rho"] = np.nan
    avc_true = df["FinancialInstitution"] == True
    avc_false = df["FinancialInstitution"] == False
    df.loc[avc_true, "rho"] = 1.25 * (0.12 * (1 - np.exp(-50.0 * df.loc[avc_true, "masterpdtal"]) / 1 - np.exp(-50.0)) + 0.24 * (1 - (1 - np.exp(-50.0 * df.loc[avc_true, "masterpdtal"]) / 1 - np.exp(-50.0))))
    df.loc[avc_false, "rho"] = 1.00 * (0.12 * (1 - np.exp(-50.0 * df.loc[avc_false, "masterpdtal"]) / 1 - np.exp(-50.0)) + 0.24 * (1 - (1 - np.exp(-50.0 * df.loc[avc_false, "masterpdtal"]) / 1 - np.exp(-50.0))))
    return df["rho"].astype(float)


def k(df):
    """Calculates the Capital Requirement(Unexpected Loss) `k`."""
    df["Probability Density"] = norm.cdf(norm.ppf(df["masterpdtal"]) + df["rho"] ** 0.5 * norm.ppf(0.999) / (1.0 - df["rho"]) ** 0.5)
    df["Conditional Expected Loss"] = (df["LGDtal"] * df["Probability Density"])
    df["k"] = (df["Conditional Expected Loss"] - df["Expected Loss (%)"])
    return df["k"].astype(float)


def rwa(df):
    df["RWA"] = df["k"] * 12.5 * df["EADTotalKFtalBelopp"] # * ADJ FACT?          # Justeringsfaktor enligt basel 1.06 för end of day justering?
    return df["RWA"]