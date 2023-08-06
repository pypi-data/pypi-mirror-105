import pathlib
import os
import preprocess


class Regressor:

    def __init__(self):
        self.PACKAGE_ROOT = None
        self.DATA_PREPROCESS = None
        self.TARGET = None
        self.FILE_NAME_FUNNEL = None
        self.FILE_NAME_ECOMMERCE = None
        self.DROP_FEATURES = None
        self.CATEGORICAL_VARS_WITH_NA = None
        self.NUMERICAL_VARS_WITH_NA = None
        self.NUMERICALS_LOG_VARS = None
        self.CATEGORICAL_VARS = None
        self.SELECTED_VARS = None
        self.PIPELINE_NAME = None
        self.PIPELINE_SAVE_FILE = None

    def package_root(self):
        self.PACKAGE_ROOT = pathlib.Path(preprocess.__file__).resolve().parent
        return self.PACKAGE_ROOT

    def data_dir(self):
        package_root = self.package_root()
        self.DATA_PREPROCESS = os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(package_root))),
                         'data'), 'preprocess')
        return self.DATA_PREPROCESS

    def data_names(self):
        self.TARGET = "price"
        self.FILE_NAME_ECOMMERCE = 'data_ecommerce.csv'
        self.FILE_NAME_FUNNEL = 'data_mkt_funnel.csv'
        return self.TARGET, self.FILE_NAME_ECOMMERCE, self.FILE_NAME_FUNNEL

    def features(self):
        self.DROP_FEATURES = ['has_company', 'has_gtin', 'average_stock']

        self.SELECTED_VARS = ['product_name_lenght', 'product_description_lenght', 'product_weight_g',
                              'product_length_cm',
                              'product_height_cm', 'origin', 'business_segment', 'lead_type',
                              'lead_behaviour_profile', 'business_type']
        return self.DROP_FEATURES, self.SELECTED_VARS

    def pipeline_regressor(self):
        self.PIPELINE_NAME = "regression"
        self.PIPELINE_SAVE_FILE = f"{self.PIPELINE_NAME}_output"
        return self.PIPELINE_NAME, self.PIPELINE_SAVE_FILE
