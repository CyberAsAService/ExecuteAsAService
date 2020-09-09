param(
    [Parameter(Mandatory=$true)][string]$address,
    [Parameter(Mandatory=$true)][string]$username,
    [Parameter(Mandatory=$true)][string]$password, #TODO -> Secure this shit
    [Parameter(Mandatory=$true)][string]$hash,
    [Parameter(Mandatory=$true)][string]$arguments
)
$arguments = '.Replace(''<insert args here>'',' + '''' + $arguments + '''' + ')' 

#$argsParse = '.Replace(''<insert args here>'', ''$downloadUrl = ''''' + $downloadUrl + ''''';$output= ''''' + $output + ''''';$uploadUrl=''''' + 'http:\\10.0.0.12:3000/repo/deployer' +''''''')'
$command = 'powershell -noninteractive "&{(New-Object Net.WebClient).DownloadString(''http://10.0.0.4:3000/repo/scripts?hash=' + $hash + ''')' + $arguments +'} | iex"'
#psexec \\$address -u $username -p $password /accepteula cmd /c 'powershell -noninteractive "&{(New-Object Net.WebClient).DownloadString(''http://10.0.0.12:3000/repo/scripts?hash='$hash''').Replace(''ï»¿'', '''').Replace(''<insert args here>'', ''$downloadUrl = '' + '''$downloadUrl';'' + ''$output='' +'''$output';''+''$uploadUrl='' + ''""http:\\10.0.0.12:3000/repo/deployer"""";'')} | iex"'

write-host $command
./psexec \\$address -u $username -p $password /accepteula -d cmd /c $command