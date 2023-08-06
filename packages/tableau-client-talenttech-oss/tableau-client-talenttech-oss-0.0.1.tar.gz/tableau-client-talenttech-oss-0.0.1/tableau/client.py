import logging
import tableauserverclient as TSC
import sys


class Client:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
    logging.captureWarnings(True)

    def __init__(
            self,
            url_server_tableau,
            user_name_tableau,
            password_tableau,

    ):
        self.url_server_tableau = url_server_tableau
        self.password_tableau = password_tableau
        self.user_name_tableau = user_name_tableau
        self.connect_to_server()

    def connect_to_server(
            self
    ):
        """
        init server tableau connection
        :return: server tableau connection
        """
        logging.info('connecting to server')
        try:
            tableau_auth = TSC.TableauAuth(self.user_name_tableau, self.password_tableau)
            self.server = TSC.Server(self.url_server_tableau, use_server_version=True)
            self.server_auth = self.server.auth.sign_in(tableau_auth)
        except:
            logging.info('error connecting')

    def dashboard_refresh(
        self,
        dashboard_name
    ):
        """
        start jobs extract refresh for dashboard
        """
        self.dashboard_name = dashboard_name
        with self.server_auth:
            all_datasource, all_pagination = self.server.workbooks.get()
            for workbooks in all_datasource:

                if workbooks.name == self.dashboard_name:
                    workbook_id = workbooks.id
            if workbook_id == '':
                logging.info('Dashboard not found')
            else:
                try:
                    result = self.server.workbooks.refresh(workbook_id)
                    logging.info('Dashboard start updating on '+str(result.created_at))
                except:
                    logging.info('Dashboard is already starting')

