$a = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("aGVsbG8gd29ybGQ="))
Invoke-Expression $a
