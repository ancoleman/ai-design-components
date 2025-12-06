# CI/CD Security Scanning Patterns

Complete CI/CD integration patterns for GitHub Actions, GitLab CI, Jenkins, and Azure Pipelines.

## Table of Contents

1. [GitHub Actions](#github-actions)
2. [GitLab CI](#gitlab-ci)
3. [Jenkins](#jenkins)
4. [Azure Pipelines](#azure-pipelines)

---

## GitHub Actions

### Multi-Stage Security Pipeline

```yaml
name: Security Scan Pipeline

on:
  pull_request:
  push:
    branches: [main]

jobs:
  # Stage 1: Fast checks (secrets, SAST)
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Gitleaks Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Semgrep Scan
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten

  # Stage 2: Dependency scanning
  dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Dependency Review
        uses: actions/dependency-review-action@v3
        with:
          fail-on-severity: high

  # Stage 3: Container scanning (after fast checks)
  container:
    runs-on: ubuntu-latest
    needs: [secrets, sast]
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: HIGH,CRITICAL
          exit-code: 1

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: trivy-results.sarif

      - name: Generate SBOM
        run: |
          trivy image --format cyclonedx \
            --output sbom.json \
            myapp:${{ github.sha }}

      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json

  # Stage 4: DAST (only on main branch)
  dast:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: container
    steps:
      - uses: actions/checkout@v4

      - name: OWASP ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: https://staging.example.com
          fail_action: true
```

## GitLab CI

```yaml
stages:
  - security-fast
  - security-scan
  - security-test

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

# Fast checks
gitleaks:
  stage: security-fast
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --verbose --exit-code 1
  allow_failure: false

semgrep:
  stage: security-fast
  image: returntocorp/semgrep
  script:
    - semgrep ci --config=p/security-audit
  allow_failure: false

# Container scanning
trivy-scan:
  stage: security-scan
  image: aquasec/trivy:latest
  script:
    - trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE_TAG
  artifacts:
    reports:
      container_scanning: gl-container-scanning-report.json

# SBOM generation
sbom-generate:
  stage: security-scan
  image: aquasec/trivy:latest
  script:
    - trivy image --format cyclonedx --output sbom.json $IMAGE_TAG
  artifacts:
    paths:
      - sbom.json
    expire_in: 90 days

# DAST
zap-scan:
  stage: security-test
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t https://staging.example.com -r zap-report.html
  artifacts:
    paths:
      - zap-report.html
    when: always
  only:
    - main
```

## Jenkins

```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = "myapp"
        IMAGE_TAG = "${env.GIT_COMMIT}"
    }

    stages {
        stage('Secret Scanning') {
            steps {
                sh 'gitleaks detect --source . --verbose --exit-code 1'
            }
        }

        stage('SAST') {
            steps {
                sh 'semgrep ci --config=p/security-audit'
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Container Scan') {
            steps {
                sh """
                    trivy image --severity HIGH,CRITICAL \
                      --exit-code 1 \
                      --format json \
                      --output trivy-results.json \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Generate SBOM') {
            steps {
                sh """
                    trivy image --format cyclonedx \
                      --output sbom.json \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                """
                archiveArtifacts artifacts: 'sbom.json'
            }
        }

        stage('DAST') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker run -v $(pwd):/zap/wrk/:rw \
                      owasp/zap2docker-stable \
                      zap-baseline.py -t https://staging.example.com \
                      -r zap-report.html
                '''
            }
        }
    }

    post {
        always {
            publishHTML([
                reportDir: '.',
                reportFiles: 'zap-report.html',
                reportName: 'ZAP Security Report'
            ])
        }
        failure {
            emailext(
                subject: "Security Scan Failed: ${env.JOB_NAME}",
                body: "Build ${env.BUILD_NUMBER} failed security scans.",
                to: "security-team@example.com"
            )
        }
    }
}
```

## Azure Pipelines

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  imageName: 'myapp'
  imageTag: $(Build.BuildId)

stages:
  - stage: SecurityFast
    displayName: 'Fast Security Checks'
    jobs:
      - job: Secrets
        steps:
          - task: Bash@3
            displayName: 'Gitleaks Scan'
            inputs:
              targetType: 'inline'
              script: |
                wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
                tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
                ./gitleaks detect --source . --verbose --exit-code 1

      - job: SAST
        steps:
          - task: Bash@3
            displayName: 'Semgrep Scan'
            inputs:
              targetType: 'inline'
              script: |
                pip install semgrep
                semgrep ci --config=p/security-audit

  - stage: ContainerScan
    displayName: 'Container Security Scan'
    dependsOn: SecurityFast
    jobs:
      - job: BuildAndScan
        steps:
          - task: Docker@2
            displayName: 'Build image'
            inputs:
              command: 'build'
              repository: $(imageName)
              tags: $(imageTag)

          - task: Bash@3
            displayName: 'Trivy Scan'
            inputs:
              targetType: 'inline'
              script: |
                wget https://github.com/aquasecurity/trivy/releases/download/v0.48.0/trivy_0.48.0_Linux-64bit.tar.gz
                tar -xzf trivy_0.48.0_Linux-64bit.tar.gz
                ./trivy image --severity HIGH,CRITICAL --exit-code 1 $(imageName):$(imageTag)

          - task: Bash@3
            displayName: 'Generate SBOM'
            inputs:
              targetType: 'inline'
              script: |
                ./trivy image --format cyclonedx --output $(Build.ArtifactStagingDirectory)/sbom.json $(imageName):$(imageTag)

          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: '$(Build.ArtifactStagingDirectory)/sbom.json'
              artifactName: 'sbom'
```

See complete examples in `examples/ci-cd/` directory.
