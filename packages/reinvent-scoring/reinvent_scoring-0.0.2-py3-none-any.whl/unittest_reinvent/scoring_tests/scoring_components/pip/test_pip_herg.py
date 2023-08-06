import os
import shutil
import unittest
from unittest.mock import MagicMock

import numpy as np
import numpy.testing as npt
import pytest

from reinvent_scoring.scoring.score_components import HERGPiP
from unittest_reinvent.fixtures.paths import MAIN_TEST_PATH
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_c_lab_component
from unittest_reinvent.scoring_tests.scoring_components.fixtures import score, celecoxib
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import TransformationTypeEnum


class Test_pip_HERG(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        enum = ScoringFunctionComponentNameEnum()
        csp_enum = ComponentSpecificParametersEnum()
        parameters = create_c_lab_component(enum.HERG_PIP)
        parameters.specific_parameters[csp_enum.TRANSFORMATION] = False
        if not os.path.isdir(MAIN_TEST_PATH):
            os.makedirs(MAIN_TEST_PATH)

        cls.query_smiles = [celecoxib, "CCC", "CCCCC"]
        cls.expected_scores = [10.970, 122.917, 24.849]

        cls.component = HERGPiP(parameters)

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(MAIN_TEST_PATH):
            shutil.rmtree(MAIN_TEST_PATH)

    @pytest.mark.integration
    def test_pip_1(self):
        npt.assert_almost_equal(score(self.component, self.query_smiles), self.expected_scores, decimal=3)

    def test_pip_empty_response(self):
        self.component._parse_compound = MagicMock(return_value=np.nan)
        npt.assert_almost_equal(score(self.component, self.query_smiles), [0, 0, 0], 3)


class Test_pip_HERG_transformation(unittest.TestCase):
    def setUp(cls):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        enum = ScoringFunctionComponentNameEnum()
        ts_parameters = create_c_lab_component(enum.HERG_PIP)
        ts_parameters.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.STEP
        ts_parameters.specific_parameters[csp_enum.HIGH] = 200
        ts_parameters.specific_parameters[csp_enum.LOW] = 20
        if not os.path.isdir(MAIN_TEST_PATH):
            os.makedirs(MAIN_TEST_PATH)

        cls.query_smiles = [celecoxib, "CCC", "CCCCC"]
        cls.expected_scores = [10.970, 122.917, 24.849]
        cls.expected_scores = [0.0, 1.0, 1.0]
        cls.component = HERGPiP(ts_parameters)

    def tearDown(self):
        if os.path.isdir(MAIN_TEST_PATH):
            shutil.rmtree(MAIN_TEST_PATH)

    @pytest.mark.integration
    def test_pip_transformed_1(self):
        npt.assert_almost_equal(score(self.component, self.query_smiles), self.expected_scores, decimal=3)

    def test_pip_empty_response(self):
        self.component._parse_compound = MagicMock(return_value=np.nan)
        npt.assert_almost_equal(score(self.component, self.query_smiles), [0, 0, 0], 3)
