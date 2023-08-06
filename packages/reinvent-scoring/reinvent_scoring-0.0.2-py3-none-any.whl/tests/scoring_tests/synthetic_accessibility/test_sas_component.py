import unittest

import numpy.testing as npt

from reinvent_scoring.chemistry import GeneralChemistry
from reinvent_scoring.scoring.score_components.synthetic_accessibility.sas_component import SASComponent
from unittest_reinvent.fixtures.paths import SAS_MODEL_PATH
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_activity_component_regression
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum


class Test_sas_component(unittest.TestCase):

    def setUp(self):
        csp_enum = ComponentSpecificParametersEnum()
        ts_parameters = create_activity_component_regression()
        ts_parameters.specific_parameters[csp_enum.TRANSFORMATION] = False
        ts_parameters.model_path = SAS_MODEL_PATH
        chemistry = GeneralChemistry()

        self.query_smiles = ['COc1ccc(NCCNC(=O)C(CC(C)C)NC(=O)c2ccc(OCc3ccccc3)cc2)cc1',
                             'CC(C)(C(=O)c1ccc(Cl)c(-n2c(=O)[nH]c3csc(C(=O)O)c3c2=O)c1)c1ccccc1',
                             'COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21']
        self.query_mols = [chemistry.smile_to_mol(smile) for smile in self.query_smiles]
        self.component = SASComponent(ts_parameters)

    def test_sas(self):
        summary = self.component.calculate_score(self.query_mols)
        npt.assert_almost_equal(summary.total_score, [0.97, 0.17, 0.93], decimal=2)
