package sr.ice.server;
import Devices.*;
import com.zeroc.Ice.Current;

import java.util.HashMap;
import java.util.Map;

public class FridgeI implements Fridge {

    private final Map<String, Boolean> lightsOn = new HashMap<String, Boolean>();
    private final Map<String, Float> fridgeTemps = new HashMap<String, Float>();
    protected final float minFridgeTemp = 2;
    protected final float maxFridgeTemp = 15;

    @Override
    public void switchLight(boolean lightState, Current current) {
        lightsOn.putIfAbsent(current.id.name, false);
        boolean isLight = lightsOn.get(current.id.name);
        System.out.println(current.id.category + "/" + current.id.name + " - switch light to: " + lightState);
        lightsOn.put(current.id.name, !isLight);
    }

    @Override
    public boolean isLightOn(Current current) {
        lightsOn.putIfAbsent(current.id.name, false);
        System.out.println(current.id.category + "/" + current.id.name + " - is light on: " + lightsOn.get(current.id.name));
        return lightsOn.get(current.id.name);
    }

    @Override
    public void setFridgeTemp(float newTemp, Current current) throws RangeException {
        if (newTemp > maxFridgeTemp || newTemp < minFridgeTemp){
            System.out.println(current.id.category + "/" + current.id.name + " - number out of range in setFridgeTemp call: " + newTemp);
            throw (new RangeException(newTemp, minFridgeTemp, maxFridgeTemp));
        }
        System.out.println(current.id.category + "/" + current.id.name + " - change fridge temperature to: " + newTemp);
        fridgeTemps.put(current.id.name, newTemp);
    }

    @Override
    public float getFridgeTemp(Current current) {
        fridgeTemps.putIfAbsent(current.id.name, (float) 6);
        System.out.println(current.id.category + "/" + current.id.name + " - get fridge temperature: " + fridgeTemps.get(current.id.name));
        return fridgeTemps.get(current.id.name);
    }
}
