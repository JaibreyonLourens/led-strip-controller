
from classes.MqttClientHandler import *




def print_menu():
    print("What would you like to do?")
    print("1. Turn on the LED")
    print("2. Turn off the LED")
    print("3. Change the color of the LED")
    print("4. read the credentials file")
    print("5. Exit")


def main():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

    # #create an instance of the class
    # led = ledController(pixels, 0, 0, 0, 9)
    # #ask the user what they want to do
    # print_menu()
    # choice = int(input("Enter your choice: "))
    # while choice != 5:
    #     if choice == 1:
    #         led.led_on()
    #     elif choice == 2:
    #         led.led_off()
    #     elif choice == 3:
    #         led.change_color_value()
    #     elif choice == 4:
    #         readCredentials(credentialsData)
    #     else:
    #         print("Invalid choice")
    #     print_menu()
    #     choice = int(input("Enter your choice: "))
    # print("Goodbye")
    # del led"
if __name__ == "__main__":
    main()
