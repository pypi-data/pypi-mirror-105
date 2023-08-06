import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
import os
from preprocess.config.config import Regressor

def load_dataset():
    config_regressor = Regressor()
    df_ecommerce = pd.read_csv(os.path.join(config_regressor.DATA_PROCESSED, 'data_ecommerce.csv'))
    df_mkt_funnel = pd.read_csv(os.path.join(config_regressor.DATA_PROCESSED, 'data_mkt_funnel.csv'))
    df = df_ecommerce[
        ['order_id', 'product_category_name', 'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
         'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']].merge(
        df_mkt_funnel[
            ['order_id', 'origin', 'business_segment', 'lead_type', 'lead_behaviour_profile', 'has_company', 'has_gtin',
             'average_stock', 'business_type', 'declared_product_catalog_size', 'declared_monthly_revenue', 'price']],
        how='inner', on='order_id')
    config
    return df


df = load_dataset()
print(df.head())
