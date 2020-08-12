$Counter = 0
$StartPort = 1
$EndPort = 65535
$total = $EndPort - $StartPort
$HostAddress = '3.127.38.18'
$ErrorActionPreference= 'silentlycontinue'

$fast_performance = Measure-Command -Expression {
  for ($StartPort; $StartPort -le $EndPort; $StartPort++ )
    {  
      $Counter++
      Write-Progress -Activity "Checking ports." -Status "$Counter Ports Complete:" -PercentComplete ($counter/$total*100);
      $tcp = new-object System.Net.Sockets.TcpClient
      $tcp.ReceiveTimeout = 5 
      $tcp.SendTimeout = 5 
      $tcp.Connect($HostAddress,$StartPort) 
      $tcp.close() 
    }
}
Write-Host $fast_performance