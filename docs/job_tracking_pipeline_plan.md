# Job Tracking System - Azure DevOps Integration Plan

## **Overview**
This document outlines the steps to integrate the **Job Tracking System** into **Azure DevOps** and automate its deployment using the **Deployment Automation System**.

---

## **Phase 1: Integrating Job Tracking System into Azure DevOps**
### **Step 1: Create a Repository in Azure DevOps**
- Add the **Job Tracking System** repository to **Azure DevOps**.
- Push existing code to Azure DevOps.
- Set up **branch protection rules and permissions**.

### **Step 2: Configure Azure DevOps Pipeline**
- Create a **new YAML pipeline** (`azure-pipelines.yml`).
- Start with a **basic validation and packaging pipeline**:
  ```yaml
  trigger:
    branches:
      include:
        - main
        - develop

  pool:
    name: Coles-Private-Hosted-Linux-NonProd-Scalable
    vmImage: 'ubuntu-latest'

  steps:
    - checkout: self
    - script: |
        echo "Running linting checks..."
        python -m flake8 src/
      displayName: "Lint Code"
    - script: |
        echo "Running tests..."
        python -m unittest discover -s tests
      displayName: "Run Unit Tests"
    - script: |
        echo "Packaging application..."
        tar -czvf job_tracking.tar.gz src/
      displayName: "Package Application"
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: job_tracking.tar.gz
        artifactName: "JobTrackingApp"
      displayName: "Upload Build Artifact"
  ```

### **Step 3: Deploy to `ldctlm01` via SSH**
- Modify the pipeline to deploy the **Job Tracking System** automatically.
  ```yaml
  - task: SSH@0
    inputs:
      sshEndpoint: 'ldctlm01_ctmsrv'
      runOptions: 'inline'
      inline: |
        echo "[INFO] Deploying Job Tracking System..."
        mkdir -p /opt/job_tracking/
        tar -xzvf $(Pipeline.Workspace)/JobTrackingApp/job_tracking.tar.gz -C /opt/job_tracking/
        echo "[INFO] Deployment completed successfully."
    displayName: "Deploy Job Tracking System"
  ```

---

## **Phase 2: Enhancing Deployment Automation System**
### **Step 4: Modify Deployment Automation Pipeline**
- Ensure **Deployment Automation System** supports Job Tracking System deployment.
- Introduce **new deployment step** in `deploy.py`.

### **Step 5: Enable Version Comparison in Deployment Pipeline**
- Implement `AzureDevOpsManager.compare_with_github()`.
- Modify pipeline to **block deployment if GitHub and Azure DevOps versions mismatch**:
  ```yaml
  - script: |
      python deployment-automation/src/deploy.py --steps compare --app job-tracking
    displayName: "Compare Job Tracking System Versions"
  ```

---

## **Phase 3: Expanding Deployment Automation Capabilities**
### **Step 6: Implement Job Tracking Deployment as a Deployment Step**
- Add a **dedicated deployment step** inside `deploy.py`.
- Modify the `steps_config.json` to register **Job Tracking System deployment**.

### **Step 7: Implement JFrog Artifact Upload for Job Tracking System**
- Modify `deploy.py` to **upload artifacts to JFrog**.
- Ensure the pipeline **automatically uploads new versions**.

---

## **Final Deliverables**
✅ **Job Tracking System integrated into Azure DevOps**  
✅ **A fully working pipeline that builds, tests, and deploys Job Tracking System**  
✅ **Deployment Automation System updated to support Job Tracking System deployment**  
✅ **Deployment process streamlined for future applications**

