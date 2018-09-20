import pygame
from lutador import Lutador
from background import Background
from music import Music
from telaselecao import Telaselecao
from menu import Menu
from colisao import Colisao

class Game(object):

    lista_tempo_1 = []
    lista_tempo_2 = []
    count = 0
    # construtor, responsável pela inicialização
    def __init__(self, titulo, tamanho_tela):
        self.amb = pygame
        self.amb.init()
        self.amb.display.set_caption(titulo)
        self.screen_size = largura, altura = tamanho_tela
        self.screen = self.amb.display.set_mode(self.screen_size, 0, 32)

        self.menu_ativo = True
        self.telaselecao_ativo = False
        self.jogo_acabou = False
        
        self.clock = self.amb.time.Clock()
        self.amb.key.set_repeat(5,3)

    def criar_lutadores(self):
        self.player1 = Lutador(self.amb, self.screen, self.telaselect.nome_1, (50, 410), self.telaselect.baseSeq_1, True)
        self.player2 = Lutador(self.amb, self.screen, self.telaselect.nome_2, (700, 410), self.telaselect.baseSeq_2)
        self.colidir = Colisao(self.player1, self.player2, self.amb)

    def iniciar_jogo(self):
        self.count += 1

        if self.count < 60:
            tempo = self.amb.time.get_ticks()//1000
            self.lista_tempo_1.append(tempo)
            
            self.player1.vivo = False
            self.player2.vivo = False
            
            if tempo == (self.lista_tempo_1[0] + 1):
                self.screen.blit(self.lista_init[0], (250, 275))
            
            elif tempo == (self.lista_tempo_1[0] + 2):
                self.screen.blit(self.lista_init[1], (250, 275))
            
            elif tempo == (self.lista_tempo_1[0] + 3):
                self.screen.blit(self.lista_init[2], (250, 275))
            
            elif tempo == (self.lista_tempo_1[0] + 4):
                self.screen.blit(self.lista_init[3], (250, 275))
            
        elif self.count == 61:
            self.player1.vivo = True
            self.player2.vivo = True
    
        self.music.volume = 0.3
        self.screen.blit(self.barra_vida, (205, 50))
        self.player1.desenhar(self)
        self.player2.desenhar(self)
        self.colidir.verificar_colisoes()

    def carregar_animacao_inicial(self):
        self.lista_init = [self.amb.image.load("../img/Selecao/3.png").convert_alpha(),
                           self.amb.image.load("../img/Selecao/2.png").convert_alpha(),
                           self.amb.image.load("../img/Selecao/1.png").convert_alpha(),
                           self.amb.image.load("../img/Selecao/fight.png").convert_alpha()]

    def acabar_jogo(self, player1):
        if player1:
            self.screen.blit(self.amb.image.load("../img/Fim/player2.png").convert_alpha(), (30, 282))
        else:
            self.screen.blit(self.amb.image.load("../img/Fim/player1.png").convert_alpha(), (30, 282))

        self.screen.blit(self.amb.image.load("../img/Fim/F5.png").convert_alpha(), (338, 540))
        self.screen.blit(self.amb.image.load("../img/Fim/ENTER.png").convert_alpha(), (115, 416))

        self.jogo_acabou = True

        """self.lista_tempo_2.append(self.lista_tempo_1[len(self.lista_tempo_1) - 1])

        if (self.lista_tempo_1[len(self.lista_tempo_1) - 1]) == (self.lista_tempo_2[0] + 5):
            self.menu_ativo = True"""

    def rodar(self):
        self.rodando = True
        fps = 12

        self.Pfundo = Background(self.amb, self.screen, self)
        self.music = Music(self.amb)
        self.menu = Menu(self.amb, self.screen, 150, (290,165), self) 
        self.telaselect = Telaselecao(self.amb, self.screen)
        
        self.barra_vida = self.amb.image.load("../img/Lifebar/lifebar.png").convert_alpha()

        self.carregar_animacao_inicial()

        while self.rodando:
            self.screen.fill((0, 0, 0))

            self.Pfundo.desenhar()
            
            self.music.verificar_ativacao()

            if self.menu_ativo:
                self.menu.desenhar()
            
            elif self.telaselecao_ativo:
                self.telaselect.desenhar()
                self.count = 0
            
            else:
                self.iniciar_jogo()

            for event in self.amb.event.get():                
                
                self.key = self.amb.key.get_pressed()
                
                if event.type == self.amb.QUIT:
                    self.rodando = False
                
                if event.type == self.amb.KEYDOWN:
                    if self.menu_ativo:
                        if self.menu.instrucoes:
                            self.menu.eventos_instrucoes(self.key)
                        
                        else:
                            self.menu.tratar_eventos(self.key)
                    
                    elif self.telaselecao_ativo:
                        self.telaselect.tratar_eventos(self.key, self)
                    
                    else:
                        self.player1.tratar_eventos(self.key)
                        self.player2.tratar_eventos(self.key)

                        if self.jogo_acabou:
                            if self.key[self.amb.K_F5]:
                                self.menu_ativo = True
                                self.count = 0
                                self.lista_tempo_1 = []

                            elif self.key[self.amb.K_RETURN]:
                                self.criar_lutadores()
                                self.count = 0
                                self.lista_tempo_1 = []

                            self.jogo_acabou = False
                    
                    if self.key[self.amb.K_EQUALS]:
                        if fps <= 20:
                            fps += 1

                    if self.key[self.amb.K_MINUS]:
                        if fps > 1:
                            fps -= 1

                if event.type == self.amb.KEYUP:
                    if self.menu_ativo is False and self.telaselecao_ativo is False:
                        
                        if self.player1.vivo:
                            if event.key == self.player1.frente or event.key == self.player1.tras:
                                self.player1.trocar_estado("parado")

                        if self.player2.vivo:
                            if event.key == self.player2.frente or event.key == self.player2.tras:
                                self.player2.trocar_estado("parado")
            
            self.amb.display.flip()
            
            self.clock.tick(fps)

        self.amb.quit()

if __name__ == "__main__":
    g = Game("Blood Walls",(1100,700))
    g.rodar()
