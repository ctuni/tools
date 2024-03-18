import os

import pytest

from nf_core.modules.modules_json import ModulesJson
from nf_core.subworkflows.install import SubworkflowInstall

from ..utils import (
    GITLAB_BRANCH_TEST_BRANCH,
    GITLAB_REPO,
    GITLAB_SUBWORKFLOWS_BRANCH,
    GITLAB_SUBWORKFLOWS_ORG_PATH_BRANCH,
    GITLAB_URL,
    with_temporary_folder,
)

"""
Test the 'nf-core subworkflows patch' command
"""


def setup_patch(self, pipeline_dir, modify_subworkflow):
    # Install the subworkflow bam_sort_stats_samtools
    subworkflow_path = os.path.join(self.subworkflow_install.dir, "subworkflows", "nf-core", "bam_sort_stats_samtools")
    sub_subworkflow_path = os.path.join(self.subworkflow_install.dir, "subworkflows", "nf-core", "bam_stats_samtools")
    samtools_index_path = os.path.join(self.subworkflow_install.dir, "modules", "nf-core", "samtools", "index")
    samtools_sort_path = os.path.join(self.subworkflow_install.dir, "modules", "nf-core", "samtools", "sort")
    samtools_stats_path = os.path.join(self.subworkflow_install.dir, "modules", "nf-core", "samtools", "stats")
    samtools_idxstats_path = os.path.join(self.subworkflow_install.dir, "modules", "nf-core", "samtools", "idxstats")
    samtools_flagstat_path = os.path.join(self.subworkflow_install.dir, "modules", "nf-core", "samtools", "flagstat")

    if modify_subworkflow:
        # Modify the subworkflow
        subworkflow_path = Path(pipeline_dir, "subworkflows", "nf-core", "bam_sort_stats_samtools")
        modify_subworkflow(subworkflow_path / "main.nf")


def modify_subworkflow(path):
    """Modify a file to test patch creation"""
    with open(path) as fh:
        lines = fh.readlines()
    # We want a patch file that looks something like:
    # -    ch_fasta // channel: [ val(meta), path(fasta) ]
    for line_index in range(len(lines)):
        if lines[line_index] == "    ch_fasta // channel: [ val(meta), path(fasta) ]\n":
            to_pop = line_index
    lines.pop(to_pop)
    with open(path, "w") as fh:
        fh.writelines(lines)


def test_create_patch_change(self):
    """Test creating a patch when there is a change to the module"""


def test_create_patch_no_change(self):
    """Test creating a patch when there is no change to the subworkflow"""
    # Try creating a patch file
    # Check that no patch file has been added to the directory


def test_create_patch_try_apply_failed(self):
    """Test creating a patch file and applying it to a new version of the the files"""


def test_create_patch_try_apply_successful(self):
    """Test creating a patch file and applying it to a new version of the the files"""


def test_create_patch_update_fail(self):
    """Test creating a patch file and updating a subworkflow when there is a diff conflict"""


def test_create_patch_update_success(self):
    """
    Test creating a patch file and the updating the subworkflow

    Should have the same effect as 'test_create_patch_try_apply_successful'
    but uses higher level api
    """


def test_remove_patch(self):
    """Test creating a patch when there is no change to the subworkflow"""