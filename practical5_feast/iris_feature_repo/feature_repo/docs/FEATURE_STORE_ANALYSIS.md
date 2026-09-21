# Feature Store Analysis

## 1. Elimination of Training-Serving Skew

Feast provides the same registered feature definitions for both
offline and online retrieval.

The `iris_engineered_features` FeatureView is used during:

- Online feature retrieval
- Historical feature retrieval
- Feature Service retrieval

This ensures that engineered features such as:

- `sepal_area`
- `petal_area`
- `sepal_to_petal_length_ratio`
- `petal_length_bin`

are defined consistently across different consumers.

Therefore, the risk of training-serving skew is reduced.

## 2. Feature Reusability

The registered features can be reused by different models and tasks
without reimplementing the feature engineering logic.

In Step 8, the `iris_feature_service` was used to retrieve the same
registered features without recalculating or redefining them.

This demonstrates that features can be shared across different
machine-learning use cases.

## 3. Centralized Feature Governance

The feature definitions are centralized in `features.py`.

This file acts as a single source of truth for:

- Entities
- Data sources
- Feature Views
- Feature schemas
- Feature Services

Models and other consumers can therefore use the registered features
instead of maintaining separate feature definitions.

## Conclusion

The Feast feature store provides a centralized way to define, manage,
retrieve, and reuse machine-learning features.

The experiment demonstrated:

1. Online feature retrieval.
2. Historical feature retrieval.
3. Reuse through a Feature Service.
4. Centralized feature definitions.
5. Consistent feature usage across different consumers.