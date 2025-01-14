class Parser:
    def pars_data(self, data: dict) -> dict:
        print('Successfully parsed the data.')
        data.update({
            'pars': 'ok'
        })
        return data
