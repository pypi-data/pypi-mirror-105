import os
import numpy as np
import pytest

import autofit as af
import autolens as al
from autolens.analysis import result as res
from autolens.mock import mock

pytestmark = pytest.mark.filterwarnings(
    "ignore:Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of "
    "`arr[seq]`. In the future this will be interpreted as an arrays index, `arr[np.arrays(seq)]`, which will result "
    "either in an error or a different result."
)

directory = os.path.dirname(os.path.realpath(__file__))


class TestResultAbstract:
    def test__max_log_likelihood_tracer_available_as_result(
        self, analysis_imaging_7x7, samples_with_result
    ):

        model = af.Collection(
            galaxies=af.Collection(
                lens=al.Galaxy(redshift=0.5), source=al.Galaxy(redshift=1.0)
            )
        )

        search = mock.MockSearch(name="test_search_2", samples=samples_with_result)

        result = search.fit(model=model, analysis=analysis_imaging_7x7)

        assert isinstance(result.max_log_likelihood_tracer, al.Tracer)
        assert result.max_log_likelihood_tracer.galaxies[0].light.intensity == 1.0
        assert result.max_log_likelihood_tracer.galaxies[1].light.intensity == 2.0

    def test__max_log_likelihood_tracer_source_light_profile_centres_correct(
        self, analysis_imaging_7x7
    ):

        lens = al.Galaxy(redshift=0.5, light=al.lp.SphSersic(intensity=1.0))

        source = al.Galaxy(
            redshift=1.0, light=al.lp.SphSersic(centre=(1.0, 2.0), intensity=2.0)
        )

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.Result(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert result.source_plane_light_profile_centre.in_list == [(1.0, 2.0)]

        source = al.Galaxy(
            redshift=1.0,
            light=al.lp.SphSersic(centre=(1.0, 2.0), intensity=2.0),
            light1=al.lp.SphSersic(centre=(3.0, 4.0), intensity=2.0),
        )

        source_1 = al.Galaxy(
            redshift=1.0, light=al.lp.SphSersic(centre=(5.0, 6.0), intensity=2.0)
        )

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source, source_1])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.Result(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert result.source_plane_light_profile_centre.in_list == [(1.0, 2.0)]

        tracer = al.Tracer.from_galaxies(galaxies=[al.Galaxy(redshift=0.5)])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.Result(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert result.source_plane_light_profile_centre == None

    def test__max_log_likelihood_tracer_source_inversion_centres_correct(
        self, analysis_imaging_7x7
    ):

        lens = al.Galaxy(redshift=0.5, light=al.lp.SphSersic(intensity=1.0))

        source = al.Galaxy(
            redshift=1.0,
            pixelization=al.pix.Rectangular((3, 3)),
            regularization=al.reg.Constant(coefficient=1.0),
        )

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultImaging(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert (
            result.source_plane_inversion_centre.in_list[0]
            == result.max_log_likelihood_fit.inversion.brightest_reconstruction_pixel_centre.in_list[
                0
            ]
        )

        lens = al.Galaxy(redshift=0.5, light=al.lp.SphSersic(intensity=1.0))
        source = al.Galaxy(redshift=1.0)

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultImaging(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert result.source_plane_inversion_centre == None

    def test__max_log_likelihood_tracer_source_centres_correct(
        self, analysis_imaging_7x7
    ):

        lens = al.Galaxy(redshift=0.5, light=al.lp.SphSersic(intensity=1.0))
        source = al.Galaxy(
            redshift=1.0,
            light=al.lp.SphSersic(centre=(9.0, 8.0), intensity=2.0),
            pixelization=al.pix.Rectangular((3, 3)),
            regularization=al.reg.Constant(coefficient=1.0),
        )

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultImaging(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert result.source_plane_centre.in_list[0] == pytest.approx(
            (-0.916666, -0.916666), 1.0e-4
        )

    def test__max_log_likelihood_tracer__multiple_image_positions_of_source_plane_centres_and_separations(
        self, analysis_imaging_7x7
    ):

        lens = al.Galaxy(
            redshift=0.5,
            mass=al.mp.EllIsothermal(
                centre=(0.001, 0.001),
                einstein_radius=1.0,
                elliptical_comps=(0.0, 0.111111),
            ),
        )

        source = al.Galaxy(
            redshift=1.0,
            light=al.lp.SphSersic(centre=(0.0, 0.0), intensity=2.0),
            light1=al.lp.SphSersic(centre=(0.0, 0.1), intensity=2.0),
            pixelization=al.pix.Rectangular((3, 3)),
            regularization=al.reg.Constant(coefficient=1.0),
        )

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultImaging(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        mask = al.Mask2D.unmasked(
            shape_native=(100, 100), pixel_scales=0.05, sub_size=1
        )

        result.analysis.dataset.data.mask = mask

        multiple_images = result.image_plane_multiple_image_positions

        grid = al.Grid2D.from_mask(mask=mask)

        solver = al.PositionsSolver(grid=grid, pixel_scale_precision=0.001)

        multiple_images_manual = solver.solve(
            lensing_obj=tracer,
            source_plane_coordinate=result.source_plane_inversion_centre[0],
        )

        assert multiple_images.in_list[0] == multiple_images_manual.in_list[0]

    def test__image_plane_multiple_image_positions_and_threshold(
        self, analysis_imaging_7x7
    ):

        tracer = al.Tracer.from_galaxies(
            galaxies=[
                al.Galaxy(
                    redshift=0.5,
                    mass=al.mp.EllIsothermal(
                        centre=(0.1, 0.0),
                        einstein_radius=1.0,
                        elliptical_comps=(0.0, 0.0),
                    ),
                ),
                al.Galaxy(redshift=1.0, bulge=al.lp.SphSersic(centre=(0.0, 0.0))),
            ]
        )

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.Result(
            samples=samples, model=None, analysis=analysis_imaging_7x7, search=None
        )

        assert result.image_plane_multiple_image_positions.in_list[0][
            0
        ] == pytest.approx(1.0004, 1.0e-2)
        assert result.image_plane_multiple_image_positions.in_list[1][
            0
        ] == pytest.approx(-1.0004, 1.0e-2)

        assert result.positions_threshold_from() == pytest.approx(0.000973519, 1.0e-4)
        assert result.positions_threshold_from(factor=5.0) == pytest.approx(
            5.0 * 0.000973519, 1.0e-4
        )
        assert result.positions_threshold_from(minimum_threshold=0.2) == pytest.approx(
            0.2, 1.0e-4
        )


class TestResultDataset:
    def test__results_include_mask__available_as_property(
        self, analysis_imaging_7x7, masked_imaging_7x7, samples_with_result
    ):

        result = res.ResultDataset(
            samples=samples_with_result,
            analysis=analysis_imaging_7x7,
            model=None,
            search=None,
        )

        assert (result.mask == masked_imaging_7x7.mask).all()

    def test__results_include_positions__available_as_property(
        self, analysis_imaging_7x7, masked_imaging_7x7, samples_with_result
    ):

        result = res.ResultDataset(
            samples=samples_with_result,
            analysis=analysis_imaging_7x7,
            model=None,
            search=None,
        )

        assert result.positions == None

        analysis = al.AnalysisImaging(
            dataset=masked_imaging_7x7,
            positions=al.Grid2DIrregular([[(1.0, 1.0)]]),
            settings_lens=al.SettingsLens(positions_threshold=1.0),
        )

        result = res.ResultDataset(
            samples=samples_with_result, analysis=analysis, model=None, search=None
        )

        assert (result.positions[0] == np.array([1.0, 1.0])).all()

    def test__results_include_pixelization__available_as_property(
        self, analysis_imaging_7x7
    ):

        lens = al.Galaxy(redshift=0.5, light=al.lp.EllSersic(intensity=1.0))
        source = al.Galaxy(
            redshift=1.0,
            pixelization=al.pix.VoronoiMagnification(shape=(2, 3)),
            regularization=al.reg.Constant(),
        )

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultDataset(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert isinstance(result.pixelization, al.pix.VoronoiMagnification)
        assert result.pixelization.shape == (2, 3)

        lens = al.Galaxy(redshift=0.5, light=al.lp.EllSersic(intensity=1.0))
        source = al.Galaxy(
            redshift=1.0,
            pixelization=al.pix.VoronoiBrightnessImage(pixels=6),
            regularization=al.reg.Constant(),
        )

        source.hyper_galaxy_image = np.ones(9)

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultDataset(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert isinstance(result.pixelization, al.pix.VoronoiBrightnessImage)
        assert result.pixelization.pixels == 6

    def test__results_include_pixelization_grid__available_as_property(
        self, analysis_imaging_7x7
    ):

        galaxy = al.Galaxy(redshift=0.5, light=al.lp.EllSersic(intensity=1.0))

        tracer = al.Tracer.from_galaxies(galaxies=[galaxy])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultDataset(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert result.max_log_likelihood_pixelization_grids_of_planes == [None]

        lens = al.Galaxy(redshift=0.5, light=al.lp.EllSersic(intensity=1.0))
        source = al.Galaxy(
            redshift=1.0,
            pixelization=al.pix.VoronoiBrightnessImage(pixels=6),
            regularization=al.reg.Constant(),
        )

        source.hyper_galaxy_image = np.ones(9)

        tracer = al.Tracer.from_galaxies(galaxies=[lens, source])

        samples = mock.MockSamples(max_log_likelihood_instance=tracer)

        result = res.ResultDataset(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        assert result.max_log_likelihood_pixelization_grids_of_planes[-1].shape == (
            6,
            2,
        )

    def test___image_dict(self, analysis_imaging_7x7):

        galaxies = af.ModelInstance()
        galaxies.lens = al.Galaxy(redshift=0.5)
        galaxies.source = al.Galaxy(redshift=1.0)

        instance = af.ModelInstance()
        instance.galaxies = galaxies

        result = res.ResultImaging(
            samples=mock.MockSamples(max_log_likelihood_instance=instance),
            model=af.ModelMapper(),
            analysis=analysis_imaging_7x7,
            search=None,
        )

        image_dict = result.image_galaxy_dict
        assert isinstance(image_dict[("galaxies", "lens")], np.ndarray)
        assert isinstance(image_dict[("galaxies", "source")], np.ndarray)

        result.instance.galaxies.lens = al.Galaxy(redshift=0.5)

        image_dict = result.image_galaxy_dict
        assert (image_dict[("galaxies", "lens")].native == np.zeros((7, 7))).all()
        assert isinstance(image_dict[("galaxies", "source")], np.ndarray)


class TestResultImaging:

    pass


class TestResultInterferometer:

    pass


class TestResultPointsource:

    pass
