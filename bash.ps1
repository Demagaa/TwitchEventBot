# Set your domain and Flask app port
$Domain = "your_domain.com"
$FlaskAppPort = 5000

# Install IIS
Add-WindowsFeature Web-Server

# Install URL Rewrite module
Install-Module -Name IISAdministration -Force -AllowClobber

# Create and configure a new site
$SiteName = "FlaskSite"
New-WebSite -Name $SiteName -PhysicalPath "C:\Path\To\Your\FlaskApp" -Port 80 -HostHeader $Domain

# Configure URL Rewrite for reverse proxy
$config = @{
    rules = @(
        @{
            name = "ReverseProxyInboundRule"
            match = @{
                url = "(.*)"
            }
            action = @{
                type = "Rewrite"
                url = "http://localhost:$FlaskAppPort/{R:1}"
            }
        }
    )
} | ConvertTo-Json

Set-WebConfiguration -PSPath "IIS:\Sites\$SiteName" -Filter "/system.webServer" -Value $config

# Start the site
Start-WebSite -Name $SiteName
