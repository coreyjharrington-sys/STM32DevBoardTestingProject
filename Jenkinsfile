pipeline {
    agent { label 'self-hosted' }   // run on Windows Jenkins agent

    // triggers {
    //     // Equivalent to workflow_dispatch, push, pull_request
    //     // Jenkins doesn't have native PR triggers without plugins,
    //     // but you can configure GitHub webhooks to trigger builds.
    // }

    stages {
        stage('Checkout repo') {
            steps {
                checkout scm
            }
        }

        stage('Ensure Docker is available') {
            steps {
                powershell '''
                docker --version
                if ($LASTEXITCODE -ne 0) {
                  Write-Host "Docker not found"
                  exit 1
                }
                '''
            }
        }

        stage('Compile in Docker') {
            steps {
                powershell '''
                docker run --rm -v "$env:WORKSPACE\\firmware:/workspace/firmware" stm32devboardcompiler make clean all
                '''
            }
        }

        stage('Ensure STM32 Programmer CLI is available') {
            steps {
                powershell '''
                STM32_Programmer_CLI --version
                if ($LASTEXITCODE -ne 0) {
                  Write-Host "STM32_Programmer_CLI not found"
                  exit 1
                }
                '''
            }
        }

        stage('Program STM32 Devboard') {
            steps {
                powershell '''
                STM32_Programmer_CLI -c port=SWD -d firmware\\build\\Devboardv1.0Project.bin 0x08000000 -rst
                '''
            }
        }

        stage('Verify Python installation') {
            steps {
                powershell '''
                python --version
                if ($LASTEXITCODE -ne 0) {
                  Write-Host "Python not found"
                  exit 1
                }
                '''
            }
        }

        stage('Ensure Conda is available') {
            steps {
                powershell '''
                conda --version
                if ($LASTEXITCODE -ne 0) {
                  Write-Host "Conda not found"
                  exit 1
                }
                '''
            }
        }

        stage('Set up Conda environment') {
            steps {
                powershell '''
                & "$env:CONDA_PREFIX\\shell\\condabin\\conda-hook.ps1"
                conda activate testframework
                conda env update --file environment.yml --name testframework --prune
                '''
            }
        }

        stage('Pause for USB reconnect') {
            steps {
                input message: 'Please reconnect the USB cable now, then click Continue.'
            }
        }

        stage('Run HITL tests') {
            steps {
                powershell '''
                & "$env:CONDA_PREFIX\\shell\\condabin\\conda-hook.ps1"
                conda activate testframework
                python -m pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Archive test artifacts') {
            steps {
                archiveArtifacts artifacts: 'results.xml', fingerprint: true
                archiveArtifacts artifacts: 'TestReport.html', fingerprint: true
            }
        }
    }
}