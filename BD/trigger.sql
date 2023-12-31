delimiter |
create or replace TRIGGER modifsSurDemandeUpdate before update on DEMANDE for each row
begin
    declare presente int;
    declare mes varchar(255);

    SELECT COUNT(ifnull(DEMANDE.idDemande, 0)) into presente FROM DEMANDE WHERE DEMANDE.idDemande = new.idDemande AND idEtatD = 2;

    if presente > 0 then
        set mes = concat("La modification ne peut être effectuée sur la demande (id demande : ", new.idDemande,") car celle-ci est associée à un bon de commande.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end |
delimiter ;


delimiter |
create or replace TRIGGER emailUtilisateurUniqueInsert before insert on UTILISATEUR for each row
begin
    declare compteur int;
    declare mes varchar(255);
    SELECT COUNT(*) INTO compteur from UTILISATEUR WHERE email = new.email;
    if compteur > 0 then
        set mes = concat("L'email ", new.email, " est déjà utilisé.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end |
delimiter ;

delimiter |
create or replace TRIGGER emailUtilisateurUniqueUpdate before update on UTILISATEUR for each row 
begin
    declare compteur int;
    declare mes varchar(255);
    SELECT COUNT(*) INTO compteur from UTILISATEUR WHERE email = new.email;
    if compteur > 0 then
        if old.email <> new.email then 
            set mes = concat("L'email ", new.email, " est déjà utilisé.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
        end if;
    end if;
end |
delimiter ;


delimiter |
create or replace FUNCTION demandesEnAttenteAncien() returns varchar(255)
begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT DEMANDE.idDemande FROM DEMANDE JOIN BONCOMMANDE ON DEMANDE.idDemande = BONCOMMANDE.idDemande WHERE BONCOMMANDE.idEtat = 1 ;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            if listeDemandes = '' then 
                SET listeDemandes = id ;
            else 
                SET listeDemandes = concat(listeDemandes, ", ", id) ;
            end if ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end |
delimiter ;

delimiter |
create or replace FUNCTION demandesEnAttente() returns varchar(255)
begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT DEMANDE.idDemande FROM DEMANDE WHERE idEtatD = 2;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            if listeDemandes = '' then 
                SET listeDemandes = id ;
            else 
                SET listeDemandes = concat(listeDemandes, ", ", id) ;
            end if ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end |
delimiter ;

delimiter |
create or replace FUNCTION nombreDemandesEnAttenteAncien() returns varchar(255)
begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT COUNT(DEMANDE.idDemande) FROM DEMANDE JOIN BONCOMMANDE ON DEMANDE.idDemande = BONCOMMANDE.idDemande WHERE BONCOMMANDE.idEtat = 1 ;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            SET listeDemandes = id ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end |
delimiter ;

delimiter |
create or replace FUNCTION nombreDemandesEnAttente() returns varchar(255)
begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT COUNT(DEMANDE.idDemande) FROM DEMANDE ;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            SET listeDemandes = id ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end |
delimiter ;


delimiter |
CREATE OR REPLACE TRIGGER archivageBonCommande AFTER UPDATE ON BONCOMMANDE FOR EACH ROW
BEGIN 
    declare idBC int;
    declare idE int ;
    declare idU int ;
    declare d date ;
    declare fini BOOLEAN default false;

    declare infosBonCommande cursor for
        SELECT * FROM BONCOMMANDE WHERE idBonCommande = new.idBonCommande and idEtat = 4 ;
    
    declare continue handler for not found set fini = true ;
    open infosBonCommande ;
    while not fini do
        fetch infosBonCommande into idBC, idE, idU, d ;
        if not fini then
            INSERT INTO ARCHIVEBONCOMMANDE (idBonCommande, idEtat, idUtilisateur, dateArchiveBonCommande) VALUES (idBC, idE, idU, d) ;
        end if ;
    end while ;
    close infosBonCommande ;
end |
delimiter ;

delimiter |
CREATE OR REPLACE TRIGGER archivageCommandes AFTER INSERT ON ARCHIVEBONCOMMANDE FOR EACH ROW
BEGIN
    declare idA int ;
    declare idM int ;
    declare qte int ;
    declare fini BOOLEAN default false;

    declare infosCommandes cursor for
        SELECT A.idArchiveBonCommande, C.idMateriel, C.quantite FROM COMMANDE C INNER JOIN ARCHIVEBONCOMMANDE A ON C.idBonCommande = A.idBonCommande WHERE A.idArchiveBonCommande =  new.idArchiveBonCommande ;
    
    declare continue handler for not found set fini = true ;
    open infosCommandes ;
    while not fini do
        fetch infosCommandes into idA, idM, qte ;
        if not fini then
            INSERT INTO ARCHIVECOMMANDE(idArchiveBonCommande, idMateriel, quantite) VALUES (idA, idM, qte) ;
        end if ;
    end while ;
    close infosCommandes ;
end |
delimiter ;

delimiter |
CREATE OR REPLACE function recupereidMateriel(idMU int) returns int
BEGIN
declare idM int;
SELECT idMateriel INTO idM FROM MATERIELUNIQUE WHERE idMaterielUnique = idMU ;
return idM;
end |
delimiter ;

delimiter |
CREATE OR REPLACE function recupereStockLabo(idM int) returns int
BEGIN
declare stock float;
SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM ;
return stock;
end |
delimiter ;

delimiter |
create or replace procedure alertesPeremption() 
BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE datePeremption <= CURDATE() ;

    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(1, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end |
delimiter ;


delimiter |
create or replace procedure alertesPeremptionDixJours() 
BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE datePeremption > CURDATE() AND datePeremption <= CURDATE() + INTERVAL 10 DAY ;

    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(2, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end |
delimiter ;

delimiter |
create or replace procedure alertesQuantiteSeuil() 
BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE NATURAL JOIN MATERIEL WHERE quantiteApproximative <= (seuilAlerte/4) ;

    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(3, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end |
delimiter ;

delimiter |
create or replace procedure alertesQuantiteAZero() 
BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE NATURAL JOIN MATERIEL WHERE quantiteApproximative > (seuilAlerte/4) AND quantiteApproximative = 0 ;
    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(4, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end |
delimiter ;

delimiter |
create or replace procedure gestionAlertes() 
BEGIN
    DELETE FROM ALERTESENCOURS ;
    call alertesPeremption() ;
    call alertesPeremptionDixJours() ;
    call alertesQuantiteAZero() ;
    call alertesQuantiteSeuil() ;
end |
delimiter ;

SELECT COUNT(*) FROM ALERTESENCOURS ;


delimiter |
create or replace EVENT insereAlertesAuto ON SCHEDULE EVERY 1 minute DO
BEGIN
    DELETE FROM ALERTESENCOURS ;
    INSERT INTO debug VALUES ("test") ;
    call alertesPeremption() ;
    call alertesPeremptionDixJours() ;
    call alertesQuantiteAZero() ;
    call alertesQuantiteSeuil() ;
end |
delimiter ;

delimiter |
create or replace TRIGGER empecheSuppressionsStockLaboratoire before delete on STOCKLABORATOIRE for each row
begin
    declare mes varchar(255);

    set mes = concat("Les suppressions ne sont pas autorisés sur la table STOCKLABORATOIRE. Si un objet n'est plus en stock, veuillez mettre sa quantité à 0.");
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
end |
delimiter ;


delimiter |
CREATE OR REPLACE TRIGGER modificationStockLaboInsert AFTER INSERT ON RESERVELABORATOIRE FOR EACH ROW
BEGIN
    declare idM INT;
    declare stock INT;
    declare fini BOOLEAN default false;

    declare curseur cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE idMaterielUnique = new.idMaterielUnique;

    declare continue handler for not found set fini = true ;

    open curseur;

    boucle: loop
        fetch curseur into idM;
        if fini then
            LEAVE boucle;
        end if;

        SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM;

        if stock is null then
            INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (idM, 1);
        else
            UPDATE STOCKLABORATOIRE SET quantiteLaboratoire = stock + 1 WHERE idMateriel = idM;
        end if;
    end loop;
    close curseur;
end |
delimiter ;

delimiter |
CREATE OR REPLACE TRIGGER modificationStockLaboUpdate AFTER UPDATE ON RESERVELABORATOIRE FOR EACH ROW
BEGIN
    declare idM INT;
    declare stock INT;
    declare fini BOOLEAN default false;

    declare curseur cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE idMaterielUnique = new.idMaterielUnique;

    declare continue handler for not found set fini = true ;

    open curseur;

    boucle: loop
        fetch curseur into idM;
        if fini then
            LEAVE boucle;
        end if;

        SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM;

        if stock is null then
            INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (idM, 1);
        else
            UPDATE STOCKLABORATOIRE SET quantiteLaboratoire = stock + 1 WHERE idMateriel = idM;
        end if;
    end loop;
    close curseur;
end |
delimiter ;

delimiter |
CREATE OR REPLACE TRIGGER modificationStockLaboDelete AFTER DELETE ON RESERVELABORATOIRE FOR EACH ROW
BEGIN
    declare idM INT;
    declare stock INT;
    declare fini BOOLEAN default false;

    declare curseur cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE idMaterielUnique = old.idMaterielUnique;

    declare continue handler for not found set fini = true ;

    open curseur;

    boucle: loop
        fetch curseur into idM;
        if fini then
            LEAVE boucle;
        end if;

        SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM;

        if stock - 1 > 0 then
            UPDATE STOCKLABORATOIRE SET quantiteLaboratoire = stock - 1 WHERE idMateriel = idM;
        end if;
    end loop;
    close curseur;
end |
delimiter ;

