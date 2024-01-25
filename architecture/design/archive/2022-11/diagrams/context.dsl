workspace {
  !identifiers hierarchical

    model {
        publisher = person "Data Publisher" "A person who has data to publish"
        consumer = person "Data Consumer" "A person who uses the data from our platform"
        manager = person "Data Manager" "A person who controls the data on our platform"

        group "Planning" {
            publishYourData  = softwareSystem "Publish Your Data" {
            }
            
            findYourData  = softwareSystem "Find Your Data" {
            }
        
            manageYourData  = softwareSystem "Manage Your Data" {
                api = container "Flask API" {
                }           
                web = container "Web App" {
                }  
                config = container "Postgres" "Stores configuration" "" "Database"
            manageYourData.web -> manageYourData.api
            manageYourData.api -> config

            }
            
            workflowManagement = softwareSystem "Workflow Management" {
                dlp = container "Digital land Python" {
                }
            }
        }
        
        group AWS {
            S3 = softwareSystem "AWS S3" {
            }
        }
                
        publisher -> publishYourData
        publishYourData -> workflowManagement
        manageYourData -> S3
        workflowManagement -> S3

        manager -> manageYourData
        
        consumer -> findYourData

    }
    
    views {
      styles {
        element "Person" {
            background #1168bd
            color #ffffff
            fontSize 22
            shape Person
        }
        element "Software System" {
            background #1168bd
            color #ffffff
        }
       element "Container" {
                background #438dd5
                color #ffffff
        }
        element "Component" {
            background #85bbf0
            color #000000
        }
        element "Database" {
            shape Cylinder
        }
    }
}