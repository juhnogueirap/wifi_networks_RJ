run-slice_grid:
	@pipenv run python -m etl_scripts.01_slice_grid

run-join-results:
	@pipenv run python -m etl_scripts.03_join_results

run-per-city-per-features:
	@pipenv run python -m analysis_scripts.map_networks_per_city_per_features

run-map-per-city:
	@pipenv run python -m analysis_scripts.map_networks_per_city

run-per-ap:
	@pipenv run python -m analysis_scripts.networks_per_APs

run-nws-in-years:
	@pipenv run python -m analysis_scripts.x_networks_in_y_years

run-per-bairro-aps:
	@pipenv run python -m analysis_scripts.networks_per_bairro_Rio
