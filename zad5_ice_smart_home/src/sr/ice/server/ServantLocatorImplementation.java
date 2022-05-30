package sr.ice.server;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Object;


public class ServantLocatorImplementation implements ServantLocator {

    @Override
    public LocateResult locate(Current current) throws UserException {
//        Object obj = current.adapter.find(current.id);
//        if (obj == null) {
////            current.adapter.add(current., new Identity());
//            System.out.println("[ServantLocator] Creating new Identity");
//            return new LocateResult();
//        }
        System.out.println("[ServantLocator] Creating new Servant for: " + current.id.category + "/" + current.id.name);
        String category = current.id.category.toLowerCase();

        if (category.equals("freezer")) {
            FridgeWithFreezerI fridgeWithFreezerI = new FridgeWithFreezerI();
            current.adapter.add(fridgeWithFreezerI, current.id);
            return new LocateResult(fridgeWithFreezerI, null);
        }
        else if (category.equals("sensor")) {
            SensorI sensorI = new SensorI();
            current.adapter.add(sensorI, current.id);
            return new LocateResult(sensorI, null);
        }
        else if (category.equals("hsensor")) {
            HumiditySensorI humiditySensorI = new HumiditySensorI();
            current.adapter.add(humiditySensorI, current.id);
            return new LocateResult(humiditySensorI, null);
        }
        else if (category.equals("psensor")) {
            PressureSensorI pressureSensorI = new PressureSensorI();
            current.adapter.add(pressureSensorI, current.id);
            return new LocateResult(pressureSensorI, null);
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
