from os import path

import pytest

import autofit as af
import autolens as al
from autolens.mock import mock

directory = path.dirname(path.realpath(__file__))


@pytest.fixture(name="path")
def make_path():
    return path.join("{}".format(path.dirname(path.realpath(__file__))), "files")


@pytest.fixture(name="samples")
def make_samples():
    galaxy_0 = al.Galaxy(redshift=0.5, light=al.lp.EllSersic(centre=(0.0, 1.0)))
    galaxy_1 = al.Galaxy(redshift=1.0, light=al.lp.EllSersic())

    tracer = al.Tracer.from_galaxies(galaxies=[galaxy_0, galaxy_1])

    return mock.MockSamples(max_log_likelihood_instance=tracer)


@pytest.fixture(name="model")
def make_model():
    return af.Collection(
        galaxies=af.Collection(
            lens=af.Model(al.Galaxy, redshift=0.5, light=al.lp.EllSersic),
            source=af.Model(al.Galaxy, redshift=1.0, light=al.lp.EllSersic),
        )
    )

#
# def test__tracer_generator_from_aggregator(masked_imaging_7x7, samples, model):
#
#     search = mock.MockSearch(samples=samples)
#     search.paths = af.DirectoryPaths(path_prefix="aggregator_tracer_gen")
#
#     analysis = al.AnalysisImaging(dataset=masked_imaging_7x7)
#
#     search.fit(model=model, analysis=analysis)
#
#     agg = af.Aggregator(directory=search.paths.output_path)
#
#     tracer_gen = al.agg.Tracer(aggregator=agg)
#
#     for tracer in tracer_gen:
#
#         assert tracer.galaxies[0].redshift == 0.5
#         assert tracer.galaxies[0].light.centre == (0.0, 1.0)
#         assert tracer.galaxies[1].redshift == 1.0
#
#
# def test__imaging_generator_from_aggregator(imaging_7x7, mask_2d_7x7, samples, model):
#
#     masked_imaging_7x7 = imaging_7x7.apply_mask(mask=mask_2d_7x7)
#     masked_imaging_7x7 = masked_imaging_7x7.apply_settings(
#         settings=al.SettingsImaging(
#             grid_class=al.Grid2DIterate,
#             grid_inversion_class=al.Grid2DInterpolate,
#             fractional_accuracy=0.5,
#             sub_steps=[2],
#             pixel_scales_interp=0.1,
#         )
#     )
#
#     analysis = al.AnalysisImaging(dataset=masked_imaging_7x7)
#
#     search = mock.MockSearch(samples=samples)
#     search.paths = af.DirectoryPaths(path_prefix="aggregator_masked_imaging_gen")
#
#     search.fit(model=model, analysis=analysis)
#
#     agg = af.Aggregator(directory=search.paths.output_path)
#
#     imaging_gen = al.agg.Imaging(aggregator=agg)
#
#     for imaging in imaging_gen:
#         assert (imaging.image == masked_imaging_7x7.image).all()
#         assert isinstance(imaging.grid, al.Grid2DIterate)
#         assert isinstance(imaging.grid_inversion, al.Grid2DInterpolate)
#         assert imaging.grid.sub_steps == [2]
#         assert imaging.grid.fractional_accuracy == 0.5
#         assert imaging.grid_inversion.pixel_scales_interp == (0.1, 0.1)
#
#
# def test__fit_imaging_generator_from_aggregator(masked_imaging_7x7, samples, model):
#     analysis = al.AnalysisImaging(dataset=masked_imaging_7x7)
#
#     search = mock.MockSearch(samples=samples)
#     search.paths = af.DirectoryPaths(path_prefix="aggregator_fit_imaging_gen")
#
#     search.fit(model=model, analysis=analysis)
#
#     agg = af.Aggregator(directory=search.paths.output_path)
#
#     fit_imaging_gen = al.agg.FitImaging(aggregator=agg)
#
#     for fit_imaging in fit_imaging_gen:
#         assert (fit_imaging.image == masked_imaging_7x7.image).all()
#
#
# def test__interferometer_generator_from_aggregator(
#     visibilities_7,
#     visibilities_noise_map_7,
#     uv_wavelengths_7x2,
#     mask_2d_7x7,
#     samples,
#     model,
# ):
#     interferometer_7 = al.Interferometer(
#         visibilities=visibilities_7,
#         noise_map=visibilities_noise_map_7,
#         uv_wavelengths=uv_wavelengths_7x2,
#         real_space_mask=mask_2d_7x7,
#         settings=al.SettingsInterferometer(
#             transformer_class=al.TransformerDFT,
#             grid_class=al.Grid2DIterate,
#             grid_inversion_class=al.Grid2DInterpolate,
#             fractional_accuracy=0.5,
#             sub_steps=[2],
#             pixel_scales_interp=0.1,
#         ),
#     )
#
#     search = mock.MockSearch(samples=samples)
#     search.paths = af.DirectoryPaths(path_prefix="aggregator_interferometer_gen")
#
#     analysis = al.AnalysisInterferometer(dataset=interferometer_7)
#
#     search.fit(model=model, analysis=analysis)
#
#     agg = af.Aggregator(directory=search.paths.output_path)
#
#     interferometer_gen = al.agg.Interferometer(aggregator=agg)
#
#     for interferometer in interferometer_gen:
#         assert (interferometer.visibilities == interferometer_7.visibilities).all()
#         assert (interferometer.real_space_mask == mask_2d_7x7).all()
#         assert isinstance(interferometer.grid, al.Grid2DIterate)
#         assert isinstance(interferometer.grid_inversion, al.Grid2DInterpolate)
#         assert interferometer.grid.sub_steps == [2]
#         assert interferometer.grid.fractional_accuracy == 0.5
#         assert interferometer.grid_inversion.pixel_scales_interp == (0.1, 0.1)
#         assert isinstance(interferometer.transformer, al.TransformerDFT)
#
#
# def test__fit_interferometer_generator_from_aggregator(
#     interferometer_7, mask_2d_7x7, samples, model
# ):
#
#     search = mock.MockSearch(samples=samples)
#     search.paths = af.DirectoryPaths(path_prefix="aggregator_fit_interferometer_gen")
#
#     analysis = al.AnalysisInterferometer(dataset=interferometer_7)
#
#     search.fit(model=model, analysis=analysis)
#
#     agg = af.Aggregator(directory=search.paths.output_path)
#
#     fit_interferometer_gen = al.agg.FitInterferometer(aggregator=agg)
#
#     for fit_interferometer in fit_interferometer_gen:
#         assert (fit_interferometer.visibilities == interferometer_7.visibilities).all()
#         assert (fit_interferometer.interferometer.real_space_mask == mask_2d_7x7).all()


class MockResult:
    def __init__(self, log_likelihood):
        self.log_likelihood = log_likelihood
        self.log_evidence_values = log_likelihood
        self.model = log_likelihood


class MockAggregator:
    def __init__(self, grid_search_result):
        self.grid_search_result = grid_search_result

    @property
    def grid_search_results(self):
        return iter([self.grid_search_result])

    def values(self, str):
        return self.grid_search_results


# def test__results_array_from_results_file(path):
#
#     results = [
#         MockResult(log_likelihood=1.0),
#         MockResult(log_likelihood=2.0),
#         MockResult(log_likelihood=3.0),
#         MockResult(log_likelihood=4.0),
#     ]
#
#     lower_limit_lists = [[0.0, 0.0], [0.0, 0.5], [0.5, 0.0], [0.5, 0.5]]
#     physical_lower_limits_lists = [[-1.0, -1.0], [-1.0, 0.0], [0.0, -1.0], [0.0, 0.0]]
#
#     grid_search_result = af.GridSearchResult(
#         results=results,
#         physical_lower_limits_lists=physical_lower_limits_lists,
#         lower_limit_lists=lower_limit_lists,
#     )
#
#     aggregator = MockAggregator(grid_search_result=grid_search_result)
#
#     array = al.agg.grid_search_result_as_array(aggregator=aggregator)
#
#     assert array.native == pytest.approx(np.array([[3.0, 2.0], [1.0, 4.0]]), 1.0e4)
#     assert array.pixel_scales == (1.0, 1.0)


# def test__results_array_from_real_grid_search_pickle(path):
#
#     with open("{}/{}.pickle".format(path, "grid_search_result"), "rb") as f:
#         grid_search_result = pickle.load(f)
#
#     array = al.agg.grid_search_log_evidences_as_array_from_grid_search_result(
#         grid_search_result=grid_search_result
#     )
#
#     print(array.native)
#
#     array = al.agg.grid_search_subhalo_masses_as_array_from_grid_search_result(
#         grid_search_result=grid_search_result
#     )
#
#     print(array.native)
#
#     array = al.agg.grid_search_subhalo_centres_as_array_from_grid_search_result(
#         grid_search_result=grid_search_result
#     )
#
#     print(array)
