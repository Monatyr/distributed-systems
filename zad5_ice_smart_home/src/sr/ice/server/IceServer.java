package sr.ice.server;
// **********************************************************************
//
// Copyright (c) 2003-2019 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

import Devices.DevicesManager;
import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.Util;
import com.zeroc.Ice.ObjectAdapter;
import com.zeroc.Ice.Identity;

public class IceServer
{
	public void t1(String[] args)
	{
		int status = 0;
		Communicator communicator = null;

		try	{
			communicator = Util.initialize(args);

			// 2. Konfiguracja adaptera
			// METODA 1 (polecana produkcyjnie): Konfiguracja adaptera Adapter1 jest w pliku konfiguracyjnym podanym jako parametr uruchomienia serwera
//			ObjectAdapter adapter = communicator.createObjectAdapter("Adapter1");
			
			// METODA 2 (niepolecana, dopuszczalna testowo): Konfiguracja adaptera Adapter1 jest w kodzie Ÿród³owym
			//ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("Adapter1", "tcp -h 127.0.0.2 -p 10000");
			//ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("Adapter1", "tcp -h 127.0.0.2 -p 10000 : udp -h 127.0.0.2 -p 10000");

			ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("Adapter1", "tcp -h 127.0.0.2 -p 10000 -z : udp -h 127.0.0.2 -p 10000 -z");

			// 3. Stworzenie serwanta/serwantów
			String[] devices = {"fridge/f1", "fridge/f2", "fridge/fwf1", "microwave/m1",
								"sensor/s1", "sensor/ps1", "sensor/ps2", "sensor/hs1"};
			DevicesManagerI devicesManagerServant = new DevicesManagerI();
			devicesManagerServant.setDevicesNames(devices, null);

			FridgeI fridgeServant = new FridgeI();
			FridgeWithFreezerI fridgeWithFreezerServant = new FridgeWithFreezerI();
			MicrowaveI microwaveServant = new MicrowaveI();
			SensorI sensorServant = new SensorI();
			PressureSensorI pressureSensorServant = new PressureSensorI();
			HumiditySensorI humiditySensorServant = new HumiditySensorI();


			// 4. Dodanie wpisów do tablicy ASM, skojarzenie nazwy obiektu (Identity) z serwantem
			adapter.add(devicesManagerServant, new Identity("dm", "manager"));

			adapter.add(fridgeServant, new Identity("f1", "fridge"));
			adapter.add(fridgeServant, new Identity("f2", "fridge"));
			adapter.add(fridgeWithFreezerServant, new Identity("fwf1", "fridge"));
			adapter.add(microwaveServant, new Identity("m1", "microwave"));
			adapter.add(sensorServant, new Identity("s1", "sensor"));
			adapter.add(pressureSensorServant, new Identity("ps1", "sensor"));
			adapter.add(pressureSensorServant, new Identity("ps2", "sensor"));
			adapter.add(humiditySensorServant, new Identity("hs1", "sensor"));

			// 5. Aktywacja adaptera i wejœcie w pêtlê przetwarzania ¿¹dañ
			adapter.activate();
			
			System.out.println("Entering event processing loop...");
			
			communicator.waitForShutdown(); 		
			
		}
		catch (Exception e) {
			System.err.println(e);
			status = 1;
		}
		if (communicator != null) {
			try {
				communicator.destroy();
			}
			catch (Exception e) {
				System.err.println(e);
				status = 1;
			}
		}
		System.exit(status);
	}


	public static void main(String[] args)
	{
		IceServer app = new IceServer();
		app.t1(args);
	}
}
