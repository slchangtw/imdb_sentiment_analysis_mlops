params = {
    "direction": "minimize",
    "n_trials": 3,
    "metric": "loss_val",
    "params": {
        "int": {
            "max_iter": {"low": 800, "high": 1200},
            "max_depth": {"low": 3, "high": 10},
            "min_samples_leaf": {"low": 10, "high": 25},
        },
        "float": {
            "learning_rate": {"low": 0.1, "high": 0.5, "log": True},
            "l2_regularization": {"low": 1e-10, "high": 1e-3, "log": True},
        },
    },
}
