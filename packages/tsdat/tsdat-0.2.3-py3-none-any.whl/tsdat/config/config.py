import yaml
from yamllint import linter
from yamllint.config import YamlLintConfig
from typing import List, Dict
from .keys import Keys
from .pipeline_definition import PipelineDefinition
from .dataset_definition import DatasetDefinition
from .quality_manager_definition import QualityManagerDefinition


class Config:
    """
    Wrapper for Dictionary of config values that provides helper functions for
    quick access.
    """

    def __init__(self, dictionary: Dict):
        pipeline_dict = dictionary.get(Keys.PIPELINE)
        dataset_dict = dictionary.get(Keys.DATASET_DEFINITION)
        quality_managers_dict = dictionary.get(Keys.QUALITY_MANAGEMENT, {})

        self.pipeline_definition = PipelineDefinition(pipeline_dict)
        self.dataset_definition = DatasetDefinition(dataset_dict, self.pipeline_definition.output_datastream_name)

        self.quality_managers = self._parse_quality_managers(quality_managers_dict)

    def _parse_quality_managers(self, dictionary) -> Dict[str, QualityManagerDefinition]:
        quality_managers: Dict[str, QualityManagerDefinition] = {}
        for manager_name, manager_dict in dictionary.items():
            quality_managers[manager_name] = QualityManagerDefinition(manager_name, manager_dict)
        return quality_managers

    @classmethod
    def load(self, filepaths: List[str]):
        """-------------------------------------------------------------------
        Load one or more yaml config files which define data following 
        mhkit-cloud data standards.
        
        TODO: add a schema validation check on yaml so users can know if the 
        file is valid
        
        Args:
            filepaths (List[str]): The paths to the config files to load

        Returns:
            Config: A Config instance created from the filepaths.
        -------------------------------------------------------------------"""
        if isinstance(filepaths, str):
            filepaths = [filepaths]
        config = dict()
        for filepath in filepaths:
            Config.lint_yaml(filepath)
            with open(filepath, 'r') as file:
                dict_list = list(yaml.safe_load_all(file))
                for dictionary in dict_list:
                    config.update(dictionary)
        return Config(config)

    @staticmethod
    def lint_yaml(filename):
        conf = YamlLintConfig('{"extends": "relaxed", "rules": {"line-length": "disable", "trailing-spaces": "disable", "empty-lines": "disable", "new-line-at-end-of-file": "disable"}}')
        with open(filename) as file:
            gen = linter.run(file, conf)
            errors = [error for error in gen if error.level == "error"]
            if errors:
                errors = "\n".join("\t\t" + str(error) for error in errors)
                raise Exception(f"Syntax errors found in yaml file {filename}: \n{errors}")
