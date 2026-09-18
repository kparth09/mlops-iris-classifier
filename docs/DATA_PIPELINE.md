# Data Pipeline Documentation

## Overview

This project uses a modular DVC pipeline for collecting, preprocessing,
feature engineering, and validating Iris dataset data.

The pipeline consists of four stages:

```text
Raw Data Source
      |
      v
+-------------+
|   Collect   |
+-------------+
      |
      v
+-------------+
| Preprocess  |
+-------------+
      |
      v
+-------------+
|  Features   |
+-------------+
      |
      v
+-------------+
|  Validate   |
+-------------+
      |
      v
Validated Data