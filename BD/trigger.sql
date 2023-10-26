delimiter |
create or replace TRIGGER modifsSurDemandeUpdate before update on DEMANDE for each row
begin
    declare presente int;
    declare mes varchar(255);

    SELECT COUNT(ifnull(DEMANDE.idDemande, 0)) into presente FROM DEMANDE JOIN BONCOMMANDE ON DEMANDE.idDemande = BONCOMMANDE.idDemande WHERE DEMANDE.idDemande = new.idDemande ;

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
        set mes = concat("L'email ", new.email, " est déjà utilisé.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end |
delimiter ;


delimiter |
create or replace FUNCTION demandesEnAttente() returns varchar(255)
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
create or replace TRIGGER modificationStockLaboInsert after insert on RESERVELABORATOIRE for each row
BEGIN
    declare idM int ;
    declare stock int ;

    
    SELECT recupereidMateriel(new.idMaterielUnique) into idM ;
    SELECT recupereStockLabo(idM) into stock ;
    INSERT into debug VALUE (stock) ;
    if stock is null then
        INSERT INTO STOCKLABORATOIRE VALUES (idM, 1) ;
    else 
        UPDATE STOCKLABORATOIRE set quantiteLaboratoire = stock + 1 WHERE idMateriel = idM ;
    end if ;
end |
delimiter ;

delimiter |
create or replace TRIGGER modificationStockLaboUpdate after update on RESERVELABORATOIRE for each row
BEGIN
    declare idM int ;
    declare qte int ;
    declare stock int ;

    SELECT recupereidMateriel(new.idMaterielUnique) into idM ;
    SELECT recupereStockLabo(idM) into stock ;
    if stock is null then
        INSERT INTO STOCKLABORATOIRE VALUES (idM, qte) ;
    else 
        UPDATE STOCKLABORATOIRE set quantiteLaboratoire = stock + qte WHERE idMateriel = idM ;
    end if ;
end |
delimiter ;