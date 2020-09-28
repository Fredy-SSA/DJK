while ($true) {
    
$uri = "http://jservice.io/api/random"
$game = Invoke-RestMethod -Uri $uri
$game.question
"----------------------------------------------"
Write-Host $game.answer -ForegroundColor Green
"______________________________________________"
Start-Sleep -seconds 5

}