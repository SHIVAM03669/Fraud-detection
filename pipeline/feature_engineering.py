def add_features(df):
    # example: transaction frequency (if user id exists)
    # skipping user_id since dataset doesn't have it

    # time-based normalization
    df['Time'] = df['Time'] / df['Time'].max()

    return df