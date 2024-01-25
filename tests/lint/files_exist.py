from pathlib import Path

import nf_core.lint


def test_files_exist_missing_config(self):
    """Lint test: critical files missing FAIL"""
    new_pipeline = self._make_pipeline_copy()

    Path(new_pipeline, "CHANGELOG.md").unlink()

    lint_obj = nf_core.lint.PipelineLint(new_pipeline)
    lint_obj._load()
    lint_obj.nf_config["manifest.name"] = "nf-core/testpipeline"

    results = lint_obj.files_exist()
    assert results["failed"] == ["File not found: `CHANGELOG.md`"]


def test_files_exist_missing_main(self):
    """Check if missing main issues warning"""
    new_pipeline = self._make_pipeline_copy()

    Path(new_pipeline, "main.nf").unlink()

    lint_obj = nf_core.lint.PipelineLint(new_pipeline)
    lint_obj._load()

    results = lint_obj.files_exist()
    assert "File not found: `main.nf`" in results["warned"]


def test_files_exist_depreciated_file(self):
    """Check whether depreciated file issues warning"""
    new_pipeline = self._make_pipeline_copy()

    nf = Path(new_pipeline, "parameters.settings.json")
    nf.touch()

    lint_obj = nf_core.lint.PipelineLint(new_pipeline)
    lint_obj._load()

    results = lint_obj.files_exist()
    assert results["failed"] == ["File must be removed: `parameters.settings.json`"]


def test_files_exist_pass(self):
    """Lint check should pass if all files are there"""

    new_pipeline = self._make_pipeline_copy()
    lint_obj = nf_core.lint.PipelineLint(new_pipeline)
    lint_obj._load()

    results = lint_obj.files_exist()
    assert results["failed"] == []


def test_files_exist_hint(self):
    """Check if hint is added to missing crate file"""
    new_pipeline = self._make_pipeline_copy()

    Path(new_pipeline, "ro-crate-metadata.json").unlink()

    lint_obj = nf_core.lint.PipelineLint(new_pipeline)
    lint_obj._load()

    results = lint_obj.files_exist()
    assert results["warned"] == [
        "File not found: `ro-crate-metadata.json`. Run `nf-core rocrate` to generate this file. Read more about RO-Crates in the [nf-core/tools docs](https://nf-co.re/tools#create-a-ro-crate-metadata-file)."
    ]
