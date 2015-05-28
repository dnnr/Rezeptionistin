# Rezeptionistin
Der freundliche IRC-Bot für Ihren Kanal.

# Features

* `!gt` - PING Hello Nachricht, mit nick
* `!help` - Zeige Hilfe, antwort im Query
* URL Title - Fetcht den Titel von http(s) links und postet den Inhalt in den Channel

# Installation

``` bash
git clone https://github.com/dnnr/Rezeptionistin
```

Nach dem Klonen müssen die Abhängigkeiten installiert, und eine config.ini Datei angelegt werden.

``` bash
cd rezeptionistin
pip install -r requirements.txt
cp config.ini.example config.ini
```

**! config.ini muss vor der Benutzung angepasst werden**

# Benutzung

``` bash
./rezeptionistin.py
```

# Konfiguration

Es wird automatisch die `config.ini` im gleichen Verzeichnis gelesen.

``` ini
[IRC]
server = irc.freenode.net
port = 6667
nick = Rezeptionistin
ircchan = #...
debugchan = #...

[HTTP]
useragent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3
```
