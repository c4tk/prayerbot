# -*- coding: utf-8 -*-
from rdb import db
from models import Intent, BibleVerse

# create the database and the db tables
db.create_all()

# insert prayer requests
# db.session.add(Intent(1099770976753951, u"Potrzebuje modlitwy w intencji mojej mamy"))
# db.session.add(Intent(1099770976753951, u"O powrot do zdrowia"))
# db.session.add(Intent(1209178385783730, u"O rozeznanie drogi"))
# db.session.add(Intent(10208414992228182, u"O Swiatowe Dni Mlodziezy"))
# db.session.add(Intent(10208414992228182, u"W intencji Bogu wiadomej"))
# db.session.add(Intent(215380638847054, u"W intencji Bogu wiadomej"))

# insert Bible verses
db.session.add(BibleVerse(u"Lecz ci, co zaufali Panu, odzyskują siły, otrzymują skrzydła jak orły: biegną bez zmęczenia, bez znużenia idą", u"Iz 40,31"))
db.session.add(BibleVerse(u"Nie sądźcie, abyście nie byli sądzeni. Bo takim sądem, jakim sądzicie, i was osądzą; i taką miarą jaką wy mierzycie, wam odmierzą", u"Mt 7,1"))
db.session.add(BibleVerse(u"Bóg jest światłością, a nie ma w Nim żadnej ciemności.", u"1 J 1,5b"))
db.session.add(BibleVerse(u"Niech przeto ten, komu się zdaje, że stoi, baczy, aby nie upadł.", u"1 Kor 10,12"))
db.session.add(BibleVerse(u"Bądźcie trzeźwi! Czuwajcie! Przeciwnik wasz, diabeł, jak lew ryczący krąży szukając kogo pożreć.", u"1 P 5,8"))
db.session.add(BibleVerse(u"Kamień odrzucony przez budujących stał się kamieniem węgielnym. Stało się to przez Pana: cudem jest w oczach naszych. Oto dzień, który Pan uczynił: radujmy się zeń i weselmy!", u"Ps 118,22-24"))
db.session.add(BibleVerse(u"Miłosierny jest Pan i łaskawy, nieskory do gniewu i bardzo łagodny. Nie wiedzie sporu do końca i nie płonie gniewem na wieki. Nie postępuje z nami według naszych grzechów ani według win naszych nam nie odpłaca.", u"Ps 103,8-10"))
db.session.add(BibleVerse(u"Bo kto chce zachować swoje życie, straci je; a kto straci swe życie z mego powodu, znajdzie je.", u"Mt 16,25"))
db.session.add(BibleVerse(u"Cóż bowiem za korzyść odniesie człowiek, choćby cały świat zyskał, a na swej duszy szkodę poniósł?", u"Mt 16,26"))
db.session.add(BibleVerse(u"Oto przyjdę niebawem, a moja zapłata jest ze Mną, by tak każdemu odpłacić, jaka jest jego praca. Jam Alfa i Omega, Pierwszy i Ostatni, Początek i Koniec.", u"Ap 22,12"))
db.session.add(BibleVerse(u"I wszystko, cokolwiek działacie słowem lub czynem, wszystko (czyńcie) w imię Pana Jezusa, dziękując Bogu Ojcu przez Niego.",u"Kol 3,18"))
db.session.add(BibleVerse(u"Gniewajcie się, a nie grzeszcie: niech nad waszym gniewem nie zachodzi słońce!",u"Ef 4,26"))
db.session.add(BibleVerse(u"Bądźcie dla siebie nawzajem dobrzy i miłosierni! Przebaczajcie sobie, tak jak i Bóg nam przebaczył w Chrystusie.",u"Ef 4,32"))
db.session.add(BibleVerse(u"Bądźcie więc naśladowcami Boga, jako dzieci umiłowane, i postępujcie drogą miłości, bo i Chrystus was umiłował i samego siebie wydał za nas w ofierze i dani na wdzięczną wonność Bogu.",u"Ef 5,1-2"))
db.session.add(BibleVerse(u"Ku wolności wyswobodził nas Chrystus. A zatem trwajcie w niej i nie poddawajcie się na nowo pod jarzmo niewoli!",u"Ga 5,1"))
db.session.add(BibleVerse(u"Bo całe Prawo wypełnia się w tym jednym nakazie: Będziesz miłował bliźniego swego jak siebie samego.",u"Ga 5,14"))
db.session.add(BibleVerse(u"Jeśliście więc razem z Chrystusem powstali z martwych, szukajcie tego, co w górze, gdzie przebywa Chrystus zasiadając po prawicy Boga. Dążcie do tego, co w górze, nie do tego, co na ziemi.",u"Kol 3,1-2"))
db.session.add(BibleVerse(u"Jako więc wybrańcy Boży - święci i umiłowani - obleczcie się w serdeczne miłosierdzie, dobroć, pokorę, cichość, cierpliwość, znosząc jedni drugich i wybaczając sobie nawzajem, jeśliby miał ktoś zarzut przeciw drugiemu: jak Pan wybaczył wam, tak i wy!",u"Kol 3,12-13"))
db.session.add(BibleVerse(u"Trwajcie gorliwie na modlitwie, czuwając na niej wśród dziękczynienia.",u"Kol 4,2"))
db.session.add(BibleVerse(u"Weź udział w trudach i przeciwnościach jako dobry żołnierz Chrystusa Jezusa!",u"2 Tm 2,3"))
db.session.add(BibleVerse(u"Nauka to zasługująca na wiarę: Jeżeliśmy bowiem z Nim współumarli, wespół z Nim i żyć będziemy. Jeśli trwamy w cierpliwości, wespół z Nim też królować będziemy. Jeśli się będziemy Go zapierali, to i On nas się zaprze.",u"2 Tm,11-12"))
db.session.add(BibleVerse(u"Kto doznaje pokusy, niech nie mówi, że Bóg go kusi. Bóg bowiem ani nie podlega pokusie ku złemu, ani też nikogo nie kusi.",u"Jk 1,13"))
db.session.add(BibleVerse(u"Każde dobro, jakie otrzymujemy, i wszelki dar doskonały zstępują z góry, od Ojca świateł, u którego nie ma przemiany ani cienia zmienności.",u"Jk 1,17"))
db.session.add(BibleVerse(u"Wiedzcie, bracia moi umiłowani: każdy człowiek winien być chętny do słuchania, nieskory do mówienia, nieskory do gniewu. Gniew bowiem męża nie wykonuje sprawiedliwości Bożej.",u"Jk 1,19-20"))
db.session.add(BibleVerse(u"Wprowadzajcie zaś słowo w czyn, a nie bądźcie tylko słuchaczami oszukującymi samych siebie. Jeżeli bowiem ktoś przysłuchuje się tylko słowu, a nie wypełnia go, podobny jest do człowieka oglądającego w lustrze swe naturalne odbicie.",u"Jk 1,22-23"))
db.session.add(BibleVerse(u"Jaki z tego pożytek, bracia moi, skoro ktoś będzie utrzymywał, że wierzy, a nie będzie spełniał uczynków? Czy [sama] wiara zdoła go zbawić?",u"Jk 2,14"))
db.session.add(BibleVerse(u"Tak też i wiara, jeśli nie byłaby połączona z uczynkami, martwa jest sama w sobie.",u"Jk 2,17"))
db.session.add(BibleVerse(u"Modlicie się, a nie otrzymujecie, bo się źle modlicie, starając się jedynie o zaspokojenie swych żądz.",u"Jk 4,3"))
db.session.add(BibleVerse(u"Jeden jest Prawodawca i Sędzia, w którego mocy jest zbawić lub potępić. A ty kimże jesteś, byś sądził bliźniego?",u"Jk 4,12"))
db.session.add(BibleVerse(u"Nie oddawajcie złem za zło ani złorzeczeniem za złorzeczenie! Przeciwnie zaś, błogosławcie!",u"1 P 3,9a"))
db.session.add(BibleVerse(u"Przede wszystkim miejcie wytrwałą miłość jedni ku drugim, bo miłość zakrywa wiele grzechów.",u"1 P 4,8"))
db.session.add(BibleVerse(u"Ale cieszcie się, im bardziej jesteście uczestnikami cierpień Chrystusowych, abyście się cieszyli i radowali przy objawieniu się Jego chwały.",u"1 P 4,13"))
db.session.add(BibleVerse(u"Zatem również ci, którzy cierpią zgodnie z wolą Bożą, niech dobrze czyniąc, wiernemu Stwórcy oddają swe dusze!",u"1 P 4,18"))

# commit the changes
db.session.commit()
