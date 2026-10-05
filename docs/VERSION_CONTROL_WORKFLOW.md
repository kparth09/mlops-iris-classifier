# Version Control Workflow — MLOps Iris Classifier

## 1. Overview

This document describes the Git-based version control workflow
used for the MLOps Iris Classifier project.

- **Repository:** mlops-iris-classifier
- **Primary language:** Python
- **Maintainer:** Parth Khandelwal

## 2. Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable and deployable code |
| `develop` | Integration branch for development |
| `feature/add-classification-report` | Adds classification report functionality |
| `conflict-demo-a` | Demonstrates one side of a merge conflict |
| `conflict-demo-b` | Demonstrates the other side and conflict resolution |

### Workflow

Changes are developed on feature branches and merged into
`develop` through Pull Requests.

The general flow is:

`feature/* → Pull Request → develop → main`

The `conflict-demo-*` branches were created specifically to
practice merge conflict resolution.

## 3. Commit Convention

Commits follow the format:

`<type>: <short description>`

Common types include:

- `feat:` — new functionality
- `fix:` — bug fixes
- `docs:` — documentation changes
- `chore:` — tooling and configuration changes
- `refactor:` — code restructuring

Examples:

```text
feat: add classification report to training script
docs: update README title
merge: resolve conflict in training script
```

## 4. Resolving Merge Conflicts

When a merge reports a conflict, Git marks the file with
`<<<<<<<`, `=======` and `>>>>>>>` markers showing both sides:

```text
<<<<<<< HEAD
/iris_raw.csv
=======
>>>>>>> origin/main
```

Resolve it by editing the file to keep the intended content, then stage it:

```bash
git add <file>
git commit
```

To abandon a merge entirely:

```bash
git merge --abort
```