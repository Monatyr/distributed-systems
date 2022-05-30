package sr.ice.server;

import Devices.Fridge;
import Devices.Microwave;
import Devices.RangeException;
import com.zeroc.Ice.Current;
import com.zeroc.Ice.OutputStream;
import com.zeroc.Ice.UserException;
import com.zeroc.IceInternal.Incoming;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletionStage;

public class MyDefaultI implements Microwave, Fridge {

    Map<String, Float> fridgeTemps = new HashMap<>();
    Map<String, Float> microwaveTemps = new HashMap<>();
    Map<String, Boolean> lightsOn = new HashMap<>();
    protected final float minFridgeTemp = 2;
    protected final float maxFridgeTemp = 15;
    private final float minTemp = 0;
    private final float maxTemp = 100;

    @Override
    public void switchLight(boolean lightState, Current current) {
        lightsOn.putIfAbsent(current.id.name, false);
        boolean isLight = lightsOn.get(current.id.name);
        System.out.println(current.id.name + " - switch light to: " + lightState);
        lightsOn.put(current.id.name, !isLight);
    }

    @Override
    public boolean isLightOn(Current current) {
        lightsOn.putIfAbsent(current.id.name, false);
        System.out.println(current.id.name + " - is light on: " + lightsOn.get(current.id.name));
        return lightsOn.get(current.id.name);
    }

    @Override
    public void setFridgeTemp(float newTemp, Current current) throws RangeException {
        if (newTemp > maxFridgeTemp || newTemp < minFridgeTemp){
            System.out.println(current.id.name + " - number out of range in setFridgeTemp call: " + newTemp);
            throw (new RangeException(newTemp, minFridgeTemp, maxFridgeTemp));
        }
        System.out.println(current.id.name + " - change fridge temperature to: " + newTemp);
        fridgeTemps.put(current.id.name, newTemp);
    }

    @Override
    public float getFridgeTemp(Current current) {
        fridgeTemps.putIfAbsent(current.id.name, (float) 6);
        System.out.println(current.id.name + " - get fridge temperature: " + fridgeTemps.get(current.id.name));
        return fridgeTemps.get(current.id.name);
    }

    @Override
    public void setTemp(float newTemp, Current current) throws RangeException { //TODO: setMicrowaveTemp
        if (newTemp > maxTemp || newTemp < minTemp) {
            System.out.println(current.id.name + " - number out of range in setTemp call: " + newTemp);
            throw (new RangeException(newTemp, minTemp, maxTemp));
        }
        System.out.println(current.id.name + " - change microwave temperature to: " + newTemp);
        microwaveTemps.put(current.id.name, newTemp);
    }

    @Override
    public float getTemp(Current current) { //TODO: getMicrowaveTemp
        microwaveTemps.putIfAbsent(current.id.name, (float) 0);
        System.out.println(current.id.name + " - get microwave temperature: " + microwaveTemps.get(current.id.name));
        return microwaveTemps.get(current.id.name);
    }

    @Override
    public String[] ice_ids(Current current) {
        if (current.id.category.equals("fridge"))
            return Fridge.super.ice_ids(current);
        else
            return Microwave.super.ice_ids(current);
    }

    @Override
    public String ice_id(Current current) {
        if (current.id.category.equals("fridge"))
            return Fridge.super.ice_id(current);
        else
            return Microwave.super.ice_id(current);
    }

    @Override
    public CompletionStage<OutputStream> _iceDispatch(Incoming in, Current current) throws UserException {
        if (current.id.category.equals("fridge"))
            return Fridge.super._iceDispatch(in, current);
        else
            return Microwave.super._iceDispatch(in, current);
    }
}
