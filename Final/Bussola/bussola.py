import pygame
import socket
pygame.init()

largura, altura = 800, 600
display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Bússola")

fundo = (48, 25, 52)  # Roxo

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server

imagem_bussola = pygame.image.load('./Bussola/bussola.png')
imagem_ponteiro = pygame.image.load('./Bussola/ponteiro.png')
imagem_ponteiro = pygame.transform.scale(imagem_ponteiro, (360, 100))

imagem_ponteiro_menor = pygame.image.load('./Bussola/ponteiro_menor.png')
imagem_ponteiro_menor = pygame.transform.scale(imagem_ponteiro_menor, (180, 50))

# TEM QUE MEXER ESTA VARIAVEL PRA TROCAR
angulo = [0,90]

def rotacionar_imagem(imagem, angulo):
    return pygame.transform.rotate(imagem, angulo)

# Função principal
def main():
    global angulo
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
     
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, PORT))
                s.listen(1)
                s.settimeout(0.2)
                conn, addr = s.accept()
                with conn:
                    angulo = float(conn.recv(1024).decode())
                    print(angulo)
            except: pass


        display.fill(fundo)
        display.blit(imagem_bussola, (largura//2 - imagem_bussola.get_width()//2, altura//2 - imagem_bussola.get_height()//2))
        
        ponteiro_rotacionado = rotacionar_imagem(imagem_ponteiro, -angulo[0])
        display.blit(ponteiro_rotacionado, (largura//2 - ponteiro_rotacionado.get_width()//2, altura//2 - ponteiro_rotacionado.get_height()//2))
        
        ponteiro_rotacionado2 = rotacionar_imagem(imagem_ponteiro_menor, -angulo[1])
        display.blit(ponteiro_rotacionado2, (largura//2 - ponteiro_rotacionado.get_width()//2, altura//2 - ponteiro_rotacionado.get_height()//2))
 

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()