# Wordle Game Client 
import argparse
import json #importing for holding the information in the server
import socket
import ssl    #importing for TSL encryption
import random #using for generating guess
import string  #using for generating guess

# defining the send json message function
def send_json_message(sock, message):
    json_msg = json.dumps(message)
    sock.sendall(json_msg.encode() + b'\n')

# defining the receive json message function
def receive_json_msg(sock):
    data = " "
    # if it meets the correct message then it would decode the message 
    # till it finish
    while True:
        char = sock.recv(1).decode()
        if char == '\n':
            break
        data += char
    return json.loads(data)

def generate_guess(word_list):
   return random.choice(word_list)

def main():
    # Read word list from a text file
    with open("wordlist.txt", "r") as file:
        word_list = [line.strip() for line in file]

    normal_flag = None  # Initialize with default value
    parser = argparse.ArgumentParser(description="Our Wordle Game Client")
    parser.add_argument("-p", "--port", type=int, help="Transmission Control Protocol port number (def: 27993)", default=27993)
    parser.add_argument("-s", "--tls", action="store_true", help="Use TLS encryption connection")
    # creating the parser for username and hostname
    parser.add_argument("hostname", type=str, help="The hostname of the server")
    parser.add_argument("username", type=str, help="northeastern_username")

    arg = parser.parse_args()

    # Initalizing the variables
    game_id = None
    normal_flag = None
    tls_flag = None

    # printing based on the server and user input
    print("Parsed Command-Line Arguments:")
    print(f"Transmission Control Protocol Port: {arg.port}")
    print(f"TLS Encryption: {arg.tls}")
    print(f"Hostname: {arg.hostname}")
    print(f"Username: {arg.username}")

    port = 27993

    try:
        # Initializing a socket connection both with or without TLS encryption
        if arg.tls:
            cont = ssl.create_default_context()
            sock = cont.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                , server_hostname=arg.hostname)
            port = 27994  # The TLS port used for the game
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = arg.port

        sock.connect((arg.hostname, port))
        # Sending "Hello" message to the server
        hello_msg = {
            "type": "hello",
            "northeastern_username": arg.username
        }

        # This will store the msg sent to the server
        send_json_message(sock, hello_msg)

        # Receiving and parsing the "start" message from the server
        response = receive_json_msg(sock)
        print("Received response from server:", response)

        # Making sure that the message is "start" before parsing it
        if response["type"] == "start":
            game_id = response["id"]
            print(f"The Game ID is: {game_id}")
        else:
            print("Error: This response from the server is unexpected")

        # Load word list from a text file
        with open("wordlist.txt", "r") as file:
            word_list = [line.strip() for line in file]

        # adding guesses logic
        maximum_guesses = 500
        guess_count = 0

        maximum_retry = 500
        retry_count = 0

        while guess_count < maximum_guesses:
            guess = generate_guess(word_list)  
            guess_msg = {
                "type": "guess",
                "id": game_id,
                "word": guess
            }
            send_json_message(sock, guess_msg)
            response = receive_json_msg(sock)
      
            # Handle retry response
            if response["type"] == "retry":     
                    print(" The server has requested a retry. Generating a new guess....")
                    retry_count += 1
                    if retry_count >= maximum_retry:
                         print(f"You have reached the maximum number of retries ({maximum_retry}). Exiting the current loop.")
                         break

            elif response["type"] == "bye":
                # Handle bye response and extract the secret flag so it can be saved
                normal_flag = response.get("flag", " The secret flag is not found")
                tls_flag = response.get("tls_flag", " The TLS secret flag is not found")
                break

            elif response["type"] == "error":
                handle_error_response(response)
                break
           
            guess_count += 1

        if guess_count == maximum_guesses:
            print(" You have reached the maximum number of guesses available.")

        # Save the secret flags to a file
        save_flags_file(normal_flag, tls_flag)
        
    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        sock.close()

def handle_error_response(response):
    error_msg = response.get("message", "This error is unknown to the system")
    print(f"Error: {error_msg}")

def save_flags_file(normal_flag, tls_flag):
    with open("secretFlags.txt", "w") as file:
        file.write(f"Normal Flag: {normal_flag}\n")
        file.write(f"TLS Flag: {tls_flag}\n")
        print("Secret flags has been saved to 'secret_flags.txt'.")

# this stays the last line 
if __name__ == "__main__":
    main()