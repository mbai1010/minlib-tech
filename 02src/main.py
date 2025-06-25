from minlib_shrink import run_shrink_process
import config
import os


def main():
    component_paths = [
        os.path.join(entry["path"], entry["name"])
        for entry in config.COMPONENTS
    ]    
    run_shrink_process(input_files=component_paths)


if __name__ == "__main__":
    main()
