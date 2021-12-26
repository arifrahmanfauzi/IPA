import pandas as pd
import numpy as np


class IPA:

    def __init__(self, url_file_1, url_file_2):
        self.url_file_1 = file_harapan
        self.url_fule_2 = file_persepsi

    def filtering_column(file_path):
        print("run filtering column...")
        result = pd.read_excel(file_path).drop(
            columns=['Nim'])
        return result

    def validity_test(file_path, a, b, c, d, e):
        """Validity for 5 category:

        tangiable, realibility, responsiveness, assurance, empathy

        params:
        file_path: path for excel file
        a b c d e: this for initial column in every category
        Return: JSON of correlation matrix
        """

        data_kuesioner = IPA.filtering_column(file_path)

        tangiable = data_kuesioner.loc[0:, a:'Total_A']
        corr_matrix1 = tangiable.corr().round(3).loc['Total_A'].to_dict()
        realibility = data_kuesioner.loc[0:, b:'Total_B']
        corr_matrix2 = realibility.corr().round(3).loc['Total_B'].to_dict()
        responsiveness = data_kuesioner.loc[0:, c:'Total_C']
        corr_matrix3 = responsiveness.corr().round(3).loc['Total_C'].to_dict()
        assurance = data_kuesioner.loc[0:, d:'Total_D']
        corr_matrix4 = assurance.corr().round(3).loc['Total_D'].to_dict()
        empathy = data_kuesioner.loc[0:, e:'Total_E']
        corr_matrix5 = empathy.corr().round(3).loc['Total_E'].to_dict()

        hasil = {'A': corr_matrix1, 'B': corr_matrix2,
                 'C': corr_matrix3, 'D': corr_matrix4, 'E': corr_matrix5}

        return hasil

    def uji_realibilitas(file_path, a, b, c, d, e):
        data_kuesioner = pd.read_excel(file_path)
        tangiable = data_kuesioner.loc[0:, a:'Total_A']
        realibility = data_kuesioner.loc[0:, b:'Total_B']
        responsiveness = data_kuesioner.loc[0:, c:'Total_C']
        assurance = data_kuesioner.loc[0:, d:'Total_D']
        empathy = data_kuesioner.loc[0:, e:'Total_E']

        return {'A': IPA.cronbatch_alpha(tangiable).round(3), 'B': IPA.cronbatch_alpha(realibility).round(3),
                'C': IPA.cronbatch_alpha(responsiveness).round(3), 'D': IPA.cronbatch_alpha(assurance).round(3),
                'E': IPA.cronbatch_alpha(empathy).round(3)}

    def cronbatch_alpha(file_path):
        itemscores = np.asarray(file_path.iloc[:, :-1])
        itemvars = itemscores.var(axis=0, ddof=0)
        tscores = itemscores.sum(axis=0)
        nitems = itemscores.shape[1]
        nitems_row = itemscores.shape[0]
        # result
        total = itemscores.sum(axis=1)**2
        total_kuadrat_baris = total.sum()

        total_varians = (total_kuadrat_baris -
                         ((itemscores.sum()**2) / nitems_row)) / nitems_row
        # kedua = (itemvars.sum() /  1)
        result = (nitems / (nitems-1)) * (1 - (itemvars.sum() / total_varians))
        return result

    def ipa_test(file_path_1, file_path_2):
        harapan = IPA.filtering_column(file_path_1).sum()
        presepsi = IPA.filtering_column(file_path_2).sum()

        result = pd.DataFrame(presepsi/harapan*100, columns=['IPA'])

        return result.round(3)

    def SE(file_path):
        harapan = IPA.filtering_column(file_path).mean()
        result = pd.DataFrame(harapan, columns=['SE']).round(3)

        return result

    def SP(file_path):
        presepsi = IPA.filtering_column(file_path).mean()
        result = pd.DataFrame(presepsi, columns=['SP']).round(3)

        return result

    def GAP(file_path_1, file_path_2):
        SE = IPA.SE(file_path_1)
        SP = IPA.SP(file_path_2)

        # mencari nilai sumbu X  dan Y
        SE_mean = SE.mean()
        SP_mean = SP.mean()

        #  KP = SP - SE
        frameGAP = pd.concat([SE, SP], axis=1)
        frameGAP['GAP'] = frameGAP['SP'] - frameGAP['SE']

        data = frameGAP['GAP']

        return data.round(3)

    def group(file_path_1, file_path_2):
        """Description

        Keyword arguments:
        file_path_1 -- file data harapan
        file_path_2 -- file data presepsi
        Return: JSON data GAP
        """

        data_IPA = IPA.ipa_test(file_path_1, file_path_2)
        data_SE = IPA.SE(file_path_1)
        data_SP = IPA.SP(file_path_2)
        data_GAP = IPA.GAP(file_path_1, file_path_2)
        results = pd.concat([data_IPA, data_SE, data_SP, data_GAP], axis=1)

        return results

    def kuadran(data_harapan, data_presepsi):
        SE_Harapan = IPA.SE(data_harapan)
        SP_Presepsi = IPA.SP(data_presepsi)

        # sumbu
        convert_SP = SP_Presepsi.mean()
        convert_SE = SE_Harapan.mean()

        # sumbu X dan Y
        X = pd.DataFrame(convert_SP, columns=['X'])
        sumbu_X = X.rename(index={"SP": 0})
        Y = pd.DataFrame(convert_SE, columns=['Y'])
        sumbu_Y = Y.rename(index={"SE": 0})

        kartasius = pd.concat([sumbu_X, sumbu_Y], axis='columns')

        return kartasius
