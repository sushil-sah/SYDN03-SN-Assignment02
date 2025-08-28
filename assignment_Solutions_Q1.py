def encrypt_char(c, shift1, shift2):
    # checking if the character is lower, upper or other as we need to perform different encryption logic depending on character case
    if c.islower():
        '''
            For lowercase letters:
                - If the letter is in the first half of the alphabet (a-m): shift forward by shift1 * shift2 positions
                - If the letter is in the second half (n-z): shift backward by shift1 + shift2positions
        '''
        # for 1st half of the lower case alphabet
        if c <= 'm':
            # calculating the total shift that has to be applied to a character
            shift = shift1 * shift2
            # 1. determing the difference of position of provided character from character 'a'
            original_position = ord(c) - ord('a')
            # 2. determing the position after adding the shift that has to be applied for encryption
            shifted_position = original_position + shift
            wrapped_position = shifted_position % 26
            # 3. adding wrapped position with position of 'a' to get the final position and convert it into character using chr built-in function
            encrypted_character = chr(wrapped_position + ord('a'))
            return encrypted_character
        
        # for second half of the lower case alphabet
        else:
            # calculating the total shift that has to be applied to a character
            shift = -(shift1 + shift2)
            # merged logic 1,2 and 3 in above logic to make the code more concise as the above code is for more clear illustration only
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        
    elif c.isupper():
        '''
            For uppercase letters:
                - If the letter is in the first half (A-M): shift backward by shift1 positions
                - If the letter is in the second half (N-Z): shift forward by shift2² positions (shift2 squared)
        '''
        # for 1st half of the upper case alphabets (A-M)
        if c <= 'M':
            # calculating the shift
            shift = -shift1
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        
        # for 2nd half of the upper case alphabets (N-Z)
        else:
            # calcualing the shift i.e shift2 ^ 2
            shift = shift2 ** 2
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        
    # if c is not alphabet returning it without any changes
    else:
        return c
    

# for decryption the logic applied in encryption will be reverted
def decrypt_char(c, shift1, shift2):
    if c.islower():
        '''
            For lowercase letters:
                - If the letter is in the first half of the alphabet (a-m): shift backward by shift1 * shift2 positions as it was forward in encryption
                - If the letter is in the second half (n-z): shift forward by shift1 + shift2 positions as it was backward originally
        '''
        if c <= 'm':
            # calculating the shift
            shift = -(shift1 * shift2)
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        
        else:
            # calculating the shift
            shift = (shift1 + shift2)
            print(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        
    elif c.isupper():
        '''
            For uppercase letters:
                - If the letter is in the first half (A-M): shift forward by shift1 positions as it was shifted backward originally
                - If the letter is in the second half (N-Z): shift backward by shift2² positions (shift2 squared) as it was shifted forward originally
        '''
        if c <= 'M':
            # calculating the shift
            shift = shift1
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        
        else:
            # calculating the shift
            shift = -(shift2 ** 2)
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    else:
        return c

# function takes raw_file, encrypt file, two shift values as an argument and calles a encrypt_char function where encryption logic is implemented
def encrypt_file(raw_file, encrypted_file, shift1, shift2):
    print(f'encryption of file {raw_file} has started')

    # opening an original file in read mode and storing the file content in raw_content for further processing
    with open(raw_file, "r") as f:
        raw_content = f.read()
    
    # calling a function encrypt_char where encryption logic is implemented and joining all the results and storing them in a variable to write in a file
    encrypted_content = "".join(encrypt_char(c, shift1, shift2) for c in raw_content)

    # opening encrypted file in write mode to create a new empty file and write encrypted content
    with open(encrypted_file, "w") as f:
        f.write(encrypted_content)

# function takes encrypted_file, decrypted file, two shift values as an argument and calles a decrypt_char function where decryption logic is implemented
def decrypt_file(encrypted_file, decrypted_file, shift1, shift2):
    print(f'decryption of file {encrypted_file} has started')

    # opening an encrypted file in read mode and storing the file content in encrypted_file_content for further processing
    with open(encrypted_file, "r") as f:
        encrypted_file_content = f.read()

    # calling a function decrypt_char where decryption logic is implemented and joining all the results and storing them in a variable to write in a file    
    decrypted_content = "".join(decrypt_char(c, shift1, shift2) for c in encrypted_file_content)

    # opening decrypted file in write mode to create a new empty file and write decrypted content
    with open(decrypted_file, "w") as f:
        f.write(decrypted_content)

''' This function verifies if the original file content and decrypted file content matches or not. 
        - If it matches True is returned
        - Else False is returned
'''
def verify_content(raw_file, decrypted_file):
    print('verification process started')
    with open(raw_file, "r") as f1, open(decrypted_file, "r") as f2:
        return f1.read() == f2.read()

# take two shift values from the user i.e. shift1 and shift2
shift1 = int(input('Enter the value for shift1: '))
shift2 = int(input('Enter the value for shift2: '))

# assigning the file name to each variables to increase the reusability 
raw_file = 'raw_text.txt'
encrypted_file = 'encrypted_text.txt'
decrypted_file = 'decrypted_text.txt'

# calling the function to encrypt the original file and generate a new encrypted file
encrypt_file(raw_file, encrypted_file, shift1, shift2)
print(f'Encryption of file {raw_file} completed and encrypted data is written in file {encrypted_file}')

# calling the function to decrypt the encrypted file and generate a new decrypted file
decrypt_file(encrypted_file, decrypted_file, shift1, shift2)
print(f'Decryption of file {encrypted_file} completed and decrypted data is written in file {decrypted_file}')


''' validation of the generated decrypted file from decrypt_file function with original raw file
         - if the content in the files are same then Decryption successful will be printed
         - else Decryption failure will be printed
'''
if verify_content(raw_file, decrypted_file):
    print('Decryption successful! Files match')
else:
    print('Decryption failure! Files don\'t match')