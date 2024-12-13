import pygame
import socket
pygame.init()

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 30)


largura, altura = 800*1.2, 600*1.2
display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Bússola")

fundo = (225, 225 , 225)  # Roxo

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server

imagem_bussola = pygame.image.load('./AR1.png')
imagem_bussola = pygame.transform.scale(imagem_bussola,(500,500))

imagem_ponteiro = pygame.image.load('./tip_orange.png')
imagem_ponteiro = pygame.transform.scale_by(imagem_ponteiro, 0.23)


# TEM QUE MEXER ESTA VARIAVEL PRA TROCAR
angulo = 0
curr_rotation = 0

def rotacionar_imagem(imagem, angulo):
    return pygame.transform.rotate(imagem, angulo)

# Função principal
def main():
    global angulo
    global curr_rotation
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        with open(r"C:\Users\pedro\OneDrive\Documentos\Eletrica\Eletrica\TCC - Macapá\TCC-AoA\Final\Bussola\angle.txt","r") as file:
            try:
                o_angulo,el,azi=file.readline().split(",")
                o_angulo=float(o_angulo)
                angulo= -o_angulo-90
            except: pass
        
        display.fill(fundo)
        display.blit(imagem_bussola, (largura//2 - imagem_bussola.get_width()//2, altura//2 - imagem_bussola.get_height()//2))
        
        curr_rotation += (angulo-curr_rotation)/4
        ponteiro_rotacionado = rotacionar_imagem(imagem_ponteiro, -curr_rotation)
        display.blit(ponteiro_rotacionado, (largura//2 - ponteiro_rotacionado.get_width()//2, altura//2 - ponteiro_rotacionado.get_height()//2))

        text_angulo = my_font.render("AoA no plano xz: {:.2f}".format(o_angulo), False, (0, 0, 0))
        display.blit(text_angulo,(0,0))

        text_azi = my_font.render("AoA azimutal: {:.2f}".format(float(azi)), False, (0, 0, 0))
        display.blit(text_azi,(0,100))

        text_el = my_font.render("AoA elevação: {:.2f}".format(float(el)), False, (0, 0, 0))
        display.blit(text_el,(0,200))

        pygame.display.flip()
        pygame.time.delay(25)

    pygame.quit()

if __name__ == "__main__":
    main()