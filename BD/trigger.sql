delimiter |
create or replace TRIGGER emailUtilisateurUnique before insert on UTILISATEUR for each row
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
create or replace TRIGGER insereSommeCommande after insert on AJOUTERMATERIEL for each row
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

SELECT demandesEnAttente() ;

