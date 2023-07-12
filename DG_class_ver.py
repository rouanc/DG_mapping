
class DG:
    def __init__(self):
        pass

    def get_sequences(self, base_path):
        '''
        Return list of sequences(Path) under base_path
        '''
        data_path = Path(base_path)
        data_list = list()
        if data_path.exists():
            for data in data_path.iterdir():
                data_list.append(data)
            print("Found " + str(len(data_list)) +
                  " sequences from " + base_path)
            return data_list
        else:
            print("Base path not exist!")
            return False

    def analysis(self, ref_data, exp_data):
        # time alignment
        # error calculation
        pass
