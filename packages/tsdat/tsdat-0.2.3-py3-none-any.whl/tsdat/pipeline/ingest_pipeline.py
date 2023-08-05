import re
import warnings
import xarray as xr
from typing import Dict, List, Union
from .pipeline import Pipeline
from tsdat.io.filehandlers import FileHandler
from tsdat.qc import QualityManagement
from tsdat.utils import DSUtil
from tsdat.config import DatasetDefinition, VariableDefinition
from .pipeline import Pipeline


class IngestPipeline(Pipeline):

    def run(self, filepath: Union[str, List[str]]) -> None:
        """-------------------------------------------------------------------
        Runs the Ingest Pipeline from start to finish.

        Args:
        ---
            filepath (str): The path to the file (or archive containing
                            a collection of files) to run the Ingest Pipeline 
                            on.
        -------------------------------------------------------------------"""
        # If the file is a zip/tar, then we need to extract the individual files
        with self.storage.tmp.extract_files(filepath) as file_paths:

            # Open each raw file into a Dataset, standardize the raw file names and store.
            raw_dataset_mapping: Dict[str, xr.Dataset] = self.read_and_persist_raw_files(file_paths)

            # Customize the raw data before it is used as input for standardization
            raw_dataset_mapping: Dict[str, xr.Dataset] = self.hook_customize_raw_datasets(raw_dataset_mapping)

            # Standardize the dataset and apply corrections / customizations
            dataset = self.standardize_dataset(raw_dataset_mapping)
            dataset = self.hook_customize_dataset(dataset, raw_dataset_mapping)

            # Apply quality control / quality assurance to the dataset.
            previous_dataset = self.get_previous_dataset(dataset)
            dataset = QualityManagement.run(dataset, self.config, previous_dataset)

            # Apply any final touches to the dataset and persist the dataset
            dataset = self.hook_finalize_dataset(dataset)
            dataset = self.store_and_reopen_dataset(dataset)

            # Hook to generate custom plots
            self.hook_generate_and_persist_plots(dataset)
    
    def hook_customize_dataset(self, dataset: xr.Dataset, raw_mapping: Dict[str, xr.Dataset]) -> xr.Dataset:
        """-------------------------------------------------------------------
        Hook to allow for user customizations to the standardized dataset such
        as inserting a derived variable based on other variables in the
        dataset.  This method is called immediately after the apply_corrections
        hook and before Quality Management occurs.

        Args:
        ---
            dataset (xr.Dataset): The dataset to customize.
            raw_mapping (Dict[str, xr.Dataset]):    The raw dataset mapping.

        Returns:
        ---
            xr.Dataset: The customized dataset.
        -------------------------------------------------------------------"""
        return dataset

    def hook_customize_raw_datasets(self, raw_dataset_mapping: Dict[str, xr.Dataset]) -> Dict[str, xr.Dataset]:
        """-------------------------------------------------------------------
        Hook to allow for user customizations to one or more raw xarray Datasets
        before they merged and used to create the standardized dataset.  The
        raw_dataset_mapping will contain one entry for each file being used
        as input to the pipeline.  The keys are the standardized raw file name,
        and the values are the datasets.

        This method would typically only be used if the user is combining
        multiple files into a single dataset.  In this case, this method may
        be used to correct coordinates if they don't match for all the files,
        or to change variable (column) names if two files have the same
        name for a variable, but they are two distinct variables.

        This method can also be used to check for unique conditions in the raw
        data that should cause a pipeline failure if they are not met.

        This method is called before the inputs are merged and converted to
        standard format as specified by the config file.

        Args:
        ---
            raw_dataset_mapping (Dict[str, xr.Dataset])     The raw datasets to
                                                            customize.

        Returns:
        ---
            Dict[str, xr.Dataset]: The customized raw dataset.
        -------------------------------------------------------------------"""
        return raw_dataset_mapping

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        """-------------------------------------------------------------------
        Hook to apply any final customizations to the dataset before it is
        saved. This hook is called after Quality Management has occured.

        Args:
            dataset (xr.Dataset): The dataset to finalize.

        Returns:
            xr.Dataset: The finalized dataset to save.
        -------------------------------------------------------------------"""
        return dataset

    def hook_generate_and_persist_plots(self, dataset: xr.Dataset) -> None:
        """-------------------------------------------------------------------
        Hook to allow users to create plots from the xarray dataset after 
        the dataset has been finalized and just before the dataset is
        saved to disk.

        To save on filesystem space (which is limited when running on the
        cloud via a lambda function), this method should only
        write one plot to local storage at a time. An example of how this 
        could be done is below:

        ```
        filename = DSUtil.get_plot_filename(dataset, "sea_level", "png")
        with self.storage._tmp.get_temp_filepath(filename) as tmp_path:
            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(dataset["time"].data, dataset["sea_level"].data)
            fig.save(tmp_path)
            storage.save(tmp_path)
        
        filename = DSUtil.get_plot_filename(dataset, "qc_sea_level", "png")
        with self.storage._tmp.get_temp_filepath(filename) as tmp_path:
            fig, ax = plt.subplots(figsize=(10,5))
            DSUtil.plot_qc(dataset, "sea_level", tmp_path)
            storage.save(tmp_path)
        ```

        Args:
        ---
            dataset (xr.Dataset):   The xarray dataset with customizations and 
                                    QC applied. 
        -------------------------------------------------------------------"""
        pass

    def read_and_persist_raw_files(self, file_paths: List[str]) -> List[str]:
        """-------------------------------------------------------------------
        Renames the provided RAW files according to MHKiT-Cloud Data Standards
        naming conventions for RAW data and returns a list of filepaths to the
        renamed files.

        Args:
        ---
            file_paths (List[str]): A list of paths to the original raw files.

        Returns:
        ---
            List[str]: A list of paths to the renamed raw files.
        -------------------------------------------------------------------"""
        raw_dataset_mapping = {}

        if isinstance(file_paths, str):
            file_paths = [file_paths]

        for file_path in file_paths:

            # read the raw file into a dataset
            with self.storage.tmp.fetch(file_path) as tmp_path:
                dataset = FileHandler.read(tmp_path)

                # Don't use dataset if no FileHandler is registered for it
                if dataset is not None:
                    # create the standardized name for raw file
                    new_filename = DSUtil.get_raw_filename(dataset, tmp_path, self.config)

                    # add the raw dataset to our dictionary
                    raw_dataset_mapping[new_filename] = dataset

                    # save the raw data to storage
                    self.storage.save(tmp_path, new_filename)

                else:
                    warnings.warn(f"Couldn't use extracted raw file: {tmp_path}")

        return raw_dataset_mapping
