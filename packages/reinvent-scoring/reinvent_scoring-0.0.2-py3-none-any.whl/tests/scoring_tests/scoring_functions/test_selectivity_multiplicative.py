import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomProduct
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_activity_component_regression, \
    create_predictive_property_component_regression, create_custom_alerts_configuration
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_selectivity_multiplicative_function(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        activity = create_activity_component_regression()
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})

        custom_alerts = create_custom_alerts_configuration()

        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1[c,n]nc([N;H]C2CCN(S(=O)=O)CC2)[c,n]c1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, qed_score, custom_alerts, matching_substructure])

    def test_special_selectivity_multiplicative_1(self):
        score = self.sf_state.get_final_score(smiles=["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"])
        self.assertAlmostEqual(score.total_score[0], 0.2893, 3)

    def test_special_selectivity_multiplicative_2(self):
        score_1 = self.sf_state.get_final_score(smiles=["c1[nH]nc(-c2nc3c(-c4cccc(CN(C)C)c4)cccc3[nH]2)c1NC(=O)Cc1ccncc1"])
        score_2 = self.sf_state.get_final_score(smiles=["c1[nH]nc(-c2nc3c(-c4cccc(CN(C)C)c4)cccc3[nH]2)c1NC(=O)Cc1ccncc1"])
        self.assertAlmostEqual(score_1.total_score[0], 0.142, 3)
        self.assertAlmostEqual(score_2.total_score[0], 0.142, 3)


class Test_selectivity_multiplicative_function_with_predictive_property(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        predictive_property = create_predictive_property_component_regression()
        activity = create_activity_component_regression()
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})

        custom_alerts = create_custom_alerts_configuration()

        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1[c,n]nc([N;H]C2CCN(S(=O)=O)CC2)[c,n]c1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, qed_score, custom_alerts, matching_substructure, predictive_property])

    def test_special_selectivity_multiplicative_1(self):
        score = self.sf_state.get_final_score(smiles=["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"])
        self.assertAlmostEqual(score.total_score[0], 0.2142, 3)


class Test_selectivity_multiplicative_function_with_predictive_property_and_alert(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        predictive_property = create_predictive_property_component_regression()
        self.activity = create_activity_component_regression()
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})

        custom_alerts = create_custom_alerts_configuration()

        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1[c,n]nc([N;H]C2CCN(S(=O)=O)CC2)[c,n]c1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[self.activity, qed_score, custom_alerts, matching_substructure, predictive_property])

    def test_special_selectivity_multiplicative_with_alert_1(self):
        score = self.sf_state.get_final_score(smiles=["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"])
        self.assertAlmostEqual(score.total_score[0], 0.2142, 3)

    def test_special_selectivity_multiplicative_with_alert_2(self):
        score = self.sf_state.get_final_score(smiles=["CCCOOOCCCCO"])
        self.assertEqual(score.total_score, 0)

    def test_special_selectivity_multiplicative_with_alert_3(self):
        score = self.sf_state.get_final_score(smiles=["COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"])
        self.assertAlmostEqual(score.total_score[0], 0.0599, 3)

    def test_special_selectivity_multiplicative_with_alert_4(self):
        score = self.sf_state.get_final_score(smiles=["C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)O"])
        self.assertEqual(score.total_score[0], 0)


class Test_selectivity_multiplicative_function_with_predictive_property_no_sigm_trans(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        predictive_property = create_predictive_property_component_regression()
        activity = create_activity_component_regression()
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=["CCCOOO"],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1[c,n]nc([N;H]C2CCN(S(=O)=O)CC2)[c,n]c1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, qed_score, custom_alerts, matching_substructure, predictive_property])

    def test_special_selectivity_multiplicative_no_sigm_trans_1(self):
        score = self.sf_state.get_final_score(smiles=["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"])
        self.assertAlmostEqual(score.total_score[0], 0.2142, 3)

    def test_special_selectivity_multiplicative_no_sigm_trans_2(self):
        score = self.sf_state.get_final_score(smiles=["COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"])
        self.assertAlmostEqual(score.total_score[0], 0.0599, 3)

    def test_special_selectivity_multiplicative_no_sigm_trans_3(self):
        score = self.sf_state.get_final_score(smiles=["CCCOOOCCCOOO"])
        self.assertEqual(score.total_score, 0)

    def test_special_selectivity_multiplicative_no_sigm_trans_4(self):
        score = self.sf_state.get_final_score(smiles=["C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)O"])
        self.assertAlmostEqual(score.total_score[0], 0.0591, 3)
