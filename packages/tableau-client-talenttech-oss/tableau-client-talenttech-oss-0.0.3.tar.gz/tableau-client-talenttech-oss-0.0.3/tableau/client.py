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
        self.status_connection = False
        logging.info('try connect to server')
        try:
            tableau_auth = TSC.TableauAuth(self.user_name_tableau, self.password_tableau)
            self.server = TSC.Server(self.url_server_tableau, use_server_version=True)
            self.server_auth = self.server.auth.sign_in(tableau_auth)
            self.status_connection = True
        except:
            logging.info('error connecting to server')

    def get_dashboard_id(
            self,
            dashboard_name
    ):
        if self.status_connection:
            with self.server_auth:
                self.workbook_id = ''
                all_datasource, all_pagination = self.server.workbooks.get()
                for workbooks in all_datasource:
                    if workbooks.name == dashboard_name:
                        self.workbook_id = workbooks.id
                        # self.workbook = self.server.workbooks.get_by_id(self.workbook_id)
                        # logging.info([view.name for view in self.workbook.views])
            if self.workbook_id == '':
                    logging.info('Dashboard '+dashboard_name +' not found on server')

    def dashboard_refresh(
        self,
        dashboard_name
    ):
        """
        start jobs extract refresh for dashboard
        """
        self.connect_to_server()
        self.get_dashboard_id(dashboard_name)
        if self.workbook_id != '':
            with self.server_auth:
                try:
                    result = self.server.workbooks.refresh(self.workbook_id)
                    logging.info('Dashboard start updating on '+str(result.created_at))
                except:
                    logging.info('Dashboard extract refresh is already starting')

    def view_to_csv(
            self,
            dashboard_name,
            view_name,
            csv_path,
    ):
        """
        export view to csv file
        """
        self.get_dashboard_id(dashboard_name)
        self.connect_to_server()
        is_found = False
        if self.workbook_id != '':
            with self.server_auth:
                try:
                    workbook = self.server.workbooks.get_by_id(self.workbook_id)
                    for view in workbook.views:
                        if view.name == view_name:
                            self.server.views.populate_csv(view)
                            with open(csv_path, 'wb') as f:
                                f.write(b''.join(view.csv))
                                logging.info('View ' + view_name + ' export to csv')
                                is_found = True
                    if is_found == False:
                        logging.info('View ' + view_name +' not found in workbook '+dashboard_name)
                except:
                    logging.info('Error!')

