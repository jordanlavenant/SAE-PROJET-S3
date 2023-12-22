from sqlalchemy import text


class RELOAD:
    
    def reload_alert(cnx):
        """
        Reloads the alerts by executing the stored procedure 'gestionAlertes()' in the database.

        Parameters:
        cnx (connection): The database connection object.

        Raises:
        Exception: If there is an error during the reload process.

        """
        try:
            cnx.execute(text("call gestionAlertes();"))
            cnx.commit()
        except:
            print("Erreur lors du reload des alertes")
            raise
