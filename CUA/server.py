from Crypto.Cipher import AES
from Crypto.Util.number import * 
from Ransom import RNG
from ID import ID 
import hashlib

FLAG = "W1{?????????????????????}"


rng = RNG()
id  = ID(rng)


class Server:

    def __init__(self,rng,id):
        self.rng = rng
        self.id = id
        self.key = hashlib.sha256(long_to_bytes(self.rng.getrandbits(36))).digest()
        self.cipher = AES.new(self.key, AES.MODE_GCM)
        self.db = {}   
        self.accounts = {} 
        self.ID = {}
    
    def encrypt_data(self, data: bytes) -> bytes:
        nonce = self.cipher.nonce
        ciphertext, tag = self.cipher.encrypt_and_digest(data)
        return nonce + tag + ciphertext
    
    def store_user_data(self, username: str, data: bytes):
        encrypted_data = self.encrypt_data(data)
        self.db[username] = encrypted_data
        return encrypted_data 

    def hash_password(self, password) -> str:
        return hashlib.sha512(password).hexdigest()

    def register(self, username, password) -> bool:
        if username in self.accounts:
            return False
        
        if not isinstance(username, str) or not isinstance(password, str):
            return False
        try:         
            self.ID[username] = self.id.getID(username)
            temp = password.encode('utf-8', errors='ignore')
            salt = long_to_bytes(int(self.ID[username]))

        except Exception as e:
            print(e)
            return False 
        
        self.accounts[username] = self.hash_password(salt + temp)
        return True
    
    def login(self, username, password) -> bool:
        if username not in self.accounts:
            return False
        
        try:
            temp = password.encode()
            salt = long_to_bytes(int(self.ID[username]))
        except Exception as e:
            print(e)
            return False 
        
        if self.accounts[username] == self.hash_password(salt + temp):
            return True
        return False
    
def banner_login():
    print(r"""
██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
            """)

def banner_register():
    print(r"""
██████╗ ███████╗ ██████╗ ██╗███████╗████████╗███████╗██████╗
██╔══██╗██╔════╝██╔════╝ ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██████╔╝█████╗  ██║  ███╗██║███████╗   ██║   █████╗  ██████╔╝
██╔══██╗██╔══╝  ██║   ██║██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║███████╗╚██████╔╝██║███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                      """)

def banner_admin():
    print(r"""
 ██████╗██╗   ██╗ █████╗     ███╗   ██╗ ██████╗ ██╗  ██╗███████╗
██╔════╝██║   ██║██╔══██╗    ████╗  ██║██╔════╝ ██║  ██║██╔════╝
██║     ██║   ██║███████║    ██╔██╗ ██║██║  ███╗███████║█████╗
██║     ██║   ██║██╔══██║    ██║╚██╗██║██║   ██║██╔══██║██╔══╝
╚██████╗╚██████╔╝██║  ██║    ██║ ╚████║╚██████╔╝██║  ██║███████╗
    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                """)

def menu():
    print(r"""
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝

████████╗ ██████╗     ███╗   ███╗██╗   ██╗     ██████╗██╗   ██╗ █████╗
╚══██╔══╝██╔═══██╗    ████╗ ████║╚██╗ ██╔╝    ██╔════╝██║   ██║██╔══██╗
   ██║   ██║   ██║    ██╔████╔██║ ╚████╔╝     ██║     ██║   ██║███████║
   ██║   ██║   ██║    ██║╚██╔╝██║  ╚██╔╝      ██║     ██║   ██║██╔══██║
   ██║   ╚██████╔╝    ██║ ╚═╝ ██║   ██║       ╚██████╗╚██████╔╝██║  ██║
   ╚═╝    ╚═════╝     ╚═╝     ╚═╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═╝

 ██████╗██╗  ██╗ █████╗ ██╗     ██╗     ███████╗███╗   ██╗ ██████╗ ███████╗
██╔════╝██║  ██║██╔══██╗██║     ██║     ██╔════╝████╗  ██║██╔════╝ ██╔════╝
██║     ███████║███████║██║     ██║     █████╗  ██╔██╗ ██║██║  ███╗█████╗
██║     ██╔══██║██╔══██║██║     ██║     ██╔══╝  ██║╚██╗██║██║   ██║██╔══╝
╚██████╗██║  ██║██║  ██║███████╗███████╗███████╗██║ ╚████║╚██████╔╝███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
""")
    
    print("1. Register")
    print("2. Login")
    print("3. Reset database")
    print("4. Talk to admin")
    print("5. Exit")
    print("> ", end='')


def main():
    Server_Instance = Server(rng, id)
    Server_Instance.register("admin", Server_Instance.rng.urandom(16).decode('utf-8', errors='ignore'))
    

    while True:
        menu()
        choice = input().strip()
        if choice == '1':
            banner_register()
            
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if Server_Instance.register(username, password):
                
                print("Registration successful, here is your account information: ")
                print(f"Username: {username}")
                print(f"ID: {Server_Instance.ID[username]}")
            else:
                print("Registration failed.")

        elif choice == '2':
            banner_login()

            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if Server_Instance.login(username, password):
                print(f"Login successful.")
                if username == "admin":
                    print(f"Here is the flag: {FLAG}")
            else:
                print("Login failed.")
        elif choice == '3':
            Server_Instance.db = {}
            Server_Instance.accounts = {}
            Server_Instance.ID = {}
            Server_Instance.id.reset_ID()
            Server_Instance.register("admin", Server_Instance.rng.urandom(16).decode('utf-8', errors='ignore'))
            print("Database reset.")
        elif choice == '4':
            banner_admin()

            content = input("Enter your message to admin: ")
            try:
                content = content.encode()
            except:
                print("Something went wrong.")
                continue
            Server_Instance.store_user_data("admin", content)
            print("Message sent to admin.")

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()