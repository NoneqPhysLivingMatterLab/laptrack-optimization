# Scripts for "LapTrack: Linear assignment particle tracking with tunable metrics"
Parameter optimization for [LapTrack](https://github.com/yfukai/laptrack) with [Ray-Tune](https://www.ray.io/ray-tune).

## Executing the analysis

```bash
conda env create -f conda_env_minimum.yaml
conda activate optlaptrack

python execute.py --n-jobs=1 conditions_drift.yaml # for the cell migration dataset
python execute.py --n-jobs=1 conditions_synthetic.yaml # for the coloured particles dataset
python execute.py --n-jobs=1 conditions_homeostasis.yaml # for the mouse epidermis dataset

cd tracking_scripts
python a1_homeostasis_simple_LAP_baseline_grid.py # to perform grid search for the mouse epidermis dataset
python a2-1_yeast_toolkit_benchmark.py # to perform grid search for the Yeast Image Toolkit dataset
# execute a2-2_yeast_toolkit_benchmark_evaluation_platform.py 
# with following the instruction at the file top
# to evaluate the scores for the Yeast Image Toolkit dataset results
python a3_C2C12_simple_LAP_baseline_grid.py # to perform grid search for the C2C12 dataset
```

## Directories
- **data** the organized datasets
- **tracking_scripts** the tracking and plotting scripts
- **setting_yaml** YAML setting files for tracking scripts
- **results** the tracking results
- **plots** the result plots

## Tracking scripts
Located in `tracking_scripts`, executed via `execute.py`.
- **01_simple_LAP.py** LAP with Euclidean distance only
- **02_simple_LAP_with_drift.py** LAP with Euclidean distance and the drift term
- **03_simple_LAP_with_similarity-simple.py** LAP with the feature Euclidean distance term
- **04_simple_LAP_with_overlap_dist_sum.py** LAP with overlap cost function 

## Plotting scripts
Located in `tracking_scripts`, executed as Jupyter notebooks in, e.g., Visual Studio Code.
- **z1-1_make_grid_search_plots.py** Generate Fig. 2(b), S1, and S3.
- **z1-2_make_yeast_grid_search_plots.py** Generate Fig. S2.
- **z2_CellMigration_summarize_results.py** Generate Fig. 2(d) and S2.
- **z3_synthetic_summarize_results.py** Generate Fig. 2(f) and S3.
- **z4_homeostasis_summarize_results.py** Generate Fig. 2(g).
- **z5_summarize_properties.py** Summarize particle counts.

## Other scripts
Located in `tracking_scripts`.
- **a1_homeostasis_simple_LAP_baseline_grid.py** Performs grid search for the mouse epidermis dataset.
- **a2-1_yeast_toolkit_benchmark.py** Performs grid search for the Yeast Image Toolkit dataset.
- **a2-2_yeast_toolkit_benchmark_evaluation_platform.py** Evaluate tracking scores for the Yeast Image Toolkit dataset results (generated by a2-1_yeast_toolkit_benchmark.py).
- **a3_C2C12_simple_LAP_baseline_grid.py** Performs grid search for the C2C12 dataset.

## Datasets
Located in `data`. 
- **CellMigration** Data for the cell migration dataset.
- **homeostasis** Data for the mouse epidermis dataset.
- **synthetic** Data for the coloured particles dataset.
- **yeast_image_toolkit_benchmark** Data for the Yeast Image Toolkit dataset.
- **C2C12** Data for the C2C12 dataset.

## Results
Located in `results`.
- **CellMigration_use_0.05** Results for the cell migration dataset.
- **homeostasis** Results for the mouse epidermis dataset.
- **homeostasis_grid_search** Results for parameter grid search with the mouse epidermis dataset.
- **synthetic** Reksults for the coloured particles dataset.
- **yeast_image_toolkit_benchmark** Results for parameter grid search with the Yeast Image Toolkit dataset.
- **C2C12_grid_search** Results for parameter grid search with the C2C12 dataset.

## Interactive annotation example
- The example for interactive annotation with napari is located in [The LapTrack repository](https://github.com/yfukai/laptrack/blob/720815bbf9f209d3e7bd6142ee9b5b43ec4ee0b3/docs/examples/napari_interactive_fix.ipynb).

## Credits

- The data in `data/CellMigration` are generated from data in [10.5281/zenodo.6087728](https://doi.org/10.5281/zenodo.6087728), which are distributed with [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode).
- The data in `data/homeostasis` are generated from data in the [Cell interaction paper repository](https://github.com/NoneqPhysLivingMatterLab/cell_interaction_gnn).
- The data in `data/C2C12` are generated from data in https://osf.io/ysaq2/, which is distributed with [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode). See [10.1038/sdata.2018.237](https://doi.org/10.1038/sdata.2018.237) for details.
- The data in `data/yeast_image_toolkit_benchmark` is generated from data in [Yeast Image Toolkit website](http://yeast-image-toolkit.biosim.eu/pmwiki.php) with the author consent.

## Note

To reproduce the publication result in the precisely same environment, 
the following command should be executed at the commit `160a34f20f3e6a6ac4f894eb9fe4f6092a747843`.

```bash
python execute.py --n-jobs=1 conditions_drift.yaml # for the cell migration dataset
python execute.py --n-jobs=1 conditions_synthetic.yaml # for the coloured particles dataset
python execute.py --n-jobs=1 conditions_homeostasis.yaml # for the mouse epidermis dataset

cd tracking_scripts
python a1_homeostasis_simple_LAP_baseline_grid.py # to perform grid search for the mouse epidermis dataset 
```