import sys
from os import path

import dill
import numpy as np
import pytest

import autofit as af
from autofit.mock import mock

pytestmark = pytest.mark.filterwarnings("ignore::FutureWarning")


class MockDynestyResults:
    def __init__(self, samples, logl, logwt, ncall, logz, nlive):
        self.samples = samples
        self.logl = logl
        self.logwt = logwt
        self.ncall = ncall
        self.logz = logz
        self.nlive = nlive


class MockDynestySampler:
    def __init__(self, results):
        self.results = results


class TestDynestyConfig:

    def test__loads_from_config_file_if_not_input(self):

        dynesty = af.DynestyStatic(
            prior_passer=af.PriorPasser(sigma=2.0, use_errors=False, use_widths=False),
            nlive=151,
            dlogz=0.1,
            iterations_per_update=501,
            number_of_cores=2,
        )

        assert dynesty.prior_passer.sigma == 2.0
        assert dynesty.prior_passer.use_errors is False
        assert dynesty.prior_passer.use_widths is False
        assert dynesty.iterations_per_update == 501

        assert dynesty.config_dict_search["nlive"] == 151
        assert dynesty.config_dict_run["dlogz"] == 0.1
        assert dynesty.number_of_cores == 2

        dynesty = af.DynestyStatic()

        assert dynesty.prior_passer.sigma == 3.0
        assert dynesty.prior_passer.use_errors is True
        assert dynesty.prior_passer.use_widths is True
        assert dynesty.iterations_per_update == 500

        assert dynesty.config_dict_search["nlive"] == 150
        assert dynesty.config_dict_run["dlogz"] == None
        assert dynesty.number_of_cores == 1

        dynesty = af.DynestyDynamic(
            prior_passer=af.PriorPasser(sigma=2.0, use_errors=False, use_widths=False),
            facc=0.4,
            iterations_per_update=501,
            dlogz_init=0.2,
            number_of_cores=3,
        )

        assert dynesty.prior_passer.sigma == 2.0
        assert dynesty.prior_passer.use_errors is False
        assert dynesty.prior_passer.use_widths is False
        assert dynesty.iterations_per_update == 501

        assert dynesty.config_dict_search["facc"] == 0.4
        assert dynesty.config_dict_run["dlogz_init"] == 0.2
        assert dynesty.number_of_cores == 3

        dynesty = af.DynestyDynamic()

        assert dynesty.prior_passer.sigma == 3.0
        assert dynesty.prior_passer.use_errors is True
        assert dynesty.prior_passer.use_widths is True
        assert dynesty.iterations_per_update == 501

        assert dynesty.config_dict_search["facc"] == 0.6
        assert dynesty.config_dict_run["dlogz_init"] == 0.01
        assert dynesty.number_of_cores == 4

    def test__samples_from_model(self):
        # Setup pickle of mock Dynesty sampler that the samples_from_model function uses.

        results = MockDynestyResults(
            samples=np.array(
                [[1.0, 2.0, 3.0, 5.0], [1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0]]
            ),
            logl=[1.0, 2.0, 3.0],
            logwt=[np.log(1.0), np.log(2.0), np.log(3.0)],
            ncall=[5.0, 5.0],
            logz=[-2.0, -1.0, 0.0],
            nlive=3,
        )

        sampler = MockDynestySampler(results=results)

        paths = af.DirectoryPaths(path_prefix=path.join("non_linear", "dynesty"))
        paths._identifier = "tag"

        dynesty = af.DynestyStatic(nlive=3)
        dynesty.paths = paths

        with open(path.join(dynesty.paths.samples_path, "dynesty.pickle"), "wb") as f:
            dill.dump(sampler, f)

        model = af.ModelMapper(mock_class=mock.MockClassx4)
        model.mock_class.two = af.LogUniformPrior(lower_limit=1e-8, upper_limit=10.0)

        samples = dynesty.samples_via_sampler_from_model(model=model)

        assert isinstance(samples.parameters, list)
        assert isinstance(samples.parameters[0], list)
        assert isinstance(samples.log_likelihoods, list)
        assert isinstance(samples.log_priors, list)
        assert isinstance(samples.log_posteriors, list)
        assert isinstance(samples.weights, list)

        assert samples.parameters == [
            [1.0, 2.0, 3.0, 5.0],
            [1.0, 2.0, 3.0, 4.0],
            [1.0, 2.0, 3.0, 4.0],
        ]
        assert samples.log_likelihoods == [1.0, 2.0, 3.0]
        assert samples.log_priors == [0.2, 0.25, 0.25]
        assert samples.weights == pytest.approx([1.0, 2.0, 3.0], 1.0e-4)
        assert samples.total_samples == 10
        assert samples.log_evidence == 0.0
        assert samples.number_live_points == 3
