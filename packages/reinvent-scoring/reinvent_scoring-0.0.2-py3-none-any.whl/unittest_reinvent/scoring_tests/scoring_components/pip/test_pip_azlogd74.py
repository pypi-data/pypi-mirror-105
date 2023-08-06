import os
import shutil
import unittest
from unittest.mock import MagicMock

import numpy as np
import numpy.testing as npt
import pytest

from reinvent_scoring.scoring.score_components import AZlogD74PiP
from unittest_reinvent.fixtures.paths import MAIN_TEST_PATH
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_c_lab_component
from unittest_reinvent.scoring_tests.scoring_components.fixtures import score, celecoxib
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_pip_azlogd74(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        enum = ScoringFunctionComponentNameEnum()
        csp_enum = ComponentSpecificParametersEnum()
        parameters = create_c_lab_component(enum.AZ_LOGD74_PIP)
        parameters.specific_parameters[csp_enum.TRANSFORMATION] = False
        if not os.path.isdir(MAIN_TEST_PATH):
            os.makedirs(MAIN_TEST_PATH)

        cls.query_smiles = [celecoxib, "CCC", "CCCCC"]
        cls.expected_scores = [3.444, 1.290,  2.667]

        cls.component = AZlogD74PiP(parameters)

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(MAIN_TEST_PATH):
            shutil.rmtree(MAIN_TEST_PATH)

    @pytest.mark.integration
    def test_pip_1(self):
        npt.assert_almost_equal(score(self.component, self.query_smiles), self.expected_scores, decimal=1)

    def test_pip_empty_response(self):
        self.component._parse_compound = MagicMock(return_value=np.nan)
        npt.assert_almost_equal(score(self.component, self.query_smiles), [0, 0, 0], 3)


class Test_pip_azlogd74_transformation(unittest.TestCase):
    def setUp(cls):
        enum = ScoringFunctionComponentNameEnum()
        parameters = create_c_lab_component(enum.AZ_LOGD74_PIP)
        if not os.path.isdir(MAIN_TEST_PATH):
            os.makedirs(MAIN_TEST_PATH)

        cls.query_smiles = [celecoxib, 'CCC', "CCCCC"]
        cls.expected_raw_scores = [3.444, 1.290,  2.667]
        cls.expected_scores = [0.029, 0.002, 0.012]
        cls.component = AZlogD74PiP(parameters)

    def tearDown(self):
        if os.path.isdir(MAIN_TEST_PATH):
            shutil.rmtree(MAIN_TEST_PATH)

    @pytest.mark.integration
    def test_pip_transformed_1(self):
        npt.assert_almost_equal(score(self.component, self.query_smiles), self.expected_scores, decimal=3)

    def test_pip_empty_response(self):
        self.component._parse_compound = MagicMock(return_value=np.nan)
        npt.assert_almost_equal(score(self.component, self.query_smiles), [0, 0, 0], 3)
