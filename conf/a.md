microsoft-edge-stable | 121.0.2277.128-1 | https://packages.microsoft.com/repos/edge stable/main amd64 Packages

https://msedgedriver.azureedge.net/

<Name>123.0.2420.53/edgedriver_linux64.zip</Name>
<Url>https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/123.0.2420.53/edgedriver_linux64.zip</Url>
<Last-Modified>Thu, 08 Feb 2024 19:57:57 GMT</Last-Modified>

sudo nano /etc/apt/sources.list.d/microsoft-edge.list
deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main
wget -q https://packages.microsoft.com/keys/microsoft.asc -O microsoft.asc
sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/microsoft.gpg microsoft.asc
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list'
sudo apt update
apt list -a microsoft-edge-stable
microsoft-edge-stable/stable 123.0.2420.53-1 amd64 
sudo apt install microsoft-edge-stable=123.0.2420.53-1


sudo wget https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/123.0.2420.53/edgedriver_linux64.zip
unzip edgedriver_linux64.zip
sudo mv msedgedriver /usr/local/bin/


