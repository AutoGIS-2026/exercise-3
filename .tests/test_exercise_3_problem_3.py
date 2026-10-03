from points_decorator import points
import pandas as pd
import geopandas as gpd
import pyproj


# Expected population within 1.5 km of each shopping centre. Geocoding results (and,
# hence, the buffers) vary slightly with the addresses used and with Nominatim updates.
EXPECTED_POPULATION = {
    "Forum": 55504,
    "Iso Omena": 26698,
    "Itis": 20889,
    "Jumbo": 10956,
    "REDI": 26341,
    "Sello": 24877,
    "Tripla": 24394,
}
RELATIVE_TOLERANCE = 0.1


def population_results(variables):
    """
    Find the per-shopping-centre population sums among the notebook’s variables.

    Students may name the result as they like, group by `id` or by `name`, and
    spell the names differently ("Iso Omena", "Iso-Omena", ...), so compare the
    sorted values only.
    """
    for value in variables.values():
        if isinstance(value, pd.DataFrame):
            candidates = [value[column] for column in value.select_dtypes("number").columns]
        elif isinstance(value, pd.Series):
            candidates = [value]
        else:
            continue
        for series in candidates:
            if len(series) == len(EXPECTED_POPULATION):
                yield series


def matches_expected(series):
    actual = sorted(float(value) for value in series)
    expected = sorted(EXPECTED_POPULATION.values())
    return all(
        abs(a - e) <= RELATIVE_TOLERANCE * e
        for a, e in zip(actual, expected)
    )


class TestProblem3:
    @points(1, "Problem 3, Part 1: Did you load the population grid from the WFS service into a GeoDataFrame `population_grid` in EPSG:3879?")
    def test_problem_3_part_1_grid(self, problem3):
        section_data, namespace = problem3
        section = "Part 1"
        variables = section_data[section]['variables']
        source = section_data[section]['source']

        assert isinstance(variables['population_grid'], gpd.GeoDataFrame)
        assert variables['population_grid'].crs == pyproj.CRS("EPSG:3879")
        assert "wfs" in source.lower()

    @points(1, "Problem 3, Part 1: Did you import the shopping centre buffers?")
    def test_problem_3_part_1_centres(self, problem3):
        section_data, namespace = problem3
        section = "Part 1"
        variables = section_data[section]['variables']

        assert isinstance(variables['shopping_centre_buffers'], pd.DataFrame)
        assert len(variables['shopping_centre_buffers']) == 7

    @points(4, "Problem 3, Part 2: Did you carry out a spatial join (`sjoin`) using the `within` predicate?")
    def test_problem_3_part_2(self, problem3):
        section_data, namespace = problem3
        section = "Part 2"
        source = section_data[section]['source']

        assert "sjoin" in source
        assert "within" in source

    @points(4, "Problem 3, Part 3: Are the population numbers for the shopping centres realistic?")
    def test_problem_3_part_3_population(self, problem3):
        section_data, namespace = problem3
        section = "Part 3"
        variables = section_data[section]['variables']

        assert any(
            matches_expected(series)
            for series in population_results(variables)
        )
