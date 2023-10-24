create or replace trigger emailDiplicata before insert on UTILISATEUR for each row
begin
declare cpt int default 0;
    select count(*) into cpt
    from UTILISATEUR 
    where email = new.email;
    if cpt >= 1 then
        signal SQLSTATE '45000' set message_text = 'Il existe deja un compte avec cet email';
    end if;
    IF cpt = 0 THEN
    	INSERT INTO UTILISATEUR VALUES(new.nom, new.prenom, new.email);
    END IF;
END
