from pathlib import Path
from typing import Dict, List, Union

from nf_core.modules.modules_json import ModulesJson, ModulesJsonType


def modules_json(self) -> Dict[str, List[str]]:
    """Make sure all modules described in the ``modules.json`` file are actually installed

    Every module installed from ``nf-core/modules`` must have an entry in the ``modules.json`` file
    with an associated version commit hash.

    * Failure: If module entries are found in ``modules.json`` for modules that are not installed
    """
    passed = []
    warned = []
    failed = []

    # Load pipeline modules and modules.json
    _modules_json = ModulesJson(self.wf_path)
    _modules_json.load()
    modules_json_dict: Union[ModulesJsonType, None] = _modules_json.modules_json
    modules_dir = Path(self.wf_path, "modules")

    if _modules_json and modules_json_dict is not None:
        all_modules_passed = True

        for repo in modules_json_dict["repos"].keys():
            # Check if the modules.json has been updated to keep the
            if "modules" not in modules_json_dict["repos"][repo] or not repo.startswith("http"):
                failed.append(
                    "Your `modules.json` file is outdated. "
                    "It will be automatically generated by running any module command."
                )
                continue

            for dir in modules_json_dict["repos"][repo]["modules"].keys():
                for module, module_entry in modules_json_dict["repos"][repo]["modules"][dir].items():
                    if not Path(modules_dir, dir, module).exists():
                        failed.append(
                            f"Entry for `{Path(modules_dir, dir, module)}` found in `modules.json` but module is not installed in "
                            "pipeline."
                        )
                        all_modules_passed = False
                    if module_entry.get("branch") is None:
                        failed.append(f"Entry for `{Path(modules_dir, dir, module)}` is missing branch information.")
                    if module_entry.get("git_sha") is None:
                        failed.append(f"Entry for `{Path(modules_dir, dir, module)}` is missing version information.")
        if all_modules_passed:
            passed.append("Only installed modules found in `modules.json`")
    else:
        warned.append("Could not open `modules.json` file.")

    return {"passed": passed, "warned": warned, "failed": failed}