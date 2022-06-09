package sr.ice.server;
// **********************************************************************
//
// Copyright (c) 2003-2019 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

import com.zeroc.Ice.*;

import java.lang.Exception;

public class IceServer1
{
	public void t1(String[] args)
	{
		int status = 0;
		Communicator communicator = null;

		try	{
			communicator = Util.initialize(args);

			//Adapter
			ObjectAdapter adapter = communicator.createObjectAdapter("Adapter1");

			String[] devices = {"fridge/f1", "fridge/f2", "microwave/m1"};
			DevicesManagerI devicesManagerServant = new DevicesManagerI();
			devicesManagerServant.setDevicesNames(devices, null);

			ServantLocatorImplementation servantLocator = new ServantLocatorImplementation();
			servantLocator.devicesManagerI = devicesManagerServant;
			MyDefaultI myDefaultI = new MyDefaultI();

			//Dodanie wpisów do tablicy ASM, skojarzenie nazwy obiektu (Identity) z serwantem
			adapter.add(devicesManagerServant, new Identity("dm", "manager")); //manager

			adapter.addServantLocator(servantLocator, ""); //servant locator

			adapter.addDefaultServant(myDefaultI, "fridge"); //default
			adapter.addDefaultServant(myDefaultI, "microwave"); //default

			//Aktywacja adaptera i wejœcie w pêtlê przetwarzania ¿¹dañ
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
		IceServer1 app = new IceServer1();
		app.t1(args);
	}
}
