# GitLab CI/CD Cache Guide

GitLab provides a caching system for jobs to speed up pipelines by reusing dependencies like `node_modules`, Ruby gems, and other build artifacts. This guide covers how to configure and use caching effectively.

---

## Key Features

* **Cache Storage**: Data is saved in the GitLab Runner and can also be stored in external storage such as S3, MinIO, GCS, etc.
* **Branch-Specific Caching**: Maintain separate caches per branch, job, or stage.
* **Fallbacks**: Jobs can pull cache from other branches if the current branch does not have cache.
* **Simple Cache**: Uses file locks and directory caching for efficiency.

---

## Basic Cache Example

Cache dependencies like Ruby gems and Yarn modules:

```yaml
test-job:
  stage: build
  cache:
    - key:
        files:
          - Gemfile.lock
      paths:
        - vendor/ruby
    - key:
        files:
          - yarn.lock
      paths:
        - .yarn-cache/
  script:
    - bundle config set --local path 'vendor/ruby'
    - bundle install
    - yarn install --cache-folder .yarn-cache
    - echo "Run tests..."
```

**Behavior**:
If the lock file (`Gemfile.lock` or `yarn.lock`) changes, the cache is updated automatically.

---

## Branch Cache with Fallbacks

When creating a new branch, it may not have a cache yet. You can pull from the default branch (e.g., `main` or `master`) or a global default cache:

```yaml
test-job:
  stage: build
  cache:
    - key: cache-$CI_COMMIT_REF_SLUG
      fallback_keys:
        - cache-$CI_DEFAULT_BRANCH
        - cache-default
      paths:
        - vendor/ruby
  script:
    - bundle config set --local path 'vendor/ruby'
    - bundle install
    - echo "Run tests..."
```

---

## Default Cache Configuration

Define a global cache for all jobs and override it for specific jobs as needed:

```yaml
default:
  cache: &global_cache
    key: $CI_COMMIT_REF_SLUG
    paths:
      - node_modules/
      - public/
      - vendor/
    policy: pull-push

job:
  cache:
    <<: *global_cache
    policy: pull  # Override policy for this job
```

---

## Cache Policies

| Policy    | Description                                            |
| --------- | ------------------------------------------------------ |
| pull      | Only fetch the cache, do not update it.                |
| pull-push | Fetch the cache and update it after the job completes. |

---

## Cache Examples

* **Per Job & Branch**

```yaml
cache:
  key: "$CI_JOB_NAME-$CI_COMMIT_REF_SLUG"
```

* **Per Stage & Branch**

```yaml
cache:
  key: "$CI_JOB_STAGE-$CI_COMMIT_REF_SLUG"
```

---

## Conditional Cache Policy

Update cache only on the default branch; otherwise, just pull:

```yaml
conditional-policy:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      variables:
        POLICY: pull-push
    - if: $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH
      variables:
        POLICY: pull
  stage: build
  cache:
    key: gems
    policy: $POLICY
    paths:
      - vendor/bundle
  script:
    - echo "This job pulls and pushes the cache depending on the branch"
    - echo "Downloading dependencies..."
```

---

## Cache Based on Lock Files

Update cache automatically when `package-lock.json` changes:

```yaml
default:
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
```

**Tip**: This ensures your npm modules are always synced with the lock file.

---

## Summary

* Use **branch-specific keys** for independent caches.
* Use **fallback_keys** to share cache between branches.
* **Policies** control whether cache is updated or only fetched.
* Use **lock files** to trigger cache updates automatically.

Caching effectively can dramatically reduce build times and maintain clean, efficient pipelines.

