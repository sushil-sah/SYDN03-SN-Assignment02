def encrypt_file(raw_file, encrypted_File, shift1, shift2):
    print('encryption function called')
    # need to call a function to perform encryption

def decrypt_file(encrypted_file, decrypted_file, shift1, shift2):
    print('decryption function called')
    # need to call a function to perform decryption

def verify(raw_file, decrypted_file):
    print('verification function called')
    # need to open two files and check if they are same


shift1 = int(input('Enter the value for shift1: '))
shift2 = int(input('Enter the value for shift2: '))
raw_file = 'raw_text.txt'
encrypted_file = 'encrypted_text.txt'
decrypted_file = 'decrypted_text.txt'
encrypt_file(raw_file, encrypted_file, shift1, shift2)
print(f'Encryption of file {raw_file} completed and encrypted data is written in file {encrypted_file}')

decrypt_file(encrypted_file, decrypted_file, shift1, shift2)
print(f'Decryption of file {encrypted_file} completed and decrypted data is written in file {decrypted_file}')

if verify(raw_file, decrypted_file):
    print('Decryption successful! Files match')
else:
    print('Decryption failure! Files don\'t match')