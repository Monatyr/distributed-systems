package sr.ice.server;

import com.zeroc.Ice.*;

import java.lang.Exception;

public class IceServer2
{
    public void t1(String[] args)
    {
        int status = 0;
        Communicator communicator = null;

        try	{
            communicator = Util.initialize(args);

            //Adapter
            ObjectAdapter adapter = communicator.createObjectAdapter("Adapter2");

            String[] devices = {};
            DevicesManagerI devicesManagerServant = new DevicesManagerI();
            devicesManagerServant.setDevicesNames(devices, null);

            //Dodanie wpisów do tablicy ASM, skojarzenie nazwy obiektu (Identity) z serwantem
            adapter.add(devicesManagerServant, new Identity("dm", "manager"));

            ServantLocatorImplementation servantLocator = new ServantLocatorImplementation();
            servantLocator.devicesManagerI = devicesManagerServant;
            adapter.addServantLocator(servantLocator, "");

            //Aktywacja adaptera i wejście w pętlę przetwarzania żądań
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
        IceServer2 app = new IceServer2();
        app.t1(args);
    }
}
