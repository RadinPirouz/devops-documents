# GitLab CI/CD Cache Guide

GitLab CI/CD provides a caching mechanism to speed up pipeline execution by reusing dependencies and build artifacts such as `node_modules`, Ruby gems, or compiled binaries. This guide covers how to configure, optimize, and manage caching effectively.

---

## Key Features of GitLab Cache

* **Cache Storage**: Cache data is stored in the GitLab Runner and can optionally be persisted in external storage such as S3, MinIO, Google Cloud Storage (GCS), or Azure Blob Storage.
* **Branch-Specific Caching**: Create independent caches per branch, job, or pipeline stage to avoid conflicts.
* **Fallbacks**: Jobs can retrieve cache from other branches if the current branch has no cache yet.
* **Simple & Efficient**: Uses file locks and directory caching to maximize efficiency without complex configurations.

---

## Basic Cache Example

A typical caching configuration for Ruby gems and Yarn modules:

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
If the lock file (`Gemfile.lock` or `yarn.lock`) changes, the cache is updated automatically, ensuring dependencies remain consistent with the project.

---

## Configuring GitLab Runner to Use S3 Cache

You can configure the GitLab Runner to save cache to S3 storage as follows:

```toml
[[runners]]
  [runners.cache]
    Type = "s3"
    [runners.cache.s3]
      ServerAddress = "s3.example.com"
      AccessKey = "access-key"
      SecretKey = "secret-key"
      BucketName = "runner"
      Insecure = true  # true = http, false = https
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
```

---

## Branch-Specific Cache with Fallbacks

When a new branch does not yet have a cache, it can use fallback caches from other branches:

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

Define a global cache and override it per job as necessary:

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
    policy: pull  # Overrides global policy for this job
```

---

## Cache Policies

| Policy    | Description                                       |
| --------- | ------------------------------------------------- |
| pull      | Fetches cache without updating it                 |
| pull-push | Fetches cache and updates it after job completion |

---

## Cache Examples

**Per Job & Branch**:

```yaml
cache:
  key: "$CI_JOB_NAME-$CI_COMMIT_REF_SLUG"
```

**Per Stage & Branch**:

```yaml
cache:
  key: "$CI_JOB_STAGE-$CI_COMMIT_REF_SLUG"
```

---

## Conditional Cache Policy

Update cache only on the default branch while other branches only fetch:

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

Automatically update cache when lock files change, e.g., `package-lock.json`:

```yaml
default:
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
```

**Tip**: Using lock files ensures that cached dependencies are always consistent with the project’s declared versions.

---

## Best Practices Summary

* Use **branch-specific keys** for independent caches to avoid conflicts.
* Use **fallback_keys** to share caches across branches.
* Use **cache policies** to control whether cache is updated or only fetched.
* Leverage **lock files** to trigger cache updates automatically.

Proper caching can dramatically reduce build times, improve pipeline efficiency, and ensure consistent builds across branches and environments.
