import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomProduct
from reinvent_scoring.scoring.score_summary import FinalSummary
from unittest_reinvent.fixtures.paths import SCIKIT_REGRESSION_PATH
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_activity_component_regression, \
    create_offtarget_activity_component_regression, create_custom_alerts_configuration
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import TransformationTypeEnum


class Test_desirability_multiplicative_function(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        sf_enum = ScoringFunctionComponentNameEnum()
        activity = create_activity_component_regression()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.
        off_activity = create_offtarget_activity_component_regression()

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }

        selectivity = ComponentParameters(component_type=sf_enum.SELECTIVITY,
                                           name="desirability",
                                           weight=1.,
                                           smiles=[],
                                           model_path="",
                                           specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": off_activity.model_path,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters,
                                               "delta_transformation_parameters": delta_params
                                           })

        qed_score = ComponentParameters(component_type=sf_enum.QED_SCORE,
                                        name="qed_score",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        matching_substructure = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure",
                                                    weight=1.,
                                                    smiles=["[*]n1cc(c([NH])cc1=O)"],
                                                    model_path="",
                                                    specific_parameters={})

        custom_alerts = create_custom_alerts_configuration()

        self.sf_state = CustomProduct(
            parameters=[activity, selectivity, qed_score, matching_substructure, custom_alerts])

    def test_desirability_multiplicative_1(self):
        score = self.sf_state.get_final_score(smiles=["CCC"])
        self.assertAlmostEqual(score.total_score[0], 0.1148, 3)

    def test_desirability_multiplicative_2(self):
        score = self.sf_state.get_final_score(smiles=["Cn1cc(c([NH])cc1=O)"])
        self.assertAlmostEqual(score.total_score[0], 0.1726, 3)

    def test_desirability_multiplicative_3(self):
        score = self.sf_state.get_final_score(smiles=["c1ccc2c(c1)c(cnc2O)C(=O)"])
        self.assertAlmostEqual(score.total_score[0], 0.1357, 3)

    def test_desirability_multiplicative_4(self):
        score = self.sf_state.get_final_score(smiles=["C1CCCCCCCCC1", "12"])
        self.assertAlmostEqual(score.total_score[0], 0., 3)
        self.assertEqual(score.total_score[1], 0)


class Test_special_desirability_multiplicative_function(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        sf_enum = ScoringFunctionComponentNameEnum()
        activity = create_activity_component_regression()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.
        off_activity = create_offtarget_activity_component_regression()
        off_activity.weight = 4
        off_activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        off_activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        off_activity.specific_parameters[csp_enum.COEF_SI] = 150.
        off_activity.specific_parameters[csp_enum.COEF_SE] = 150.
        off_activity.model_path = SCIKIT_REGRESSION_PATH
        off_activity2 = create_offtarget_activity_component_regression()
        off_activity2.weight = 4

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }

        selectivity_1 = ComponentParameters(component_type=sf_enum.SELECTIVITY,
                                           name="selectivity_1",
                                           weight=4.,
                                           smiles=[],
                                           model_path="",
                                           specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": off_activity.model_path,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters,
                                               "delta_transformation_parameters": delta_params
                                           })

        selectivity_2 = ComponentParameters(component_type=sf_enum.SELECTIVITY,
                                           name="selectivity_2",
                                           weight=4.,
                                           smiles=[],
                                           model_path="",
                                           specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": off_activity2.model_path,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity2.specific_parameters,
                                               "delta_transformation_parameters": delta_params
                                           })

        qed_score = ComponentParameters(component_type=sf_enum.QED_SCORE,
                                        name="qed_score",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        custom_alerts = ComponentParameters(component_type=sf_enum.CUSTOM_ALERTS,
                                            name="custom_alerts",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure",
                                                    weight=1.,
                                                    smiles=["c1[c,n]nc([N;H]C2CCN(S(=O)=O)CC2)[c,n]c1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, selectivity_1, selectivity_2, qed_score, custom_alerts, matching_substructure])

    def test_special_desirability_multiplicative_1(self):
        score = self.sf_state.get_final_score(smiles=["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"])
        self.assertAlmostEqual(score.total_score[0], 0.087, 3)

    def test_special_desirability_multiplicative_2(self):
        score = self.sf_state.get_final_score(smiles=["COc1ccc2nc(NC3CCN(S(=O)(=O)c4ccc(C)cc4)CC3)cc(C)c2c1"])
        self.assertAlmostEqual(score.total_score[0], 0.062, 3)

    def test_special_desirability_multiplicative_3(self):
        score = self.sf_state.get_final_score(smiles=["Fc1cccc(CNc2ccnc(Nc3cnccn3)n2)c1"])
        self.assertAlmostEqual(score.total_score[0], 0.028, 3)


class Test_selectivity_function_with_double_sigmoid(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        enum = ScoringFunctionComponentNameEnum()
        activity = create_activity_component_regression()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.
        off_activity = create_offtarget_activity_component_regression()

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }

        selectivity = ComponentParameters(component_type=enum.SELECTIVITY,
                                           name="desirability",
                                           weight=1.,
                                           smiles=[],
                                           model_path="",
                                           specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": off_activity.model_path,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters,
                                               "delta_transformation_parameters": delta_params
                                           })

        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure",
                                                    weight=1.,
                                                    smiles=["[*]n1cc(c([NH])cc1=O)"],
                                                    model_path="",
                                                    specific_parameters={})
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, selectivity, qed_score, matching_substructure, custom_alerts])


    def test_selectivity_function_with_scikit_and_wrapped_models_1(self):
        score: FinalSummary = self.sf_state.get_final_score(smiles=["Cn1cc(c([NH])cc1=O)"])
        self.assertAlmostEqual(score.total_score[0], 0.1726, 3)

    def test_selectivity_function_with_scikit_and_wrapped_models_2(self):
        score = self.sf_state.get_final_score(smiles=["c1ccc2c(c1)c(cnc2O)C(=O)"])
        self.assertAlmostEqual(score.total_score[0], 0.1357, 3)

