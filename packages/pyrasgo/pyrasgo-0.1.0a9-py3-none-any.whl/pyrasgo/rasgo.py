import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import webbrowser

from pyrasgo.api.create import Create
from pyrasgo.api.delete import Delete
from pyrasgo.api.get import Get
from pyrasgo.api.match import Match
from pyrasgo.api.publish import Publish
from pyrasgo.api.read import Read
from pyrasgo.api.save import Save
from pyrasgo.api.update import Update

from pyrasgo.primitives.feature import Feature, FeatureList
from pyrasgo.primitives.feature_set import FeatureSet
from pyrasgo.primitives.source import DataSource
from pyrasgo.primitives.collection import Collection

from pyrasgo import schemas as api
from pyrasgo.schemas.enums import Granularity, ModelType

from pyrasgo.storage.dataframe.evaluate  import Evaluate

from pyrasgo.utils import ingestion
from pyrasgo.utils.monitoring import track_usage


class Rasgo():
    """
    Base connection object to handle interactions with the Rasgo API.
    """
    from pyrasgo.version import __version__
    from pyrasgo.storage import dataframe as df

    def __init__(self, api_key: str):
        self.get = Get(api_key=api_key)
        self.match = Match(api_key=api_key)
        self.create = Create(api_key=api_key)
        self.update = Update(api_key=api_key)
        self.publish = Publish(api_key=api_key)
        self.read = Read(api_key=api_key)
        self.delete = Delete(api_key=api_key)
        self.save = Save(api_key=api_key)
        self.df.evaluate = Evaluate(api_key=api_key)

    def open_docs(self):
        webbrowser.open("https://docs.rasgoml.com/rasgo-docs/pyrasgo/pyrasgo-getting-started")

    def pronounce_rasgo(self):
        webbrowser.open("https://www.spanishdict.com/pronunciation/rasgo?langFrom=es")

# ---------
# Get Calls
# ---------
    @track_usage
    def get_collection(self, collection_id: int) -> Collection:
        """
        Returns a Rasgo Collection (set of joined Features) matching the specified id
        """
        return self.get.collection(collection_id)

    @track_usage
    def get_collection_attributes(self, collection_id: int) -> api.CollectionAttributes:
        """
        Returns a dict of attributes for a collection
        """
        return self.get.collection_attributes(collection_id)

    @track_usage
    def get_collections(self, include_shared: bool=False) -> List[Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) that I have author access to. Add an include_shared 
        parameter to return all Rasgo Collections that I have any access to (author or shared access)
        :param include_shared: Boolean value indicating if the return should include all accessible collections
        """
        return self.get.collections(include_shared=include_shared)

    @track_usage
    def get_collections_by_attribute(self, key: str, value: str = None) -> List[Collection]:
        """
        Returns a list of Rasgo Collections that match an attribute
        """
        return self.get.collections_by_attribute(key, value)

    @track_usage
    def get_columns_by_featureset(self, feature_set_id: int) -> List[api.Column]:
        """
        Returns all Columns in the specified FeatureSet
        """
        self.get.columns_by_featureset(feature_set_id)

    @track_usage
    def get_data_sources(self) -> List[DataSource]:
        """
        Returns all DataSources available in your organization or Rasgo Community
        """
        return self.get.data_sources()

    @track_usage
    def get_data_source(self, data_source_id: int) -> DataSource:
        """
        Returns the DataSource with the specified id
        """
        return self.get.data_source(data_source_id)

    @track_usage
    def get_data_source_columns(self, data_source_id: int) -> List[api.DataSourceColumn]:
        """
        Returns columns in the DataSource with the specified id
        """
        return self.get.data_source_columns(data_source_id)

    @track_usage
    def get_data_source_stats(self, data_source_id: int):
        """
        Returns the stats profile of the specificed data source
        """
        return self.get.data_source_stats(data_source_id)

    @track_usage
    def get_dimensionalities(self) -> List[api.Dimensionality]:
        """
        Returns all Dimensionalities available in your organization or Rasgo Community
        """
        return self.get.dimensionalities()
    
    @track_usage
    def get_feature(self, feature_id: int) -> Feature:
        """
        Returns the Feature with the specified id
        """
        return self.get.feature(feature_id)
    
    @track_usage
    def get_feature_attributes(self, feature_id: int) -> api.FeatureAttributes:
        """
        Returns a dict of attributes for a feature
        """
        return self.get.feature_attributes(feature_id)

    @track_usage
    def get_feature_attributes_log(self, feature_id: int) -> tuple:
        """
        Returns a list of all attributes values logged to a feature over time
        """
        return self.get.feature_attributes_log(feature_id)

    @track_usage
    def get_feature_set(self, feature_set_id: int) -> FeatureSet:
        """
        Returns the FeatureSet (set of Fetures) with the specified id
        """
        return self.get.feature_set(feature_set_id)

    @track_usage
    def get_feature_sets(self) -> List[FeatureSet]:
        """
        Returns a list of FeatureSets (set of Features) available in your organization or Rasgo Community
        """
        return self.get.feature_sets()

    @track_usage
    def get_feature_stats(self, feature_id: int) -> Optional[api.FeatureStats]:
        """
        Returns the stats profile for the specified Feature
        """
        return self.get.feature_stats(feature_id)
    
    @track_usage
    def get_features(self) -> FeatureList:
        """
        Returns a list of Features available in your organization or Rasgo Community
        """
        return self.get.features()

    @track_usage
    def get_features_by_attribute(self, key: str, value: str = None) -> List[Feature]:
        """
        Returns a list of features that match an attribute
        """
        return self.get.features_by_attribute(key, value)

    @track_usage
    def get_features_by_featureset(self, feature_set_id) -> FeatureList:
        """
        Returns a list of Features in the specific FeatureSet
        """
        return self.get.features_by_featureset(feature_set_id)

    @track_usage
    def get_shared_collections(self) -> List[Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) shared in my organization or in Rasgo community
        """
        return self.get.shared_collections()

    @track_usage
    def get_source_columns(self, table: Optional[str] = None, database: Optional[str] = None, schema: Optional[str] = None, data_type: Optional[str] = None) -> pd.DataFrame:
        """
        Returns a DataFrame of columns in Snowflake tables and views that are queryable as feature sources
        """
        return self.get.source_columns(table, database, schema, data_type)

    @track_usage
    def get_source_tables(self, database: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        Return a DataFrame of Snowflake tables and views that are queryable as feature sources
        """
        return self.get.source_tables(database, schema)


# -------------------
# Post / Create Calls
# -------------------
    @track_usage
    def create_collection(self, name: str,
                          type: Union[str, ModelType],
                          granularity: Union[str, Granularity],
                          description: Optional[str] = None,
                          is_shared: Optional[bool] = False) -> Collection:
        return self.create.collection(name, type, granularity, description, is_shared)

    @track_usage
    def put_collection_attributes(self, collection_id: int, attributes: List[dict]):
        """
        Create or update attributes on a Rasgo Collection

        param attributes: dict [{"key": "value"}, {"key": "value"}]
        """
        return self.update.collection_attributes(collection_id, attributes)

    @track_usage
    def put_feature_attributes(self, feature_id: int, attributes: List[dict]):
        """
        Create or update attributes on a feature

        param attributes: dict [{"key": "value"}, {"key": "value"}]
        """
        return self.update.feature_attributes(feature_id, attributes)


# ------------------
# Workflow Functions
# ------------------    
    @track_usage
    def prepare_feature_set_dict(self, feature_set_id: int = None):
        """
        Returns a dict of metadata values for the specificed Rasgo FeatureSet
        
        params
        ------
        feature_set_id: int: ID of a Rasgo FeatureSet
        
        Alternate Usage
        ---------------
        Pass in no params to return a blank featureset dict template
        """
        if feature_set_id:
            fs = self.get.feature_set(feature_set_id)
            return ingestion.save_feature_set_to_dict(fs)
        return ingestion.RASGO_DICT

    @track_usage
    def prepare_feature_set_yml(self, feature_set_id: int, file_name: str, directory: str = None):
        """
        Saves a yml file of metadata values for the specificed Rasgo FeatureSet to a directory location
        
        params
        ------
        feature_set_id: int: ID of a Rasgo FeatureSet
        file_name: str: name for the output file 
        directory: str: full dir location for the output file (minus file_name)
        """
        fs = self.get.feature_set_yml(feature_set_id)
        return ingestion.save_feature_set_to_yaml(fs, file_name=file_name, directory=directory)

    @track_usage
    def publish_features(self, features_dict: dict) -> FeatureSet:
        return self.publish.features(features_dict)

    @track_usage
    def publish_features_from_df(self, 
                                 df: pd.DataFrame, 
                                 dimensions: List[str], 
                                 features: List[str],
                                 granularity: List[str] = [], 
                                 tags: List[str] = [], 
                                 sandbox: bool = True) -> FeatureSet:
        """
        Creates a Feature Set from a pandas dataframe

        :dataframe: Pandas DataFrame containing all columns that will be registered with Rasgo
        :param dimensions: List of columns in df that should be used for joins to other featursets
        :param features: List of columns in df that should be registered as features in Rasgo
        :param granularity: List of grains that describe the form of the data. Common values are: 'day', 'week', 'month', 'second'
        :param tags: List of tags to be added to all features in the df
        :return: description of the featureset created
        """
        return self.publish.features_from_df(df, dimensions, features, granularity, tags, sandbox)

    @track_usage
    def publish_features_from_source(self, 
                                     data_source_id: int,
                                     features: List[str], 
                                     dimensions: List[str], 
                                     granularity: List[str] = [], 
                                     tags: List[str] = [],
                                     feature_set_name: str = None,
                                     sandbox: bool = True, 
                                     if_exists: str = 'fail') -> FeatureSet:
        """
        Publishes a FeatureSet from an existing DataSource table

        params:
            data_source_id: ID to a Rasgo DataSource
            features: List of column names that will be features
            dimensions: List of column names that will be dimensions
            granularity: List of grains that describe the form of the data. Common values are: 'day', 'week', 'month', 'second'
            tags: List of tags to be added to all features
            feature_set_name: Optional name for the FeatureSet (if not passed a random string will be assigned)

            if_exists:  fail - returns an error message if a featureset already exists against this table
                        return - returns the featureset without operating on it
                        edit - edits the existing featureset
                        new - creates a new featureset

        return:
            Rasgo FeatureSet
        """
        return self.publish.features_from_source(data_source_id, features, dimensions, granularity, tags, feature_set_name, sandbox, if_exists)

    @track_usage
    def publish_features_from_yml(self, 
                                  yml_file: str, 
                                  sandbox: Optional[bool] = True, 
                                  git_repo: Optional[str] = None) -> FeatureSet:
        """
        Publishes metadata about a FeatureSet to Pyrasgo

        :param yml_file: Rasgo compliant yml file that describes the featureset(s) being created
        :param sandbox: Status of the features (True = 'Sandboxed' | False = 'Productionized')
        :param git_repo: Filepath string to these feature recipes in git
        :return: description of the featureset created
        """
        return self.publish.features_from_yml(yml_file, sandbox, git_repo)

    @track_usage
    def publish_source_data(self, 
                            source_type: str, 
                            file_path: Optional[Path] = None, 
                            df: Optional[pd.DataFrame] = None, 
                            table: Optional[str] = None, 
                            table_database:Optional[str] = None, 
                            table_schema: Optional[str] = None,
                            data_source_name: Optional[str] = None, 
                            data_source_domain: Optional[str] = None, 
                            data_source_table_name: Optional[str] = None, parent_data_source_id: Optional[int] = None, 
                            if_exists: Optional[str] = 'fail'
                            ) -> DataSource:
        """
        Push a csv, Dataframe, or table to a Snowflake table and register it as a Rasgo DataSource (TM)

        NOTES: csv files will import all columns as strings

        params:
            source_type: Values: ['csv', 'dataframe', 'table']
            df: pandas DataFrame (only use when passing source_type = 'dataframe')
            file_path: full path to a file on your local machine (only use when passing source_type = 'csv')
            table: name of a valid Snowflake table in your Rasgo account (only use when passing source_type = 'table')
            table_database: Optional: name of the database of the table passed in 'table' param (only use when passing source_type = 'table')
            table_schema: Optional: name of the schema of the table passed in 'table' param (only use when passing source_type = 'table')
            
            data_source_name: Optional name for the DataSource (if not provided a random string will be used)
            data_source_table_name: Optional name for the DataSource table in Snowflake (if not provided a random string will be used)
            data_source_domain: Optional domain for the DataSource (default is NULL)
            parent_data_source_id: Optional ID of a valid Rasgo DataSource that is a parent to this DataSource (default is NULL)

            if_exists: Values: ['fail', 'append', 'replace'] directs the function what to do if a DataSource already exists with this table name  (defaults to fail)

        return:
            Rasgo DataSource
        """
        return self.publish.source_data(source_type, file_path, df, table, table_database, table_schema, data_source_name, data_source_domain, data_source_table_name, parent_data_source_id, if_exists)

    @track_usage
    def read_collection_data(self, 
                             collection_id: int,
                             filters: Optional[Dict[str, str]] = None,
                             limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo Collection

        :param collection_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        return self.read.collection_data(collection_id, filters, limit)

    @track_usage
    def read_feature_data(self, 
                          feature_id: int,
                          filters: Optional[Dict[str, str]] = None,
                          limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo Feature data

        :param feature_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        return self.read.feature_data(feature_id, filters, limit)

    @track_usage
    def read_source_data(self, 
                         source_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo DataSource

        :param source_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        return self.read.source_data(source_id, filters, limit)