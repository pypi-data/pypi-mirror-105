import copy
import importlib
import json
import logging
import os
import sys

import setuptools


def get_plugin_package_name_from_path(path):
    for pkg_name in setuptools.find_packages(where=path):
        importlib.import_module(name="{}.plugin".format(pkg_name))
        return pkg_name
    raise Exception("No plugin packages found. Note: plugin modules must contain an __init__.py and a plugin.py file")


def create_manifest_files(path):
    print("CREATING MANIFEST")
    sys.path.append(path)
    from pistarlab.utils import env_helpers
    module_name = get_plugin_package_name_from_path(path)
    sys.path.append(path)
    pluginmod = importlib.import_module(name="{}.plugin".format(module_name))
    manifest_data = pluginmod.manifest()
    # plugin_id = pluginmod.PLUGIN_ID
    # plugin_version = pluginmod.PLUGIN_VERSION

    output_path = os.path.join(path, module_name)
    manifest_files_path = os.path.join(output_path, 'manifest_files')
    os.makedirs(manifest_files_path, exist_ok=True)
    # Probe environment metadata
    env_specs = manifest_data.get('env_specs')
    if env_specs is not None:
        updated_env_specs = []
        for spec_data in env_specs:
            metadata = env_helpers.probe_env_metadata(spec_data, image_path=manifest_files_path)
            spec_data['metadata'] = metadata
            updated_env_specs.append(copy.deepcopy(spec_data))
        manifest_data["env_specs"] = updated_env_specs

    with open(os.path.join(output_path, "manifest.json"), 'w') as f:
        json.dump(manifest_data, f, indent=2)
    print("Registry saved to {}".format(output_path))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True, choices=["save_manifest"], help="options = [save_manifest]")
    parser.add_argument("--plugin_path", help="Path to plugin project root")
    args = parser.parse_args()
    if args.action == "save_manifest":
        create_manifest_files(args.plugin_path)
    else:
        print(f"Unknown action {args.action}")


if __name__ == "__main__":
    # Setup Logging
    root = logging.getLogger('pistarlab_plugin')
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    main()
