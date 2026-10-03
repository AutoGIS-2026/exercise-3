from points_decorator import points
import os
import pandas as pd
import geopandas as gpd


class TestProblem2:
    @points(1, "Problem 2, Part 1: Did you read the file `shopping_centres.gpkg` into a dataframe?")
    def test_problem_2_part_1(self, problem2):
        section_data, namespace = problem2
        section = "Part 1"
        variables = section_data[section]['variables']

        assert isinstance(variables['shopping_centres'], pd.DataFrame)
        assert len(variables['shopping_centres']) == 7, "The dataframe does not have the correct number of rows."

    @points(0.25, "Problem 2, Part 2: Did you create buffers for the shopping centers?")
    def test_problem_2_part_2_buffer(self, problem2):
        section_data, namespace = problem2
        section = "Part 2"
        source = section_data[section]['source']

        assert "buffer" in source

    @points(0.25, "Problem 2, Part 2: Did you overwrite the `geometry` column with the buffer polygons?")
    def test_problem_2_part_2_geom(self, problem2):
        section_data, namespace = problem2
        section = "Part 2"
        variables = section_data[section]['variables']

        geom = variables['shopping_centres'].geometry.iloc[0]
        assert geom.is_valid
        assert geom.geom_type == "Polygon"

    @points(0.5, "Problem 2, Part 2: The buffer area is not within the expected range: did you use a 1500 m distance?")
    def test_problem_2_part_2_area(self, problem2):
        section_data, namespace = problem2
        section = "Part 2"
        variables = section_data[section]['variables']

        geom = variables['shopping_centres'].geometry.iloc[0]
        assert geom.is_valid
        assert geom.geom_type == "Polygon"
        expected_area = 3.14159 * 1500**2
        tolerance = 0.05 * expected_area
        assert abs(geom.area - expected_area) < tolerance

    @points(1, "Problem 2, Part 3: Did you save the buffers into a new layer `buffers` in `shopping_centres.gpkg`?")
    def test_problem_2_part_3(self, problem2):
        assert os.path.exists("data/shopping_centres.gpkg")
        layers = gpd.list_layers("data/shopping_centres.gpkg")["name"]
        assert any("buffer" in layer.lower() for layer in layers)
