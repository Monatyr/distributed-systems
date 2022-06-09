import sys, Ice
import Devices
import re, signal


def signal_handler(signal, frame):
    print("Exit")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def fridge_functions(fridge, command):
    if(command[2] == "switchlight"):
        try:
            fridge.switchLight(command[3] == 'true')
        except IndexError as e:
            print(e)
    elif(command[2] == "setfridgetemp"):
        try:
            fridge.setFridgeTemp(float(command[3]))
        except (ValueError, IndexError) as e:
            print(e)
        except Devices.RangeException as e:
            print(f"[ERROR] Given value must be between {e.min} and {e.max}. Actual value: {e.number}")
    elif(command[2] == "islighton"):
        print(fridge.isLightOn())
    elif(command[2] == "getfridgetemp"):
        print(fridge.getFridgeTemp())
    else:
        print("Invalid function")


def fridge_with_freezer_functions(fridge_with_freezer, command):
    if(command[2] == "switchlight"):
        try:
            fridge_with_freezer.switchLight(command[3] == 'true')
        except IndexError as e:
            print(e)
    elif(command[2] == "islighton"):
        print(fridge_with_freezer.isLightOn())
    elif(command[2] == "setfridgetemp"):
        try:
            fridge_with_freezer.setFridgeTemp(float(command[3]))
        except (ValueError, IndexError) as e:
            print(e)
        except Devices.RangeException as e:
            print(f"[ERROR] Given value must be between {e.min} and {e.max}. Actual value: {e.number}")
    elif(command[2] == "getfridgetemp"):
        print(fridge_with_freezer.getFridgeTemp())
    elif(command[2] == "setfreezertemp"):
        try:
            fridge_with_freezer.setFreezerTemp(float(command[3]))
        except (ValueError, IndexError) as e:
            print(e)
    elif(command[2] == "getfreezertemp"):
        print(fridge_with_freezer.getFreezerTemp())
    else:
        print("Invalid function")


def microwave_functions(microwave, command):
    if(command[2] == "settemp"):
        try:
            microwave.setTemp(float(command[3]))
        except (ValueError, IndexError) as e:
            print(e)
        except Devices.RangeException as e:
            print(f"[ERROR] Given value must be between {e.min} and {e.max}. Actual value: {e.number}")
    elif(command[2] == "gettemp"):
        print(microwave.getTemp())
    else:
        print("Invalid function")


def sensor_functions(sensor, command):
    if(command[2] == "gettemp"):
        print(sensor.getTemp())
    elif(command[2] == "getluminousintensity"):
        print(sensor.getLuminousIntensity())
    elif(command[2] == "makemeasurements"):
        sensor.makeMeasurements()
    elif(command[2] == "gettimeofday"):
        curr_time = sensor.getTimeOfDay()
        print(f"{curr_time.hour}:{curr_time.minute}:{curr_time.second}")
    elif(command[2] == "getallmeasurements"):
        measurements = sensor.getAllMeasurements()
        for el, value in measurements.items():
            print(f"{el}: {value}")
    else:
        print("Invalid funciton")


def pressure_sensor_functions(pressure_sensor, command):
    if(command[2] == "gettemp"):
        print(pressure_sensor.getTemp())
    elif(command[2] == "getluminousintensity"):
        print(pressure_sensor.getLuminousIntensity())
    elif(command[2] == "makemeasurements"):
        pressure_sensor.makeMeasurements()
    elif(command[2] == "gettimeofday"):
        curr_time = pressure_sensor.getTimeOfDay()
        print(f"{curr_time.hour}:{curr_time.minute}:{curr_time.second}")
    elif(command[2] == "getallmeasurements"):
        measurements = pressure_sensor.getAllMeasurements()
        for el, value in measurements.items():
            print(f"{el}: {value}")
    elif(command[2] == "getpressure"):
        print(pressure_sensor.getPressure())
    else:
        print("Invalid funciton")

def humidity_sensor_functions(humidity_sensor, command):
    if(command[2] == "gettemp"):
        print(humidity_sensor.getTemp())
    elif(command[2] == "getluminousintensity"):
        print(humidity_sensor.getLuminousIntensity())
    elif(command[2] == "makemeasurements"):
        humidity_sensor.makeMeasurements()
    elif(command[2] == "gettimeofday"):
        curr_time = humidity_sensor.getTimeOfDay()
        print(f"{curr_time.hour}:{curr_time.minute}:{curr_time.second}")
    elif(command[2] == "getallmeasurements"):
        measurements = humidity_sensor.getAllMeasurements()
        for el, value in measurements.items():
            print(f"{el}: {value}")
    elif(command[2] == "gethumidity"):
        print(humidity_sensor.getHumidity())
    else:
        print("Invalid funciton")


with Ice.initialize(sys.argv) as communicator:

    servers = [("127.0.0.2", "10000"), ("127.0.0.3", "10000")] #ip and port
    curr_server_index = 0
    devices_manager_base_1 = communicator.stringToProxy(f'manager/dm:tcp -h {servers[0][0]} -p {servers[0][1]}')
    devices_manager_1 = Devices.DevicesManagerPrx.checkedCast(devices_manager_base_1)
    devices_manager_base_2 = communicator.stringToProxy(f'manager/dm:tcp -h {servers[1][0]} -p {servers[1][1]}')
    devices_manager_2 = Devices.DevicesManagerPrx.checkedCast(devices_manager_base_2)
    managers = [devices_manager_1, devices_manager_2]

    print("\nTo send a command type: <device_name> <function_name> <args>\nIf you don't know devices' names type: 'names'\n")
    print("If you want to see available servers type: 'servers'\nIf you want to switch servers type: change <server_id>")

    while True:
        command = input("> ").strip().lower()
        command = re.split(r",|\s|/", command)
        command = [el for el in command if el]
            
        if command[0] == "names" and len(command) == 1:
            names = devices_manager_1.getAllDevicesNames()
            names.extend(devices_manager_2.getAllDevicesNames())
            print("[devices_names]")
            for i, m in enumerate(managers):
                names = m.getAllDevicesNames()
                print(f"Server '{i+1}': ", end='')
                for name in names:
                    print(name, end=" ")
                print()
        elif command[0] == "servers" and len(command) == 1:
            for i, el in enumerate(servers):
                print(f"Server '{i+1}': {servers[i][0]}:{servers[i][1]}")
            print(f"Current server: '{curr_server_index+1}'")
        elif command[0] == "change" and len(command) == 2:
            if command[1].isnumeric():
                if command[1][0] != '0' and int(command[1]) > 0 and int(command[1]) <= len(servers):
                    curr_server_index = int(command[1])-1
                    print(f"Changed to server '{int(command[1])}'")
                else:
                    print("Illegal arguments")
        elif command[0] == "exit":
            print("Exit")
            break
        elif command[0] == "fridge": #LODÓWKI
            fridge_base = communicator.stringToProxy(f'fridge/{command[1]}:tcp -h {servers[curr_server_index][0]} -p {servers[curr_server_index][1]}')
            fridge = Devices.FridgePrx.checkedCast(fridge_base)
            fridge_functions(fridge, command)
        elif command[0] == "freezer": #LODÓWKI Z ZAMRAŻARKĄ
            fridge_with_freezer_base = communicator.stringToProxy(f'freezer/{command[1]}:tcp -h {servers[curr_server_index][0]} -p {servers[curr_server_index][1]}')
            fridge_with_freezer = Devices.FridgeWithFreezerPrx.checkedCast(fridge_with_freezer_base)
            fridge_with_freezer_functions(fridge_with_freezer, command)
        elif command[0] == "microwave": #MIKROFALE
            microwave_base = communicator.stringToProxy(f'microwave/{command[1]}:tcp -h {servers[curr_server_index][0]} -p {servers[curr_server_index][1]}')
            microwave = Devices.MicrowavePrx.checkedCast(microwave_base)
            microwave_functions(microwave, command)
        elif command[0] == "sensor": #SENSORY
            sensor_base = communicator.stringToProxy(f'sensor/{command[1]}:tcp -h {servers[curr_server_index][0]} -p {servers[curr_server_index][1]}')
            sensor = Devices.SensorPrx.checkedCast(sensor_base)
            sensor_functions(sensor, command)
        elif command[0] == "psensor": #SENSORY Z CIŚNIENIEM
            pressure_sensor_base = communicator.stringToProxy(f'psensor/{command[1]}:tcp -h {servers[curr_server_index][0]} -p {servers[curr_server_index][1]}')
            pressure_sensor = Devices.PressureSensorPrx.checkedCast(pressure_sensor_base)
            pressure_sensor_functions(pressure_sensor, command)
        elif command[0] == "hsensor": #SENSORY Z WILGOCIĄ
            humidity_sensor_base = communicator.stringToProxy(f'hsensor/{command[1]}:tcp -h {servers[curr_server_index][0]} -p {servers[curr_server_index][1]}')
            humidity_sensor = Devices.HumiditySensorPrx.checkedCast(humidity_sensor_base)
            humidity_sensor_functions(humidity_sensor, command)
        else:
            print("Invalid command")