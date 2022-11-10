##############
#
# The script to perform tracking of C2C12 datasets
# with grid points of the cutoff parameters.
#
###############

########### Importing packages ###########

from laptrack import LapTrack
from functools import partial
from itertools import product
from ray import tune
from ray.tune.search import BasicVariantGenerator
import numpy as np
import os
from os import path

from utils.common import power_dist, read_yaml
from utils.data_loader import read_data
from laptrack.scores import calc_scores

LAP_NAME = "01-2_Simple_LAP_baseline_grid"

########### Setting the search range of each parameters ###########

# max_dists ... the cutoff for the cost function at tracking
max_dists = np.linspace(2, 47, 16).tolist()
# gap_closing_max_dists ... the cutoff for the cost function at gap closing
split_max_dists = np.linspace(2, 47, 16).tolist()
gap_closings = [0, 1]

config = {
    "max_distance": tune.grid_search(max_dists),
    "splitting_max_distance": tune.grid_search(split_max_dists),
    #    "gap_closing_max_distance": tune.grid_search(np.linspace(4, 20, 4)) ,
    "gap_closing": tune.grid_search(gap_closings),
}
initial_configs = [
    {
        "max_distance": max_dist,
        "splitting_max_distance": split_max_dist,
        #    "gap_closing_max_distance": 20,
        "gap_closing": gap_closing,
    }
    for max_dist, split_max_dist, gap_closing in product(
        max_dists, split_max_dists, gap_closings
    )
]

########### A function to get a LapTrack object with a given config ###########

def get_tracker(config, regionprop_keys=None):
    ws = [1, 1] + [0] * (len(regionprop_keys) - 1)
    dist_power = 2
    return LapTrack(
        track_cost_cutoff=config["max_distance"] ** dist_power,
        splitting_cost_cutoff=config["splitting_max_distance"] ** dist_power,
        gap_closing_cost_cutoff=config["splitting_max_distance"] ** dist_power,
        gap_closing_max_frame_count=config["gap_closing"],
        track_dist_metric=partial(power_dist, ws=ws, power=dist_power),
        splitting_dist_metric=partial(power_dist, ws=ws, power=dist_power),
    )

########### The main function for grid search ###########

def main():
    base_dir = "../data/C2C12/organized_data/BMP2_updated"
    yaml_path = "../setting_yaml/C2C12.yaml"
    results_dir = "../results/C2C12_grid_search"
    os.makedirs(results_dir, exist_ok=True)

    single_shot_count = 52

    yaml_params = read_yaml(yaml_path)
    regionprop_keys = yaml_params["regionprop_keys"]
    normalize_exclude_keys = yaml_params["normalize_exclude_keys"]
    coords, track_labels, true_edges, GT_TRA_images = read_data(
        base_dir, regionprop_keys
    )

    ########### The function to track, save scores and results ###########
    def calc_fitting_score(config, report=True):
        lt = get_tracker(
            config,
            regionprop_keys=regionprop_keys,
        )
        # track the cells
        track_tree = lt.predict(coords)
        predicted_edges = list(track_tree.edges())
        # calculate the score
        score_dict = calc_scores(true_edges, predicted_edges)
        if report:
            tune.report(**score_dict)

    #    # test run
    #    test_config = initial_configs[0].copy()
    #    calc_fitting_score(test_config, report=False)

    ########### Execute grid search by Ray-Tune ###########
    config2 = config.copy()
    search_alg = BasicVariantGenerator(
        points_to_evaluate=initial_configs,
        max_concurrent=single_shot_count,
    )
    analysis = tune.run(
        calc_fitting_score,
        config=config2,
        metric="Jaccard_index",
        mode="max",
        search_alg=search_alg,
        #                resources_per_trial={"cpu": single_shot_count*4}
    )
    ########### Save results ###########
    # sort the result by connection Jaccard index and save
    analysis_df = analysis.results_df.sort_values(by="Jaccard_index", ascending=False)
    analysis_df.to_csv(path.join(results_dir, "C2C12_grid_search.csv"))


if __name__ == "__main__":
    main()
