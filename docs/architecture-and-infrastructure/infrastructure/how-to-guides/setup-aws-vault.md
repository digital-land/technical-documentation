# Setup aws vault

## Background

 * This guide helps you securely store and use aws credentials using aws-vault.
 
 * For more detail regarding setting up multiple MHCLG aws accounts or profiles, please visit [Programmatic Access and Federated Access](https://mhclg.sharepoint.com.mcas.ms/sites/CloudPlatforms/SitePages/Programmatic-Access-and-Federated-Access.aspx?etag=%22%7b665C2313-CAD5-4088-B149-4D57D774D2F1%7d%2c398%22).
 
 ## Prerequisites
 
 * Have the aws cli installed. 

 ## Installation for different OS

 * macOS (with Homebrew)

    ```
      brew install aws-vault
    ```
 * Linux (Debian/Ubuntu)

    ```
      sudo curl -L https://github.com/99designs/aws-vault/releases/latest/download/aws-vault-linux-amd64 
      -o /usr/local/bin/aws-vault

      sudo chmod +x /usr/local/bin/aws-vault
    ```

 * Windows (with Chocolatey)

    ```
      choco install aws-vault
    ```

## aws profile configuration

 * For how to configure your aws profile and authenticate to MHCLG platform, please use this [guide](https://mhclg.sharepoint.com.mcas.ms/sites/CloudPlatforms/SitePages/Programmatic-Access-and-Federated-Access.aspx?etag=%22%7b665C2313-CAD5-4088-B149-4D57D774D2F1%7d%2c398%22).

