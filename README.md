jogger-util
===========

An experimental utility to mass-edit your blog entries on jogger.pl

https://github.com/automatthias/jogger-util

This tool is a workaround for a problem where the administration panel of
jogger.pl does not allow for bulk operations such as changing commenting
permissions. The inherent problem with this script is that it depends on the
HTML served by the control panel, so the script will break when jogger.pl
changes something in the HTML template.


Prerequisites
-------------

1. Python 3
2. virtualenv (on Ubuntu: `sudo apt-get install python-virtualenv`)


Installation
------------

    mkdir ~/py3env
    virtualenv -p /usr/bin/python3 ~/py3env
    source ~/py3env/bin/activate
    pip install beautifulsoup4 requests
    cd
    git clone https://github.com/automatthias/jogger-util.git
    cd jogger-util
    python setup.py install
    jogger-set-all-entries --help


Polskie instrukcje
------------------

Jeżeli masz problemy ze spamem na swoim joggerze i pragniesz ustawić uprawnienia
do komentarzy we wszystkich swoich postach na przykład na „tylko dla
zalogowanych”, narzędzie to potrafi zrobić to za jednym zamachem. Jest jedno
niezbyt małe _ale:_

Jest to **bardzo niebezpieczne narzędzie.** Jeżeli coś pójdzie nie tak (np.
w narzędziu jest błąd), możesz sobie skasować lub uszkodzić całą zawartość
swojego bloga. W związku z tym
**UŻYWASZ JOGGER-UTIL WYŁĄCZNIE NA WŁASNĄ ODPOWIEDZIALNOŚĆ.**

Narzędzie nazywa się jogger-set-all-entries i wygląda tak:

    $ jogger-set-all-entries --help
    usage: jogger-set-all-entries [-h] [--jabberid JABBERID] {jogger,nobody,all}
    
    positional arguments:
      {jogger,nobody,all}  Set comment permissions
    
    optional arguments:
      -h, --help           show this help message and exit
      --jabberid JABBERID  Jabber ID.

Narzędzie służy do tego, żeby ustawić uprawnienia do komentowania we wszystkich
wpisach, bez wyjątku. Możliwości są trzy:

* `all` czyli komentować mogą wszyscy, w tym anonimy
* `jogger` czyli tylko zalogowani
* `nobody` czyli nikt nie może komentować

Przykładowe użycie, które ustawia uprawnienia do komentowania na „wyłącznie dla
zalogowanych”.

    jogger-set-all-entries --jabberid ziutek@example.com jogger


Kontakt
-------

W razie pytań można się ze mną kontaktować przez
[github](https://github.com/automatthias),
[Google+](http://google.com/+MaciejBlizi%C5%84ski),
[Twitter](https://twitter.com/automatthias) oraz adres email zaszyty w pliku
setup.py.
