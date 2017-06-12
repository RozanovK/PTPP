# PTPP
Plain Text Transfer Protocol

## Opis

Protokół PTTP (Plain Text Transfer Protocol) jest uproszczoną wersją HTTP, składa się on z jednej komendy:

GET /path/to/file PTPP/1.0

## Funkcjonalność

* Przyjmuje połączenia TCP
* Można zdefiniować katalog jaki serwuje, jeśli katalogiem tym będzie: /var/pttp, a klient wyśle GET /path/to/file PTPP/1.0, zostanie mu wysłana zawartość pliku: /var/pttp/path/to/file.
* Jeśli serwerowi zostanie wysłane ścieżka do katalogu serwer wyśle listę możliwych do pobrania plików i podkatalogów w danym katalogu.
* Żądania wysyłane na port P1 są wysyłane tekstem jawnym.