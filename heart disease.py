import PySimpleGUI as sg
import pandas as pd
import joblib

# Definindo o tema da janela para preto
sg.theme('DarkBlack1')

def main():
    #Fazendo Load do modelo
    best_RFC = joblib.load('best_RFC_model.pkl')


    def analisarS2(best_RFC,df_paciente):
    # Mostrar o DataFrame df_paciente
        y_paciente = best_RFC.predict(df_paciente)

        return y_paciente

    def exibir_resultado(y_paciente):
        if y_paciente == 0:
            mensagem = 'O paciente está bem.'
        elif y_paciente == 1:
            mensagem = 'Corra, o paciente está em estado crítico!'
        else:
            mensagem = 'Algo deu errado!'
        ''' Window Resultado'''
        layout = [
            [sg.Text(mensagem)],
            [sg.Button('Próximo'), sg.Button('Fechar')]
        ]

        window_resultado  = sg.Window('Resultado da Análise', layout)

        while True:
            event, values = window_resultado.read()
            if event == sg.WINDOW_CLOSED or event == 'Fechar':
                window_resultado.close()
                return 'Fechar'
            elif event == 'Próximo':
                window_resultado.close()
                return 'Próximo'

    # Definindo o layout da janela
    layout = [
        [sg.Text('Age'), sg.Input(key='age', size=(10, 1), justification='center')],
        [sg.Text('Sex'), sg.Input(key='sex', size=(10, 1), justification='center')],
        [sg.Text('Chest Pain Type'), sg.Input(key='chest_pain', size=(10, 1), justification='center')],
        [sg.Text('Resting BP (mm Hg)'), sg.Input(key='resting_bp', size=(10, 1), justification='center')],
        [sg.Text('Cholesterol (mg/dl)'), sg.Input(key='cholesterol', size=(10, 1), justification='center')],
        [sg.Text('Fasting Blood Sugar'), sg.Input(key='blood_sugar', size=(10, 1), justification='center')],
        [sg.Text('Resting ECG'), sg.Input(key='resting_ecg', size=(10, 1), justification='center')],
        [sg.Text('Max Heart Rate'), sg.Input(key='max_heart_rate', size=(10, 1), justification='center')],
        [sg.Text('Exercise Angina'), sg.Input(key='exercise_angina', size=(10, 1), justification='center')],
        [sg.Text('Oldpeak'), sg.Input(key='oldpeak', size=(10, 1), justification='center')],
        [sg.Text('ST Slope'), sg.Input(key='st_slope', size=(10, 1), justification='center')],
        [sg.Button('Submit')],
        [sg.Button('Exit')]
    ]

    # Criando a janela
    window = sg.Window('Dados do Paciente', layout)

    # Loop para interagir com a janela
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Submit':
            try:
                df_paciente = pd.DataFrame({
            'age': [float(values['age'])],
            'sex': [float(values['sex'])],
            'chest pain type': [float(values['chest_pain'])],
            'resting bp s': [float(values['resting_bp'])],
            'cholesterol': [float(values['cholesterol'])],
            'fasting blood sugar': [float(values['blood_sugar'])],
            'resting ecg': [float(values['resting_ecg'])],
            'max heart rate': [float(values['max_heart_rate'])],
            'exercise angina': [float(values['exercise_angina'])],
            'oldpeak': [float(values['oldpeak'])],
            'ST slope': [float(values['st_slope'])]
            })
            except ValueError:
                sg.popup_error('Por favor, preencha todos os campos com números válidos.')
                continue
            
            keys = []

            # Iterar sobre todos os elementos na janela
            for row in layout:
                for element in row:
                    # Verificar se o elemento tem uma chave
                    if isinstance(element, (sg.Input, sg.Button, sg.Text)):
                        if element.Key:
                            keys.append(element.Key)
            
            # Verificar se o DataFrame não está vazio
            if df_paciente.empty:
                sg.popup_error('Por favor, preencha todos os campos.')
                continue
            
            y_paciente = analisarS2(best_RFC, df_paciente)
            
            # Chamar a função para exibir a janela com base no resultado da análise
            resultado = exibir_resultado(y_paciente) 
            
            if resultado == 'Fechar':
                break
            elif resultado == 'Próximo':
                reiniciar_aplicacao(window)
            continue
            
def reiniciar_aplicacao(window):
    window.close()
    main()
    
main()