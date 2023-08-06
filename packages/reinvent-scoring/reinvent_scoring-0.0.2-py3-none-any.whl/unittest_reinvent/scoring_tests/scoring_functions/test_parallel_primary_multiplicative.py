import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.scoring_function_factory import ScoringFunctionFactory
from reinvent_scoring.scoring.scoring_function_parameters import ScoringFuncionParameters
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import \
    create_predictive_property_component_regression
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import ScoringFunctionNameEnum


class Test_parallel_primary_multiplicative_function(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        sf_name_enum = ScoringFunctionNameEnum()
        activity = create_predictive_property_component_regression()
        activity.weight = 1
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1[c,n]nc([N;H]C2CCN(S(=O)=O)CC2)[c,n]c1"],
                                                    model_path="",
                                                    specific_parameters={})

        sf_parameters = ScoringFuncionParameters(name=sf_name_enum.CUSTOM_PRODUCT,
                                                 parameters=[vars(activity), vars(qed_score), vars(custom_alerts),
                                                             vars(matching_substructure)], parallel=True)
        self.sf_instance = ScoringFunctionFactory(sf_parameters=sf_parameters)

    def test_primary_multiplicative_1(self):
        smiles = ["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1" for i in range(2)]
        score = self.sf_instance.get_final_score(smiles=smiles)
        self.assertAlmostEqual(score.total_score[0], 0.2893, 3)

    def test_primary_multiplicative_2(self):
        smiles = ["COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21" for i in range(2)]
        score = self.sf_instance.get_final_score(smiles=smiles)
        self.assertAlmostEqual(score.total_score[0], 0.0811, 3)
