# DVC Workflow

## Overview

DVC (Data Version Control) is used to version and manage datasets alongside Git.

Git tracks the DVC metadata files (`.dvc`), while DVC tracks the actual dataset contents.

## DVC Remote

A local directory is configured as the DVC remote:

```bash
mkdir -p ~/dvc-remote-storage
dvc remote add -d myremote ~/dvc-remote-storage