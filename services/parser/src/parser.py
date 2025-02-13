class Parser:
    @staticmethod
    def pars_ads_list(ads_list: list) -> list:
        ads_pars_list = list()
        for ads in ads_list:
            for widget in ads.get('list_widgets', list()):
                if widget['widget_type'] == 'POST_ROW':
                    ads_pars_list.append(widget)
        return ads_pars_list
