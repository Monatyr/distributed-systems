package sr.ice.server;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Object;


public class ServantLocatorImplementation implements ServantLocator {

    public DevicesManagerI devicesManagerI;

    @Override
    public LocateResult locate(Current current) throws UserException {
        System.out.println("[ServantLocator] Creating new Servant for: " + current.id.category + "/" + current.id.name);
        String category = current.id.category.toLowerCase();

        String[] newName = {current.id.category + "/" + current.id.name};
        devicesManagerI.setDevicesNames(newName, null);

        switch (category) {
            case "freezer" -> {
                FridgeWithFreezerI fridgeWithFreezerI = new FridgeWithFreezerI();
                current.adapter.add(fridgeWithFreezerI, current.id);
                return new LocateResult(fridgeWithFreezerI, null);
            }
            case "sensor" -> {
                SensorI sensorI = new SensorI();
                current.adapter.add(sensorI, current.id);
                return new LocateResult(sensorI, null);
            }
            case "hsensor" -> {
                HumiditySensorI humiditySensorI = new HumiditySensorI();
                current.adapter.add(humiditySensorI, current.id);
                return new LocateResult(humiditySensorI, null);
            }
            case "psensor" -> {
                PressureSensorI pressureSensorI = new PressureSensorI();
                current.adapter.add(pressureSensorI, current.id);
                return new LocateResult(pressureSensorI, null);
            }
            case "fridge" -> {
                FridgeI fridgeI = new FridgeI();
                current.adapter.add(fridgeI, current.id);
                return new LocateResult(fridgeI, null);
            }
            case "microwave" -> {
                MicrowaveI microwaveI = new MicrowaveI();
                current.adapter.add(microwaveI, current.id);
                return new LocateResult(microwaveI, null);
            }
        }
        return null;
    }

    @Override
    public void finished(Current current, Object object, java.lang.Object o) throws UserException {

    }

    @Override
    public void deactivate(String s) {

    }
}
