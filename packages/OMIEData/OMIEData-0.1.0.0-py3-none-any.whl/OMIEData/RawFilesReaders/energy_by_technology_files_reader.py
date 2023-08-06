import pandas as pd
import locale

from OMIEData.RawFilesReaders.omie_file_reader import OMIEFileReader
from OMIEData.RawFilesReaders.data_types_energy_by_technology import DataTypesEnergyByTechnologyFile


class EnergyByTechnologyHourlyFileReader(OMIEFileReader):

    def __init__(self, types=None):

        self.conceptsToLoad = [v for v in DataTypesEnergyByTechnologyFile] if not types else types

        self._dict_column_concept = {'Fecha': 'DATE',
                                     'Hora': 'HOUR',
                                     'CARBÓN': 'COAL',
                                     'FUEL-GAS': 'FUEL_GAS',
                                     'AUTOPRODUCTOR': 'SELF_PRODUCER',
                                     'NUCLEAR': 'NUCLEAR',
                                     'HIDRÁULICA': 'HYDRO',
                                     'CICLO COMBINADO': 'COMBINED_CYCLE',
                                     'EÓLICA': 'WIND',
                                     'SOLAR TÉRMICA': 'THERMAL_SOLAR',
                                     'SOLAR FOTOVOLTAICA': 'PHOTOVOLTAIC_SOLAR',
                                     'COGENERACIÓN/RESIDUOS/MINI HIDRA': 'RESIDUALS',
                                     'IMPORTACIÓN INTER.': 'IMPORT',
                                     'IMPORTACIÓN INTER. SIN MIBEL': 'IMPORT_WITHOUT_MIBEL'}

    def get_keys(self) -> list:

        key_list_retrieve = ['DATE', 'HOUR']
        key_list_retrieve.extend([str(v) for v in self.conceptsToLoad])
        return key_list_retrieve

    def data_generator(self, filename: str) -> pd.DataFrame:

        locale.setlocale(locale.LC_NUMERIC, "en_DK.UTF-8")
        df = pd.read_csv(filename, sep=';', skiprows=2, header=0, encoding='latin-1', skipfooter=1, engine='python',
                         decimal=",", thousands='.')
        df = df.rename({k: v for k, v in self._dict_column_concept.items()}, axis=1)
        df = df[[x for x in self.get_keys()]]

        return df
