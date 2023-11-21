import time as tempo
import random

# CLASSES #

class Jogo():

    def __init__(self, time1, time2):        
        self.minutos            = 0
        self.placar             = {time1: 0, time2: 0}
        self.time1              = time1
        self.time2              = time2
        self.gols_time1         = {}
        self.gols_time2         = {}
        self.time_atual         = None
        self.outro_time         = None
        self.jogador_com_a_bola = None

    # Métodos
    def imprimir_placar(self):
        print(f'Placar: {self.time1.nome} {self.placar[self.time1]} x {self.placar[self.time2]} {self.time2.nome} - Tempo: {self.minutos} minutos')
          
    def posse_da_bola(self):
        if random.random() < 0.5:
            self.time_atual = self.time1
            self.outro_time = self.time2
        else:
            self.time_atual = self.time2
            self.outro_time = self.time1        
        self.jogador_com_a_bola = random.choice(self.time_atual.escalacao) 
        return self.time_atual, self.outro_time, self.jogador_com_a_bola
        
    def iniciar_jogo(self):
       
        self.imprimir_placar()
        self.posse_da_bola()
                
        while self.minutos < 90:    

            tempo.sleep(5)      # 5 segundos reais para cada iteração no jogo
            self.minutos += 2   # 2 minutos do jogo a cada iteração   
            
            if self.jogador_com_a_bola in self.time_atual.escalacao:
                
                acao = random.random()

                if acao < 0.5: # Realizar um passe
                    jogador_mesmo_time  = random.choice(self.time_atual.escalacao)  # Escolha aleatória de um jogador alvo no mesmo time
                    jogador_adversario  = random.choice(self.outro_time.escalacao)  # Escolha aleatória de um jogador adversário na marcação
                    resultado           = self.jogador_com_a_bola.realizar_passe(jogador_mesmo_time, jogador_adversario)
                    if resultado == 'passou':
                        self.jogador_com_a_bola = jogador_mesmo_time                    
                    elif resultado == 'adversario':
                        self.jogador_com_a_bola             = jogador_adversario
                        self.time_atual, self.outro_time    = self.outro_time, self.time_atual
                    else:
                        self.posse_da_bola()
                                
                elif acao < 0.75: # Realizar um cruzamento
                    jogador_mesmo_time  = random.choice(self.time_atual.escalacao)  # Escolha aleatória de um jogador alvo no mesmo time
                    jogador_adversario  = random.choice(self.outro_time.escalacao)  # Escolha aleatória de um jogador adversário na marcação                
                    goleiro_adversario  = self.outro_time.escalacao[0]
                    resultado           = self.jogador_com_a_bola.realizar_cruzamento(jogador_mesmo_time, jogador_adversario, goleiro_adversario) 
                    if resultado == 'gol':
                        if self.time_atual == self.time1:
                            self.placar[self.time1] += 1
                            self.gols_time1[jogador_mesmo_time.nome] = self.minutos
                        else:
                            self.placar[self.time2] += 1
                            self.gols_time2[jogador_mesmo_time.nome] = self.minutos
                        self.time_atual, self.outro_time    = self.outro_time, self.time_atual
                        self.jogador_com_a_bola             = random.choice(self.time_atual.escalacao)
                    elif resultado == 'fora':
                        self.time_atual, self.outro_time    = self.outro_time, self.time_atual
                        self.jogador_com_a_bola             = random.choice(self.time_atual.escalacao)
                    else:
                        self.posse_da_bola()
                                
                else: # Realizar uma finalização
                    jogador_adversario  = random.choice(self.outro_time.escalacao)  # Escolha aleatória de um jogador adversário na marcação
                    goleiro_adversario  = self.outro_time.escalacao[0]
                    resultado           = self.jogador_com_a_bola.realizar_finalizacao(jogador_adversario, goleiro_adversario)
                    if resultado == 'gol':
                        if self.time_atual == self.time1:
                            self.placar[time1] += 1
                            self.gols_time1[self.jogador_com_a_bola.nome] = self.minutos
                        else:
                            self.placar[time2] += 1
                            self.gols_time2[self.jogador_com_a_bola.nome] = self.minutos
                        self.time_atual, self.outro_time    = self.outro_time, self.time_atual
                        self.jogador_com_a_bola             = random.choice(self.time_atual.escalacao) 
                    elif resultado == 'fora':
                        self.time_atual, self.outro_time    = self.outro_time, self.time_atual
                        self.jogador_com_a_bola             = random.choice(self.time_atual.escalacao)
                    else:
                        self.posse_da_bola()

            self.imprimir_placar()

        print('Fim de jogo!')
        print(f'- Gols do {self.time1.nome}:')
        for jogador, minuto in self.gols_time1.items():
            print(f'{jogador} - Minuto {minuto}')
        print(f'- Gols do {self.time2.nome}:')
        for jogador, minuto in self.gols_time2.items():
            print(f'{jogador} - Minuto {minuto}')

class Time():
    
    def __init__(self, nome, jogadores, formacao):
        self.nome       = self.validar_nome(nome)
        self.jogadores  = self.validar_jogadores(jogadores)
        self.formacao   = self.validar_formacao(formacao)
        self.escalacao  = self.escalar_time()
        self.reservas   = [jogador for jogador in self.jogadores if jogador not in self.escalacao]
        
    # Validadores    
    @classmethod
    def validar_nome(cls, nome):
        if 1 <= len(nome) <= 18:
            return nome
        else:
            raise ValueError('O nome do time deve conter entre 1 e 18 caracteres.')
        
    @classmethod
    def validar_jogadores(cls, jogadores):
        if 11 <= len(jogadores) <= 40:
            return jogadores
        else:
            raise ValueError('A lista de jogadores deve conter entre 11 e 40 jogadores.')

    @classmethod
    def validar_formacao(cls, formacao):
        if len(formacao) == 5 and sum(formacao) == 10:
            return formacao
        else:
            raise ValueError('A formação deve conter 5 números, e a soma deles deve ser igual a 10.')

    # Métodos
    def escalar_time(self):
        escalacao = {
            'GOL': [],
            'LAT': [],
            'ZAG': [],
            'VOL': [],
            'MEI': [],
            'ATA': [],
        }

        for jogador in self.jogadores:
            if jogador.posicao in escalacao:
                escalacao[jogador.posicao].append(jogador)
        
        if len(escalacao['GOL']) == 0: # Verifica se há pelo menos um goleiro disponível
            raise ValueError('O time deve ter pelo menos 1 goleiro.')               
        escalacao['GOL'] = random.choice(escalacao['GOL']) # Escolhe um goleiro entre as opções disponíveis
                
        formacao = self.formacao
        for posicao, quantidade in zip(['ZAG', 'LAT', 'VOL', 'MEI', 'ATA'], formacao):
            if len(escalacao[posicao]) < quantidade: # Verifica se há jogadores disponíveis para a formação escolhida
                raise ValueError(f'Não há jogadores suficientes na posição {posicao} para a formação escolhida.')
        
        escalacao_final = []
        escalacao_final.append(escalacao['GOL'])                # Goleiro
        escalacao_final.extend(escalacao['ZAG'][:formacao[0]])  # Laterais
        escalacao_final.extend(escalacao['LAT'][:formacao[1]])  # Zagueiros
        escalacao_final.extend(escalacao['VOL'][:formacao[2]])  # Volantes
        escalacao_final.extend(escalacao['MEI'][:formacao[3]])  # Meias
        escalacao_final.extend(escalacao['ATA'][:formacao[4]])  # Atacantes
        
        return escalacao_final
    
    def imprimir_escalacao(self):
        print(f'Escalação do {self.nome}:')
        for jogador in self.escalacao:
            print(f"- {jogador.numero}: {jogador.nome}")

class Jogador():
    
    def __init__(self, numero, nome, posicao, finalizacao, cabecada, cobranca_falta, passe, cruzamento, interceptacao, defesa, agressividade):
        self.numero         = self.validar_numero(numero)
        self.nome           = self.validar_nome(nome)
        self.posicao        = self.validar_posicao(posicao)
        self.finalizacao    = self.validar_atributo(finalizacao)
        self.cabecada       = self.validar_atributo(cabecada)
        self.cobranca_falta = self.validar_atributo(cobranca_falta)
        self.passe          = self.validar_atributo(passe)
        self.cruzamento     = self.validar_atributo(cruzamento)
        self.interceptacao  = self.validar_atributo(interceptacao)
        self.defesa         = self.validar_atributo(defesa)
        self.agressividade  = self.validar_atributo(agressividade)

    # Validadores da classe
    @staticmethod
    def validar_numero(numero):
        if 1 <= numero <= 99:
            return numero
        else:
            raise ValueError('O número da camisa deve estar entre 1 e 99.')

    @staticmethod
    def validar_nome(nome):
        if 1 <= len(nome) <= 18:
            return nome
        else:
            raise ValueError('O nome do jogador deve conter entre 1 e 18 caracteres.')

    @staticmethod
    def validar_atributo(valor):
        if 1 <= valor <= 99:
            return valor
        else:
            raise ValueError('Os atributos devem estar entre 1 e 99.')
        
    @staticmethod
    def validar_posicao(posicao):
        if posicao in ['GOL', 'ZAG', 'LAT', 'VOL', 'MEI', 'ATA']:
            return posicao
        else:
            raise ValueError('A posição do jogador é inválida.')
        
    # Ações do jogador        
    def realizar_passe(self, jogador_equipe, jogador_adversario):
        probabilidade_sucesso = self.passe / 100
        probabilidade_interceptacao = jogador_adversario.interceptacao / 200
        if random.random() < probabilidade_sucesso:
            if random.random() < probabilidade_interceptacao:
                print(f'{jogador_adversario.nome} bloqueou o passe de {self.nome}.')
                return 'bloqueado'
            else:
                print(f'{self.nome} passou para {jogador_equipe.nome}.')
                return 'passou'
        else:
            print(f'Passe errado de {self.nome}. Bola com {jogador_adversario.nome}.')
            return 'adversario'
    
    def realizar_cruzamento(self, jogador_equipe, jogador_adversario, goleiro_adversario):
        if self.posicao != 'GOL': # Goleiro não pode realizar cruzamento
            probabilidade_interceptacao = jogador_adversario.interceptacao / 200
            if random.random() < probabilidade_interceptacao:
                print(f'{jogador_adversario.nome} bloqueou o cruzamento de {self.nome}!')
                return 'bloqueado'
            else:
                probabilidade_cabecada  = jogador_equipe.cabecada / 100
                resultado_cabecada      = random.random()
                if resultado_cabecada < probabilidade_cabecada:
                    probabilidade_goleiro_defesa    = goleiro_adversario.defesa / 100
                    resultado_goleiro               = random.random()
                    if resultado_goleiro < 0.25:
                        print(f'GOL: {jogador_equipe.numero} - {jogador_equipe.nome} de cabeça.')
                        print(f'Assistência: {self.numero} - {self.nome}.')
                        return 'gol'
                    elif resultado_goleiro < 0.5:
                        print(f'{self.nome} cruzou e {jogador_equipe.nome} de cabeceou na trave!')
                        return 'trave'
                    elif resultado_goleiro < 0.75 and resultado_goleiro < probabilidade_goleiro_defesa:
                        print(f'{self.nome} cruzou e {goleiro_adversario.nome} defendeu a cabeçada de {jogador_equipe.nome}!')
                        return 'defesa'
                    else:
                        print(f'{self.nome} cruzou e {jogador_equipe.nome} cabeceou pra fora!')
                        return 'fora'
                else:
                    print(f'{self.nome} cruzou direto pra fora.')
                    return 'fora'
        else:
            print(f'Bola com {self.nome}.')
                
    def realizar_finalizacao(self, jogador_adversario, goleiro_adversario):
        if self.posicao != 'GOL': # Goleiro não pode realizar finalização
            probabilidade_interceptacao = jogador_adversario.interceptacao / 200
            probabilidade_sucesso       = self.finalizacao / 100
            probabilidade_defesa        = goleiro_adversario.defesa / 100
            if random.random() < probabilidade_interceptacao:
                print(f'{jogador_adversario.nome} bloqueou a finalização de {self.nome}!')
                return 'bloqueado'
            else:
                if random.random() < probabilidade_sucesso:
                    if random.random() < probabilidade_defesa:
                        print(f'{goleiro_adversario.nome} defendeu o chute de {self.nome}!')
                        return 'defesa'
                    elif random.random() < 0.8:               
                        print(f'GOL: {self.numero} - {self.nome}')
                        return 'gol'
                    else:
                        print(f'{self.nome} chutou na trave!')
                        return 'trave'
                else:
                    print(f'{self.nome} chutou pra fora!')
                    return 'fora'
        else:
            print(f'{self.nome} tem a bola dominada.')

# TIMES #

# Grêmio FBPA

# Goleiros
gabriel_grando      = Jogador(12, 'Gabriel Grando', 'GOL', 40, 49, 50, 53, 55, 57, 71, 58)
felipe_scheibig     = Jogador(41, 'Felipe Scheibig', 'GOL', 40, 49, 48, 53, 56, 51, 68, 47)
caique_santos       = Jogador(31, 'Caíque S.', 'GOL', 40, 72, 55, 58, 63, 51, 71, 47)

# Zagueiros
pedro_geromel       = Jogador(3, 'P. Geromel', 'ZAG', 63, 81, 69, 74, 75, 83, 85, 80)
walter_kannemann    = Jogador(4, 'W. Kannemann', 'ZAG', 62, 80, 65, 66, 69, 86, 85, 83)
bruno_alves         = Jogador(34, 'Bruno Alves', 'ZAG', 57, 83, 58, 67, 66, 77, 80, 78)
bruno_uvini         = Jogador(15, 'B. Uvini', 'ZAG', 54, 79, 64, 64, 67, 77, 75, 78)
rodrigo_ely         = Jogador(5, 'R. Ely', 'ZAG', 56, 80, 59, 69, 66, 77, 78, 77)

# Laterais
fabio_silva         = Jogador(2, 'Fábio', 'LAT', 51, 61, 63, 71, 74, 73, 69, 76)
joao_pedro          = Jogador(18, 'João Pedro', 'LAT', 59, 65, 67, 65, 67, 66, 65, 70)
reinaldo_silva      = Jogador(6, 'Reinaldo', 'LAT', 76, 70, 81, 76, 82, 76, 77, 82)
luis_cuiabano       = Jogador(54, 'Cuiabano', 'LAT', 68, 58, 60, 69, 69, 58, 58, 75)

# Volantes
pepe_pinto          = Jogador(23, 'Pepê', 'VOL', 67, 63, 66, 70, 71, 61, 56, 60)
felipe_carballo     = Jogador(8, 'F. Carballo', 'VOL', 59, 67, 68, 74, 69, 73, 64, 75)
mathias_villasanti  = Jogador(25, 'M. Villasanti', 'VOL', 59, 63, 68, 68, 69, 65, 66, 65)
ronald_falkoski     = Jogador(15, 'Ronald', 'VOL', 65, 64, 64, 73, 72, 67, 67, 76)

# Meias
franco_cristaldo    = Jogador(19, 'F. Cristaldo', 'MEI', 68, 62, 62, 67, 61, 51, 56, 65)
luan_guilherme      = Jogador(7, 'Luan', 'MEI', 81, 63, 76, 82, 79, 50, 50, 64)
everton_galdino     = Jogador(13, 'E. Galdino', 'MEI', 70, 62, 62, 70, 66, 50, 49, 50)
nathan_souza        = Jogador(14, 'Nathan', 'MEI', 70, 60, 67, 76, 72, 50, 53, 48)

# Atacantes
luis_suarez         = Jogador(9, 'L. Suárez', 'ATA', 90, 80, 84, 82, 78, 60, 54, 92)
andre_henrique      = Jogador(77, 'André Henrique', 'ATA', 64, 53, 59, 74, 70, 46, 49, 46)
jp_galvao           = Jogador(11, 'J.P. Galvão', 'ATA', 74, 71, 67, 71, 66, 62, 48, 65)
aldemir_ferreira    = Jogador(10, 'Ferreira', 'ATA', 65, 59, 67, 66, 68, 51, 48, 58)
lucas_besozzi       = Jogador(22, 'L. Besozzi', 'ATA', 65, 55, 55, 65, 64, 53, 44, 45)

# SC Internacional

# Goleiros
sergio_rochet       = Jogador(33, 'S. Rochet', 'GOL', 40, 51, 50, 54, 61, 60, 72, 60)
keiller_nunes       = Jogador(1, 'Keiller', 'GOL', 40, 49, 50, 57, 60, 60, 71, 60)

# Zagueiros
vitao_matos         = Jogador(44, 'Vitão', 'ZAG', 51, 73, 49, 63, 61, 71, 70, 75)
gabriel_mercado     = Jogador(25, 'G. Mercado', 'ZAG', 60, 74, 54, 66, 65, 79, 75, 83)
igor_g_silva        = Jogador(21, 'Igor Gomes', 'ZAG', 60, 74, 54, 66, 65, 79, 75, 83)
nicolas_hernandez   = Jogador(22, 'N. Hernández', 'ZAG', 53, 76, 51, 67, 69, 80, 78, 71)

# Laterais
fabricio_bustos     = Jogador(16, 'F. Bustos', 'LAT', 63, 56, 58, 76, 77, 75, 61, 75)
hugo_mallo          = Jogador(2, 'Hugo Mallo', 'LAT', 60, 66, 64, 72, 77, 80, 75, 77)
rene_martins        = Jogador(6, 'Renê', 'LAT', 60, 61, 63, 74, 77, 71, 62, 68)
dalbert_estevao     = Jogador(29, 'Dalbert', 'LAT', 57, 62, 56, 74, 73, 73, 69, 70)

# Volantes
charles_aranguiz    = Jogador(20, 'C. Aránguiz', 'VOL', 70, 68, 74, 85, 81, 77, 73, 85)
bruno_h_corsini     = Jogador(8, 'Bruno Henrique', 'VOL', 71, 73, 75, 78, 75, 73, 72, 80)
romulo_zwarg        = Jogador(40, 'Rômulo', 'VOL', 66, 64, 67, 69, 71, 67, 64, 73)
gabriel_franco      = Jogador(23, 'Gabriel', 'VOL', 65, 53, 53, 75, 70, 81, 79, 85)

# Meias
alan_patrick        = Jogador(10, 'Alan Patrick', 'MEI', 69, 60, 82, 80, 79, 55, 52, 62)
mauricio_prado      = Jogador(27, 'Mauricio', 'MEI', 71, 61, 68, 74, 71, 58, 58, 64)
johnny_cardoso      = Jogador(30, 'Johnny', 'MEI', 60, 65, 65, 73, 75, 66, 68, 65)
carlos_de_pena      = Jogador(14, 'C. de Pena', 'MEI', 66, 66, 65, 75, 70, 54, 57, 62)
gustavo_campanharo  = Jogador(17, 'G. Campanharo', 'MEI', 63, 60, 70, 79, 78, 66, 68, 70)

# Atacantes
ener_valencia       = Jogador(13, 'E. Valencia', 'ATA', 74, 78, 66, 68, 70, 55, 48, 72)
luiz_adriano        = Jogador(9, 'Luiz Adriano', 'ATA', 79, 77, 73, 77, 71, 50, 51, 55)
wanderson_campos    = Jogador(11, 'Wanderson', 'ATA', 71, 66, 69, 75, 72, 45, 42, 56)
lucca_tavares       = Jogador(45, 'Lucca', 'ATA', 71, 66, 69, 75, 72, 45, 42, 56)

# Listas de jogadores dos times
jogadores_gremio_fbpa       = [gabriel_grando, felipe_scheibig, caique_santos, pedro_geromel, walter_kannemann, bruno_alves, bruno_uvini, rodrigo_ely, fabio_silva, joao_pedro, reinaldo_silva, luis_cuiabano, pepe_pinto, felipe_carballo, mathias_villasanti, ronald_falkoski, franco_cristaldo, luan_guilherme, everton_galdino, nathan_souza, luis_suarez, andre_henrique, jp_galvao, aldemir_ferreira, lucas_besozzi]
jogadores_sc_internacional  = [sergio_rochet, keiller_nunes, vitao_matos, gabriel_mercado, igor_g_silva, nicolas_hernandez, fabricio_bustos, hugo_mallo, rene_martins, dalbert_estevao, charles_aranguiz, bruno_h_corsini, romulo_zwarg, gabriel_franco, alan_patrick, mauricio_prado, johnny_cardoso, carlos_de_pena, gustavo_campanharo, ener_valencia, luiz_adriano, wanderson_campos, lucca_tavares]

# Inicializando os times
gremio_fbpa         = Time('Grêmio', jogadores_gremio_fbpa, [2, 2, 2, 2, 2])
sc_internacional    = Time('Internacional', jogadores_sc_internacional, [2, 2, 2, 2, 2])

# Escolhendo os times para o jogo
time1 = gremio_fbpa
time1.imprimir_escalacao()

time2 = sc_internacional
time2.imprimir_escalacao()

# Iniciando o jogo
jogo = Jogo(time1, time2)
jogo.iniciar_jogo()