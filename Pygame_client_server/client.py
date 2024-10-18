import socket
import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Client')

# Tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Thiết lập font chữ
font = pygame.font.Font(None, 36)

# Biến để lưu trữ văn bản nhập
input_text = ''
input_box = pygame.Rect(100, 100, 600, 40)  # Ô input
button_rect = pygame.Rect(100, 160, 100, 40)  # Nút gửi
button_color = (0, 128, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Gửi dữ liệu khi nhấn Enter
                client_socket.sendall(input_text.encode())
                input_text = ''  # Xóa ô input sau khi gửi
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]  # Xóa ký tự cuối cùng
            else:
                input_text += event.unicode  # Thêm ký tự mới vào ô input

        # Kiểm tra nếu nhấn vào nút gửi
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                client_socket.sendall(input_text.encode())
                input_text = ''  # Xóa ô input sau khi gửi

    # Cập nhật màn hình
    screen.fill((255, 255, 255))

    # Vẽ ô input
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # Vẽ nút gửi
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render('Send', True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 5))

    pygame.display.flip()
