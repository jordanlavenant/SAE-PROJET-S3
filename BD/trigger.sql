delimiter |
create or replace TRIGGER modifsSurDemandeInsert before insert on AJOUTERMATERIEL for each row
begin
    declare presente int;
    declare mes varchar(255);

    SELECT COUNT(ifnull(DEMANDE.idDemande, 0)) into presente FROM DEMANDE JOIN BONCOMMANDE ON DEMANDE.idDemande = BONCOMMANDE.idDemande WHERE DEMANDE.idDemande = new.idDemande ;

    if presente > 0 then
        set mes = concat("Le matériel ne peut être ajouté à la demande (id demande : ", new.idDemande,") car celle-ci déjà associée à un bon de commande.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end |
delimiter ;

delimiter |
create or replace TRIGGER modifsSurDemandeUpdate before update on AJOUTERMATERIEL for each row
begin
    declare presente int;
    declare mes varchar(255);

    SELECT COUNT(ifnull(DEMANDE.idDemande, 0)) into presente FROM DEMANDE JOIN BONCOMMANDE ON DEMANDE.idDemande = BONCOMMANDE.idDemande WHERE DEMANDE.idDemande = new.idDemande ;

    if presente > 0 then
        set mes = concat("La modification ne peut être effectuée sur la demande (id demande : ", new.idDemande,") car celle-ci déjà associée à un bon de commande.");
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
CREATE OR REPLACE function recupereSommeActuelle(id int) returns float
BEGIN
declare sommeActuelle float;
SELECT prixTotalDemande INTO sommeActuelle FROM DEMANDE WHERE idDemande = id ;
return sommeActuelle;
end |
delimiter ;

delimiter |
CREATE OR REPLACE function recuperePrixMateriel(idM int, idF int, qte int) returns float
BEGIN
declare prix float;
SELECT prixMateriel INTO prix FROM MATERIELFOURNISSEUR WHERE idMateriel = idM and idFournisseur = idF ;
return prix*qte;
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
create or replace TRIGGER modificationStockLaboInsert after insert on BONCOMMANDE for each row
BEGIN
    declare idM int ;
    declare qte int ;
    declare prixIndividuel float;
    declare fini boolean default false ;
    declare etat int ;
    declare stock int ;
       
    declare produits cursor for 
        SELECT idMateriel, quantite FROM AJOUTERMATERIEL WHERE idDemande = new.idDemande;

    declare continue handler for not found set fini = true ;

    SELECT idEtat INTO etat FROM BONCOMMANDE WHERE idBonCommande = new.idBonCommande ;

    if etat = 3 then 
        open produits ;
        while not fini do
            fetch produits into idM, qte ;
            if not fini then
                SELECT recupereStockLabo(idM) into stock ;
                if stock is null then
                    INSERT INTO STOCKLABORATOIRE VALUES (idM, qte) ;
                else 
                    UPDATE STOCKLABORATOIRE set quantiteLaboratoire = stock + qte WHERE idMateriel = idM ;
                end if ;
            end if ;
        end while ;
        close produits ;
    end if;
end |
delimiter ;

delimiter |
create or replace TRIGGER modificationStockLaboUpdate after update on BONCOMMANDE for each row
BEGIN
    declare idM int ;
    declare qte int ;
    declare prixIndividuel float;
    declare fini boolean default false ;
    declare etat int ;
    declare stock int ;
       
    declare produits cursor for 
        SELECT idMateriel, quantite FROM AJOUTERMATERIEL WHERE idDemande = new.idDemande;

    declare continue handler for not found set fini = true ;

    SELECT idEtat INTO etat FROM BONCOMMANDE WHERE idBonCommande = new.idBonCommande ;

    if etat = 3 then 
        open produits ;
        while not fini do
            fetch produits into idM, qte ;
            if not fini then
                SELECT recupereStockLabo(idM) into stock ;
                if stock is null then
                    INSERT INTO STOCKLABORATOIRE VALUES (idM, qte) ;
                else 
                    UPDATE STOCKLABORATOIRE set quantiteLaboratoire = stock + qte WHERE idMateriel = idM ;
                end if ;
            end if ;
        end while ;
        close produits ;
    end if;
end |
delimiter ;

delimiter |
create or replace TRIGGER insereSommeCommandeInsert after insert on AJOUTERMATERIEL for each row
begin
    declare mes varchar(255);
    declare idM int ;
    declare idF int ;
    declare qte int ;
    declare sommePrix float default 0;
    declare prixIndividuel float;
    declare fini boolean default false ;

    declare produits cursor for 
        SELECT idMateriel, idFournisseur, quantite FROM AJOUTERMATERIEL WHERE idDemande = new.idDemande;
        
    declare continue handler for not found set fini = true ;
    open produits ;
    while not fini do
        fetch produits into idM, idF, qte ;
        if not fini then
            SELECT recuperePrixMateriel(idM, idF, qte) into prixIndividuel ;
            SET sommePrix = sommePrix + prixIndividuel ;
        end if ;
    end while ;
    close produits ;

    UPDATE DEMANDE SET prixTotalDemande = sommePrix WHERE idDemande = new.idDemande ;
end |
delimiter ;

delimiter |
create or replace TRIGGER insereSommeCommandeUpdate after update on AJOUTERMATERIEL for each row
begin
    declare mes varchar(255);
    declare idM int ;
    declare idF int ;
    declare qte int ;
    declare sommePrix float default 0;
    declare prixIndividuel float;
    declare fini boolean default false ;

    declare produits cursor for 
        SELECT idMateriel, idFournisseur, quantite FROM AJOUTERMATERIEL WHERE idDemande = new.idDemande;
        
    declare continue handler for not found set fini = true ;
    open produits ;
    while not fini do
        fetch produits into idM, idF, qte ;
        if not fini then
            SELECT recuperePrixMateriel(idM, idF, qte) into prixIndividuel ;
            SET sommePrix = sommePrix + prixIndividuel ;
        end if ;
    end while ;
    close produits ;

    UPDATE DEMANDE SET prixTotalDemande = sommePrix WHERE idDemande = new.idDemande ;
end |
delimiter ;

delimiter |
create or replace TRIGGER insereSommeCommandeDelete after delete on AJOUTERMATERIEL for each row
begin
    declare mes varchar(255);
    declare idM int ;
    declare idF int ;
    declare qte int ;
    declare sommePrix float default 0;
    declare prixIndividuel float;
    declare fini boolean default false ;

    declare produits cursor for 
        SELECT idMateriel, idFournisseur, quantite FROM AJOUTERMATERIEL WHERE idDemande = old.idDemande;
        
    declare continue handler for not found set fini = true ;
    open produits ;
    while not fini do
        fetch produits into idM, idF, qte ;
        if not fini then
            SELECT recuperePrixMateriel(idM, idF, qte) into prixIndividuel ;
            SET sommePrix = sommePrix + prixIndividuel ;
        end if ;
    end while ;
    close produits ;

    UPDATE DEMANDE SET prixTotalDemande = sommePrix WHERE idDemande = old.idDemande ;
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
create or replace TRIGGER verificationStockFournisseurInsert before insert on AJOUTERMATERIEL for each row
begin
    declare mes varchar(255);
    declare stock int ;

    SELECT stockFournisseur INTO stock FROM MATERIELFOURNISSEUR WHERE idMateriel = new.idMateriel AND idFournisseur = new.idFournisseur ; 
        
    if stock >= new.quantite then 
        UPDATE MATERIELFOURNISSEUR SET stockFournisseur = (stockFournisseur-new.quantite) WHERE idMateriel = new.idMateriel AND idFournisseur = new.idFournisseur ;
    else set mes = concat("La quantité entrée (", new.quantite, ") est supérieure à celle que le fournisseur propose (", stock, ").");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end |
delimiter ;

delimiter |
create or replace TRIGGER verificationStockFournisseurUpdate before update on AJOUTERMATERIEL for each row
begin
    declare mes varchar(255);
    declare stock int ;
    declare quantiteInitiale int ;

    SELECT stockFournisseur INTO stock FROM MATERIELFOURNISSEUR WHERE idMateriel = new.idMateriel AND idFournisseur = new.idFournisseur ; 
    SELECT quantite INTO quantiteInitiale FROM AJOUTERMATERIEL WHERE idMateriel = new.idMateriel AND idFournisseur = new.idFournisseur ; 
        
    if stock >= new.quantite then 
        UPDATE MATERIELFOURNISSEUR SET stockFournisseur = (stockFournisseur+quantiteInitiale-new.quantite) WHERE idMateriel = new.idMateriel AND idFournisseur = new.idFournisseur ;
    else set mes = concat("La quantité entrée (", new.quantite, ") est supérieure à celle que le fournisseur propose (", stock, ").");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end |
delimiter ;

delimiter |
create or replace TRIGGER verificationStockFournisseurDelete before delete on AJOUTERMATERIEL for each row
begin    
    UPDATE MATERIELFOURNISSEUR SET stockFournisseur = (stockFournisseur+old.quantite) WHERE idMateriel = old.idMateriel AND idFournisseur = old.idFournisseur ;
end |
delimiter ;