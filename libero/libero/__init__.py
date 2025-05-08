import os
import yaml

# This is a default path for localizing all the benchmark related files
libero_config_path = os.environ.get(
    "LIBERO_CONFIG_PATH", os.path.expanduser("~/.libero")
)
config_file = os.path.join(libero_config_path, "config.yaml")


def get_default_path_dict(custom_location=None):
    if custom_location is None:
        benchmark_root_path = os.path.dirname(os.path.abspath(__file__))
    else:
        benchmark_root_path = custom_location

    # This is a default path for localizing all the default bddl files
    bddl_files_default_path = os.path.join(benchmark_root_path, "./bddl_files")

    # This is a default path for localizing all the default bddl files
    init_states_default_path = os.path.join(benchmark_root_path, "./init_files")

    # This is a default path for localizing all the default datasets
    dataset_default_path = os.path.join(benchmark_root_path, "../datasets")

    # This is a default path for localizing all the default assets
    assets_default_path = os.path.join(benchmark_root_path, "./assets")

    return {
        "benchmark_root": benchmark_root_path,
        "bddl_files": bddl_files_default_path,
        "init_states": init_states_default_path,
        "datasets": dataset_default_path,
        "assets": assets_default_path,
    }


def get_libero_path(query_key):
    with open(config_file, "r") as f:
        config = dict(yaml.load(f.read(), Loader=yaml.FullLoader))

    # Give warnings in case the user needs to access the paths
    for key in config:
        if not os.path.exists(config[key]):
            print(f"[Warning]: {key} path {config[key]} does not exist!")

    assert (
        query_key in config
    ), f"Key {query_key} not found in config file {config_file}. You need to modify it. Available keys are: {config.keys()}"
    return config[query_key]


def set_libero_default_path(custom_location=os.path.dirname(os.path.abspath(__file__))):
    print(
        f"[Warning] You are changing the default path for Libero config. This will affect all the paths in the config file."
    )
    new_config = get_default_path_dict(custom_location)
    with open(config_file, "w") as f:
        yaml.dump(new_config, f)


def get_env_from_task(task, task_id=None, benchmark=None, **kwargs):
    """
    Create an environment for a specific task.
    
    Args:
        task (str): Task name
        task_id (int, optional): Task ID in the benchmark
        benchmark (str, optional): Benchmark name (e.g., 'libero_10')
        **kwargs: Additional arguments to pass to the environment
    
    Returns:
        OffScreenRenderEnv: The environment instance
    """
    from libero.libero.benchmark import get_benchmark, get_task
    from libero.libero.envs.env_wrapper import OffScreenRenderEnv
    
    # Get BDDL file path
    if benchmark is not None and task_id is not None:
        # If benchmark and task_id are provided, get the task information from the benchmark
        benchmark_obj = get_benchmark(benchmark)
        benchmark_instance = benchmark_obj()  # Create an instance of the benchmark
        task_obj = benchmark_instance.get_task(i=task_id)
        bddl_file_path = os.path.join(
            get_libero_path("bddl_files"),
            task_obj.problem_folder,
            task_obj.bddl_file
        )
    else:
        # Otherwise, construct the path from the task name
        # This assumes the task name follows the convention and is in one of the standard benchmark folders
        for benchmark_folder in ["libero_10", "libero_90", "libero_spatial", "libero_object", "libero_goal"]:
            potential_path = os.path.join(
                get_libero_path("bddl_files"),
                benchmark_folder,
                f"{task}.bddl"
            )
            if os.path.exists(potential_path):
                bddl_file_path = potential_path
                break
        else:
            # If not found in standard folders, try direct path
            bddl_file_path = os.path.join(
                get_libero_path("bddl_files"),
                f"{task}.bddl"
            )
            if not os.path.exists(bddl_file_path):
                raise FileNotFoundError(f"Could not find BDDL file for task {task}")
    
    # Create environment
    env_args = {
        "bddl_file_name": bddl_file_path,
        "camera_heights": 128,
        "camera_widths": 128,
        **kwargs  # Add any additional arguments
    }
    
    return OffScreenRenderEnv(**env_args)


if not os.path.exists(libero_config_path):
    os.makedirs(libero_config_path)

if not os.path.exists(config_file):
    # Create a default config file

    default_path_dict = get_default_path_dict()
    answer = input(
        "Do you want to specify a custom path for the dataset folder? (Y/N): "
    ).lower()
    if answer == "y":
        # If the user wants to specify a custom storage path, prompt them to enter it
        custom_dataset_path = input(
            "Enter the path where you want to store the datasets: "
        )
        full_custom_dataset_path = os.path.join(
            os.path.abspath(os.path.expanduser(custom_dataset_path)), "datasets"
        )
        # Check if the custom storage path exists, and create if it doesn't

        print("The full path of the custom storage path you entered is:")
        print(full_custom_dataset_path)
        print("Do you want to continue? (Y/N)")
        confirm_answer = input().lower()
        if confirm_answer == "y":
            if not os.path.exists(full_custom_dataset_path):
                os.makedirs(full_custom_dataset_path)
            default_path_dict["datasets"] = full_custom_dataset_path
    print("Initializing the default config file...")
    print(f"The following information is stored in the config file: {config_file}")
    # write all the paths into a yaml file
    with open(config_file, "w") as f:
        yaml.dump(default_path_dict, f)
    for key, value in default_path_dict.items():
        print(f"{key}: {value}")
