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
create or replace TRIGGER insereSommeCommande before insert on AJOUTERMATERIEL for each row
begin
    declare sommeActuelle float;
    declare mes varchar(255);

    SELECT recupereSommeActuelle(new.idDemande) INTO sommeActuelle;
    SELECT SUM()


    SELECT COUNT(*) INTO compteur from UTILISATEUR WHERE email = new.email;
    if compteur > 0 then
        set mes = concat("L'email ", new.email, " est déjà utilisé.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end |
delimiter ;