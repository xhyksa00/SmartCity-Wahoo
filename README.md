# IIS-SmartCity
This is repository for project from IIS (Informační systémy).

Theme for the project is "Chytré město":

    Úkolem zadání je vytvořit informační systém pro hlášení problémů a závad
    odhalených obyvateli města (např. nefunkční pouliční lampa). Každý problém je 
    reprezentován tiketem, který je jednoznačně identifikovatelný, má název, popis, 
    stav, autora, apod. Pro ilustrativnost je k tiketu možné přikládat obrázky, 
    průběžně přidávat komentáře a měnit jeho stav. Tiket slouží pro komunikaci mezi 
    zákazníkem a správcem města, který na základě podstaty problému může 
    vytvářet servisní požadavky a ty přiřazovat servisním pracovníkům 
    (např. výměna žárovky v lampě apod.). Servisní požadavky obsahují popis, 
    předpokládaný čas řešení, stav řešení, vykázaný čas apod. Na základě vyřešení 
    úkolů pak správce města aktualizuje stav tiketu a informuje tím obyvatele 
    o stavu řešení (řešení, čeká na vyjádření, vyřešeno, zamítnuto, apod.). 
    Uživatelé budou moci dále informační systém používat následujícím způsobem:

        administrátor:
            spravuje uživatele, jako jediný vytváří správce města

        správce města
            spravuje tikety hlášené obyvateli města
                mění a komentuje jejich stav
                vytváří servisní požadavky a přiřazuje jim servisní techniky
            má možnost přidávat servisní techniky

        servisní technik
            vyřizuje servisní požadavky vytvořené správcem města
                doplňuje údaje o řešení (předpokládaný doba řešení, cena)
                aktualizuje a komentuje jeho stav

        obyvatel:
            hlásí problémy - vytváří tikety s popisem
            vidí stav řešení nahlášených problémů
        neregistrovaný:
            má možnost se zaregistrovat a stát se obyvatelem
