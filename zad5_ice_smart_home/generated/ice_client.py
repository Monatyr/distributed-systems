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
        except (ValueError, Devices.RangeException, IndexError) as e:
            print(e)
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
        except (ValueError, Devices.RangeException, IndexError) as e:
            print(e)
    elif(command[2] == "getfridgetemp"):
        print(fridge_with_freezer.getFridgeTemp())
    elif(command[2] == "setfreezertemp"):
        try:
            fridge_with_freezer.setFreezerTemp(float(command[3]))
        except (ValueError, Devices.RangeException, IndexError) as e:
            print(e)
    elif(command[2] == "getfreezertemp"):
        print(fridge_with_freezer.getFreezerTemp())
    else:
        print("Invalid function")


def microwave_functions(microwave, command):
    if(command[2] == "settemp"):
        try:
            microwave.setTemp(float(command[3]))
        except (ValueError, Devices.RangeException, IndexError) as e:
            print(e)
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
        print(sensor.getTimeOfDay())
    elif(command[2] == "getallmeasurements"):
        print(sensor.getAllMeasurements())
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
        print(pressure_sensor.getTimeOfDay())
    elif(command[2] == "getallmeasurements"):
        print(pressure_sensor.getAllMeasurements())
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
        print(humidity_sensor.getTimeOfDay())
    elif(command[2] == "getallmeasurements"):
        print(humidity_sensor.getAllMeasurements())
    elif(command[2] == "gethumidity"):
        print(humidity_sensor.getHumidity())
    else:
        print("Invalid funciton")


with Ice.initialize(sys.argv) as communicator:

    devices_manager_base_1 = communicator.stringToProxy('manager/dm:tcp -h 127.0.0.2 -p 10000')
    devices_manager_1 = Devices.DevicesManagerPrx.checkedCast(devices_manager_base_1)

    print("\nTo send a command type: <device_name> <function_name> <args>\nIf you don't know devices' names type: 'names'\n")

    while True:
        command = input("> ").strip().lower()
        command = re.split(r",|\s|/", command)
        command = [el for el in command if el]
            
        if(command[0] == "names" and len(command) == 1):
            names = devices_manager_1.getAllDevicesNames()
            print("[devices_names]: ", end='')
            for name in names:
                print(name, end=" ")
            print()
        elif(command[0] == "exit"):
            print("Exit")
            break
        elif(command[0] == "fridge"): #LODÓWKI
            fridge_base = communicator.stringToProxy(f'fridge/{command[1]}:tcp -h 127.0.0.2 -p 10000')
            fridge = Devices.FridgePrx.checkedCast(fridge_base)
            fridge_functions(fridge, command)
        elif(command[0] == "freezer"): #LODÓWKI Z ZAMRAŻARKĄ
            fridge_with_freezer_base = communicator.stringToProxy(f'freezer/{command[1]}:tcp -h 127.0.0.2 -p 10000')
            fridge_with_freezer = Devices.FridgeWithFreezerPrx.checkedCast(fridge_with_freezer_base)
            fridge_with_freezer_functions(fridge_with_freezer, command)
        elif(command[0] == "microwave"): #MIKROFALE
            microwave_base = communicator.stringToProxy(f'microwave/{command[1]}:tcp -h 127.0.0.2 -p 10000')
            microwave = Devices.MicrowavePrx.checkedCast(microwave_base)
            microwave_functions(microwave, command)
        elif(command[0] == "sensor"): #SENSORY
            sensor_base = communicator.stringToProxy(f'sensor/{command[1]}:tcp -h 127.0.0.2 -p 10000')
            sensor = Devices.SensorPrx.checkedCast(sensor_base)
            sensor_functions(sensor, command)
        elif(command[0] == "psensor"): #SENSORY Z CIŚNIENIEM
            pressure_sensor_base = communicator.stringToProxy(f'psensor/{command[1]}:tcp -h 127.0.0.2 -p 10000')
            pressure_sensor = Devices.PressureSensorPrx.checkedCast(pressure_sensor_base)
            pressure_sensor_functions(pressure_sensor, command)
        elif(command[0] == "hsensor"): #SENSORY Z WILGOCIĄ
            humidity_sensor_base = communicator.stringToProxy(f'hsensor/{command[1]}:tcp -h 127.0.0.2 -p 10000')
            humidity_sensor = Devices.HumiditySensorPrx.checkedCast(humidity_sensor_base)
            humidity_sensor_functions(humidity_sensor, command)
        else:
            print("Invalid device category")